# 命名规范

## 核心原则

**意图驱动命名，禁止 VO/DTO 后缀**

---

## 请求参数类命名（Input）

### 强制规范（MUST）

- ❌ **禁止**以 VO、DTO 结尾
- ✅ **必须**使用意图名，清晰表达操作目的

### 命名规范

| 操作类型 | 命名规范 | 示例 |
|---------|---------|------|
| 新增 | `{Entity}Add` | `UserAdd`、`CustomerAdd` |
| 编辑 | `{Entity}Edit` | `UserEdit`、`CustomerEdit` |
| 删除 | `{Entity}Delete` | `UserDelete`、`CustomerDelete` |
| 分页查询 | `{Entity}Page` | `UserPage`、`CustomerPage` |
| 条件查询 | `{Entity}Query` | `UserQuery`、`CustomerQuery` |
| 特定操作 | `{Noun}{Verb}` | `PasswordReset`、`CustomerAudit` |

### 示例

```java
// ✅ 正确命名
public class UserAdd {
    @NotBlank(message = "登录名不能为空")
    private String loginName;

    @NotBlank(message = "密码不能为空")
    private String password;
}

public class UserEdit {
    @NotNull(message = "ID不能为空")
    private Long id;

    private String userName;
    private String phone;
}

public class UserPage {
    private String loginName;
    private Integer status;
}

// ❌ 错误命名
public class UserDTO { }        // 禁止 DTO 后缀
public class UserAddDTO { }     // 禁止 DTO 后缀
public class UserVO { }         // 禁止 VO 后缀
public class UserEditVO { }     // 禁止 VO 后缀
```

---

## 响应参数类命名（Output）

### 强制规范（MUST）

- ❌ **禁止**以 VO、DTO 结尾
- ✅ **优先**直接返回 Entity（无需脱敏或额外处理时）
- ✅ **仅当需要**脱敏、字段裁剪、额外包裹时，使用意图名

### 决策树：何时创建响应类？

```
需要返回数据？
  ├─ 包含敏感字段（密码、token）？
  │   ├─ 是 → 使用 @JsonIgnore 或创建 {Entity}Info 类
  │   └─ 否 → 继续判断
  └─ 需要按场景控制可见性？
      ├─ 是 → 使用 @JsonView 定义视图
      └─ 否 → 直接返回 Entity
```

### 命名规范

| 场景 | 命名规范 | 示例 |
|-----|---------|------|
| 直接返回（推荐） | `ResultVO<Entity>` | `ResultVO<Customer>` |
| 需要脱敏 | `{Entity}Info` | `UserInfo`、`CustomerInfo` |
| 用户档案 | `{Entity}Profile` | `UserProfile` |
| 摘要信息 | `{Entity}Summary` | `CustomerSummary` |
| 详情信息 | `{Entity}Detail` | `OrderDetail` |

### 示例

```java
// ✅ 优先：直接返回 Entity
@GetMapping("detail")
@Operation(summary = "用户详情")
public ResultVO<Customer> detail(@RequestParam Long id) {
    Customer customer = customerService.findById(id).orElseThrow();
    return ResultVO.success(customer);
}

// ✅ 需要脱敏时：创建意图命名类
@GetMapping("info")
@Operation(summary = "用户信息（脱敏）")
public ResultVO<UserInfo> info(@RequestParam Long id) {
    UserInfo info = customerService.getUserInfo(id);
    return ResultVO.success(info);
}

// UserInfo.java
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

// ❌ 错误命名
public class UserInfoVO { }     // 禁止 VO 后缀
public class UserVO { }         // 禁止 VO 后缀
public class CustomerDTO { }    // 禁止 DTO 后缀
```

---

## Entity 类命名

### 强制规范（MUST）

- ✅ 使用业务名词，不带表前缀
- ✅ 使用单数形式
- ✅ 清晰表达业务含义

### 命名规范

| 业务对象 | Entity 命名 | 表名 |
|---------|------------|------|
| 客户 | `Customer` | `tb_customer` 或 `sys_customer` |
| 订单 | `Order` | `tb_order` |
| 产品 | `Product` | `tb_product` |
| 用户 | `User` | `sys_user` |
| 角色 | `Role` | `sys_role` |

### 示例

```java
// ✅ 正确命名
@Entity
@Table(name = "sys_customer")
public class Customer extends JpaCommonBean {
    // 字段定义
}

@Entity
@Table(name = "tb_order")
public class Order extends JpaCommonBean {
    // 字段定义
}

// ❌ 错误命名
public class TbCustomer { }      // 不要包含表前缀
public class SysUser { }         // 不要包含表前缀
public class Customers { }       // 不要使用复数
public class CustomerEntity { }  // 不要加 Entity 后缀
```

---

## Service 类命名

### 强制规范（MUST）

- ✅ 接口使用 `{Entity}Service`
- ✅ 实现类使用 `{Entity}ServiceImpl`

### 示例

```java
// ✅ 正确命名
public interface CustomerService extends J2Service<Customer> {
    Optional<Customer> findByLoginName(String loginName);
}

@Service
public class CustomerServiceImpl extends J2ServiceImpl<CustomerDao, Customer, Long>
    implements CustomerService {
    // 实现
}

// ❌ 错误命名
public interface CustomerServiceInterface { }  // 不要加 Interface 后缀
public class CustomerServiceImp { }           // Impl 不要缩写
public class CustomerSvc { }                  // Service 不要缩写
```

---

## DAO 类命名

### 强制规范（MUST）

- ✅ 使用 `{Entity}Dao` 或 `{Entity}Repository`
- ✅ 继承 `JpaRepository<Entity, Long>`

### 示例

```java
// ✅ 正确命名
public interface CustomerDao extends JpaRepository<Customer, Long> {
    Optional<Customer> findByLoginName(String loginName);
}

// 或者
public interface CustomerRepository extends JpaRepository<Customer, Long> {
    Optional<Customer> findByLoginName(String loginName);
}

// ❌ 错误命名
public interface CustomerMapper { }  // 不使用 MyBatis 风格
public interface CustomerDAO { }     // 全大写不推荐
```

---

## Controller 类命名

### 强制规范（MUST）

- ✅ 使用 `{Entity}Controller`
- ✅ 不使用 `Api`、`Rest` 等前缀/后缀

### 示例

```java
// ✅ 正确命名
@PathRestController("user")
@Tag(name = "用户管理")
public class CustomerController {
    // 控制器方法
}

// ❌ 错误命名
public class CustomerApi { }           // 不要用 Api 后缀
public class CustomerRestController { }  // 不要用 Rest 前缀
public class UserController { }        // 应与 Entity 名称对应（Customer）
```

---

## 方法命名

### Service 方法命名

| 操作 | 命名规范 | 示例 |
|-----|---------|------|
| 查询单个 | `findByXxx` | `findByLoginName(String loginName)` |
| 查询列表 | `findXxxList` | `findActiveCustomerList()` |
| 查询分页 | `findXxxPage` | `findCustomerPage(PageQuery query)` |
| 保存 | `save` 或 `saveOne` | `saveCustomer(Customer customer)` |
| 更新 | `update` 或 `updateOne` | `updateCustomer(Customer customer)` |
| 删除 | `delete` 或 `deleteById` | `deleteCustomer(Long id)` |
| 判断存在 | `existsByXxx` | `existsByLoginName(String loginName)` |
| 统计 | `countByXxx` | `countActiveCustomers()` |

### Controller 方法命名

| 操作 | 命名规范 | 示例 |
|-----|---------|------|
| 新增 | `add` | `add(@RequestBody UserAdd add)` |
| 编辑 | `edit` | `edit(@RequestBody UserEdit edit)` |
| 删除 | `delete` | `delete(@RequestParam Long id)` |
| 详情 | `detail` | `detail(@RequestParam Long id)` |
| 列表 | `list` | `list(@RequestBody UserQuery query)` |
| 分页 | `page` | `page(@RequestBody UserPage page)` |

### 示例

```java
// Service
public interface CustomerService extends J2Service<Customer> {
    Optional<Customer> findByLoginName(String loginName);
    List<Customer> findActiveCustomerList();
    Page<Customer> findCustomerPage(UserPage page);
    void saveCustomer(Customer customer);
    void updateCustomer(Customer customer);
    void deleteCustomer(Long id);
    boolean existsByLoginName(String loginName);
}

// Controller
@PathRestController("user")
public class CustomerController {

    @PostMapping("add")
    public ResultVO<String> add(@RequestBody @Valid UserAdd add) { }

    @PostMapping("edit")
    public ResultVO<String> edit(@RequestBody @Valid UserEdit edit) { }

    @GetMapping("delete")
    public ResultVO<String> delete(@RequestParam Long id) { }

    @GetMapping("detail")
    public ResultVO<Customer> detail(@RequestParam Long id) { }

    @PostMapping("page")
    public ResultPageVO<Customer, JpaPageResult<Customer>> page(
        @RequestBody @Valid UserPage page) { }
}
```

---

## 字段命名

### Java 字段命名

- ✅ 使用驼峰命名法（camelCase）
- ✅ 清晰表达字段含义
- ✅ 避免缩写（除非是通用缩写，如 id、url）

```java
// ✅ 正确
private String loginName;
private String password;
private LocalDateTime lastLoginTime;
private Long roleId;

// ❌ 错误
private String login_name;   // 不使用下划线
private String pwd;          // 不使用缩写
private String s;            // 不使用单字母
```

### 数据库字段命名

- ✅ 使用下划线命名法（snake_case）
- ✅ 使用 `@Column(name = "...")` 显式指定

```java
@Column(name = "login_name", nullable = false, length = 50)
private String loginName;

@Column(name = "last_login_time")
private LocalDateTime lastLoginTime;

@Column(name = "role_id")
private Long roleId;
```

---

## 常量和枚举命名

### 常量命名

- ✅ 全大写，使用下划线分隔
- ✅ 清晰表达常量含义

```java
public class Constants {
    public static final String DEFAULT_PASSWORD = "123456";
    public static final int MAX_LOGIN_ATTEMPTS = 5;
    public static final long TOKEN_EXPIRE_TIME = 7200;
}
```

### 枚举命名

- ✅ 枚举类使用单数名词
- ✅ 枚举值全大写，使用下划线分隔

```java
public enum AccountStatus {
    NORMAL(1, "正常"),
    LOCKED(2, "锁定"),
    DELETED(3, "已删除");

    private final Integer code;
    private final String desc;

    AccountStatus(Integer code, String desc) {
        this.code = code;
        this.desc = desc;
    }
}
```

---

## 目录命名

虽然目录名保留 `dto/` 和 `vo/`（历史兼容），但**类名严格遵循意图命名规范**。

```
controller/user/
├── dto/              # 目录名保留
│   ├── UserAdd.java      # ✅ 类名不带 DTO 后缀
│   ├── UserEdit.java     # ✅ 类名不带 DTO 后缀
│   └── UserPage.java     # ✅ 类名不带 DTO 后缀
├── vo/               # 目录名保留
│   └── UserInfo.java     # ✅ 类名不带 VO 后缀
└── CustomerController.java
```

---

## 验证命令

### 检查 VO/DTO 后缀

```bash
# 检查是否存在 VO/DTO 后缀的类
grep -r "class.*\(DTO\|VO\)\s" --include="*.java" .
```

### 检查命名规范

```bash
# 检查 Controller 命名
find . -name "*Controller.java" | grep -E "(Api|Rest)"

# 检查 Service 命名
find . -name "*Service*.java" | grep -v -E "(Service\.java|ServiceImpl\.java)"

# 检查请求/响应类命名
find controller -name "*.java" | xargs grep "class" | grep -E "(DTO|VO)"
```

---

## 相关规范

- 架构规范：[./architecture.md](./architecture.md)
- Lombok 规范：[./lombok.md](./lombok.md)
- 注解规范：[./annotations.md](./annotations.md)
