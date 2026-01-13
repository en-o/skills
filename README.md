# 项目说明
> [官方skill文档](https://code.claude.com/docs/zh-CN/skills) 

我的 agent skill 集合


# 什么是 skill
agent skill 就是一个大模型可以随时翻阅的说明文档


# skill 结构

```text
my-skill/
├── SKILL.md (required - overview and navigation)
├── reference.md (detailed API docs - loaded when needed)
├── examples.md (usage examples - loaded when needed)
└── scripts/
    └── helper.py (utility script - executed, not loaded)
```

## 编写 SKILL.md

`SKILL.md` 文件是 Skill 中唯一必需的文件。它有两部分：顶部的 YAML 元数据（`---` 标记之间的部分）和告诉 Claude 如何使用 Skill 的 Markdown 说明：

> [技能创作最佳实践](https://docs.claude.com/zh-CN/docs/agents-and-tools/agent-skills/best-practices)

```md
---
name: your-skill-name
description: Brief description of what this Skill does and when to use it
---

# Your Skill Name

## Instructions
Provide clear, step-by-step guidance for Claude.

## Examples
Show concrete examples of using this Skill.
```

ps: 

- `name` **必须跟文件夹名称相同**
- `description` skill功能描述
- `Instructions`  描述模型需要遵循的规则
- `Examples` 示例

## SKILL.md属性字段说明

| 字段           | 必需 |                             描述                             |
| -------------- | ---- | :----------------------------------------------------------: |
| name           | 是   | Skill 名称。必须仅使用小写字母、数字和连字符（最多 64 个字符）。应与目录名称匹配。 |
| description    | 是   | Skill 的功能和何时使用它（最多 1024 个字符）。Claude 使用这个来决定何时应用 Skill。 |
| allowed-tools  | 否   | 当此 Skill 活跃时，Claude 可以使用而无需请求权限的工具。支持逗号分隔的值或 YAML 风格的列表。参见限制工具访问。 |
| model          | 否   | 当此 Skill 活跃时使用的模型（例如，claude-sonnet-4-20250514）。默认为对话的模型。 |
| context        | 否   | 设置为 fork 以在具有自己对话历史的分叉子代理上下文中运行 Skill。 |
| agent          | 否   | 指定当设置 context: fork 时使用哪个代理类型（例如，Explore、Plan、general-purpose 或来自 .claude/agents/ 的自定义代理名称）。如果未指定，默认为 general-purpose。仅在与 context: fork 结合时适用。 |
| hooks          | 否   | 定义限定于此 Skill 生命周期的 hooks。支持 PreToolUse、PostToolUse 和 Stop 事件。 |
| user-invocable | 否   | 控制 Skill 是否出现在斜杠命令菜单中。不影响Skill 工具或自动发现。默认为 true。参见控制 Skill 可见性。 |




# skills 存放在哪里
| 位置 | 路径                | 适用于          |
| -- | ----------------- | ------------ |
| 企业 | 参见托管设置            | 你的组织中的所有用户   |
| 个人 | ~/.claude/skills/ | 你，跨所有项目      |
| 项目 | .claude/skills/   | 在此存储库中工作的任何人 |
| 插件 | 与插件捆绑             | 安装了该插件的任何人   |
