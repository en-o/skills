# 扩展功能工作流

## 决策树：选择扩展方式

```
需要扩展功能？
  ├─ 新增字段到现有 Entity？
  │   └─ 遵循 Entity 规范 → [guides/entity.md]
  │
  ├─ 新增业务方法到 Service？
  │   └─ 遵循 Service 规范 → [guides/service.md]
  │
  ├─ 新增 API 接口到 Controller？
  │   └─ 遵循 Controller 规范 → [guides/controller.md]
  │
  ├─ 新增完整的业务模块？
  │   └─ 查阅新增模块工作流 → [workflows/add-module.md]
  │
  └─ 集成新功能（登录、权限、缓存等）？
      └─ 查阅框架文档 → https://www.yuque.com/tanning/yg9ipo
```

---

## 1️⃣ 新增字段到现有 Entity

### 工作流清单

```
新增字段进度：
- [ ] 确定字段信息（名称、类型、是否必需、是否敏感）
- [ ] 添加字段到 Entity 类
- [ ] 更新相关的请求/响应类
- [ ] 更新 Service 方法（如需要）
- [ ] 测试新字段的增删改查
```

### 步骤详解

1. **确定字段信息**
   - 字段名称（遵循驼峰命名）
   - 字段类型（String、Long、Integer、LocalDateTime 等）
   - 是否必需（nullable = false）
   - 是否敏感（需要 @JsonIgnore 或 @JsonView）
   - 是否唯一（unique = true）

2. **添加字段到 Entity**

```java
@Getter
@Setter
@Entity
public class Customer extends JpaCommonBean {

    // 新增字段
    @Column(name = "phone", length = 20)
    @Comment("手机号")
    @Schema(description = "手机号")
    @JsonView(Views.Internal.class)  // 如需控制可见性
    private String phone;

    // Long 类型需要添加序列化器
    @Column(name = "role_id")
    @JsonSerialize(using = ToStringSerializer.class)
    private Long roleId;
}
```

3. **更新请求/响应类**

```java
// controller/user/dto/UserAdd.java
@Getter
@Setter
public class UserAdd {
    // 新增字段
    @NotBlank(message = "手机号不能为空")
    private String phone;
}
```

4. **验证字段**
   - [ ] 字段注解完整（@Column、@Comment、@Schema）
   - [ ] 敏感字段控制可见性（@JsonIgnore 或 @JsonView）
   - [ ] Long 类型添加序列化器
   - [ ] 数据库字段自动创建/更新

---

## 2️⃣ 新增业务方法到 Service

### 工作流清单

```
新增方法进度：
- [ ] 确定方法功能和参数
- [ ] 在 Service 接口中声明方法
- [ ] 在 ServiceImpl 中实现方法
- [ ] 使用框架提供的基础方法
- [ ] 测试方法功能
```

### 步骤详解

1. **在 Service 接口中声明**

```java
public interface CustomerService extends J2Service<Customer> {
    // 新增方法
    Optional<Customer> findByPhone(String phone);
    List<Customer> findActiveCustomers();
}
```

2. **在 ServiceImpl 中实现**

```java
@Service
public class CustomerServiceImpl extends J2ServiceImpl<Customer>
    implements CustomerService {

    @Override
    public Optional<Customer> findByPhone(String phone) {
        // 使用框架提供的 findOne 方法
        return findOne("phone", phone, SQLOperator.EQ);
    }

    @Override
    public List<Customer> findActiveCustomers() {
        // 使用框架提供的 findList 方法
        return findList("status", 1, SQLOperator.EQ);
    }
}
```

### 框架提供的基础方法

参考：[../guides/service.md](../guides/service.md)

- `findOne(field, value, operator)` - 查询单个
- `findList(field, value, operator)` - 查询列表
- `save(entity)` - 保存
- `update(entity, operator, fields...)` - 更新
- `delete(id)` - 删除

---

## 3️⃣ 新增 API 接口到 Controller

### 工作流清单

```
新增接口进度：
- [ ] 确定接口路径和请求方式
- [ ] 创建请求类（如需要）
- [ ] 在 Controller 中添加方法
- [ ] 添加 Swagger 注解
- [ ] 测试接口功能
```

### 步骤详解

1. **创建请求类（如需要）**

```java
// controller/user/dto/PhoneQuery.java
@Getter
@Setter
@ToString
public class PhoneQuery {
    @NotBlank(message = "手机号不能为空")
    private String phone;
}
```

2. **在 Controller 中添加方法**

```java
@PathRestController("user")
@Tag(name = "用户管理")
public class CustomerController {

    private final CustomerService customerService;

    // 新增接口：根据手机号查询
    @GetMapping("find-by-phone")
    @Operation(summary = "根据手机号查询用户")
    @Parameter(name = "phone", description = "手机号", required = true)
    public ResultVO<Customer> findByPhone(@RequestParam String phone) {
        Customer customer = customerService.findByPhone(phone)
            .orElseThrow(() -> new RuntimeException("用户不存在"));
        return ResultVO.success(customer);
    }

    // 新增接口：查询活跃用户列表
    @GetMapping("active-list")
    @Operation(summary = "查询活跃用户列表")
    public ResultVO<List<Customer>> activeList() {
        List<Customer> customers = customerService.findActiveCustomers();
        return ResultVO.success(customers);
    }
}
```

3. **验证接口**
   - [ ] 添加了 @Operation 注解
   - [ ] GET 请求使用 @Parameter 注解参数
   - [ ] POST 请求使用 @RequestBody @Valid 注解参数
   - [ ] 统一返回 ResultVO 或 ResultPageVO
   - [ ] Swagger UI 中接口文档正确

---

## 4️⃣ 新增完整的业务模块

查阅详细工作流：[./add-module.md](./add-module.md)

---

## 5️⃣ 集成新功能

### 常见集成场景

#### 集成登录鉴权

参考框架文档：https://www.yuque.com/tanning/yg9ipo

1. 添加依赖：
```xml
<dependency>
    <groupId>cn.tannn.jdevelops</groupId>
    <artifactId>jdevelops-authentications-rjwt</artifactId>
</dependency>
```

2. 配置 application.yml：
```yaml
jdevelops:
  jwt:
    secret: ${your-secret}
    expire: 7200
```

3. 在 Controller 中使用：
```java
@PostMapping("login")
@ApiMapping(checkToken = false)  // 不需要鉴权
public ResultVO<String> login(@RequestBody @Valid LoginRequest request) {
    // 登录逻辑
}

@GetMapping("info")
// 默认需要鉴权
public ResultVO<Customer> info() {
    // 获取当前用户信息
}
```

#### 集成缓存

查阅框架文档中的缓存章节。

#### 集成消息队列

查阅框架文档中的消息队列章节。

---

## 🔍 查阅策略

扩展功能时，按以下顺序查阅：

1. **查官方文档**：https://www.yuque.com/tanning/yg9ipo
   - 查找功能说明和配置方式
   - 查看示例代码

2. **查 GitHub 源码**：https://github.com/en-o/Jdevelops
   - 查看最新 API
   - 理解实现细节

3. **下载文档到本地**（可选）：
   ```bash
   bash scripts/download-docs.sh
   ```

详细策略：[../reference/lookup-strategy.md](../reference/lookup-strategy.md)

---

## ✅ 扩展检查清单

扩展功能后，验证以下项：

- [ ] 新代码符合框架规范
- [ ] 包路径正确
- [ ] 注解使用正确
- [ ] 命名无 VO/DTO 后缀
- [ ] 禁用了 @Data
- [ ] 功能测试通过
- [ ] 不影响现有功能

完整检查清单：[./modify-code.md](./modify-code.md)

---

## 📚 相关参考

- 新增模块：[./add-module.md](./add-module.md)
- Entity 指南：[../guides/entity.md](../guides/entity.md)
- Controller 指南：[../guides/controller.md](../guides/controller.md)
- Service 指南：[../guides/service.md](../guides/service.md)
- 官方文档：https://www.yuque.com/tanning/yg9ipo
