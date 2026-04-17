---
name: link-capability-transition-analysis
description: 分析新老链路迁移改造过程中接口的子调用、出入参以及能力覆盖情况。用于新老链路迁移、接口改造、能力对比分析、排查链路兼容性问题等场景。
---

# 新老链路能力分析

## 概述

本 Skill 提供三大核心分析功能,用于分析新老链路迁移改造过程中的能力覆盖情况:

1. **接口出入参对比分析**: 对比新老链路接口本身的入参和出参
2. **子调用出入参对比分析**: 对比新老链路接口中子调用的入参和出参
3. **能力覆盖分析**: 分析新链路是否完全覆盖老链路的所有业务能力

**最终输出**: 生成一份完整的Markdown格式比对报告文档,包含详细的对比分析表格、风险评估和建议方案。

**详细功能说明**:
- 接口出入参对比分析: 参考 `references/interface-parameter-comparison.md`
- 子调用出入参对比分析: 参考 `references/subcall-parameter-comparison.md`
- 能力覆盖分析: 参考 `references/capability-coverage-analysis.md`

---

## 前置条件

**必须先安装语雀MCP**,才能使用本Skill读取语雀文档。

### 安装语雀MCP

访问语雀MCP详情页面:
https://skillcenter.alipay.com/mcp/detail/mcp.ant.faas.skylarkmcpserver.skylarkmcpserver

按照页面指引完成语雀MCP的安装和配置。

安装后,语雀MCP工具将自动可用,Agent可以直接调用语雀MCP工具读取文档。

### 语雀文档要求

提供语雀文档链接,该文档必须包含以下信息:

**必需信息**:
- **新老链路接口的出入参**: 接口的入参和出参的JSON格式定义
- **子调用及其出入参**: 接口内部调用的其他服务/接口名称及其出入参的JSON格式

**文档格式示例**:
```
# [接口名称] 新老链路对比文档

## 老链路接口
- 接口路径: /api/order/create
- 入参: 
```json
{
  "老链路入参": {
    "orderId": "string",
    "userId": "string"
  }
}
```
- 出参:
```json
{
  "老链路出参": {
    "success": "boolean"
  }
}
```

## 新链路接口
- 接口路径: /api/v2/order/create
- 入参:
```json
{
  "新链路入参": {
    "orderId": "string",
    "userId": "string"
  }
}
```
- 出参:
```json
{
  "新链路出参": {
    "success": "boolean"
  }
}
```
```

---

## 使用流程

### 步骤1: 安装语雀MCP

访问语雀MCP详情页面并按照指引完成安装:
https://skillcenter.alipay.com/mcp/detail/mcp.ant.faas.skylarkmcpserver.skylarkmcpserver

### 步骤2: 提供语雀文档

向Agent提供语雀文档链接,例如:
- 完整URL: `https://yuque.antfin.com/group/book/doc`
- 文档路径: `group/book/doc`

### 步骤3: Agent自动处理

Agent会自动:
1. 使用语雀MCP工具读取文档内容
2. 解析JSON格式的接口定义和子调用信息
3. 使用三大功能模块进行对比分析
4. 生成Markdown格式的比对报告

**无需手动操作脚本或命令行工具,Agent会自动完成全部流程。**

### 步骤4: 报告后处理(可选)

生成报告后,可以要求Agent对报告进行后处理:

**验证报告**:
```
请使用 scripts/report_processor.py 验证报告的完整性
```

**格式化报告**:
```
运行 python3 scripts/report_processor.py 格式化报告,添加目录和摘要
```

**完整处理**:
```
执行 scripts/report_processor.py 对报告进行验证、格式化、添加目录和摘要
```

详细使用方法参见 `scripts/README.md`。

---

## 目录结构

```
link-capability-transition-analysis/
├── SKILL.md                          # 本文档,包含基础信息和使用指南
├── references/                       # 详细功能说明
│   ├── interface-parameter-comparison.md   # 接口出入参对比分析
│   ├── subcall-parameter-comparison.md     # 子调用出入参对比分析
│   └── capability-coverage-analysis.md     # 能力覆盖分析
└── scripts/                          # 辅助工具脚本
    └── report_processor.py           # 分析报告后处理工具
```

---

## 使用示例

**示例1**: "根据语雀文档 https://yuque.antfin.com/xxx/order-migration 分析老链路 OrderService.createOrder 和新链路 NewOrderService.createOrderV2 的出入参、子调用和能力覆盖情况"

**示例2**: "根据语雀文档中的接口定义,分析老链路支付接口 paymentService.pay 迁移到新支付中心,对比接口出入参、子调用出入参,并分析能力差异"

**示例3**: "使用语雀文档 xxx 新老链路对比文档,对比订单查询接口的老实现和新实现,分析接口字段差异、子调用变化,确认业务能力是否完整覆盖"

**示例4(包含后处理)**: "根据语雀文档 https://yuque.antfin.com/xxx/order-migration 分析新老链路差异,然后使用 scripts/report_processor.py 验证报告、添加目录和摘要"

---

## 工作原理

本Skill作为Agent的分析指导框架,工作流程如下:

1. **Agent接收用户请求** - 用户提供语雀文档链接和分析需求
2. **Agent调用语雀MCP** - 使用语雀MCP工具读取文档
3. **Agent解析文档** - 提取JSON格式的接口定义和子调用信息
4. **Agent执行分析** - 参考references目录中的分析方法进行对比分析
5. **Agent生成报告** - 输出Markdown格式的对比分析报告

**关键点**: 
- 语雀MCP负责文档读取能力
- 本Skill提供分析方法和框架指导
- Agent作为执行者,协调各项能力完成分析任务
