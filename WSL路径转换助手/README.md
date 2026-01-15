# WSL路径转换助手

自动检测并转换Windows路径为WSL可访问的路径格式。

## 快速开始

### 使用Claude Code skill

直接使用此skill，当你在WSL环境中提供Windows路径时，助手会自动转换：

```
用户: "读取 C:\Users\tan\Documents\report.txt"
助手: [自动检测并转换为 /mnt/c/Users/tan/Documents/report.txt]
```

### 使用命令行工具

```bash
# 转换单个路径
python3 path_converter.py "C:\Users\tan\Documents"
# 输出: /mnt/c/Users/tan/Documents

# 转换并验证路径存在
python3 path_converter.py --verify "D:\projects\my-app"

# 详细模式
python3 path_converter.py --verbose "C:\work\project"

# 批量转换
python3 path_converter.py "C:\path1" "D:\path2" "E:\path3"

# 检查WSL环境
python3 path_converter.py --check-env
```

## 功能特性

- ✅ **自动环境检测**：检测是否运行在WSL中
- ✅ **智能路径识别**：识别各种Windows路径格式
- ✅ **自动转换**：将Windows路径转换为WSL路径
- ✅ **路径验证**：可选的路径存在性验证
- ✅ **批量处理**：支持一次转换多个路径
- ✅ **详细日志**：提供详细的转换信息

## 转换规则

| Windows路径 | WSL路径 |
|------------|---------|
| `C:\Users\tan` | `/mnt/c/Users/tan` |
| `C:` | `/mnt/c` |
| `D:\projects\app` | `/mnt/d/projects/app` |
| `E:\backup` | `/mnt/e/backup` |

## 支持的路径格式

- `C:\path\to\file` - 标准Windows路径
- `C:/path/to/file` - 正斜杠格式
- `C:` - 盘符格式
- `c:\path` - 小写盘符

## 使用示例

### 示例1：基本转换

```bash
$ python3 path_converter.py "C:\work\tan\code\skills"
/mnt/c/work/tan/code/skills
```

### 示例2：验证路径

```bash
$ python3 path_converter.py --verify --verbose "C:\Users\tan"
============================================================
原始路径: C:\Users\tan
WSL环境: 是
Windows路径: 是
转换成功: /mnt/c/Users/tan
路径验证: ✓ 目录存在
============================================================
```

### 示例3：批量转换

```bash
$ python3 path_converter.py "C:\path1" "D:\path2" "E:\path3"
/mnt/c/path1
/mnt/d/path2
/mnt/e/path3
```

### 示例4：检查环境

```bash
$ python3 path_converter.py --check-env
✓ 当前环境是WSL
  - 可以使用路径转换功能
  - Windows盘符挂载在 /mnt/ 下
```

## 命令行参数

```
usage: path_converter.py [-h] [--verify] [--verbose] [--check-env] [paths ...]

positional arguments:
  paths          要转换的Windows路径（可以是多个）

optional arguments:
  -h, --help     显示帮助信息
  --verify, -v   验证转换后的路径是否存在
  --verbose      显示详细的转换信息
  --check-env    仅检查当前是否为WSL环境
```

## 环境要求

- Python 3.6+
- WSL 1 或 WSL 2（Ubuntu、Debian等发行版）
- Windows 10/11

## 技术原理

### WSL环境检测

脚本通过以下方式检测WSL环境：

1. 检查 `/proc/version` 是否包含 "microsoft" 或 "WSL"
2. 检查 `/proc/sys/kernel/osrelease` 是否包含 "microsoft"
3. 检查 `/mnt/c` 目录是否存在

### 路径转换逻辑

1. 提取Windows盘符（如 `C:`）
2. 转换盘符为小写（`c`）
3. 构建WSL路径：`/mnt/{drive}/{path}`
4. 替换反斜杠为正斜杠

## 注意事项

1. **权限问题**：某些Windows系统目录可能需要管理员权限访问
2. **大小写敏感**：Linux文件系统大小写敏感，Windows不敏感
3. **路径存在性**：转换后的路径不一定存在，使用 `--verify` 验证
4. **特殊字符**：包含空格的路径需要用引号包裹

## 故障排除

### 问题：路径转换后不存在

**原因**：Windows路径在WSL中无法访问

**解决**：
- 检查盘符是否正确挂载到 `/mnt/`
- 使用 `ls /mnt/` 查看可用盘符
- 确认原始Windows路径是否存在

### 问题：权限拒绝

**原因**：没有访问权限

**解决**：
- 检查文件/目录权限
- 确认你有访问该路径的权限
- 某些系统目录可能需要sudo

### 问题：显示"不在WSL环境中"

**原因**：脚本在非WSL环境中运行

**解决**：
- 确认在WSL终端中运行
- 使用 `python3 path_converter.py --check-env` 验证环境

## 集成到其他工具

### 在bash脚本中使用

```bash
#!/bin/bash
# 转换Windows路径
WIN_PATH="C:\Users\tan\Documents"
WSL_PATH=$(python3 path_converter.py "$WIN_PATH")
echo "转换后的路径: $WSL_PATH"

# 使用转换后的路径
cd "$WSL_PATH"
```

### 在Python脚本中使用

```python
import subprocess

def convert_path(windows_path):
    result = subprocess.run(
        ['python3', 'path_converter.py', windows_path],
        capture_output=True,
        text=True
    )
    return result.stdout.strip()

# 使用
wsl_path = convert_path('C:\\Users\\tan\\Documents')
print(f"WSL路径: {wsl_path}")
```

## 贡献

欢迎提交问题和改进建议！

## 许可证

MIT License
