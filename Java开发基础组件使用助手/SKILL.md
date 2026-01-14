---
name: Java开发基础组件使用助手
description: JDevelops 框架的代码生成助手，用于创建、改进、新增符合规范的 Spring Boot 3.x + JPA 代码。在以下场景自动激活：创建 Spring Boot 项目、新增业务模块、编写 JPA 实体类、开发 REST API、使用 PathRestController、ApiMapping、J2Service、JpaCommonBean 等框架特性、改进现有代码使其符合规范、扩展功能时需要遵循框架最佳实践。
---

# Java开发基础组件使用助手

## 🎯 核心能力

此技能帮助您生成符合 JDevelops 框架规范的代码，涵盖：
- ✅ 创建新项目（基于标准架构）
- ✅ 新增业务模块（Entity → DAO → Service → Controller）
- ✅ 改进现有代码（规范检查和重构）
- ✅ 扩展功能（遵循框架最佳实践）

## 🚀 快速开始

### 根据任务类型选择工作流

**创建新项目？** → 查阅 [workflows/create-project.md](workflows/create-project.md)
**新增业务模块？** → 查阅 [workflows/add-module.md](workflows/add-module.md)
**改进现有代码？** → 查阅 [workflows/modify-code.md](workflows/modify-code.md)
**扩展功能？** → 查阅 [workflows/extend-feature.md](workflows/extend-feature.md)

## 📚 在线参考资源

### 框架源码
**GitHub 仓库**：https://github.com/en-o/Jdevelops

用途：
- 查看最新 API 实现
- 确认包路径和方法签名
- 理解框架设计思路

### 官方文档
**语雀知识库**：https://www.yuque.com/tanning/yg9ipo

用途：
- API 使用说明
- 配置指南
- 最佳实践

### 下载文档到本地
如需离线查阅文档，运行：
```bash
bash scripts/download-docs.sh
```

详细说明：[reference/online-resources.md](reference/online-resources.md)

## 📐 核心规范速查

### 强制规范（MUST）
- ✅ JDK 17 + Spring Boot 3.x（默认 3.2.7）
- ✅ 使用 JPA 操作数据库
- ✅ **禁止** VO/DTO 后缀，使用意图命名（UserAdd、UserEdit、UserInfo）
- ✅ **禁止** @Data 注解，按需使用 @Getter/@Setter/@ToString
- ✅ Controller 使用 `@PathRestController`（框架自定义）
- ✅ Service 继承 `J2Service<Entity>`
- ✅ Entity 继承 `JpaCommonBean` 或 `JpaCommonBean2`
- ✅ 统一返回 `ResultVO<T>` 或 `ResultPageVO<T, JpaPageResult<T>>`

详细规范：
- 架构规范 → [standards/architecture.md](standards/architecture.md)
- 命名规范 → [standards/naming.md](standards/naming.md)
- Lombok 规范 → [standards/lombok.md](standards/lombok.md)
- 注解规范 → [standards/annotations.md](standards/annotations.md)

### 分层代码生成指南
- Entity 层 → [guides/entity.md](guides/entity.md)
- Controller 层 → [guides/controller.md](guides/controller.md)
- Service 层 → [guides/service.md](guides/service.md)
- 请求/响应类 → [guides/request-response.md](guides/request-response.md)

## 📦 标准项目结构

```
src/main/java/
├── controller/{domain}/     # 控制器层（按业务域划分）
│   ├── dto/                # 请求类（UserAdd、UserEdit、UserPage）
│   ├── vo/                 # 响应类（UserInfo，仅在需要时创建）
│   └── *Controller.java
│
├── {module}/               # 业务模块（垂直拆分）
│   ├── entity/            # JPA 实体
│   ├── dao/               # DAO 接口
│   ├── service/           # Service 接口
│   └── service/impl/      # Service 实现
│
└── common/                # 公共组件
    ├── exception/         # 自定义异常
    └── pojo/              # 公共POJO
```

详细说明：[standards/architecture.md](standards/architecture.md)

## 🔍 代码生成检查清单

生成代码后，必须验证：
- [ ] 包路径符合规范（controller.{domain} 或 {module}.{layer}）
- [ ] 继承了正确的框架基类（J2Service、JpaCommonBean）
- [ ] 使用了框架注解（@PathRestController、@ApiMapping）
- [ ] 统一返回格式（ResultVO/ResultPageVO）
- [ ] 命名无 VO/DTO 后缀，使用意图命名
- [ ] 禁用了 @Data，使用按需的 Lombok 注解
- [ ] 敏感字段使用了 @JsonIgnore 或 @JsonView
- [ ] Long 类型字段添加了 @JsonSerialize(using = ToStringSerializer.class)
- [ ] 添加了 Swagger 文档注解（@Operation、@Tag）

完整清单：[workflows/modify-code.md](workflows/modify-code.md)

## 📚 完整示例

查看包含所有层的完整模块示例：[examples/complete-module.md](examples/complete-module.md)

## 🔑 查阅策略

```
遇到 API 不确定
    ↓
查阅官方文档（https://www.yuque.com/tanning/yg9ipo）
    ↓
找到了？ → 按文档说明使用
    ↓ 没找到
查看 GitHub 源码（https://github.com/en-o/Jdevelops）
    ↓
确认方法签名和包路径
    ↓
生成符合规范的代码
```

详细策略：[reference/lookup-strategy.md](reference/lookup-strategy.md)
