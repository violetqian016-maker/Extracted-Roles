# Extracted Roles

面向角色语言分析的数据集项目，包含 16 部影视和动画作品的角色台词、单轮对话、角色档案与词汇表。

[English](README.md) · [数据结构](docs/DATASET.md) · [已知问题](docs/KNOWN_ISSUES.md)

## 当前内容

| 数据层 | 文件数量 | 数据量 |
| --- | ---: | ---: |
| 原始角色台词 | 96 | 每个非空行计一条台词 |
| 提问与回复对 | 96 | 174,000 对 |
| 角色档案 | 97 | 97 个对象 |
| 角色词汇表 | 96 | 186,109 个条目，未跨文件去重 |

以上为文件统计，不能直接解释为各层已核实一致的角色数量。档案中存在一份同名人物混淆，详见已知问题。

这是数据集与检查工具项目。目前不包含原始提取流程、模型训练代码、在线聊天应用或评测结果。

## 本地使用

需要 Git 和 Python 3.10 及以上版本，无需安装第三方 Python 依赖。

```bash
git clone https://github.com/violetqian016-maker/Extracted-Roles.git
cd Extracted-Roles
python3 scripts/dataset.py validate
python3 scripts/dataset.py catalog --check
python3 -m unittest discover -s tests -v
```

原始数据目录及文件名保持不变。不同目录的作品名和角色名不完全一致，不能仅凭字符串直接关联。`docs/catalog.json` 提供全部文件的路径、条数、大小和 SHA-256 摘要。

## 校验范围

工具检查 JSON 格式、主要字段类型、对话是否为两轮、文本是否为空、目标角色与文件名是否一致、字数总和，以及跨文件对话 ID 是否重复。GitHub Actions 自动运行回归测试和目录索引检查。

格式通过不代表台词归属、剧情事实和上下文已经人工核实。部分保留样本带有短句或恢复标记；源脚本路径虽出现在数据中，对应源文件和提取程序并未收录。

## 贡献与授权

修改数据后运行 `python3 scripts/dataset.py catalog` 更新索引，再运行检查。提交问题时请附文件路径、记录 ID 或字段以及依据，见 [贡献说明](CONTRIBUTING.md)。

项目尚未声明许可证，影视台词等第三方内容的授权范围、来源链接与提取时间仍需维护者补充，见 [授权状态](RIGHTS.md)。
