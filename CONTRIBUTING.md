# 贡献指南

## 我只想上架一个插件

1. 插件仓库根目录放 `plugin.json`（字段见 README）。
2. Fork 本仓库。
3. 在 `plugins.json` 的 `plugins` 数组末尾加一条对象，字段：
   `name`、`author`、`repo`、`description`，可选 `branch`、`tags`。
4. 运行 `python3 scripts/validate.py`，确认通过。
5. 提交 PR。CI 通过 + 维护者合并 = 上架。

## 我只想上架一个模型

1. 确认 GGUF 有稳定的 `https://` 直链。
2. 在 `models.json` 的 `models` 数组加一条，至少包含
   `name`、`author`、`url`、`description`。
3. 跑校验脚本，发 PR。

## 修改已有条目

- 只改自己维护的条目，或先在 Issue 里说明。
- 下架：删除对应条目并说明原因；不要改别人的 `name` 来“抢注”。

## 命名与安全

- `name` 唯一，小写，`a-z0-9-_`，1–48 字符。
- 不接受闭源跳转、短链、需要登录才能下载的地址。
- 不接受在插件安装脚本里静默提权的行为；发现即下架。

## 审核清单（维护者）

- [ ] JSON 能解析，`scripts/validate.py` 通过
- [ ] `repo` 可访问，根目录有 `plugin.json`
- [ ] `name` 不与现有条目冲突
- [ ] 描述没有误导，仓库没有明显恶意代码
- [ ] 合并后客户端能拉到（raw 地址）
