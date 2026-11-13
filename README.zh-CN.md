# Extracted Roles

**面向角色级文本分析与动态词表增强语言生成的结构化英文对话数据集。**

[English](README.md) · [研究说明](docs/RESEARCH.md) · [数据指南](docs/DATASET.md) · [质量与流程评审](docs/PIPELINE_REVIEW.md)

Extracted Roles 将电视与动画剧本组织为角色台词、提问与回复对、词汇表和辅助档案，支持角色语言特征分析及角色条件生成评估。

数据覆盖 **16 部作品、96 个目标角色、55 万余条台词和 174,000 对提问与回复**，为词汇模式分析与对话建模提供互补资源。

## 构建方法与主要贡献

数据构建框架将异构 TXT、CSV 剧本转化为结构化的角色级分析与训练资源。

- **文本预处理与说话人归一化。** 统一剧本格式及角色别名，清除舞台说明、标记和编码噪声。
- **双输出数据构建。** 角色台词用于词汇提取，提问与回复种子用于监督微调；训练样本采用角色级平衡策略，降低高资源角色的样本集中度。
- **质量审计与对照评估。** 检查结构完整性、说话人元数据、来源可追溯性和词汇覆盖，并比较基线与动态词表增强设置的生成结果。

该流程将非结构化数据处理、抽样设计、质量度量与效果评估连接起来，支持分析数据选择和词汇条件控制对生成语言的影响。

## 数据结构

```text
影视剧本
    → 解析、清洗、说话人归一化
        → 角色台词集合 → 角色词汇表
        → 提问与回复对 → 按角色平衡的训练种子

Wikipedia 角色资料 → 辅助档案
```

双输出设计让同一批剧本分别服务于词汇分析和对话生成实验。档案补充角色背景，台词提供实际语言证据。

| 数据 | 目录 | 当前发布规模 |
| --- | --- | ---: |
| 角色台词 | `Extracted-Roles/` | 96 个文件、550,628 个非空行 |
| 提问与回复对 | `data/latest_single_pair_seed_v3/` | 174,000 对 |
| 角色词汇表 | `vocab_by_character_clean_v1/` | 186,109 个条目 |
| 辅助角色档案 | `profiles/` | 97 个文件 |

字段定义与元数据见[数据指南](docs/DATASET.md)，构建方法与统计口径见[研究说明](docs/RESEARCH.md)。

## 评估结果

研究报告的短语审计显示，**82.92% 的目标回复**至少命中一个对应角色词表中的短语，反映了词表所含语言线索在回复中的覆盖程度。

下游实验比较了不使用与使用角色动态词表（DVA）的生成设置：

| 指标 | 基线 | DVA 增强 |
| --- | ---: | ---: |
| ROUGE-L | 6.097 | 8.734 |
| 479 次有效比较中的获胜次数 | 155（32.36%） | 309（64.51%） |
| Diversity | 0.8787 | 0.7648 |

另有 15 次平局。在所测设置下，DVA 获得更高的参考文本重合度和更多成对比较获胜次数，同时多样性下降。上下文相关性与角色一致性的改善因评估维度而异。具体方法与结果解读见[研究说明](docs/RESEARCH.md)。

## 使用数据

需要 Git 和 Python 3.10 及以上版本，以下操作无需额外安装包或 API Key。

```bash
git clone https://github.com/violetqian016-maker/Extracted-Roles.git
cd Extracted-Roles
python3 scripts/dataset.py validate
```

读取某个角色的对话样本：

```python
import json
from pathlib import Path

path = Path("data/latest_single_pair_seed_v3/Big Bang Theory/SHELDON.json")
pairs = json.loads(path.read_text(encoding="utf-8"))

print(f"{len(pairs):,} pairs for Sheldon")
for turn in pairs[0]["dialogue"]:
    name = turn.get("speaker") or turn.get("interlocutor")
    print(f"{name}: {turn['text']}")
```

检查质量信号或验证文件索引：

```bash
python3 scripts/audit_dataset.py
python3 scripts/dataset.py catalog --check
```

## 项目文档

- [数据指南](docs/DATASET.md)：数据结构与字段定义。
- [研究说明](docs/RESEARCH.md)：构建方法、统计口径与实验评估。
- [质量与流程评审](docs/PIPELINE_REVIEW.md)：发布数据审计与流程优化重点。
- [语料来源](docs/SOURCES.md)：源语料信息。
- [贡献说明](CONTRIBUTING.md)与[授权信息](RIGHTS.md)。
