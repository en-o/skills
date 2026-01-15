#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
WSL路径转换工具
将Windows路径转换为WSL可访问的路径格式

用法:
    python3 path_converter.py "C:\\Users\\tan\\Documents"
    python3 path_converter.py --verify "D:\\projects\\my-app"
    python3 path_converter.py "C:\\path1" "D:\\path2" "E:\\path3"
"""

import re
import os
import sys
import argparse


def is_wsl():
    """
    检测是否运行在WSL环境中

    返回:
        bool: True表示在WSL环境中，False表示不在
    """
    try:
        # 方法1：检查 /proc/version
        if os.path.exists('/proc/version'):
            with open('/proc/version', 'r') as f:
                version = f.read().lower()
                if 'microsoft' in version or 'wsl' in version:
                    return True

        # 方法2：检查 /proc/sys/kernel/osrelease
        if os.path.exists('/proc/sys/kernel/osrelease'):
            with open('/proc/sys/kernel/osrelease', 'r') as f:
                osrelease = f.read().lower()
                if 'microsoft' in osrelease:
                    return True

        # 方法3：检查 /mnt/c 是否存在（WSL的Windows盘符挂载点）
        if os.path.exists('/mnt/c'):
            return True

        return False
    except Exception as e:
        print(f"[警告] 环境检测失败: {e}", file=sys.stderr)
        return False


def is_windows_path(path):
    """
    判断是否是Windows路径格式

    支持的格式:
    - C:\\path\\to\\file
    - C:/path/to/file
    - C:
    - c:\\path

    参数:
        path: 要检查的路径字符串

    返回:
        bool: True表示是Windows路径，False表示不是
    """
    if not path or not isinstance(path, str):
        return False

    # 匹配盘符路径：C:\path 或 C: 或 C:/path
    # 盘符必须是字母，后面跟冒号
    pattern = r'^[a-zA-Z]:[/\\]?'
    return bool(re.match(pattern, path))


def convert_windows_path_to_wsl(path):
    """
    转换Windows路径为WSL路径

    转换规则:
    - C:\\Users\\tan -> /mnt/c/Users/tan
    - C: -> /mnt/c
    - D:\\projects -> /mnt/d/projects

    参数:
        path: Windows路径字符串

    返回:
        str: 转换后的WSL路径
    """
    if not is_windows_path(path):
        return path

    # 提取盘符和剩余路径
    # 匹配: 盘符 + 冒号 + 可选的斜杠 + 剩余路径
    drive_match = re.match(r'^([a-zA-Z]):[/\\]?(.*)$', path)
    if not drive_match:
        return path

    drive = drive_match.group(1).lower()  # 盘符转小写
    rest_path = drive_match.group(2)      # 剩余路径

    # 替换所有反斜杠为正斜杠
    rest_path = rest_path.replace('\\', '/')

    # 移除开头的斜杠（如果有）
    rest_path = rest_path.lstrip('/')

    # 构建WSL路径
    if rest_path:
        wsl_path = f"/mnt/{drive}/{rest_path}"
    else:
        wsl_path = f"/mnt/{drive}"

    return wsl_path


def verify_path_exists(path):
    """
    验证路径是否存在

    参数:
        path: 要验证的路径

    返回:
        tuple: (exists: bool, message: str)
    """
    try:
        if os.path.exists(path):
            if os.path.isfile(path):
                return True, f"✓ 文件存在"
            elif os.path.isdir(path):
                return True, f"✓ 目录存在"
            else:
                return True, f"✓ 路径存在（其他类型）"
        else:
            return False, f"✗ 路径不存在"
    except Exception as e:
        return False, f"✗ 验证失败: {e}"


def convert_path(path, verify=False, verbose=False):
    """
    转换路径并可选地验证

    参数:
        path: 要转换的路径
        verify: 是否验证转换后的路径
        verbose: 是否显示详细信息

    返回:
        dict: 包含转换结果的字典
    """
    result = {
        'original': path,
        'converted': path,
        'is_windows_path': False,
        'is_wsl_env': False,
        'converted_successfully': False,
        'path_exists': None,
        'verification_message': None
    }

    # 检测WSL环境
    result['is_wsl_env'] = is_wsl()

    # 检测是否为Windows路径
    result['is_windows_path'] = is_windows_path(path)

    # 执行转换
    if result['is_wsl_env'] and result['is_windows_path']:
        converted = convert_windows_path_to_wsl(path)
        if converted != path:
            result['converted'] = converted
            result['converted_successfully'] = True

    # 验证路径（如果需要）
    if verify and result['converted_successfully']:
        exists, message = verify_path_exists(result['converted'])
        result['path_exists'] = exists
        result['verification_message'] = message

    return result


def print_result(result, verbose=False):
    """打印转换结果"""
    if verbose:
        print(f"\n{'='*60}")
        print(f"原始路径: {result['original']}")
        print(f"WSL环境: {'是' if result['is_wsl_env'] else '否'}")
        print(f"Windows路径: {'是' if result['is_windows_path'] else '否'}")

        if result['converted_successfully']:
            print(f"转换成功: {result['converted']}")
        else:
            if not result['is_wsl_env']:
                print(f"未转换: 不在WSL环境中")
            elif not result['is_windows_path']:
                print(f"未转换: 不是Windows路径格式")
            else:
                print(f"未转换: {result['converted']}")

        if result['verification_message']:
            print(f"路径验证: {result['verification_message']}")
        print(f"{'='*60}\n")
    else:
        # 简洁模式：只输出转换后的路径
        print(result['converted'])


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description='WSL路径转换工具：将Windows路径转换为WSL可访问的路径格式',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s "C:\\Users\\tan\\Documents"
    转换单个路径

  %(prog)s --verify "D:\\projects\\my-app"
    转换并验证路径是否存在

  %(prog)s --verbose "C:\\path1" "D:\\path2"
    转换多个路径并显示详细信息

  %(prog)s --check-env
    仅检查当前是否为WSL环境
        """
    )

    parser.add_argument(
        'paths',
        nargs='*',
        help='要转换的Windows路径（可以是多个）'
    )

    parser.add_argument(
        '--verify', '-v',
        action='store_true',
        help='验证转换后的路径是否存在'
    )

    parser.add_argument(
        '--verbose',
        action='store_true',
        help='显示详细的转换信息'
    )

    parser.add_argument(
        '--check-env',
        action='store_true',
        help='仅检查当前是否为WSL环境'
    )

    args = parser.parse_args()

    # 仅检查环境
    if args.check_env:
        is_wsl_env = is_wsl()
        if is_wsl_env:
            print("✓ 当前环境是WSL")
            print("  - 可以使用路径转换功能")
            print("  - Windows盘符挂载在 /mnt/ 下")
            return 0
        else:
            print("✗ 当前环境不是WSL")
            print("  - 路径转换功能不可用")
            print("  - 如果你在Windows中，请使用WSL访问此工具")
            return 1

    # 检查是否提供了路径
    if not args.paths:
        parser.print_help()
        return 1

    # 处理每个路径
    all_success = True
    for path in args.paths:
        try:
            result = convert_path(path, verify=args.verify, verbose=args.verbose)
            print_result(result, verbose=args.verbose)

            # 如果启用了验证且路径不存在，标记为失败
            if args.verify and result['path_exists'] is False:
                all_success = False

        except Exception as e:
            print(f"[错误] 处理路径 '{path}' 时出错: {e}", file=sys.stderr)
            all_success = False

    return 0 if all_success else 1


if __name__ == '__main__':
    sys.exit(main())
