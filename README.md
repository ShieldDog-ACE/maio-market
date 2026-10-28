# maio-market

maio 的插件与模型市场。所有客户端（CLI 与 Web）都从本仓库的
[`plugins.json`](plugins.json) / [`models.json`](models.json) 拉取，**不使用本地内置清单**。

- 插件市场：`plugins.json`
- 模型市场：`models.json`
- 上架方式：发 PR，改一个 JSON 条目；合并即上架
- 服务器成本：0，客户端直接读 GitHub raw

## 客户端读取地址

```text
https://raw.githubusercontent.com/ShieldDog-ACE/maio-market/main/plugins.json
https://raw.githubusercontent.com/ShieldDog-ACE/maio-market/main/models.json
```

`maio` 默认使用上面的地址；镜像或内网可用 `MAIO_MARKET_URL` 或 `--market` 覆盖。
仓库根目录下的同名文件就是全部“数据库”，没有后台、没有数据库服务。

## 插件上架（开发者）

1. 把插件放在你自己的 GitHub 仓库，根目录带 `plugin.json`：

   ```json
   {
     "name": "my-plugin",
     "version": "0.1.0",
     "description": "一句话说明",
     "author": "your-github-name",
     "main": "main.sh"
   }
   ```

2. Fork 本仓库，在 `plugins.json` 的 `plugins` 数组里加一条：

   ```json
   {
     "name": "my-plugin",
     "author": "your-github-name",
     "repo": "https://github.com/your-github-name/my-plugin",
     "description": "一句话说明",
     "tags": ["tool"]
   }
   ```

3. 发 PR。维护者会跑结构校验（`scripts/validate.py`），看一眼没大问题就合并 —— **合并即上架**。

约束：

- `name` 全仓库唯一，小写字母/数字/`-`/`_`，1–48 字符。
- `repo` 必须是公开的 `https://github.com/<owner>/<repo>`。
- 插件仓库默认读 `main` 分支；需要别的分支时加 `"branch": "master"`。
- 不接收二进制大包；插件仓库应保持轻量。

## 模型上架

在 `models.json` 的 `models` 数组加一条：

```json
{
  "name": "qwen2.5-0.5b",
  "author": "Qwen",
  "url": "https://.../model.gguf",
  "quant": "Q4_K_M",
  "context": 32768,
  "size": 0,
  "sha256": "",
  "description": "说明"
}
```

`url` 必须是可直接下载的 `https://` GGUF 地址；`sha256` 可留空，但建议填。
`maio pull <name>` 会解析这里并下载到本机模型目录。

## 本地校验

```bash
python3 scripts/validate.py
```

维护者或 CI 可跑同一脚本。校验内容：JSON 可解析、schema 版本、必填字段、
名称唯一与格式、GitHub/HTTPS URL 形状、数组元素类型。

## 目录

```text
plugins.json                 # 插件市场数据库
models.json                  # 模型市场数据库
schema/plugins.schema.json   # 结构说明（供人和工具参考）
schema/models.schema.json
scripts/validate.py          # 本地/CI 共用校验器
```

## License

MIT
