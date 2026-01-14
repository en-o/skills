#!/bin/bash

# 批量替换脚本
# 1. 修正 J2ServiceImpl 用法
# 2. 替换 com.sunway 和 com.example 包路径

SKILL_DIR="/mnt/c/work/tan/code/skills/Java开发基础组件使用助手"

echo "开始批量替换..."

# 查找所有需要修改的 .md 文件
find "$SKILL_DIR" -name "*.md" -type f | while read file; do
    echo "处理文件: $file"

    # 备份
    cp "$file" "${file}.bak"

    # 1. 替换 com.example.userservice 为 cn.tannn.example
    sed -i 's/com\.example\.userservice/cn.tannn.example/g' "$file"
    sed -i 's/com\.example/cn.tannn.example/g' "$file"

    # 2. 替换 com.sunway.sxzz 为 cn.tannn.example
    sed -i 's/com\.sunway\.sxzz/cn.tannn.example/g' "$file"
    sed -i 's/com\.sunway/cn.tannn.example/g' "$file"

done

echo "完成！"
