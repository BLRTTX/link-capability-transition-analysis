#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
分析报告后处理工具

用于格式化、验证和优化新老链路对比分析报告
"""

import argparse
import json
import re
import sys
from typing import Dict, List, Any, Optional
from datetime import datetime


class ReportProcessor:
    """报告处理器"""
    
    def __init__(self):
        self.errors = []
        self.warnings = []
        self.stats = {
            "total_checks": 0,
            "passed_checks": 0,
            "failed_checks": 0
        }
    
    def validate_report(self, report_content: str) -> Dict[str, Any]:
        """
        验证报告格式和内容完整性
        
        Args:
            report_content: Markdown格式的报告内容
        
        Returns:
            验证结果字典
        """
        self.errors = []
        self.warnings = []
        self.stats = {"total_checks": 0, "passed_checks": 0, "failed_checks": 0}
        
        # 检查必要的章节
        required_sections = [
            "接口出入参对比",
            "子调用对比",
            "能力覆盖分析"
        ]
        
        for section in required_sections:
            self.stats["total_checks"] += 1
            if section in report_content:
                self.stats["passed_checks"] += 1
            else:
                self.stats["failed_checks"] += 1
                self.errors.append(f"缺少必要章节: {section}")
        
        # 检查表格格式
        self.stats["total_checks"] += 1
        if "|" in report_content and "---" in report_content:
            self.stats["passed_checks"] += 1
        else:
            self.stats["failed_checks"] += 1
            self.errors.append("报告缺少表格或表格格式不正确")
        
        # 检查是否有风险评估
        self.stats["total_checks"] += 1
        if "风险" in report_content or "兼容性" in report_content:
            self.stats["passed_checks"] += 1
        else:
            self.stats["failed_checks"] += 1
            self.warnings.append("建议添加风险评估章节")
        
        # 检查是否有建议或方案
        self.stats["total_checks"] += 1
        if "建议" in report_content or "方案" in report_content:
            self.stats["passed_checks"] += 1
        else:
            self.stats["failed_checks"] += 1
            self.warnings.append("建议添加改进建议或解决方案章节")
        
        return {
            "valid": len(self.errors) == 0,
            "errors": self.errors,
            "warnings": self.warnings,
            "stats": self.stats
        }
    
    def format_report(self, report_content: str) -> str:
        """
        格式化报告,优化结构和排版
        
        Args:
            report_content: 原始报告内容
        
        Returns:
            格式化后的报告
        """
        lines = report_content.split('\n')
        formatted_lines = []
        
        # 添加报告头部
        if not any('报告生成时间' in line for line in lines[:5]):
            formatted_lines.append(f"# 新老链路对比分析报告\n")
            formatted_lines.append(f"**报告生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            formatted_lines.append(f"---\n")
        
        # 处理表格,确保表格前后有空行
        in_table = False
        for i, line in enumerate(lines):
            # 跳过已经添加的标题
            if i < 1 and line.startswith('#'):
                continue
            
            # 检测表格开始
            if '|' in line and not in_table:
                in_table = True
                # 在表格前添加空行
                if formatted_lines and formatted_lines[-1].strip():
                    formatted_lines.append('')
            
            # 检测表格结束
            elif in_table and '|' not in line and line.strip():
                in_table = False
                # 在表格后添加空行
                formatted_lines.append('')
            
            formatted_lines.append(line)
        
        # 确保文件末尾有空行
        if formatted_lines and formatted_lines[-1].strip():
            formatted_lines.append('')
        
        return '\n'.join(formatted_lines)
    
    def add_toc(self, report_content: str) -> str:
        """
        为报告添加目录
        
        Args:
            report_content: 报告内容
        
        Returns:
            添加目录后的报告
        """
        # 提取所有标题
        toc_items = []
        lines = report_content.split('\n')
        
        for line in lines:
            if line.startswith('##'):
                # 二级标题
                title = line.lstrip('#').strip()
                anchor = title.lower().replace(' ', '-').replace('/', '-')
                indent = "  "
                toc_items.append(f"{indent}- [{title}](#{anchor})")
            elif line.startswith('###'):
                # 三级标题
                title = line.lstrip('#').strip()
                anchor = title.lower().replace(' ', '-').replace('/', '-')
                indent = "    "
                toc_items.append(f"{indent}- [{title}](#{anchor})")
        
        # 生成目录
        toc = "## 目录\n\n" + '\n'.join(toc_items) + "\n\n---\n\n"
        
        # 插入目录到报告开头(第一个标题之后)
        insert_pos = 0
        for i, line in enumerate(lines):
            if line.startswith('#'):
                insert_pos = i + 1
                break
        
        lines.insert(insert_pos, '\n' + toc)
        
        return '\n'.join(lines)
    
    def add_summary(self, report_content: str) -> str:
        """
        为报告添加摘要章节
        
        Args:
            report_content: 报告内容
        
        Returns:
            添加摘要后的报告
        """
        # 分析报告内容,生成摘要
        summary_items = []
        
        # 统计表格数量
        table_count = report_content.count('|---')
        summary_items.append(f"- 包含 {table_count} 个对比表格")
        
        # 检查风险等级
        if '高风险' in report_content:
            high_risk_count = report_content.count('高风险')
            summary_items.append(f"- ⚠️ 发现 {high_risk_count} 个高风险项")
        if '中风险' in report_content:
            medium_risk_count = report_content.count('中风险')
            summary_items.append(f"- ⚡ 发现 {medium_risk_count} 个中风险项")
        if '低风险' in report_content:
            low_risk_count = report_content.count('低风险')
            summary_items.append(f"- ℹ️ 发现 {low_risk_count} 个低风险项")
        
        # 检查兼容性结论
        if '兼容' in report_content:
            if '不兼容' in report_content:
                summary_items.append("- ❌ 总体结论: 不兼容")
            else:
                summary_items.append("- ✅ 总体结论: 兼容")
        
        # 生成摘要章节
        summary = "## 摘要\n\n"
        summary += '\n'.join(summary_items) + "\n\n---\n\n"
        
        # 插入到报告开头
        lines = report_content.split('\n')
        insert_pos = 0
        for i, line in enumerate(lines):
            if line.startswith('#'):
                insert_pos = i + 1
                break
        
        lines.insert(insert_pos, '\n' + summary)
        
        return '\n'.join(lines)


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description="分析报告后处理工具 - 用于格式化、验证和优化新老链路对比分析报告"
    )
    parser.add_argument(
        "input",
        help="输入的Markdown报告文件路径"
    )
    parser.add_argument(
        "--output",
        "-o",
        help="输出文件路径,默认输出到控制台"
    )
    parser.add_argument(
        "--validate",
        action="store_true",
        help="验证报告格式和内容完整性"
    )
    parser.add_argument(
        "--format",
        action="store_true",
        help="格式化报告,优化结构和排版"
    )
    parser.add_argument(
        "--toc",
        action="store_true",
        help="为报告添加目录"
    )
    parser.add_argument(
        "--summary",
        action="store_true",
        help="为报告添加摘要章节"
    )
    
    args = parser.parse_args()
    
    # 读取报告文件
    try:
        with open(args.input, 'r', encoding='utf-8') as f:
            report_content = f.read()
    except FileNotFoundError:
        print(f"错误: 文件不存在: {args.input}")
        sys.exit(1)
    except Exception as e:
        print(f"错误: 读取文件失败: {e}")
        sys.exit(1)
    
    processor = ReportProcessor()
    result = report_content
    
    # 验证报告
    if args.validate:
        validation_result = processor.validate_report(report_content)
        print("\n=== 报告验证结果 ===")
        print(f"验证状态: {'✅ 通过' if validation_result['valid'] else '❌ 失败'}")
        print(f"检查项统计: 总计 {validation_result['stats']['total_checks']} 项")
        print(f"  - 通过: {validation_result['stats']['passed_checks']} 项")
        print(f"  - 失败: {validation_result['stats']['failed_checks']} 项")
        
        if validation_result['errors']:
            print("\n错误:")
            for error in validation_result['errors']:
                print(f"  ❌ {error}")
        
        if validation_result['warnings']:
            print("\n警告:")
            for warning in validation_result['warnings']:
                print(f"  ⚠️  {warning}")
        print()
    
    # 格式化报告
    if args.format:
        result = processor.format_report(result)
    
    # 添加目录
    if args.toc:
        result = processor.add_toc(result)
    
    # 添加摘要
    if args.summary:
        result = processor.add_summary(result)
    
    # 输出结果
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(result)
        print(f"结果已保存到: {args.output}")
    else:
        print(result)


if __name__ == "__main__":
    main()
