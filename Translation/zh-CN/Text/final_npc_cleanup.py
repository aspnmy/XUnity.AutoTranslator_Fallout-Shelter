#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
最终NPC对话清理脚本
"""

import os
import re
import sys

# 设置标准输出编码为UTF-8
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')

def is_conversation_line(line):
    """判断是否为对话行"""
    if not line.strip() or '=' not in line:
        return False

    english_part = line.split('=')[0].strip()

    # 明确的对话特征
    dialogue_indicators = [
        # 引号和对话标记
        r'^"',
        r'^.*" .*"$',
        r'^.*".*"$',

        # 情感表达
        r'^[A-Z][a-z]*! ',
        r'^Ha ha ha',
        r'^\*Sigh\*',

        # 互动表达
        r'^Hey, ',
        r'^Hello, ',
        r'^Excuse me',
        r'^Thank you',
        r'^Be careful',
        r'^Watch out',

        # 疑问和回答
        r'^[A-Z][a-z]*, (can|do|will|should|would|could)',
        r'^[A-Z][a-z]*\?$',  # 问号结尾的句子
        r'\?$',

        # 第一人称叙述
        r'^I (am|was|will|would|can|could|should|have|had|think|hope|wonder|need|want|know|see|hear|feel)',
        r'^I\'(m|ve|d|ll) ',

        # 角色称呼
        r'^Overseer ',
        r'^Doctor ',
        r'^Mr\. ',
        r'^Mrs\. ',
    ]

    # 检查对话特征
    for pattern in dialogue_indicators:
        if re.search(pattern, english_part, re.IGNORECASE):
            return True

    return False

def clean_npc_file():
    """清理NPC文件"""
    npc_file = r"e:\SteamLibrary\steamapps\common\Fallout Shelter\BepInEx\Translation\zh-CN\Text\fallout_shelter_zh_NPCs.txt"
    other_file = r"e:\SteamLibrary\steamapps\common\Fallot Shelter\BepInEx\Translation\zh-CN\Text\temp_other_content.txt"

    clean_npc = []
    other_content = []

    with open(npc_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    for line in lines:
        line = line.strip()
        if line and '=' in line:
            if is_conversation_line(line):
                clean_npc.append(line)
            else:
                other_content.append(line)

    # 写入清理后的NPC文件
    with open(npc_file, 'w', encoding='utf-8') as f:
        for line in sorted(set(clean_npc)):
            f.write(line + '\n')

    # 保存其他内容（临时文件）
    with open(other_file, 'w', encoding='utf-8') as f:
        for line in sorted(set(other_content)):
            f.write(line + '\n')

    return len(clean_npc), len(other_content)

def main():
    print("=== 最终NPC对话清理 ===")
    print()

    npc_count, other_count = clean_npc_file()

    print(f"保留的NPC对话: {npc_count} 条")
    print(f"移除的非对话内容: {other_count} 条")
    print()

    print("清理完成！")

if __name__ == "__main__":
    main()