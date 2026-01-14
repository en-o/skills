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

明确以下信息：
- **模块名称**（如：customer、order、product）
- **业务领域**（决定 controller 路径，如：controller.user）
- **核心字段**（哪些字段必需、哪些敏感、哪些需要脱敏）
- **是否需要脱敏**（决定是否创建 UserInfo 响应类）

### 决策树：是否需要创建响应类？

```
需要返回数据？
  ├─ 包含敏感字段（密码、token）？
  │   ├─ 是 → 使用 @JsonIgnore 或创建 UserInfo 类
  │   └─ 否 → 继续判断
  └─ 需要按场景控制可见性？
      ├─ 是 → 使用 @JsonView 定义视图
      └─ 否 → 直接返回 Entity
```

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
