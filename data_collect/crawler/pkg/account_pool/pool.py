# -*- coding: utf-8 -*-


# -*- coding: utf-8 -*-
import asyncio
import os
from typing import Dict, List, Optional

import httpx
import pandas as pd

import data_collect.crawler.config as config
import data_collect.crawler.constant as constant
from data_collect.crawler.constant import EXCEL_ACCOUNT_SAVE, MYSQL_ACCOUNT_SAVE, COOKIE_BRIDGE_ACCOUNT_SAVE
from data_collect.crawler.pkg.account_pool.field import (AccountInfoModel, AccountStatusEnum,
                                    AccountWithIpModel)
from data_collect.crawler.pkg.proxy import IpInfoModel
from data_collect.crawler.pkg.proxy.proxy_ip_pool import ProxyIpPool
from data_collect.crawler.pkg.tools import utils
from data_collect.crawler.repo.accounts_cookies import cookies_manage_sql
from data_collect.crawler.repo.accounts_cookies.cookies_manage_sql import \
    update_account_status_by_id


class AccountPoolManager:
    def __init__(self, platform_name: str, account_save_type: str):
        """
        account pool manager class constructor
        Args:
            platform_name:
            account_save_type:
        """
        self._platform_name = platform_name
        self._account_save_type = account_save_type
        self._account_list: List[AccountInfoModel] = []

    async def async_initialize(self):
        """
        async init
        Returns:

        """
        if self._account_save_type == EXCEL_ACCOUNT_SAVE:
            self.load_accounts_from_xlsx()
        elif self._account_save_type == MYSQL_ACCOUNT_SAVE:
            await self.load_accounts_from_mysql()
        elif self._account_save_type == COOKIE_BRIDGE_ACCOUNT_SAVE:
            await self.load_accounts_from_cookie_bridge()

    def load_accounts_from_xlsx(self):
        """
        load account from xlsx
        Returns:

        """
        utils.logger.info(
            f"[AccountPoolManager.load_accounts_from_xlsx] load account from {self._platform_name} accounts_cookies.xlsx"
        )
        account_cookies_file_name = "../../config/accounts_cookies.xlsx"
        account_cookies_file_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), account_cookies_file_name
        )
        df = pd.read_excel(
            account_cookies_file_path, sheet_name=self._platform_name, engine="openpyxl"
        )
        account_id = 1
        for _, row in df.iterrows():
            account = AccountInfoModel(
                id=row.get("id", account_id),
                account_name=row.get("account_name", ""),
                cookies=row.get("cookies", ""),
                status=AccountStatusEnum.NORMAL.value,
                platform_name=self._platform_name,
            )
            self.add_account(account)
            account_id += 1
            utils.logger.info(
                f"[AccountPoolManager.load_accounts_from_xlsx] load account {account}"
            )
        utils.logger.info(
            f"[AccountPoolManager.load_accounts_from_xlsx] all account load success"
        )

    async def load_accounts_from_mysql(self):
        """
        load account from mysql
        Returns:

        """
        account_list: List[Dict] = (
            await cookies_manage_sql.query_platform_accounts_cookies(
                self._platform_name
            )
        )
        for account_item in account_list:
            account = AccountInfoModel(
                id=account_item.get("id"),
                account_name=account_item.get("account_name"),
                cookies=account_item.get("cookies"),
                status=account_item.get("status"),
                platform_name=account_item.get("platform_name"),
            )
            self.add_account(account)
            utils.logger.info(
                f"[AccountPoolManager.load_accounts_from_mysql] load account {account}"
            )
        utils.logger.info(
            f"[AccountPoolManager.load_accounts_from_mysql] all account load success"
        )

    async def load_accounts_from_cookie_bridge(self):
        """
        load account from CookieBridge server
        """
        bridge_url = config.COOKIE_BRIDGE_URL.rstrip("/")
        utils.logger.info(
            f"[AccountPoolManager.load_accounts_from_cookie_bridge] "
            f"loading {self._platform_name} accounts from CookieBridge: {bridge_url}"
        )

        async with httpx.AsyncClient(timeout=10) as client:
            # 获取所有已注册的客户端账号列表
            try:
                resp = await client.get(f"{bridge_url}/api/accounts")
                resp.raise_for_status()
            except httpx.HTTPError as e:
                raise Exception(
                    f"[AccountPoolManager.load_accounts_from_cookie_bridge] "
                    f"无法连接 CookieBridge 服务 ({bridge_url})，请确认服务已启动: {e}"
                )

            data = resp.json()
            if not data.get("isok"):
                raise Exception(
                    f"[AccountPoolManager.load_accounts_from_cookie_bridge] "
                    f"CookieBridge 返回错误: {data.get('msg')}"
                )

            accounts = data.get("data", {}).get("accounts", [])
            account_id = 1

            for account_item in accounts:
                client_id = account_item.get("client_id", "")
                platforms = account_item.get("platforms", {})
                nicknames = account_item.get("nicknames", {})

                # 检查该客户端在目标平台是否有 cookie
                platform_info = platforms.get(self._platform_name, {})
                if not platform_info.get("has_cookies"):
                    continue

                # 获取该客户端在目标平台的 cookie
                try:
                    cookie_resp = await client.get(
                        f"{bridge_url}/api/cookies/{self._platform_name}",
                        params={"client_id": client_id},
                    )
                    cookie_resp.raise_for_status()
                except httpx.HTTPError as e:
                    utils.logger.warning(
                        f"[AccountPoolManager.load_accounts_from_cookie_bridge] "
                        f"获取 client_id={client_id} 的 cookie 失败: {e}"
                    )
                    continue

                cookie_data = cookie_resp.json()
                if not cookie_data.get("isok"):
                    utils.logger.warning(
                        f"[AccountPoolManager.load_accounts_from_cookie_bridge] "
                        f"client_id={client_id} 的 cookie 不可用: {cookie_data.get('msg')}"
                    )
                    continue

                cookies_str = cookie_data.get("data", {}).get("cookies", "")
                if not cookies_str:
                    continue

                account_name = nicknames.get(self._platform_name) or client_id
                account = AccountInfoModel(
                    id=account_id,
                    account_name=account_name,
                    cookies=cookies_str,
                    status=AccountStatusEnum.NORMAL.value,
                    platform_name=self._platform_name,
                )
                self.add_account(account)
                account_id += 1
                utils.logger.info(
                    f"[AccountPoolManager.load_accounts_from_cookie_bridge] "
                    f"load account {account}"
                )

            if not self._account_list:
                await self._load_cookie_bridge_fallback_account(client, bridge_url)

        if not self._account_list:
            utils.logger.warning(
                f"[AccountPoolManager.load_accounts_from_cookie_bridge] "
                f"CookieBridge 中没有找到平台 {self._platform_name} 的可用账号，"
                f"请确认 Chrome Extension 已连接且已登录该平台"
            )
        else:
            utils.logger.info(
                f"[AccountPoolManager.load_accounts_from_cookie_bridge] "
                f"all account load success, total: {len(self._account_list)}"
            )

    async def _load_cookie_bridge_fallback_account(self, client: httpx.AsyncClient, bridge_url: str):
        """Load a CookieBridge cookie set without relying on extension account registry.

        CookieBridge also supports manually/cached cookies via /api/cookies/{platform}.
        When the extension is not connected, /api/accounts can be empty while this
        endpoint still has usable cookies.
        """
        try:
            cookie_resp = await client.get(f"{bridge_url}/api/cookies/{self._platform_name}")
            cookie_resp.raise_for_status()
        except httpx.HTTPError as e:
            utils.logger.warning(
                f"[AccountPoolManager._load_cookie_bridge_fallback_account] "
                f"获取平台 {self._platform_name} 的 fallback cookie 失败: {e}"
            )
            return

        cookie_data = cookie_resp.json()
        if not cookie_data.get("isok"):
            utils.logger.warning(
                f"[AccountPoolManager._load_cookie_bridge_fallback_account] "
                f"fallback cookie 不可用: {cookie_data.get('msg')}"
            )
            return

        data = cookie_data.get("data", {})
        cookies_str = data.get("cookies", "")
        if not cookies_str:
            return

        client_id = data.get("client_id") or data.get("source") or "cookie_bridge"
        account = AccountInfoModel(
            id=1,
            account_name=f"cookie_bridge:{client_id}",
            cookies=cookies_str,
            status=AccountStatusEnum.NORMAL.value,
            platform_name=self._platform_name,
        )
        self.add_account(account)
        utils.logger.info(
            f"[AccountPoolManager._load_cookie_bridge_fallback_account] "
            f"load fallback account {account}"
        )

    def get_active_account(self) -> AccountInfoModel:
        """
        get active account
        Returns:
            AccountInfoModel: account info model
        """
        while len(self._account_list) > 0:
            account = self._account_list.pop(0)
            if account.status.value == AccountStatusEnum.NORMAL.value:
                utils.logger.info(
                    f"[AccountPoolManager.get_active_account] get active account {account}"
                )
                return account

        raise Exception(
            "[AccountPoolManager.get_active_account] 账号池中没有可用的账号"
        )

    def add_account(self, account: AccountInfoModel):
        """
        add account
        Args:
            account: account info model
        """
        self._account_list.append(account)

    async def update_account_status(
        self, account: AccountInfoModel, status: AccountStatusEnum
    ):
        """
        update account status
        Args:
            account: account info model
            status: account status enum
        """

        account.status = status
        account.invalid_timestamp = utils.get_current_timestamp()
        if self._account_save_type == MYSQL_ACCOUNT_SAVE:
            await update_account_status_by_id(account.id, account)
        elif self._account_save_type == EXCEL_ACCOUNT_SAVE:
            # excel中的账户状态好像没有更新的必要，暂且设置为todo吧
            # TODO: update account status in xlsx
            pass
        elif self._account_save_type == COOKIE_BRIDGE_ACCOUNT_SAVE:
            # CookieBridge 模式下不持久化状态，仅内存标记
            pass
        return


class AccountWithIpPoolManager(AccountPoolManager):
    def __init__(
        self,
        platform_name: str,
        account_save_type: str,
        proxy_ip_pool: Optional[ProxyIpPool] = None,
    ):
        """
        account with ip pool manager class constructor
        if proxy_ip_pool is None, then the account pool manager will not use proxy ip
        It will only use account pool
        Args:
            platform_name: platform name, defined in constant/base_constant.py
            account_save_type: account save type, defined in constant/base_constant.py
            proxy_ip_pool: proxy ip pool, defined in proxy/proxy_ip_pool.py
        """
        super().__init__(platform_name, account_save_type)
        self.proxy_ip_pool = proxy_ip_pool

    async def async_initialize(self):
        """
        async init
        Returns:

        """
        await super().async_initialize()

    async def get_account_with_ip_info(self) -> AccountWithIpModel:
        """
        get account with ip, if proxy_ip_pool is None, then return account only
        Returns:

        """
        ip_info: Optional[IpInfoModel] = None
        account: AccountInfoModel = self.get_active_account()
        if self.proxy_ip_pool:
            ip_info = await self.proxy_ip_pool.get_proxy()
            utils.logger.info(
                f"[AccountWithIpPoolManager.get_account_with_ip] enable proxy ip pool, get proxy ip: {ip_info}"
            )
        return AccountWithIpModel(account=account, ip_info=ip_info)

    async def mark_account_invalid(self, account: AccountInfoModel):
        """
        mark account invalid
        Args:
            account:

        Returns:

        """
        await self.update_account_status(account, AccountStatusEnum.INVALID)

    async def mark_ip_invalid(self, ip_info: Optional[IpInfoModel]):
        """
        mark ip invalid
        Args:
            ip_info:

        Returns:

        """
        if not ip_info:
            return
        await self.proxy_ip_pool.mark_ip_invalid(ip_info)


async def test_get_account_with_ip():
    import data_collect.crawler.db as db

    await db.init_db()
    account_pool_manager = AccountWithIpPoolManager(
        constant.XHS_PLATFORM_NAME, account_save_type=config.ACCOUNT_POOL_SAVE_TYPE
    )
    await account_pool_manager.async_initialize()
    account_with_ip = await account_pool_manager.get_account_with_ip_info()
    print(account_with_ip)
    await account_pool_manager.mark_account_invalid(account_with_ip.account)
    return account_with_ip


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(test_get_account_with_ip())
