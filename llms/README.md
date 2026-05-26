# llms

项目内所有 LLM/生图调用的统一入口,负责 direct 与 ghc 模式切换。

## 岗位分工

| 文件 | 职能 |
| --- | --- |
| `config.py` | 复用 `nori.nori_config.NoriConfig`,提供 `get_active(usage)` / `resolve(key)` / `reload()` |
| `errors.py` | LLM gateway 公共异常类型的兼容 re-export；真实 owner 是 `nori.core.contracts`，保持 `llms.*` / `llms.call.*` / `llms.client.*` 的错误身份一致 |
| `telemetry.py` | Redacted telemetry sink 和 emit 逻辑；`llms.set_telemetry_sink` / `llms.call.set_telemetry_sink` 保持同一函数身份 |
| `chat_runner.py` | Sync/async chat 执行边界；负责 client resolution、kwargs merge、chat/vision capability guard、provider text extraction 和 telemetry |
| `json_parser.py` | LLM 文本响应的 JSON object 解析；`llms.parse_json_object` / `llms.call.parse_json_object` 保持同一函数身份 |
| `json_calls.py` | JSON-mode raw chat 调用、`response_format` fallback 和 retry 分类；`llms.call._chat_json_raw` 等旧内部路径保持同一函数身份 |
| `request_params.py` | Chat/image 请求参数合并与 token-limit 规范化；`llms.call._merge_kwargs` 等旧内部路径保持同一函数身份 |
| `capabilities.py` | Chat/vision/image reference 能力校验；`llms.call._ensure_*` 旧内部路径保持同一函数身份 |
| `results.py` | Chat/image provider response 归一化与空结果错误；`llms.call._extract_chat_text` / `_collect_image_results` 等旧内部路径保持同一函数身份 |
| `image_inputs.py` | Reference image 输入归一化、MIME sniff 和 data-uri 构造；`llms.call._load_image_bytes` 等旧内部路径保持同一函数身份 |
| `image_providers.py` | Google / relay / OpenAI-compatible image provider dispatch helper；`llms.call._image_*` 等旧内部路径保持同一函数身份 |
| `image_runner.py` | Image 执行边界；负责 active image model resolution、reference input filtering、capability guard、provider dispatch、result validation 和 telemetry |
| `structured_outputs.py` | Intent/target 等结构化 LLM helper 的字符串清洗和 parse-error 分类；旧模块私有 `_clean_str` 路径保持同一函数身份 |
| `structured_models.py` | 结构化 LLM helper 结果模型的兼容 re-export；真实 owner 是 `nori.core.contracts` |
| `structured_calls.py` | Intent/target 等结构化 LLM helper 的非抛错 JSON 调用包装；统一返回 `data/raw/error` |
| `structured_prompts.py` | Intent/target 等结构化 LLM helper 的 prompt 构造；旧模块私有 `_build_*_prompt` 路径保留薄代理 |
| `mode.py` | `current_mode()` / `set_mode("direct"\|"ghc")` / `ensure_ready()` 预检，复用客户端配置校验 |
| `client.py` | OpenAI SDK 同步 / 异步客户端工厂,输出 `ClientBundle(client, model)`,并提供已解析模型的 bundle builder 与配置校验 |
| `call.py` | `chat` / `chat_json` / `chat_json_with_raw` / `achat` / `image` 公共 facade；chat 执行、JSON retry、image execution 分别委托到专门模块 |
| `intent_extractor.py` | 可选意图抽取 helper,复用 `chat_json(json_mode=True)`,失败返回结构化 `error` |
| `target_selector.py` | 可选编辑目标选择 helper,复用 `chat_json(json_mode=True)`,强制 selector 白名单 |
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

## Telemetry

`set_telemetry_sink(callable | None)` 注册进程内 telemetry sink。记录只包含 redacted 元数据：

- `operation`: `chat` / `achat` / `image`
- `usage`
- `model_key` / `provider_id` / `model_id`
- `duration_ms`
- `success`
- `error_type`（失败时）

Telemetry 不包含 prompt、messages、API key、图片字节或响应正文；sink 自身异常会被吞掉，不影响业务调用。实现放在 `llms.telemetry`，`llms.__init__` 和 `llms.call` 继续 re-export 同一个 `set_telemetry_sink` 函数。

公共异常类型定义在 `nori.core.contracts`。`llms.errors`、`llms.__init__`、`llms.call` 和 `llms.client` 会继续 re-export 同一个类对象，避免调用方按旧路径捕获异常时出现 identity drift。

## 最小示例

```python
from llms import chat, chat_json, set_mode, ensure_ready

set_mode("ghc")          # 切到本地 ghc-api 代理
ensure_ready("llm")      # 失败时给出启动命令
print(chat([{"role": "user", "content": "只回复 OK"}]))
print(chat_json([{"role": "user", "content": "只输出 JSON：{\"ok\": true}"}]))
```

`chat_json(..., json_mode=True)` 会优先请求 OpenAI 兼容 JSON object mode；如果 provider/SDK 明确拒绝 `response_format` 或 JSON mode，默认自动去掉 `response_format` 重试一次；其他 provider 错误或无关 `TypeError` 不会被这个 fallback 吞掉。默认 `json_mode=False` 不注入 `response_format`，避免改变中转和本地代理行为。需要同时拿到解析结果和原始模型文本时，用 `chat_json_with_raw(...) -> (data, raw)`，不要在 helper 里重复包装 `chat`。Raw call、fallback retry 和错误分类实现放在 `llms.json_calls`，`llms.call` 继续保留 `_chat_json_raw` / `_is_response_format_error` 等旧内部别名。

JSON parsing 实现放在 `llms.json_parser`。`llms.__init__` 和 `llms.call` 继续 re-export 同一个 `parse_json_object` 函数，避免旧调用路径出现 identity drift。

`build_client_bundle(model, usage)` / `build_async_client_bundle(model, usage)` 用于已解析模型，避免调用方为了构造 SDK client 再解析一次 active model。`validate_api_key(...)` 是 provider API key 的共享校验点；`validate_client_config(...)` 在此基础上校验 OpenAI-compatible `base_url`。`get_client(...)` / `get_async_client(...)` 和 `ensure_ready(...)` 都会用它们校验 active provider 配置，空值抛 `LLMClientConfigError`。

Sync/async chat 执行实现放在 `llms.chat_runner`。`chat_text(...)` / `achat_text(...)` 负责解析 active client、合并 chat kwargs、执行 chat/vision capability guard、调用 provider、抽取文本并发 telemetry；`llms.call.chat` / `achat` 保留为薄 facade，并保留旧测试/调用方可 monkeypatch `llms.call.get_client` / `get_async_client` 的兼容面。`chat(...)` / `achat(...)` 要求 active chat model 的 `type` 为 `llm` 或 `vision`。当 `usage="vision"` 或 messages 内含 `image_url` / `input_image` / `image` parts 时，模型还必须声明 `supports_vision=true`；否则抛 `ChatCapabilityError`，避免把多模态 payload 发给纯文本模型。provider 返回空文本 content、空 `choices` 或缺失 `message.content` 时抛 `ChatResultError`，并记录失败 telemetry。

Provider response 归一化实现放在 `llms.results`。`extract_chat_text(...)` 兼容对象和 dict-shaped chat responses；`collect_image_results(...)` 收集 URL 和 `b64_json` 并统一返回 URL/data-uri；空文本或空图片结果分别抛 `ChatResultError` / `ImageResultError`。

能力校验实现放在 `llms.capabilities`。`ensure_chat_capability(...)` 负责 text/vision chat model 与 multimodal message guard；`ensure_image_capability(...)` 负责 image model type 与 `supports_reference_image` guard；`messages_need_vision(...)` 集中识别 OpenAI-style image parts。

请求参数合并实现放在 `llms.request_params`。Chat 路径使用 `merge_chat_kwargs(...)` 注入 `temperature_fixed`、规范化 `max_output` 到 `max_completion_tokens` / `max_tokens`，并复制合并 `extra_body`；image 路径使用 `merge_image_kwargs(...)`，只合并 image-safe `extra_body`，不继承 chat-only token/temperature 字段。

图片输入归一化实现放在 `llms.image_inputs`。`load_image_bytes(...)` 把 bytes、data-uri、本地路径和 base64 字符串统一为 bytes，并把不可读输入返回为空 bytes 交给上层过滤；`sniff_mime(...)` / `bytes_to_data_uri(...)` 负责 provider 参考图 payload 的 MIME 和 data-uri 构造。`llms.call` 保留旧的 `_load_image_bytes` / `_bytes_to_data_uri` / `_sniff_mime` 导入别名，避免内部兼容路径漂移。

Provider-specific image dispatch 实现放在 `llms.image_providers`。`image_openai_edit(...)` 只负责 OpenAI-compatible `images.edit` 文件包装，`image_relay_generate_with_references(...)` 只负责 relay 参考图 payload variant retry，`image_google(...)` 只负责 Google native `google-genai` 调用。`llms.call` 保留 `_image_openai_edit` / `_image_relay_generate_with_references` / `_image_google` 旧内部别名。

Image 执行实现放在 `llms.image_runner`。`image_outputs(...)` 负责解析一次 active image model、过滤 reference inputs、执行 image capability guard、按 provider 调度、校验空结果和发 telemetry；`llms.call.image` 保留为薄 facade，并显式保留旧测试/调用方可 monkeypatch `llms.call.get_active` / `build_client_bundle` / `_image_google` 等兼容面。

Intent/target 这类结构化 helper 的输出清洗放在 `llms.structured_outputs`。`clean_str(...)` 统一处理空串、`null` / `none` / `n/a` / `未知`，`chat_json_error_reason(...)` 统一把空响应和坏 JSON 分成 `empty_response` / `parse_error`。`llms.intent_extractor._clean_str` 和 `llms.target_selector._clean_str` 保留为同一函数别名。

结构化 helper 的 JSON 调用错误边界放在 `llms.structured_calls`。`call_structured_json(...)` 统一调用 `chat_json_with_raw(json_mode=True)`，成功返回 `StructuredCallResult(data, raw)`，失败返回 `error=empty_response|parse_error|api_error:*`，让 `intent_extractor.py` / `target_selector.py` 只保留各自 prompt 和结果语义。

结构化 helper 的 prompt 构造放在 `llms.structured_prompts`。Intent 字段说明、枚举提示、候选数量约束，以及 target selector 资产目录、history 拼接和 summary 截断都集中在这里；`intent_extractor.py` / `target_selector.py` 保留 `_build_*_prompt` 薄代理以兼容旧测试和内部调用。

`image(...)` 只解析一次 active image model，并用同一个 model 做 capability 判断和 OpenAI-compatible bundle 构造。它要求 active image model 的 `type` 为 `image`。`image(..., reference_images=[...])` 还会先检查 `supports_reference_image`。OpenAI-compatible image requests 会合并模型级 `extra_body`，但不会继承 chat-only 的 token/temperature 参数；调用方传入的 `extra_body` 会先复制再合并，避免隐藏 mutation。Google native image path 在进入 `google-genai` 前也复用 `validate_api_key(...)`。类型或能力不匹配时抛 `ImageCapabilityError`，配置缺失时抛 `LLMClientConfigError`，provider 返回空图片结果时抛 `ImageResultError`，避免请求进入 provider SDK 或下游业务后才以不透明错误失败。

## 模式切换

| 模式 | base_url | 前置 |
| --- | --- | --- |
| `direct` | 各服务商官方 endpoint | 复制 `api_config.example.yaml`，优先用 `providers.*.api_key_env` 指向环境变量 |
| `ghc` | `http://localhost:8313/v1` | 先启动 `ghc-api -p 8313 -a 127.0.0.1`，再用 `NORI_MODE=ghc` 或 `set_mode("ghc")` |

`current_mode()`、`set_mode(...)` 和 `ensure_ready(...)` 都会 trim runtime mode 值；`NORI_MODE=" ghc "` 会和配置加载层一样被视为 `ghc`。`ensure_ready()` 会先复用 `validate_client_config` 检查 `api_key` / `base_url`，再在 ghc 模式下 GET `/v1/models`,不通则报错并提示启动命令。没显式调用 `ensure_ready()` 的业务路径也会在客户端工厂处使用同一套校验。

## 配置文件

查找顺序：

```text
NORI_CONFIG
-> ./api_config.yaml
-> nori/api_config.yaml
-> repo_root/api_config.yaml
```

`api_config.yaml` 是本地私有文件，不提交。仓库提交的是 `api_config.example.yaml` 和 [wiki/refs/api-config.md](../wiki/refs/api-config.md)。

Provider 推荐写法：

```yaml
providers:
  openai:
    base_url: https://api.openai.com/v1
    api_key_env: OPENAI_API_KEY
```

也支持 `api_key: ${OPENAI_API_KEY}`。如果显式设置 `NORI_CONFIG` 但文件不存在，配置加载会直接报错，避免误用其他配置。

## 验证

```bash
python -m pytest tests/test_nori_config.py tests/test_llms_client.py tests/test_llms_errors.py tests/test_llms_mode.py tests/test_llms_chat_runner.py tests/test_llms_image_runner.py tests/test_llms_call_json.py tests/test_llms_intent_target_helpers.py tests/test_llms_image_capabilities.py tests/test_llms_telemetry.py -q
```

Live 验证另走 `scripts/smoke_*.py`，不要放进默认测试套件。
