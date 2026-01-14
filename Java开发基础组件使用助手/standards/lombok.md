# Lombok 使用规范

## 核心原则

**禁止 @Data，按需选择 Lombok 注解**

---

## 强制规范（MUST）

### ❌ 禁止使用

```java
@Data  // ❌ 禁止使用，过于宽泛
```

**原因**：
- `@Data` = `@Getter` + `@Setter` + `@ToString` + `@EqualsAndHashCode` + `@RequiredArgsConstructor`
- 过于宽泛，可能导致不必要的方法生成
- `toString()` 可能输出敏感信息
- `equals()` 和 `hashCode()` 可能不符合业务需求

---

## ✅ 推荐使用

根据实际需求按需选择：

| 注解 | 功能 | 适用场景 |
|-----|------|---------|
| `@Getter` | 生成 getter 方法 | 所有需要读取字段的类 |
| `@Setter` | 生成 setter 方法 | 需要修改字段的类 |
| `@ToString` | 生成 toString 方法 | DTO、VO 类（方便日志调试） |
| `@NoArgsConstructor` | 无参构造器 | JPA Entity、简单 POJO |
| `@AllArgsConstructor` | 全参构造器 | 不可变对象、Builder 模式 |
| `@Builder` | Builder 模式 | 构建复杂对象（VO、配置类） |
| `@EqualsAndHashCode` | equals 和 hashCode | 需要比较的对象 |
| `@RequiredArgsConstructor` | final 字段构造器 | 依赖注入（Controller、Service） |

---

## 分场景使用指南

### Entity 实体类

**推荐组合**：`@Getter` + `@Setter`

**不推荐**：`@ToString`（可能输出敏感信息）

```java
// ✅ 正确
@Getter
@Setter
@Entity
@Table(name = "sys_customer")
public class Customer extends JpaCommonBean {

    @Column(name = "login_name")
    private String loginName;

    @Column(name = "password")
    @JsonIgnore  // 不序列化密码字段
    private String password;

    @Column(name = "phone")
    private String phone;
}

// ❌ 错误
@Data  // 禁止使用
@Entity
public class Customer extends JpaCommonBean {
    // ...
}

// ❌ 错误
@Getter
@Setter
@ToString  // Entity 不建议使用 ToString
@Entity
public class Customer extends JpaCommonBean {
    private String password;  // ToString 可能暴露敏感信息
}
```

---

### DTO 请求类

**推荐组合**：`@Getter` + `@Setter` + `@ToString`

**可选**：`@NoArgsConstructor` + `@AllArgsConstructor`

```java
// ✅ 正确
@Getter
@Setter
@ToString
public class UserAdd {
    @NotBlank(message = "登录名不能为空")
    private String loginName;

    @NotBlank(message = "密码不能为空")
    private String password;

    private String phone;
}

// ✅ 正确（带构造器）
@Getter
@Setter
@ToString
@NoArgsConstructor
@AllArgsConstructor
public class UserEdit {
    @NotNull(message = "ID不能为空")
    private Long id;

    private String userName;
    private String phone;
}

// ❌ 错误
@Data  // 禁止使用
public class UserAdd {
    // ...
}
```

---

### VO 响应类

**推荐组合**：`@Getter` + `@Setter` + `@Builder`

**可选**：`@NoArgsConstructor` + `@AllArgsConstructor`（Builder 需要）

```java
// ✅ 正确（Builder 模式）
@Getter
@Setter
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class UserInfo {
    private Long id;
    private String loginName;
    private String userName;

    @JsonSerialize(using = ToStringSerializer.class)
    private Long roleId;
}

// ✅ 正确（简单响应类）
@Getter
@Setter
public class UserInfo {
    private Long id;
    private String loginName;
    private String userName;
}

// ❌ 错误
@Data  // 禁止使用
@Builder
public class UserInfo {
    // ...
}
```

---

### Controller 类

**推荐组合**：`@RequiredArgsConstructor`（用于依赖注入）

**可选**：`@Slf4j`（用于日志）

```java
// ✅ 正确（使用构造器注入）
@PathRestController("user")
@Tag(name = "用户管理")
@RequiredArgsConstructor  // 生成 final 字段的构造器
@Slf4j
public class CustomerController {

    private final CustomerService customerService;

    @PostMapping("add")
    public ResultVO<String> add(@RequestBody @Valid UserAdd add) {
        log.info("新增用户：{}", add);
        customerService.saveCustomer(add);
        return ResultVO.success("新增成功");
    }
}

// ✅ 正确（手动构造器注入）
@PathRestController("user")
@Tag(name = "用户管理")
@Slf4j
public class CustomerController {

    private final CustomerService customerService;

    public CustomerController(CustomerService customerService) {
        this.customerService = customerService;
    }

    // 方法...
}

// ❌ 错误（使用字段注入）
@PathRestController("user")
public class CustomerController {

    @Autowired  // 不推荐使用字段注入
    private CustomerService customerService;
}
```

---

### Service 实现类

**推荐组合**：`@RequiredArgsConstructor`（用于依赖注入）

```java
// ✅ 正确
@Service
@RequiredArgsConstructor
public class CustomerServiceImpl extends J2ServiceImpl<Customer>
    implements CustomerService {

    private final CustomerDao customerDao;

    @Override
    public Optional<Customer> findByLoginName(String loginName) {
        return findOne("loginName", loginName, SQLOperator.EQ);
    }
}

// ✅ 正确（手动构造器注入）
@Service
public class CustomerServiceImpl extends J2ServiceImpl<Customer>
    implements CustomerService {

    private final CustomerDao customerDao;

    public CustomerServiceImpl(CustomerDao customerDao) {
        this.customerDao = customerDao;
    }

    // 方法...
}
```

---

### 不可变对象

**推荐组合**：`@Getter` + `@AllArgsConstructor` + `@Builder`

```java
// ✅ 正确（不可变对象）
@Getter
@AllArgsConstructor
@Builder
public class UserToken {
    private final String token;
    private final Long expireTime;
    private final String refreshToken;
}

// 使用示例
UserToken token = UserToken.builder()
    .token("xxx")
    .expireTime(System.currentTimeMillis() + 7200)
    .refreshToken("yyy")
    .build();
```

---

### 简单 POJO

**推荐组合**：`@Getter` + `@Setter` + `@NoArgsConstructor`

```java
// ✅ 正确
@Getter
@Setter
@NoArgsConstructor
public class UserProfile {
    private String name;
    private Integer age;
    private String address;
}
```

---

## 字段可见性控制

### 使用 @JsonIgnore（永久隐藏）

```java
@Getter
@Setter
@Entity
public class Customer extends JpaCommonBean {

    private String loginName;

    @JsonIgnore  // 该字段永远不会被序列化
    private String password;

    @JsonIgnore  // 内部字段，不对外暴露
    private String internalToken;
}
```

### 使用 @JsonView（按场景控制）

```java
// 定义视图接口
public class Views {
    public interface Public {}
    public interface Internal extends Public {}
    public interface Admin extends Internal {}
}

// Entity 中使用
@Getter
@Setter
@Entity
public class Customer extends JpaCommonBean {

    @JsonView(Views.Public.class)
    private Long id;

    @JsonView(Views.Public.class)
    private String loginName;

    @JsonView(Views.Internal.class)  // 仅内部接口可见
    private String phone;

    @JsonView(Views.Admin.class)  // 仅管理员接口可见
    private String email;

    @JsonIgnore  // 永不序列化
    private String password;
}

// Controller 中使用
@GetMapping("public-info")
@JsonView(Views.Public.class)
public ResultVO<Customer> publicInfo(@RequestParam Long id) {
    // 只返回带有 Views.Public 的字段：id, loginName
    return ResultVO.success(customerService.findById(id).orElseThrow());
}

@GetMapping("admin-info")
@JsonView(Views.Admin.class)
public ResultVO<Customer> adminInfo(@RequestParam Long id) {
    // 返回带有 Views.Admin 及其父类视图的字段
    return ResultVO.success(customerService.findById(id).orElseThrow());
}
```

---

## 最佳实践总结

### 推荐的注解组合

| 场景 | 推荐注解组合 | 说明 |
|-----|------------|------|
| Entity 实体类 | `@Getter` + `@Setter` + `@JsonIgnore/@JsonView` | 避免 toString 输出敏感信息 |
| DTO 请求类 | `@Getter` + `@Setter` + `@ToString` | 方便日志调试 |
| VO 响应类 | `@Getter` + `@Setter` + `@Builder` | 方便构建返回对象 |
| Controller | `@RequiredArgsConstructor` + `@Slf4j` | 构造器注入 + 日志 |
| Service | `@RequiredArgsConstructor` | 构造器注入 |
| 不可变对象 | `@Getter` + `@AllArgsConstructor` + `@Builder` | 线程安全 |
| 简单POJO | `@Getter` + `@Setter` + `@NoArgsConstructor` | 最小化依赖 |

---

## 验证命令

### 检查是否使用了 @Data

```bash
# 检查项目中是否存在 @Data 注解
grep -r "@Data" --include="*.java" .

# 如果有结果，说明存在违规使用
```

### 检查 Entity 是否使用了 @ToString

```bash
# 检查 Entity 是否使用了 @ToString
find . -path "*/entity/*.java" -exec grep -l "@ToString" {} \;

# Entity 类不应该使用 @ToString
```

---

## 迁移指南

### 从 @Data 迁移到推荐注解

```java
// 迁移前
@Data
@Entity
public class Customer extends JpaCommonBean {
    private String loginName;
    private String password;
}

// 迁移后
@Getter
@Setter
@Entity
public class Customer extends JpaCommonBean {
    private String loginName;

    @JsonIgnore
    private String password;
}
```

```java
// 迁移前
@Data
public class UserAdd {
    private String loginName;
    private String password;
}

// 迁移后
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

---

## 常见问题

### Q1：为什么 Entity 不推荐使用 @ToString？

**A**：`toString()` 方法可能输出敏感信息（如密码），在日志中暴露。如果确实需要，使用 `@ToString(exclude = {"password"})` 排除敏感字段。

### Q2：为什么不推荐 @Autowired 字段注入？

**A**：构造器注入的优势：
- 依赖关系更明确
- 更易于单元测试
- 避免空指针异常
- 可以将依赖声明为 final

### Q3：Builder 模式什么时候使用？

**A**：适用场景：
- 响应类（VO）构建
- 配置类构建
- 不可变对象构建
- 字段较多的对象构建

---

## 相关规范

- 命名规范：[./naming.md](./naming.md)
- 架构规范：[./architecture.md](./architecture.md)
- Entity 指南：[../guides/entity.md](../guides/entity.md)
