#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
智能路径检测和转换工具
自动从任意文本中检测Windows路径并转换为WSL路径

用法:
    python3 smart_converter.py "参考：C:\\var ， 文档：C:\\tools"
    python3 smart_converter.py "我需要读取 C:\\work\\project\\README.md 这个文件"
    echo "切换到 D:\\projects\\my-app 目录" | python3 smart_converter.py --stdin
"""

import re
import sys
import argparse
from path_converter import is_wsl, convert_windows_path_to_wsl


def extract_windows_paths(text):
    """
    从文本中提取所有Windows路径

    支持的格式:
    - C:\\path\\to\\file
    - C:/path/to/file
    - C:
    - D:\\folder\\subfolder
    - E:/data/backup
    - C:\\Program Files\\App\\file.exe (包含空格)

    参数:
        text: 要解析的文本

    返回:
        list: 找到的所有Windows路径（去重后）
    """
    found_paths = []

    # 策略：使用更严格的路径组件匹配
    # 路径组件只能包含：字母、数字、空格、点、下划线、连字符、括号
    # 不能包含：中文字符、中文标点、特殊符号

    # 定义合法的路径字符（不包含中文）
    # 允许：字母、数字、空格、. _ - ( )
    path_char = r'[a-zA-Z0-9\s._\-()]'

    # 匹配完整路径：盘符 + 斜杠 + 路径组件
    # 使用贪婪匹配确保捕获完整路径
    pattern1 = r'[a-zA-Z]:[/\\](?:' + path_char + r'+[/\\])*' + path_char + r'+'

    matches = re.finditer(pattern1, text)
    for match in matches:
        path = match.group(0)
        # 清理路径末尾的空格、标点和斜杠
        path = path.rstrip('.,;:!?/\\，。、；：！？ ')

        if path and len(path) > 3:  # 至少 "C:\x"
            if path not in found_paths:
                found_paths.append(path)

    # 匹配单独的盘符（后面跟空白、标点或结束）
    pattern2 = r'([a-zA-Z]:)(?=[\s，。、；：！？,;]|$)'
    matches2 = re.finditer(pattern2, text)
    for match in matches2:
        path = match.group(1)
        # 检查是否已经被包含在更长的路径中
        is_part_of_longer = any(
            existing.startswith(path + '/') or existing.startswith(path + '\\')
            for existing in found_paths
        )
        if not is_part_of_longer and path not in found_paths:
            found_paths.append(path)

    return found_paths


def smart_convert_text(text, show_detection=True):
    """
    智能转换文本中的所有Windows路径

    参数:
        text: 包含Windows路径的文本
        show_detection: 是否显示检测到的路径

    返回:
        tuple: (converted_text, conversions)
            - converted_text: 转换后的文本
            - conversions: 转换记录列表 [(original, converted), ...]
    """
    # 检测WSL环境
    if not is_wsl():
        if show_detection:
            print("[警告] 当前不在WSL环境中，路径不会被转换", file=sys.stderr)
        return text, []

    # 提取所有Windows路径
    windows_paths = extract_windows_paths(text)

    if not windows_paths:
        if show_detection:
            print("[信息] 未检测到Windows路径", file=sys.stderr)
        return text, []

    # 转换路径并记录
    conversions = []
    converted_text = text

    for win_path in windows_paths:
        wsl_path = convert_windows_path_to_wsl(win_path)
        if wsl_path != win_path:
            conversions.append((win_path, wsl_path))
            # 替换文本中的路径
            # 使用 re.escape 确保特殊字符被正确处理
            converted_text = converted_text.replace(win_path, wsl_path)

    # 显示检测和转换信息
    if show_detection and conversions:
        print(f"\n[检测到 {len(conversions)} 个Windows路径]", file=sys.stderr)
        for original, converted in conversions:
            print(f"  {original}", file=sys.stderr)
            print(f"  → {converted}", file=sys.stderr)
        print("", file=sys.stderr)

    return converted_text, conversions


def process_text(text, show_detection=True, output_only_result=False):
    """
    处理文本并输出结果

    参数:
        text: 输入文本
        show_detection: 是否显示检测信息
        output_only_result: 是否只输出结果（不显示检测信息）
    """
    converted_text, conversions = smart_convert_text(
        text,
        show_detection=show_detection and not output_only_result
    )

    # 输出转换后的文本
    print(converted_text)

    return len(conversions) > 0


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description='智能路径检测和转换工具：自动从文本中检测并转换Windows路径',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s "参考：C:\\var ， 文档：C:\\tools"
    自动检测并转换文本中的Windows路径

  %(prog)s "我需要读取 C:\\work\\project\\README.md 这个文件"
    在描述中检测路径

  echo "切换到 D:\\projects\\my-app 目录" | %(prog)s --stdin
    从标准输入读取文本

  %(prog)s --quiet "C:\\path1 和 D:\\path2"
    只输出转换结果，不显示检测信息

  %(prog)s --test
    测试路径检测功能
        """
    )

    parser.add_argument(
        'text',
        nargs='?',
        help='包含Windows路径的文本'
    )

    parser.add_argument(
        '--stdin',
        action='store_true',
        help='从标准输入读取文本'
    )

    parser.add_argument(
        '--quiet', '-q',
        action='store_true',
        help='安静模式：只输出转换后的文本，不显示检测信息'
    )

    parser.add_argument(
        '--test',
        action='store_true',
        help='测试路径检测功能（显示测试用例）'
    )

    args = parser.parse_args()

    # 测试模式
    if args.test:
        test_cases = [
            "参考：C:\\var ， 文档：C:\\tools",
            "我输入xxxxxxxxx之后来一个 C:\\tools\\nginx 这里的什么什么",
            "读取文件 D:/projects/app/config.json 的内容",
            "切换到 E:\\backup\\data 目录",
            "路径 C: 和 D:\\path\\to\\file 都需要转换",
            "这是一个普通的文本，没有Windows路径",
            "C:\\Program Files\\MyApp\\bin\\app.exe",
            "多个路径：C:\\path1, D:\\path2, E:\\path3",
        ]

        print("=== 路径检测测试 ===\n")
        for i, test_text in enumerate(test_cases, 1):
            print(f"测试用例 {i}:")
            print(f"输入: {test_text}")
            paths = extract_windows_paths(test_text)
            if paths:
                print(f"检测到: {paths}")
            else:
                print("检测到: 无Windows路径")
            print()

        return 0

    # 获取输入文本
    if args.stdin:
        text = sys.stdin.read()
    elif args.text:
        text = args.text
    else:
        parser.print_help()
        return 1

    # 处理文本
    show_detection = not args.quiet
    has_conversions = process_text(text, show_detection=show_detection, output_only_result=args.quiet)

    return 0 if has_conversions else 0


if __name__ == '__main__':
    sys.exit(main())
