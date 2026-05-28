#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
从源文件中删除NPC对话脚本
"""

import os
import re
import sys

# 设置标准输出编码为UTF-8
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')

def remove_npc_from_file(source_file, npc_file, output_file):
    """从源文件中删除NPC对话"""
    # 读取NPC对话
    npc_lines = set()
    with open(npc_file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line and '=' in line:
                npc_lines.add(line)

    print(f"读取到 {len(npc_lines)} 条NPC对话")

    # 读取源文件并删除NPC对话
    remaining_lines = []
    removed_count = 0

    with open(source_file, 'r', encoding='utf-8') as f:
        for line in f:
            stripped_line = line.strip()
            if stripped_line in npc_lines:
                removed_count += 1
            else:
                remaining_lines.append(line.rstrip('\n'))

    # 写入输出文件
    with open(output_file, 'w', encoding='utf-8') as f:
        for line in remaining_lines:
            f.write(line + '\n')

    return removed_count, len(remaining_lines)

def main():
    base_path = r"e:\SteamLibrary\steamapps\common\Fallout Shelter\BepInEx\Translation\zh-CN\Text"

    files_to_process = [
        ("fallout_shelter_zh_story.txt", "fallout_shelter_zh_story.txt"),
        ("fallout_shelter_zh_Tutorial.txt", "fallout_shelter_zh_Tutorial.txt"),
        ("_Substitutions.txt", "_Substitutions.txt"),
        ("_Postprocessors.txt", "_Postprocessors.txt")
    ]

    npc_file = os.path.join(base_path, "fallout_shelter_zh_NPCs.txt")

    print("=== 从源文件中删除NPC对话 ===")
    print()

    total_removed = 0

    for source_name, output_name in files_to_process:
        source_file = os.path.join(base_path, source_name)
        output_file = os.path.join(base_path, output_name)

        if os.path.exists(source_file):
            print(f"处理文件: {source_name}")

            # 读取原始行数
            with open(source_file, 'r', encoding='utf-8') as f:
                original_count = len(f.readlines())

            # 删除NPC对话
            removed, remaining = remove_npc_from_file(source_file, npc_file, output_file)

            print(f"  原始行数: {original_count}")
            print(f"  删除行数: {removed}")
            print(f"  剩余行数: {remaining}")
            print()

            total_removed += removed

    print(f"总共删除: {total_removed} 条NPC对话")
    print("处理完成！")

if __name__ == "__main__":
    main()