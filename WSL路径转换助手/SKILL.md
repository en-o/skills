---
name: WSL路径转换助手
description: 自动检测Windows路径并转换为WSL可访问的路径格式。在WSL环境中处理Windows路径时自动转换，支持各种Windows路径格式。
---

# WSL路径转换助手

## 🎯 核心能力

此技能帮助您在WSL（Windows Subsystem for Linux）环境中自动处理Windows路径转换：
- ✅ 自动检测当前是否运行在WSL环境中
- ✅ 识别Windows路径格式（如 `C:\path\to\file` 或 `c:` 盘符）
- ✅ 自动转换为WSL可访问的路径（如 `/mnt/c/path/to/file`）
- ✅ 支持所有Windows盘符（C:、D:、E: 等）
- ✅ 处理路径中的空格和特殊字符
- ✅ 验证转换后的路径是否存在

## 🚀 使用场景

### 场景1：用户提供Windows路径
```
用户: "请读取 C:\Users\tan\Documents\report.txt 文件"
助手: [自动检测到Windows路径，转换为 /mnt/c/Users/tan/Documents/report.txt]
```

### 场景2：处理盘符路径
```
用户: "切换到 D: 盘"
助手: [转换为 /mnt/d/ 并切换目录]
```

### 场景3：混合路径
```
用户: "复制 C:\work\project 到 /home/user/backup"
助手: [识别并转换Windows路径部分]
```

## 🔍 工作原理

### 环境检测

**检测是否为WSL环境**：
1. 检查 `/proc/version` 文件是否包含 "microsoft" 或 "WSL"
2. 检查 `/proc/sys/kernel/osrelease` 是否包含 "microsoft"
3. 检查是否存在 `/mnt/c` 目录（WSL挂载点）

### 路径识别

**识别Windows路径的特征**：
1. **标准Windows路径**：`C:\path\to\file`、`D:\folder\subfolder`
2. **盘符形式**：`c:`、`C:`、`d:` 等
3. **UNC路径**：`\\server\share\path`（转换为 `/mnt/server/share/path`）
4. **混合斜杠**：`C:/path/to/file`（Windows也支持正斜杠）

### 转换规则

| Windows路径 | WSL路径 | 说明 |
|------------|---------|------|
| `C:\Users\tan` | `/mnt/c/Users/tan` | 标准路径转换 |
| `C:` | `/mnt/c` | 盘符转换 |
| `c:\path` | `/mnt/c/path` | 小写盘符也支持 |
| `D:\work\project` | `/mnt/d/work/project` | 其他盘符 |
| `C:\Program Files\app` | `/mnt/c/Program Files/app` | 保留空格 |

**转换步骤**：
1. 提取盘符（如 `C:`）
2. 转换盘符为小写（`c`）
3. 替换为 `/mnt/c`
4. 将反斜杠 `\` 替换为正斜杠 `/`
5. 处理路径中的特殊字符和空格

## 📝 使用指南

### 自动转换模式（默认）

当检测到WSL环境时，自动转换用户输入中的Windows路径：

```python
# 示例：用户输入包含Windows路径
用户输入: "读取 C:\work\tan\code\project\README.md"

# 助手自动处理
1. 检测到当前环境是WSL ✓
2. 识别到Windows路径: C:\work\tan\code\project\README.md
3. 转换为: /mnt/c/work/tan/code/project/README.md
4. 执行读取操作
```

### 手动转换模式

用户也可以显式请求转换：

```
用户: "帮我把这个路径转换为WSL格式: D:\data\backup\file.zip"
助手: "已转换为: /mnt/d/data/backup/file.zip"
```

## 🛠️ 转换工具

### Python脚本：path_converter.py

提供独立的路径转换脚本：

```bash
# 基本用法
python3 path_converter.py "C:\Users\tan\Documents"
# 输出: /mnt/c/Users/tan/Documents

# 批量转换
python3 path_converter.py "C:\path1" "D:\path2" "E:\path3"

# 验证路径是否存在
python3 path_converter.py --verify "C:\Users\tan\Documents"
```

**脚本功能**：
- 自动检测WSL环境
- 转换Windows路径为WSL路径
- 可选的路径验证（检查转换后路径是否存在）
- 支持批量转换
- 详细的错误提示

### 使用示例

**示例1：读取Windows路径下的文件**
```
用户: "读取 C:\work\tan\code\skills\README.md"
助手:
1. 检测到WSL环境 ✓
2. 转换路径: C:\work\tan\code\skills\README.md
   → /mnt/c/work/tan/code/skills/README.md
3. 读取文件内容...
```

**示例2：切换到Windows目录**
```
用户: "切换到 D:\projects\my-app"
助手:
1. 转换路径: D:\projects\my-app → /mnt/d/projects/my-app
2. 执行: cd /mnt/d/projects/my-app
3. 当前目录: /mnt/d/projects/my-app
```

**示例3：处理包含空格的路径**
```
用户: "列出 C:\Program Files\MyApp 的内容"
助手:
1. 转换路径: C:\Program Files\MyApp → /mnt/c/Program Files/MyApp
2. 执行: ls "/mnt/c/Program Files/MyApp"
3. 显示目录内容...
```

## 🔧 技术实现

### 环境检测代码

```python
def is_wsl():
    """检测是否运行在WSL环境中"""
    try:
        # 方法1：检查 /proc/version
        with open('/proc/version', 'r') as f:
            version = f.read().lower()
            if 'microsoft' in version or 'wsl' in version:
                return True

        # 方法2：检查 /proc/sys/kernel/osrelease
        with open('/proc/sys/kernel/osrelease', 'r') as f:
            osrelease = f.read().lower()
            if 'microsoft' in osrelease:
                return True

        # 方法3：检查 /mnt/c 是否存在
        import os
        if os.path.exists('/mnt/c'):
            return True

        return False
    except:
        return False
```

### 路径转换代码

```python
import re
import os

def is_windows_path(path):
    """判断是否是Windows路径"""
    # 匹配盘符路径：C:\path 或 C: 或 C:/path
    pattern = r'^[a-zA-Z]:[/\\]?'
    return bool(re.match(pattern, path))

def convert_windows_path_to_wsl(path):
    """转换Windows路径为WSL路径"""
    if not is_windows_path(path):
        return path

    # 提取盘符（如 C:）
    drive_match = re.match(r'^([a-zA-Z]):[/\\]?(.*)$', path)
    if not drive_match:
        return path

    drive = drive_match.group(1).lower()  # 盘符转小写
    rest_path = drive_match.group(2)      # 剩余路径

    # 替换反斜杠为正斜杠
    rest_path = rest_path.replace('\\', '/')

    # 构建WSL路径
    if rest_path:
        wsl_path = f"/mnt/{drive}/{rest_path}"
    else:
        wsl_path = f"/mnt/{drive}"

    return wsl_path

def auto_convert_path(path):
    """自动转换路径（仅在WSL环境中）"""
    if is_wsl() and is_windows_path(path):
        converted = convert_windows_path_to_wsl(path)
        print(f"[路径转换] {path} → {converted}")
        return converted
    return path
```

## 📋 使用检查清单

在WSL环境中处理路径时：
- [ ] 自动检测是否为WSL环境
- [ ] 识别用户输入中的Windows路径
- [ ] 自动转换为WSL路径格式
- [ ] 验证转换后的路径是否存在（可选）
- [ ] 处理路径中的特殊字符和空格
- [ ] 提供清晰的转换日志

## ⚠️ 注意事项

1. **路径验证**：转换后建议验证路径是否存在
2. **权限问题**：某些Windows系统目录可能需要管理员权限
3. **符号链接**：WSL中的符号链接可能指向Windows路径
4. **大小写敏感**：Linux文件系统大小写敏感，Windows不敏感
5. **路径长度**：Windows路径长度限制（260字符）在WSL中不适用

## 🎯 最佳实践

1. **始终使用绝对路径**：避免相对路径混淆
2. **引用包含空格的路径**：使用双引号
3. **验证路径存在性**：转换后检查路径是否有效
4. **统一路径分隔符**：在WSL中统一使用正斜杠 `/`

## 📚 相关资源

- WSL官方文档：https://docs.microsoft.com/en-us/windows/wsl/
- WSL文件系统：https://docs.microsoft.com/en-us/windows/wsl/filesystems
- Ubuntu on WSL：https://ubuntu.com/wsl

## 🔑 工作流程

```
用户输入路径
    ↓
检测当前环境
    ↓
是WSL环境？
    ├─ 否 → 直接使用原路径
    └─ 是 → 继续
         ↓
    是Windows路径？
    ├─ 否 → 直接使用原路径
    └─ 是 → 执行转换
         ↓
    转换为WSL路径
    (/mnt/{drive}/path)
         ↓
    验证路径存在？（可选）
    ├─ 存在 → 使用转换后路径
    └─ 不存在 → 警告用户
```

## 🚨 错误处理

常见错误和解决方案：

| 错误 | 原因 | 解决方案 |
|-----|------|---------|
| 路径不存在 | Windows路径在WSL中无法访问 | 检查盘符是否挂载到 /mnt/ |
| 权限拒绝 | 没有访问权限 | 检查文件/目录权限 |
| 无效的盘符 | 盘符不存在 | 确认盘符在Windows中是否存在 |
| 特殊字符问题 | 路径包含特殊字符 | 使用引号包裹路径 |
