#!/bin/bash

# 文档下载脚本
# 使用 yuque-dl 工具下载 JDevelops 框架文档到本地

set -e

echo "=== JDevelops 文档下载工具 ==="
echo ""

# 检查 Node.js 是否安装
if ! command -v node &> /dev/null; then
    echo "❌ 错误：未检测到 Node.js"
    echo "请先安装 Node.js：https://nodejs.org/"
    exit 1
fi

# 检查 npm 是否安装
if ! command -v npm &> /dev/null; then
    echo "❌ 错误：未检测到 npm"
    echo "请先安装 npm"
    exit 1
fi

echo "✅ 检测到 Node.js 和 npm"
echo ""

# 安装 yuque-dl（如果未安装）
if ! command -v yuque-dl &> /dev/null; then
    echo "📦 正在安装 yuque-dl..."
    npm install -g yuque-dl
    echo "✅ yuque-dl 安装完成"
    echo ""
fi

# 文档地址
YUQUE_URL="https://www.yuque.com/tanning/yg9ipo"
OUTPUT_DIR="./docs"

echo "📚 开始下载文档..."
echo "文档地址：$YUQUE_URL"
echo "保存路径：$OUTPUT_DIR"
echo ""

# 创建输出目录
mkdir -p "$OUTPUT_DIR"

# 下载文档
yuque-dl "$YUQUE_URL" -o "$OUTPUT_DIR"

echo ""
echo "✅ 文档下载完成！"
echo "📁 文档位置：$OUTPUT_DIR"
echo ""
echo "使用方法："
echo "  - 查看文档列表：ls $OUTPUT_DIR"
echo "  - 打开文档：cat $OUTPUT_DIR/<文件名>.md"
echo ""

# 列出下载的文档
echo "已下载的文档："
ls -lh "$OUTPUT_DIR"

echo ""
echo "=== 下载完成 ==="