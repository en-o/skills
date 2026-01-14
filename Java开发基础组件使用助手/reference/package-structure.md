# 包结构选择指南

在使用 JDevelops 框架开发时，有两种主要的包结构组织方式。本文档详细说明两种方式的优缺点和适用场景。

## 包结构对比

### 方式 A：传统三层架构（推荐）

按技术层次划分，相同层次的代码放在同一包下。

```
src/main/java/com/example/project/
├── controller/              # 控制器层（统一管理）
│   ├── user/               # 用户领域
│   │   ├── dto/           # 用户相关请求类
│   │   │   ├── UserAdd.java
│   │   │   ├── UserEdit.java
│   │   │   └── UserPage.java
│   │   ├── vo/            # 用户相关响应类（可选）
│   │   │   └── UserInfo.java
│   │   └── UserController.java
│   │
│   └── order/              # 订单领域
│       ├── dto/
│       └── OrderController.java
│
├── entity/                 # 实体层（所有实体集中）
│   ├── User.java
│   ├── Role.java
│   ├── Order.java
│   └── Product.java
│
├── dao/                    # DAO 层（所有 DAO 集中）
│   ├── UserDao.java
│   ├── RoleDao.java
│   ├── OrderDao.java
│   └── ProductDao.java
│
├── service/                # Service 接口层
│   ├── UserService.java
│   ├── RoleService.java
│   ├── OrderService.java
│   └── ProductService.java
│
└── service/impl/           # Service 实现层
    ├── UserServiceImpl.java
    ├── RoleServiceImpl.java
    ├── OrderServiceImpl.java
    └── ProductServiceImpl.java
```

#### 优点
- ✅ **结构清晰**: 按层次划分，易于理解
- ✅ **易于定位**: 快速找到某一层的所有类
- ✅ **代码复用**: 同层代码易于共享和复用
- ✅ **团队协作**: 不同层次可以由不同人员维护
- ✅ **适合中小型项目**: 项目规模不大时，结构简单高效

#### 缺点
- ⚠️ 大型项目中，单个包下类数量可能过多
- ⚠️ 跨层修改时需要在多个包之间切换

#### 适用场景
- 中小型项目（< 50 个实体）
- 团队规模较小（< 10 人）
- 业务模块耦合度较高
- 希望快速开发、结构简单

---

### 方式 B：垂直切分（模块化）

按业务模块划分，每个模块内包含完整的技术层次。

```
src/main/java/com/example/project/
├── controller/              # 控制器层（统一管理）
│   ├── user/
│   │   ├── dto/
│   │   │   ├── UserAdd.java
│   │   │   └── UserEdit.java
│   │   └── UserController.java
│   │
│   └── order/
│       ├── dto/
│       └── OrderController.java
│
├── user/                    # 用户模块（垂直拆分）
│   ├── entity/
│   │   ├── User.java
│   │   └── Role.java
│   ├── dao/
│   │   ├── UserDao.java
│   │   └── RoleDao.java
│   ├── service/
│   │   ├── UserService.java
│   │   └── RoleService.java
│   └── service/impl/
│       ├── UserServiceImpl.java
│       └── RoleServiceImpl.java
│
├── order/                   # 订单模块（垂直拆分）
│   ├── entity/
│   │   ├── Order.java
│   │   └── OrderItem.java
│   ├── dao/
│   │   ├── OrderDao.java
│   │   └── OrderItemDao.java
│   ├── service/
│   │   └── OrderService.java
│   └── service/impl/
│       └── OrderServiceImpl.java
│
└── product/                 # 商品模块（垂直拆分）
    ├── entity/
    ├── dao/
    ├── service/
    └── service/impl/
```

#### 优点
- ✅ **模块独立**: 每个模块包含完整的业务逻辑
- ✅ **易于拆分**: 可以轻松拆分成独立的微服务
- ✅ **职责清晰**: 模块边界明确，减少耦合
- ✅ **适合大型项目**: 多模块并行开发互不干扰
- ✅ **利于团队分工**: 不同团队负责不同模块

#### 缺点
- ⚠️ 目录层次较深，需要更多导航
- ⚠️ 跨模块复用代码相对困难
- ⚠️ 小型项目中可能显得过度设计

#### 适用场景
- 大型项目（> 50 个实体）
- 团队规模较大（> 10 人）
- 业务模块独立性强
- 未来可能拆分成微服务

---

## 选择建议

### 推荐决策树

```
项目规模？
  ├─ 小型项目（< 20 实体）
  │   └─ 选择：传统三层架构（A）
  │
  ├─ 中型项目（20-50 实体）
  │   ├─ 模块耦合度高？ → 传统三层架构（A）
  │   └─ 模块独立性强？ → 垂直切分（B）
  │
  └─ 大型项目（> 50 实体）
      ├─ 未来会拆分微服务？ → 垂直切分（B）
      └─ 单体应用？ → 根据团队偏好选择
```

### 具体建议

| 项目类型 | 推荐方式 | 原因 |
|---------|---------|------|
| 管理后台（用户、角色、权限、菜单） | A - 传统三层架构 | 模块数量少，耦合度高，结构简单高效 |
| 电商平台（用户、商品、订单、支付） | B - 垂直切分 | 模块独立，业务复杂，便于后续拆分 |
| 内容管理系统（文章、分类、标签、评论） | A - 传统三层架构 | 模块关联紧密，共享逻辑多 |
| SaaS 多租户系统 | B - 垂直切分 | 租户隔离，模块独立，易于扩展 |
| 微服务单个服务 | B - 垂直切分 | 为未来拆分做准备 |

---

## 混合模式

在实际项目中，可以采用混合模式：

### 模式 1：核心模块垂直切分 + 公共模块水平切分

```
src/main/java/com/example/project/
├── controller/              # 控制器层（统一）
│   ├── user/
│   └── order/
│
├── common/                  # 公共模块（水平切分）
│   ├── entity/             # 公共实体（如字典、配置）
│   │   ├── Dictionary.java
│   │   └── SystemConfig.java
│   ├── dao/
│   └── service/
│
├── user/                    # 用户模块（垂直切分）
│   ├── entity/
│   ├── dao/
│   └── service/
│
└── order/                   # 订单模块（垂直切分）
    ├── entity/
    ├── dao/
    └── service/
```

**适用场景**: 有少量公共实体（字典、配置），但核心业务模块独立性强

### 模式 2：小模块三层 + 大模块垂直

```
src/main/java/com/example/project/
├── controller/
│
├── entity/                  # 小模块实体（三层架构）
│   ├── Dictionary.java
│   └── SystemLog.java
│
├── dao/                     # 小模块 DAO
│   ├── DictionaryDao.java
│   └── SystemLogDao.java
│
├── service/                 # 小模块 Service
│
└── order/                   # 大模块（垂直切分）
    ├── entity/
    │   ├── Order.java
    │   ├── OrderItem.java
    │   ├── OrderLog.java
    │   └── OrderRefund.java
    ├── dao/
    └── service/
```

**适用场景**: 部分模块简单（如字典），部分模块复杂（如订单）

---

## 迁移指南

### 从三层架构迁移到垂直切分

如果项目从传统三层架构增长到需要垂直切分：

1. **创建模块包**: 创建新的模块包（如 `user/`、`order/`）
2. **移动相关类**: 将 Entity、DAO、Service 移动到对应模块包
3. **更新导入**: 更新其他类中的 import 语句
4. **保持 Controller**: Controller 层可以保持统一管理
5. **逐步迁移**: 可以一个模块一个模块地迁移，不必一次性全部迁移

---

## 常见问题

### Q1: Controller 一定要按业务域划分吗？

**A**: 是的，无论采用哪种包结构，Controller 都推荐按业务域划分（`controller.{domain}`）。这样可以：
- API 路径清晰（`/api/user/*`、`/api/order/*`）
- 前端对接方便
- API 文档分组明确

### Q2: 公共实体（如字典、配置）放在哪里？

**A**:
- 传统三层架构：放在 `entity/` 包下
- 垂直切分：创建 `common/entity/` 包
- 混合模式：根据使用频率决定

### Q3: 跨模块调用怎么处理？

**A**:
- 避免直接调用其他模块的 DAO
- 通过 Service 层接口调用
- 如果频繁跨模块，考虑提取公共服务

### Q4: 如何处理模块间的依赖？

**A**:
- 定义清晰的接口边界
- 使用 Spring 的依赖注入
- 避免循环依赖
- 考虑使用事件驱动解耦

---

## 参考资源

- JDevelops 框架源码：https://github.com/en-o/Jdevelops
- 官方文档：https://www.yuque.com/tanning/yg9ipo
- 架构规范：[../standards/architecture.md](../standards/architecture.md)
