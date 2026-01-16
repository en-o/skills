---
name: Java开发基础组件使用助手
description: 用于 JDevelops 框架或纯 Spring Boot 开发的代码生成助手，生成符合规范的 Spring Boot 3.x + JPA 代码。支持 JDevelops 框架开发、纯 Spring Boot 开发、REST API、Entity/Service/Controller 开发。
---

# Java开发基础组件使用助手

## 🎯 核心能力

此技能帮助您生成符合规范的 Spring Boot 3.x 代码，涵盖：
- ✅ 创建新项目（JDevelops 框架或纯 Spring Boot）
- ✅ 新增业务模块（Entity → DAO → Service → Controller）
- ✅ 改进现有代码（规范检查和重构）
- ✅ 扩展功能（遵循框架最佳实践）

### 支持的技术栈

**JDevelops 框架模式**：
- Spring Boot 3.x + JPA
- JDevelops 框架组件（J2Service、JpaCommonBean、PathRestController 等）
- 统一返回格式（ResultVO、ResultPageVO）
- 框架注解和工具类

**纯 Spring Boot 模式**：
- Spring Boot 3.x + JPA
- 标准 Spring Data JPA
- 标准 @RestController
- 自定义返回格式或标准格式

## 🚀 快速开始

### 📋 需求分析和确认流程（首要步骤）

**在开始任何代码生成前，必须完成需求分析和确认流程**：

#### 🔍 框架选择和检测

**创建新项目时**：
- 如果用户未明确说明使用 JDevelops 框架，**必须询问**选择：
  - 【选项 A】JDevelops 框架（推荐）
  - 【选项 B】纯 Spring Boot
- 根据用户选择采用对应的规范和模板

**添加功能/修改项目时**：
- **自动检测**项目使用的框架（无需询问）
- 读取 `pom.xml` 文件检查依赖：
  - 找到 `cn.tannn.jdevelops` → JDevelops 框架项目
  - 只有标准 Spring 依赖 → 纯 Spring Boot 项目
- 通知用户检测结果，使用对应规范生成代码

#### 流程图

```
用户描述需求
    ↓
AI 总结提炼需求
    ↓
展示需求总结 → 询问："是否满意此需求总结？"
    ↓
满意？
├─ 是 → 询问包结构选择（创建新项目时）→ 制定开发计划 → 开始执行
└─ 否 → 询问："是否有新的需求或调整？"
         ↓
    收集新需求/调整
         ↓
    重新总结提炼（包含新需求）
         ↓
    返回"询问是否满意"
```

**⚠️ 重要提醒**：
- **创建新项目时**：需求确认后，必须先询问包结构选择（A/B/C），然后再制定开发计划
- **添加业务模块时**：如果是首次添加模块，也需要询问包结构选择
- 详细的包结构选择流程参考：[workflows/requirement-analysis.md - 步骤 3.5](workflows/requirement-analysis.md#步骤-35-包结构选择重要)

#### 详细步骤

**步骤 1: 收集需求**
- 让用户描述需求（无论是创建项目还是添加功能）
- 鼓励用户详细说明业务场景、功能要求、技术偏好

**步骤 2: 总结提炼**
- AI 对需求进行结构化总结
- 提炼关键要点：
  - 业务目标
  - 核心功能
  - 技术要求
  - 数据模型
  - 接口定义

**步骤 3: 确认需求**
- 展示需求总结
- 询问："以上需求总结是否准确？是否满意？"

**步骤 4: 迭代优化（如果不满意）**
- 询问："请说明需要调整的地方，或者是否有新的需求要加入？"
- 收集补充/调整信息
- 重新总结提炼（整合新需求）
- 返回步骤 3

**步骤 5: 制定开发计划**
- 需求确认后，制定详细的开发计划：
  - 需要创建的文件清单
  - 代码生成顺序
  - 依赖关系
  - 配置项
- 展示开发计划并征得确认

**步骤 6: 开始执行**
- 按照开发计划逐步生成代码
- 在每个关键节点提供进度反馈

#### 示例对话

```
用户: "我需要创建一个用户管理模块，包含用户注册、登录、个人信息管理"

AI: "好的，让我总结一下您的需求：

【需求总结】
业务目标：实现用户管理功能
核心功能：
  1. 用户注册（用户名、密码、邮箱、手机号）
  2. 用户登录（支持用户名/邮箱/手机号登录）
  3. 个人信息管理（查看、修改个人信息）

技术实现：
  - Entity: User（继承 JpaCommonBean）
  - Controller: UserController（注册、登录、信息管理接口）
  - Service: UserService（业务逻辑处理）
  - 认证方式：推荐使用 JWT 或 Redis+JWT

请问这个需求总结是否准确？是否满意？"

用户: "基本满意，但我还需要添加密码重置和账号禁用功能"

AI: "好的，我来更新需求总结：

【需求总结（更新版）】
业务目标：实现完整的用户管理功能
核心功能：
  1. 用户注册（用户名、密码、邮箱、手机号）
  2. 用户登录（支持用户名/邮箱/手机号登录）
  3. 个人信息管理（查看、修改个人信息）
  4. 密码重置（通过邮箱验证码重置）  ← 新增
  5. 账号禁用/启用（管理员功能）      ← 新增

技术实现：
  - Entity: User（增加 status 字段标识账号状态）
  - Controller: UserController（所有用户相关接口）
  - Service: UserService、EmailService（邮件发送）
  - 认证方式：推荐 Redis+JWT（支持强制下线）

请问现在是否满意？"

用户: "满意！"

AI: "好的！现在我来制定开发计划：

【开发计划】
步骤 1: 确认项目路径
步骤 2: 创建 User Entity
  - 字段：id, loginName, password, email, phone, status...
  - 继承 JpaCommonBean
  - 敏感字段处理（password 使用 @JsonIgnore）
步骤 3: 创建 UserDao 接口
步骤 4: 创建 UserService 和实现
步骤 5: 创建请求/响应类
  - UserRegister（注册请求）
  - UserLogin（登录请求）
  - UserInfo（响应类，脱敏）
  - ResetPassword（重置密码）
步骤 6: 创建 UserController
  - POST /user/register
  - POST /user/login
  - GET /user/info
  - PUT /user/info
  - POST /user/reset-password
  - PUT /user/status（禁用/启用）
步骤 7: 验证代码规范

确认开始执行？"
```

### 🤖 交互式工作流

完成需求分析和确认后，本助手将采用**交互式对话**方式，在关键决策点会主动询问您的需求和偏好：

#### 📂 项目路径确认（重要）

在开始任何代码生成操作前，**必须**先确认项目路径：

**创建新项目时：**
- ❓ 询问："是否在当前目录下直接创建项目？"
  - ✅ 是 → 在当前目录创建项目结构
  - ❌ 否 → 询问：
    - 提供完整项目路径（如 `/home/user/projects/my-project`）
    - 或提供新建项目目录名（如 `my-project`，将在当前目录下创建）

**对现有项目添加功能时：**
- ❓ 询问："是否是当前目录下的项目？"
  - ✅ 是 → 在当前目录进行功能追加
  - ❌ 否 → 询问："请提供项目的完整路径"
    - 示例：`/home/user/projects/existing-project`
    - 示例：`C:\work\tan\code\my-project`

**路径验证：**
- 确认路径存在且有写入权限
- 对于新项目，检查目录是否为空或不存在
- 对于现有项目，验证是否为 Spring Boot 项目（检查 pom.xml 或 build.gradle）

#### 创建新项目时会询问
- 📂 **项目路径**（是否在当前目录创建，或提供路径）
- 📝 项目名称和包路径（如未提供）
- 📋 项目描述和业务场景
- 📁 **包结构选择**（三层架构 vs 垂直切分 vs 混合架构）⚠️ 重要
- 🔐 **登录鉴权选择**（不需要 / Spring Security + JWT / JDevelops 鉴权组件）⚠️ 重要
- 📦 需要集成的组件（必要/推荐/可选）
- 🔍 组件版本自动查询和建议

#### 添加业务模块时会询问
- 📂 **项目路径**（是否是当前项目，或提供项目路径）
- 📋 项目整体描述（如首次添加模块）
- 📁 包结构选择（三层架构 vs 垂直切分）
- 🗃️ 数据表结构提供方式（已有表结构、字段清单、口头描述、自己编写）
- 🎯 模块名称和业务领域
- 🔒 敏感字段和脱敏需求

**好处**: 交互式询问确保生成的代码完全符合您的项目需求，避免后续修改。

### 根据任务类型选择工作流

**📋 需求分析流程（所有任务必读）** → 查阅 [workflows/requirement-analysis.md](workflows/requirement-analysis.md)
**创建新项目？** → 查阅 [workflows/create-project.md](workflows/create-project.md)
**新增业务模块？** → 查阅 [workflows/add-module.md](workflows/add-module.md)
**改进现有代码？** → 查阅 [workflows/modify-code.md](workflows/modify-code.md)
**扩展功能？** → 查阅 [workflows/extend-feature.md](workflows/extend-feature.md)

## 📚 在线参考资源

### 组件清单和版本查询
**组件清单**: [reference/components.md](reference/components.md)
- 🔴 必要组件（jdevelops-spring-boot-starter、jdevelops-dals-jpa）
- 🟡 推荐组件（jdevelops-apis-result、springdoc-openapi）
- 🟢 可选组件（认证、文件上传、Excel、缓存等）

**版本查询工具**: `scripts/query_versions.py`
```bash
# 查询所有组件最新版本
python3 scripts/query_versions.py

# 查询指定组件
python3 scripts/query_versions.py -a jdevelops-spring-boot-starter
```

### 包结构选择
**包结构指南**: [reference/package-structure.md](reference/package-structure.md)
- 传统三层架构（适合中小型项目）
- 垂直切分模块化（适合大型项目）
- 混合模式和迁移指南

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

### ⚠️ 代码生成重要提醒

**禁止自动生成 import 语句**：
- ❌ 不要生成任何 `import` 语句（包括 `import cn.tannn.jdevelops.*`、`import lombok.*` 等）
- ✅ 只生成类的主体代码（package、注解、类定义、字段、方法）
- ✅ 让用户使用 IDE 的自动导入功能（如 IDEA 的 Alt+Enter）

原因：
- jdevelops 框架的包路径可能因项目而异
- 用户项目可能有自定义的基类实现（如 JpaCommonBean）
- IDE 会自动识别并导入正确的包

---

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
