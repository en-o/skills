# 请求/响应类生成指南

## 核心原则

- 请求类：使用意图命名（UserAdd、UserEdit、UserPage）
- 响应类：优先返回 Entity，需要脱敏时用意图名（UserInfo）
- 禁止 VO/DTO 后缀

---

## 请求类（DTO）

### 新增请求类

```java
// controller/user/dto/UserAdd.java
@Getter
@Setter
@ToString
public class UserAdd {

    @NotBlank(message = "登录名不能为空")
    @Schema(description = "登录名", requiredMode = Schema.RequiredMode.REQUIRED)
    private String loginName;

    @NotBlank(message = "密码不能为空")
    @Size(min = 6, max = 20, message = "密码长度必须在6-20之间")
    @Schema(description = "密码", requiredMode = Schema.RequiredMode.REQUIRED)
    private String password;

    @Email(message = "邮箱格式不正确")
    @Schema(description = "邮箱")
    private String email;

    @Pattern(regexp = "^1[3-9]\\d{9}$", message = "手机号格式不正确")
    @Schema(description = "手机号")
    private String phone;
}
```

### 编辑请求类

```java
// controller/user/dto/UserEdit.java
@Getter
@Setter
@ToString
public class UserEdit {

    @NotNull(message = "ID不能为空")
    @Schema(description = "用户ID", requiredMode = Schema.RequiredMode.REQUIRED)
    private Long id;

    @Schema(description = "用户名")
    private String userName;

    @Email(message = "邮箱格式不正确")
    @Schema(description = "邮箱")
    private String email;

    @Schema(description = "手机号")
    private String phone;
}
```

### 分页查询请求类

```java
// controller/user/dto/UserPage.java
@Getter
@Setter
@ToString
public class UserPage extends PageQuery {

    @Schema(description = "登录名")
    private String loginName;

    @Schema(description = "状态")
    private Integer status;

    @Schema(description = "开始时间")
    @JsonFormat(pattern = "yyyy-MM-dd HH:mm:ss")
    private LocalDateTime startTime;

    @Schema(description = "结束时间")
    @JsonFormat(pattern = "yyyy-MM-dd HH:mm:ss")
    private LocalDateTime endTime;
}
```

### 条件查询请求类

```java
// controller/user/dto/UserQuery.java
@Getter
@Setter
@ToString
public class UserQuery {

    @Schema(description = "关键词（登录名或用户名）")
    private String keyword;

    @Schema(description = "状态")
    private Integer status;

    @Schema(description = "角色ID")
    private Long roleId;
}
```

---

## 响应类（VO）

### 决策树：何时创建响应类？

```
需要返回数据？
  ├─ 包含敏感字段？
  │   └─ 是 → 使用 @JsonIgnore 或创建 UserInfo 类
  └─ 需要按场景控制可见性？
      ├─ 是 → 使用 @JsonView
      └─ 否 → 直接返回 Entity
```

### 优先：直接返回 Entity

```java
@GetMapping("detail")
@Operation(summary = "用户详情")
public ResultVO<Customer> detail(@RequestParam Long id) {
    // 直接返回 Entity（推荐）
    Customer customer = customerService.findById(id).orElseThrow();
    return ResultVO.success(customer);
}
```

### 需要脱敏时：创建响应类

```java
// controller/user/vo/UserInfo.java
@Getter
@Setter
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class UserInfo {

    @Schema(description = "用户ID")
    private Long id;

    @Schema(description = "登录名")
    private String loginName;

    @Schema(description = "用户名")
    private String userName;

    @Schema(description = "手机号（脱敏）")
    private String phone;

    @JsonSerialize(using = ToStringSerializer.class)
    @Schema(description = "角色ID")
    private Long roleId;

    // 不包含密码等敏感字段
}
```

### 使用 @JsonView 控制可见性

```java
// 定义视图
public class Views {
    public interface Public {}
    public interface Internal extends Public {}
    public interface Admin extends Internal {}
}

// Controller 中使用
@GetMapping("public-info")
@JsonView(Views.Public.class)
public ResultVO<Customer> publicInfo(@RequestParam Long id) {
    // 只返回 @JsonView(Views.Public.class) 标记的字段
    return ResultVO.success(customer);
}

@GetMapping("admin-info")
@JsonView(Views.Admin.class)
public ResultVO<Customer> adminInfo(@RequestParam Long id) {
    // 返回所有 Admin 视图及其父类视图的字段
    return ResultVO.success(customer);
}
```

---

## 常用验证注解

| 注解 | 说明 | 示例 |
|-----|------|------|
| `@NotNull` | 不能为 null | `@NotNull(message = "ID不能为空")` |
| `@NotBlank` | 不能为空字符串 | `@NotBlank(message = "用户名不能为空")` |
| `@NotEmpty` | 集合不能为空 | `@NotEmpty(message = "角色列表不能为空")` |
| `@Size` | 字符串/集合长度 | `@Size(min = 6, max = 20, message = "密码长度6-20")` |
| `@Min` | 最小值 | `@Min(value = 1, message = "年龄最小为1")` |
| `@Max` | 最大值 | `@Max(value = 150, message = "年龄最大为150")` |
| `@Email` | 邮箱格式 | `@Email(message = "邮箱格式不正确")` |
| `@Pattern` | 正则表达式 | `@Pattern(regexp = "^1[3-9]\\d{9}$")` |

---

## 对象转换

### Entity → VO

```java
// Service 中
public UserInfo getUserInfo(Long id) {
    Customer customer = findById(id).orElseThrow();

    // 使用框架工具转换
    UserInfo info = SerializableBean.to2(customer, UserInfo.class);

    // 手机号脱敏
    if (StringUtils.isNotBlank(info.getPhone())) {
        info.setPhone(info.getPhone().replaceAll("(\\d{3})\\d{4}(\\d{4})", "$1****$2"));
    }

    return info;
}
```

### DTO → Entity

```java
// Service 中
public void saveCustomer(UserAdd add) {
    // 使用框架工具转换
    Customer customer = SerializableBean.to2(add, Customer.class);

    // 额外处理
    customer.setPassword(PasswordUtil.encode(add.getPassword()));
    customer.setStatus(1);

    save(customer);
}
```

---

## 完整检查清单

### 请求类（DTO）

- [ ] 使用意图命名（UserAdd、UserEdit、UserPage）
- [ ] 禁止 VO/DTO 后缀
- [ ] 使用 `@Getter @Setter @ToString`
- [ ] 添加验证注解（@NotNull、@NotBlank 等）
- [ ] 添加 `@Schema` 文档注解
- [ ] 分页查询继承 `PageQuery`

### 响应类（VO）

- [ ] 优先直接返回 Entity
- [ ] 需要脱敏时使用意图命名（UserInfo）
- [ ] 禁止 VO/DTO 后缀
- [ ] 使用 `@Getter @Setter @Builder`
- [ ] 添加 `@Schema` 文档注解
- [ ] Long 类型添加 `@JsonSerialize`
- [ ] 不包含敏感字段

---

## 命名规范总结

| 操作类型 | 命名规范 | 文件位置 |
|---------|---------|---------|
| 新增 | `{Entity}Add` | `controller/{domain}/dto/` |
| 编辑 | `{Entity}Edit` | `controller/{domain}/dto/` |
| 删除 | `{Entity}Delete` | `controller/{domain}/dto/` |
| 分页查询 | `{Entity}Page` | `controller/{domain}/dto/` |
| 条件查询 | `{Entity}Query` | `controller/{domain}/dto/` |
| 响应类 | `{Entity}Info` | `controller/{domain}/vo/` |

---

## 参考资源

- 命名规范：[../standards/naming.md](../standards/naming.md)
- Lombok 规范：[../standards/lombok.md](../standards/lombok.md)
- Controller 指南：[./controller.md](./controller.md)
