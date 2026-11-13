# Extracted Roles

**一个文本分析项目：把格式各异的影视剧本，整理成可用于角色语言研究的结构化数据。**

[English](README.md) · [研究说明](docs/RESEARCH.md) · [数据指南](docs/DATASET.md) · [质量与流程评审](docs/PIPELINE_REVIEW.md)

这是我在复旦大学完成的本科毕业论文项目。我想研究的问题是：什么样的数据，能够帮助语言模型说出更有角色辨识度的话？角色简介提供背景，而角色自己的台词则提供词汇选择、常用表达和对话方式的具体依据。

围绕这个问题，我整理了 **16 部作品、96 个目标角色、55 万余条台词和 174,000 对提问与回复**，并配套角色词汇表与辅助档案。

## 我做了什么

我负责数据构建与验证流程，将不同格式的 TXT、CSV 剧本转化为角色级数据：

- **清理和统一原始数据。** 处理剧本格式差异，统一说话人名称，去除舞台说明、标记及编码噪声。
- **为不同分析目标设计数据。** 台词集合用于角色词汇分析，提问与回复对用于角色扮演微调；训练样本按角色进行平衡，减少台词量较大的角色对数据分布的主导。
- **用指标检验数据和方法。** 检查完整性、说话人元数据、来源和词汇覆盖，并比较基线与动态词表增强设置的生成结果。

分析工作的重点贯穿整个流程：哪些记录值得保留，如何平衡不同角色的覆盖，用什么指标衡量质量，以及实验结果能够支持什么判断。

## 数据是怎样组织的

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
| 辅助角色档案 | `profiles/` | 97 个文件，其中一份存在已知身份错误 |

字段解释见[数据指南](docs/DATASET.md)。论文与当前文件的统计差异、原始方法说明见[研究说明](docs/RESEARCH.md)。

## 实验说明了什么

论文中的短语审计显示，**82.92% 的目标回复**至少包含一个对应角色词表中的短语。这个指标衡量词汇覆盖程度，不能单独代表回复的整体质量。

下游实验比较了不使用与使用角色动态词表（DVA）的生成设置：

| 指标 | 基线 | DVA 增强 |
| --- | ---: | ---: |
| ROUGE-L | 6.097 | 8.734 |
| 479 次有效比较中的获胜次数 | 155（32.36%） | 309（64.51%） |
| Diversity | 0.8787 | 0.7648 |

另有 15 次平局。结果为所测设置下的词汇对齐和成对偏好改善提供初步证据，同时也呈现了多样性下降的取舍。上下文相关性和角色一致性没有始终改善。以上结果来自论文，原始评测程序与评分记录尚未收录。

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

## 后续改进

接下来优先统一跨目录的角色标识、复核重复样本及恢复样本，并结合来源边界准备评测划分。[质量与流程评审](docs/PIPELINE_REVIEW.md)记录了检查依据和优化顺序，[已知问题](docs/KNOWN_ISSUES.md)记录发布差异。原始数据文件保持不变。

## 项目背景

**钱睿怡 Ruiyi（Violet）Qian** · 复旦大学 · 2026 年 5 月

本科论文：《促进动态角色词表构建的高质量英文角色扮演数据集》

指导教师：**纪焘**

[语料来源](docs/SOURCES.md) · [贡献说明](CONTRIBUTING.md) · [授权状态](RIGHTS.md)

数据包含第三方影视台词，项目目前尚未声明许可证。仓库说明、文件索引和检查工具是在论文完成后借助 Codex 补充的。
