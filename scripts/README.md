# 分析报告后处理工具

用于格式化、验证和优化新老链路对比分析报告。

## 功能特性

- **报告验证**: 检查报告格式和内容完整性
- **格式化优化**: 优化报告结构和排版
- **添加目录**: 自动生成报告目录
- **添加摘要**: 自动提取关键信息生成摘要

## 前置要求

- Python 3.6+
- 无需额外依赖,使用标准库

## 使用方法

### 基本用法

```bash
python3 scripts/report_processor.py report.md
```

### 验证报告

```bash
# 验证报告格式和内容完整性
python3 scripts/report_processor.py report.md --validate
```

输出示例:
```
=== 报告验证结果 ===
验证状态: ✅ 通过
检查项统计: 总计 5 项
  - 通过: 5 项
  - 失败: 0 项
```

### 格式化报告

```bash
# 格式化报告,优化结构和排版
python3 scripts/report_processor.py report.md --format --output formatted_report.md
```

### 添加目录

```bash
# 为报告添加目录
python3 scripts/report_processor.py report.md --toc --output report_with_toc.md
```

### 添加摘要

```bash
# 为报告添加摘要章节
python3 scripts/report_processor.py report.md --summary --output report_with_summary.md
```

### 综合处理

```bash
# 验证 + 格式化 + 添加目录 + 添加摘要 + 输出
python3 scripts/report_processor.py report.md \
  --validate \
  --format \
  --toc \
  --summary \
  --output final_report.md
```

## 命令行参数

| 参数 | 说明 | 必需 | 默认值 |
|------|------|------|--------|
| input | 输入的Markdown报告文件路径 | 是 | - |
| --output, -o | 输出文件路径 | 否 | 控制台输出 |
| --validate | 验证报告格式和内容完整性 | 否 | False |
| --format | 格式化报告,优化结构和排版 | 否 | False |
| --toc | 为报告添加目录 | 否 | False |
| --summary | 为报告添加摘要章节 | 否 | False |

## 验证内容

验证报告是否包含以下必要内容:

1. **必要章节检查**:
   - 接口出入参对比
   - 子调用对比
   - 能力覆盖分析

2. **表格格式检查**:
   - 是否包含表格
   - 表格格式是否正确

3. **内容完整性检查**:
   - 风险评估章节
   - 改进建议或解决方案

## 格式化优化

自动进行以下优化:

- 添加报告头部和生成时间
- 优化表格前后的空行
- 确保报告结构清晰
- 标准化Markdown格式

## 摘要生成

自动提取以下信息生成摘要:

- 表格数量统计
- 风险等级统计(高/中/低)
- 兼容性结论
- 关键发现总结

## 使用场景

### 场景1: 验证Agent生成的报告

```bash
# Agent生成报告后,验证其完整性
python3 scripts/report_processor.py analysis_report.md --validate
```

### 场景2: 优化报告格式

```bash
# 格式化并添加目录和摘要
python3 scripts/report_processor.py analysis_report.md \
  --format \
  --toc \
  --summary \
  --output optimized_report.md
```

### 场景3: 批量处理多个报告

```bash
# 使用shell脚本批量处理
for report in reports/*.md; do
  python3 scripts/report_processor.py "$report" \
    --validate \
    --format \
    --toc \
    --summary \
    --output "processed/$(basename $report)"
done
```

## 输出示例

### 验证输出

```
=== 报告验证结果 ===
验证状态: ✅ 通过
检查项统计: 总计 5 项
  - 通过: 5 项
  - 失败: 0 项
```

### 摘要示例

```markdown
## 摘要

- 包含 3 个对比表格
- ⚠️ 发现 2 个高风险项
- ⚡ 发现 3 个中风险项
- ℹ️ 发现 1 个低风险项
- ✅ 总体结论: 兼容

---
```

### 目录示例

```markdown
## 目录

  - [接口出入参对比](#接口出入参对比)
    - [入参对比](#入参对比)
    - [出参对比](#出参对比)
  - [子调用对比](#子调用对比)
  - [能力覆盖分析](#能力覆盖分析)
  - [风险评估](#风险评估)
  - [改进建议](#改进建议)

---
```

## 注意事项

1. 输入文件必须是Markdown格式
2. 验证功能仅检查报告的完整性,不检查内容的正确性
3. 建议先生成报告,然后使用此工具进行后处理

## 与Agent协作

这个工具的设计目的是与Agent协作:

1. **Agent生成报告** - Agent使用语雀MCP读取文档并生成对比分析报告
2. **工具后处理** - 使用本工具对报告进行验证、格式化、优化
3. **最终输出** - 得到完整、规范、易读的分析报告

这样既发挥了Agent的分析能力,又通过工具保证了报告的规范性和完整性。
