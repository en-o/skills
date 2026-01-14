# 新增业务模块工作流

## 工作流清单

复制此清单并跟踪进度：

```
模块创建进度：
- [ ] 步骤1：分析需求（确定模块名、功能、字段）
- [ ] 步骤2：查阅参考资料（确认 API 和包路径）
- [ ] 步骤3：创建 Entity 类
- [ ] 步骤4：创建 DAO 接口
- [ ] 步骤5：创建 Service 接口和实现
- [ ] 步骤6：创建 Controller 和请求/响应类
- [ ] 步骤7：验证代码规范
```

---

## 步骤1：分析需求

### ⚠️ 交互式询问

**如果用户未提供以下信息，必须进行询问**：

#### 1. 项目描述和业务场景

如果用户未提供项目背景，必须先询问：
- **询问**: 请描述您的项目是做什么的？有哪些主要功能模块？
- **说明**: 了解项目整体情况，帮助规划模块结构
- **示例回答**:
  - "这是一个管理后台系统，需要基础的用户、字典、角色、权限、菜单等功能"
  - "这是一个电商平台，需要商品管理、订单管理、用户管理等模块"
  - "这是一个内容管理系统，需要文章、分类、标签、评论等功能"

#### 2. 包结构选择

如果是首次添加业务模块，需要询问包结构偏好：
- **询问**: 请选择您希望使用的包结构
- **选项**:

  - **选项 A - 传统三层架构（推荐小型项目）**:
    ```
    src/main/java/{basePackage}/
    ├── controller/{domain}/     # 控制器层（按业务域划分）
    │   ├── dto/                # 请求类
    │   └── vo/                 # 响应类
    ├── entity/                 # 实体层（所有实体集中）
    ├── dao/                    # DAO 层（所有 DAO 集中）
    ├── service/                # Service 接口层
    └── service/impl/           # Service 实现层
    ```
    - **优点**: 结构清晰、易于定位、适合中小型项目
    - **适用**: < 50 个实体的项目

  - **选项 B - 垂直切分（推荐中型项目）**:
    ```
    src/main/java/{basePackage}/
    ├── controller/{domain}/     # 控制器层（按业务域划分）
    │   ├── dto/
    │   └── vo/
    └── {module}/               # 业务模块（按功能垂直拆分）
        ├── entity/            # 模块内所有实体
        ├── dao/               # 模块内所有 DAO
        ├── service/           # 模块内所有 Service 接口
        └── service/impl/      # 模块内所有 Service 实现
    ```
    - **优点**: 模块独立、易于拆分微服务、适合大型项目
    - **适用**: 50-100 个实体，模块独立性强

  - **选项 C - 标准目录结构（推荐大型项目）**:
    ```
    src/main/java/{basePackage}/
    ├── controller/{domain}/     # 控制器层（统一管理）
    │   ├── dto/
    │   └── vo/
    ├── common/                 # 公共组件层
    ├── core/                   # 核心配置层
    └── modules/                # 业务模块层
        └── {module}/          # 大模块
            └── {submodule}/   # 子模块
                ├── entity/
                ├── dao/
                ├── service/
                └── service/impl/
    ```
    - **优点**: 高度模块化、支持大型项目、便于团队分工
    - **适用**: > 100 个实体，多团队协作，复杂业务场景

- **说明**:
  - 如果项目已有代码，则沿用现有结构
  - 新项目推荐根据项目规模选择：
    - 小型项目（< 50 实体）→ 传统三层架构（选项 A）
    - 中型项目（50-100 实体）→ 垂直切分（选项 B）
    - 大型项目（> 100 实体）→ 标准目录结构（选项 C）
  - 详细说明请参考 [../reference/package-structure.md](../reference/package-structure.md)

#### 3. 数据库结构提供方式

询问用户如何提供数据表结构：
- **询问**: 请选择如何定义数据表结构
- **选项**:
  - **选项 A**: 我已有数据库表结构（DDL 或表结构截图），请根据它生成 Entity
  - **选项 B**: 我提供字段清单，请帮我生成 Entity
  - **选项 C**: 我口头描述需求，请你设计数据表并生成 Entity
  - **选项 D**: 我自己已经写好了 Entity，跳过这步

- **说明**:
  - 选项 A 和 B：请在后续消息中提供表结构或字段清单
  - 选项 C：AI 将根据业务需求设计合理的数据表结构
  - 选项 D：直接进入 Service 和 Controller 创建

#### 4. 模块基本信息

明确以下信息：

**模块命名**：
- **选项 A（传统三层架构）**：
  - 作为类名前缀（如 Customer → CustomerDao、CustomerService）

- **选项 B（垂直切分）**：
  - 作为模块包名（如 `{basePackage}.customer`）
  - 模块内所有类都在该包下（customer.entity、customer.dao、customer.service）

- **选项 C（标准目录结构）**：
  - **大模块名**：业务领域（如 account、biz、file、logs）
  - **子模块名**：具体功能（如 account.suser、account.role、account.org）
  - 路径格式：`{basePackage}.modules.{module}.{submodule}`

**业务领域**（Controller 路径）：
- 用于：决定 Controller 所在包（controller.user、controller.sys、controller.logs）
- 无论采用哪种包结构，Controller 都统一按业务域划分

**核心字段**：
- 哪些字段必需
- 哪些字段敏感（密码、token 等）
- 哪些字段需要脱敏

**是否需要脱敏**：
- 决定是否创建单独的响应类（VO）

### 决策树：是否需要创建响应类？

```
需要返回数据？
  ├─ 包含敏感字段（密码、token）？
  │   ├─ 是 → 使用 @JsonIgnore 或创建单独响应类
  │   └─ 否 → 继续判断
  └─ 需要按场景控制可见性？
      ├─ 是 → 使用 @JsonView 定义视图
      └─ 否 → 直接返回 Entity
```

### 信息确认

在开始生成代码前，确认以下信息：
- [ ] 项目描述和业务场景已明确
- [ ] 包结构选择已确定（A/B/C）
- [ ] 数据表结构提供方式已确定
- [ ] 模块命名已明确
  - 选项 A/B：模块名（如 customer、order）
  - 选项 C：大模块名和子模块名（如 account.suser）
- [ ] 业务领域已明确（Controller 路径）
- [ ] 核心字段需求已明确

---

## 步骤2：查阅参考资料

**关键：确认包路径和 API**

### 查阅顺序

1. **查官方文档**：https://www.yuque.com/tanning/yg9ipo
   - 查找 Entity 基类（JpaCommonBean、JpaCommonBean2）
   - 查找 Service 基类（J2Service、J2ServiceImpl）
   - 查找注解用法（@PathRestController、@ApiMapping）

2. **文档找不到** → 查 GitHub 源码：https://github.com/en-o/Jdevelops
   - 查看最新方法签名
   - 确认包路径

3. **下载文档到本地**（可选）：
   ```bash
   bash scripts/download-docs.sh
   ```

详细策略：[../reference/lookup-strategy.md](../reference/lookup-strategy.md)

---

## 步骤3：创建 Entity 类

查阅详细指南：[../guides/entity.md](../guides/entity.md)

### 快速检查清单

- [ ] 继承 `JpaCommonBean` 或 `JpaCommonBean2`
- [ ] 使用 `@Getter @Setter`（**禁止** @Data）
- [ ] 使用 `@Entity @Table` 注解
- [ ] Long 类型添加 `@JsonSerialize(using = ToStringSerializer.class)`
- [ ] 敏感字段添加 `@JsonIgnore` 或 `@JsonView`
- [ ] 使用 `@Column` 指定字段属性（columnDefinition、nullable 等）
- [ ] 使用 `@Comment` 添加注释
- [ ] 使用 `@Schema` 添加 Swagger 文档

### 最小示例

```java
@Getter
@Setter
@Entity
@Table(name = "sys_customer")
@Comment("客户表")
public class Customer extends JpaCommonBean {

    @Column(name = "login_name", nullable = false, unique = true, length = 50)
    @Comment("登录名")
    @Schema(description = "登录名")
    private String loginName;

    @Column(name = "password", nullable = false)
    @Comment("密码")
    @JsonIgnore  // 敏感字段
    private String password;

    @Column(name = "role_id")
    @JsonSerialize(using = ToStringSerializer.class)
    private Long roleId;
}
```

---

## 步骤4：创建 DAO 接口

DAO 接口继承 `JpaRepository`，由框架自动实现。

```java
// {module}/dao/CustomerDao.java
public interface CustomerDao extends JpaRepository<Customer, Long> {
    // 自定义查询方法（可选）
    Optional<Customer> findByLoginName(String loginName);
}
```

---

## 步骤5：创建 Service 接口和实现

查阅详细指南：[../guides/service.md](../guides/service.md)

### Service 接口

```java
// {module}/service/CustomerService.java
public interface CustomerService extends J2Service<Customer> {
    Optional<Customer> findByLoginName(String loginName);
}
```

### Service 实现

```java
// {module}/service/impl/CustomerServiceImpl.java
@Service
public class CustomerServiceImpl extends J2ServiceImpl<Customer>
    implements CustomerService {

    private final CustomerDao customerDao;

    public CustomerServiceImpl(CustomerDao customerDao) {
        this.customerDao = customerDao;
    }

    @Override
    public Optional<Customer> findByLoginName(String loginName) {
        return findOne("loginName", loginName, SQLOperator.EQ);
    }
}
```

**关键点**：
- 继承 `J2ServiceImpl<Entity>`
- 实现 `CustomerService` 接口
- 使用构造器注入 DAO
- 使用框架提供的基础方法（findOne、save、update 等）

---

## 步骤6：创建 Controller 和请求/响应类

查阅详细指南：
- Controller：[../guides/controller.md](../guides/controller.md)
- 请求/响应类：[../guides/request-response.md](../guides/request-response.md)

### Controller 类

```java
@PathRestController("user")
@Tag(name = "用户管理", extensions = {@Extension(properties = {
    @ExtensionProperty(name = "x-order", value = "3", parseValue = true)})})
public class CustomerController {

    private final CustomerService customerService;

    public CustomerController(CustomerService customerService) {
        this.customerService = customerService;
    }

    @PostMapping("add")
    @Operation(summary = "新增用户")
    public ResultVO<String> add(@RequestBody @Valid UserAdd add) {
        // 业务逻辑
        return ResultVO.success("新增成功");
    }

    @GetMapping("detail")
    @Operation(summary = "用户详情")
    public ResultVO<Customer> detail(@RequestParam Long id) {
        Customer customer = customerService.findById(id).orElseThrow();
        return ResultVO.success(customer);
    }
}
```

### 请求类（dto/）

命名规范：**UserAdd、UserEdit、UserPage**（禁止 VO/DTO 后缀）

```java
// controller/user/dto/UserAdd.java
@Getter
@Setter
@ToString
public class UserAdd {
    @NotBlank(message = "登录名不能为空")
    private String loginName;

    @NotBlank(message = "密码不能为空")
    private String password;
}
```

### 响应类（vo/）

**优先直接返回 Entity**，仅在需要脱敏时创建：

```java
// controller/user/vo/UserInfo.java
@Getter
@Setter
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class UserInfo {
    private Long id;
    private String loginName;
    private String userName;
    // 不包含密码等敏感字段
}
```

---

## 步骤7：验证代码规范

运行完整的检查清单：[./modify-code.md](./modify-code.md)

### 快速验证命令

```bash
# 检查命名规范
grep -r "DTO\|VO" --include="*.java" . | grep "class.*\(DTO\|VO\)"

# 检查 @Data 注解
grep -r "@Data" --include="*.java" .

# 检查框架注解
grep -r "@PathRestController" --include="*.java" controller/
grep -r "extends J2Service" --include="*.java" {module}/service/
grep -r "extends JpaCommonBean" --include="*.java" {module}/entity/
```

### 必须验证的项目

- [ ] 包路径符合规范（controller.{domain} 或 {module}.{layer}）
- [ ] 继承了正确的框架基类
- [ ] 使用了框架注解（@PathRestController、@ApiMapping）
- [ ] 统一返回格式（ResultVO/ResultPageVO）
- [ ] 命名无 VO/DTO 后缀
- [ ] 禁用了 @Data
- [ ] 敏感字段使用了 @JsonIgnore 或 @JsonView
- [ ] Long 类型字段添加了 @JsonSerialize
- [ ] 添加了 Swagger 注解

---

## ✅ 完成标志

当以下所有项都完成时，模块创建完成：

- [ ] 代码符合 [../standards/](../standards/) 中的所有强制规范
- [ ] 通过检查清单验证
- [ ] 可以成功编译
- [ ] API 文档生成正确（Swagger UI）
- [ ] 基础功能测试通过

---

## 📚 相关参考

- 完整示例：[../examples/complete-module.md](../examples/complete-module.md)
- 架构规范：[../standards/architecture.md](../standards/architecture.md)
- 命名规范：[../standards/naming.md](../standards/naming.md)
- Lombok 规范：[../standards/lombok.md](../standards/lombok.md)
