# llms

项目内所有 LLM/生图调用的统一入口,负责 direct 与 ghc 模式切换。

## 岗位分工

| 文件 | 职能 |
| --- | --- |
| `config.py` | 复用 `nori.nori_config.NoriConfig`,提供 `get_active(usage)` / `resolve(key)` / `reload()` |
| `mode.py` | `current_mode()` / `set_mode("direct"\|"ghc")` / `ensure_ready()` 预检 |
| `client.py` | OpenAI SDK 同步 / 异步客户端工厂,输出 `ClientBundle(client, model)` |
| `call.py` | `chat` / `chat_json` / `achat` / `image` 高层调用,自动注入 `temperature_fixed`、`max_output`、`extra_body` |
| `__init__.py` | 对外暴露符号,内部实现可替换 |

## 交接关系

```
api_config.yaml
      │
      ▼
nori.nori_config.NoriConfig          ← 配置解析(已存在,不重复)
      │
      ▼
llms.config                          ← 桥接
      │
      ├── llms.mode                  ← direct / ghc 切换 + 预检
      │
      ▼
llms.client                          ← OpenAI / AsyncOpenAI 工厂
      │
      ▼
llms.call (chat / chat_json / achat / image) ← 业务方唯一入口
      │
      ▼
writer / reviewer / evolution / skills
```

## 调用规范

业务代码只 `from llms import ...`,禁止:

- 直接 `from openai import OpenAI`
- 直接读 `api_config.yaml`
- 直接 `os.environ["NORI_MODE"] = ...`,用 `llms.set_mode()`

## 最小示例

```python
from llms import chat, chat_json, set_mode, ensure_ready

set_mode("ghc")          # 切到本地 ghc-api 代理
ensure_ready("llm")      # 失败时给出启动命令
print(chat([{"role": "user", "content": "只回复 OK"}]))
print(chat_json([{"role": "user", "content": "只输出 JSON：{\"ok\": true}"}]))
```

## 模式切换

| 模式 | base_url | 前置 |
| --- | --- | --- |
| `direct` | 各服务商官方 endpoint | 在 `api_config.yaml.providers.*.api_key` 填 key |
| `ghc` | `http://localhost:8313/v1` | 先启动 `ghc-api -p 8313 -a 127.0.0.1` |

`ensure_ready()` 会在 ghc 模式下 GET `/v1/models`,不通则报错并提示启动命令。

## 验证

```bash
source ~/.venvs/ghc-api/bin/activate
python skills/evolution/smoke_ghc.py --mode ghc --usage llm
```

通过判据:`proxy_ok=True` + `chat_ok=True`。
