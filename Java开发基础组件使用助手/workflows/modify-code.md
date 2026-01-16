# 改进现有代码工作流

## 代码规范检查清单

使用此清单检查和改进现有代码，确保符合 JDevelops 框架规范。

---

## 📋 完整检查清单

复制此清单并逐项验证：

```
代码规范检查：
- [ ] 架构规范
- [ ] 命名规范
- [ ] Lombok 使用规范
- [ ] Entity 层规范
- [ ] Controller 层规范
- [ ] Service 层规范
- [ ] 请求/响应类规范
- [ ] 注解使用规范
- [ ] 字段可见性控制
```

---

## 1. 架构规范

详细规范：[../standards/architecture.md](../standards/architecture.md)

### 检查项

- [ ] 包路径符合规范：
  - Controller：`{package}.controller.{domain}`
  - Entity：`{package}.{module}.entity`
  - Service：`{package}.{module}.service`
  - DAO：`{package}.{module}.dao`

- [ ] 目录结构符合规范：
  ```
  controller/{domain}/dto/    # 请求类
  controller/{domain}/vo/     # 响应类
  {module}/entity/            # 实体类
  {module}/dao/               # DAO 接口
  {module}/service/           # Service 接口
  {module}/service/impl/      # Service 实现
  ```

- [ ] 没有跨层调用（Controller 不能直接调用 DAO）

### 验证命令

```bash
# 检查包结构
find . -name "*.java" | grep -E "(controller|entity|service|dao)" | head -20
```

---

## 2. 命名规范

详细规范：[../standards/naming.md](../standards/naming.md)

### 检查项

- [ ] **请求类命名**：使用意图名，禁止 VO/DTO 后缀
  - ✅ 正确：`UserAdd`、`UserEdit`、`UserPage`
  - ❌ 错误：`UserDTO`、`UserAddDTO`、`UserVO`

- [ ] **响应类命名**：优先返回 Entity，需要脱敏时用意图名
  - ✅ 优先：`ResultVO<Customer>`（直接返回 Entity）
  - ✅ 脱敏时：`UserInfo`（不带 VO 后缀）
  - ❌ 错误：`UserInfoVO`、`UserVO`

- [ ] **Entity 命名**：使用业务名词，不带表前缀
  - ✅ 正确：`Customer`、`Order`、`Product`
  - ❌ 错误：`TbCustomer`、`SysUser`

### 验证命令

```bash
# 检查是否存在 VO/DTO 后缀的类
grep -r "class.*\(DTO\|VO\)\s" --include="*.java" .

# 检查请求/响应类命名
find controller -name "*.java" | xargs grep -l "class"
```

---

## 3. Lombok 使用规范

详细规范：[../standards/lombok.md](../standards/lombok.md)

### 检查项

- [ ] **禁止使用 @Data 注解**
  - ❌ 错误：`@Data`
  - ✅ 正确：根据需求使用 `@Getter`、`@Setter`、`@ToString`

- [ ] **Entity 类**：使用 `@Getter @Setter`（不用 @ToString）
  ```java
  @Getter
  @Setter
  @Entity
  public class Customer extends JpaCommonBean { }
  ```

- [ ] **DTO/VO 类**：使用 `@Getter @Setter @ToString`
  ```java
  @Getter
  @Setter
  @ToString
  public class UserAdd { }
  ```

- [ ] **Builder 模式**：使用 `@Getter @Setter @Builder`
  ```java
  @Getter
  @Setter
  @Builder
  @NoArgsConstructor
  @AllArgsConstructor
  public class UserInfo { }
  ```

### 验证命令

```bash
# 检查是否使用了 @Data
grep -r "@Data" --include="*.java" .
```

---

## 4. Entity 层规范

详细规范：[../guides/entity.md](../guides/entity.md)

### 检查项

- [ ] 继承 `JpaCommonBean` 或 `JpaCommonBean2`
- [ ] 使用 `@Entity @Table` 注解
- [ ] 使用 `@Getter @Setter`（不用 @Data）
- [ ] Long 类型字段添加 `@JsonSerialize(using = ToStringSerializer.class)`
- [ ] 敏感字段使用 `@JsonIgnore` 或 `@JsonView`
- [ ] 使用 `@Column` 指定字段属性
- [ ] 使用 `@Comment` 添加注释
- [ ] 使用 `@Schema` 添加 Swagger 文档

### 验证命令

```bash
# 检查 Entity 是否继承基类
grep -r "class.*extends JpaCommonBean" --include="*.java" {module}/entity/

# 检查 Long 类型是否添加 @JsonSerialize
grep -r "private Long" --include="*.java" {module}/entity/ | \
  grep -v "@JsonSerialize"
```

---

## 5. Controller 层规范

详细规范：[../guides/controller.md](../guides/controller.md)

### 检查项

- [ ] 使用 `@PathRestController("{path}")`（不是 @RestController）
- [ ] 使用 `@Tag` 添加 Swagger 文档
- [ ] 使用构造器注入 Service（不用 @Autowired）
- [ ] 统一返回格式：`ResultVO<T>` 或 `ResultPageVO<T, JpaPageResult<T>>`
- [ ] GET 请求使用 `@Parameter` 注解参数
- [ ] POST 请求使用 `@RequestBody @Valid` 注解参数
- [ ] **分页查询使用 `@PostMapping("page")` + `@RequestBody @Valid`**（不是 @GetMapping + @RequestParam）
- [ ] 每个方法添加 `@Operation` 注解

### 验证命令

```bash
# 检查是否使用 @PathRestController
grep -r "@RestController" --include="*.java" controller/

# 检查是否使用 @Autowired（应该用构造器注入）
grep -r "@Autowired" --include="*.java" controller/

# 检查返回类型
grep -r "public.*{" --include="*Controller.java" controller/ | \
  grep -v "ResultVO\|ResultPageVO"
```

---

## 6. Service 层规范

详细规范：[../guides/service.md](../guides/service.md)

### 检查项

- [ ] Service 接口继承 `J2Service<Entity>`
- [ ] **Service 实现继承 `J2ServiceImpl<DAO, Entity, ID>`（必须包含三个泛型参数）**
- [ ] 实现类使用 `@Service` 注解
- [ ] **使用无参构造器调用 `super(Entity.class)`**
- [ ] **DAO 通过框架自动注入，无需手动注入**
- [ ] 方法命名遵循规范（findByXxx、saveOne、updateOne 等）

### 验证命令

```bash
# 检查 Service 是否继承 J2Service
grep -r "interface.*Service" --include="*.java" {module}/service/ | \
  grep -v "extends J2Service"

# 检查 ServiceImpl 是否继承 J2ServiceImpl
grep -r "class.*ServiceImpl" --include="*.java" {module}/service/impl/ | \
  grep -v "extends J2ServiceImpl"
```

---

## 7. 请求/响应类规范

详细规范：[../guides/request-response.md](../guides/request-response.md)

### 检查项

- [ ] 请求类使用意图命名（UserAdd、UserEdit、UserPage）
- [ ] 响应类优先返回 Entity，需要时用意图名（UserInfo）
- [ ] 使用 `@Getter @Setter @ToString`（DTO）
- [ ] 使用 `@NotNull`、`@NotBlank` 等校验注解
- [ ] 分页请求继承 `PageQuery`

### 示例

```java
// 请求类
@Getter
@Setter
@ToString
public class UserAdd {
    @NotBlank(message = "登录名不能为空")
    private String loginName;
}

// 响应类（仅在需要脱敏时创建）
@Getter
@Setter
@Builder
public class UserInfo {
    private Long id;
    private String loginName;
    // 不包含密码
}
```

---

## 8. 注解使用规范

详细规范：[../standards/annotations.md](../standards/annotations.md)

### 检查项

- [ ] Controller 使用 `@PathRestController`
- [ ] 鉴权控制使用 `@ApiMapping` 或 `@ApiPlatform`
- [ ] Swagger 文档使用 `@Tag`、`@Operation`、`@Parameter`、`@Schema`
- [ ] Entity 使用 `@Entity`、`@Table`、`@Column`、`@Comment`
- [ ] 时间格式化使用 `@JsonFormat`
- [ ] 枚举使用 `@Enumerated(EnumType.STRING)`

---

## 9. 字段可见性控制

### 检查项

- [ ] 敏感字段（密码、token）使用 `@JsonIgnore`
- [ ] 需要按场景控制的字段使用 `@JsonView`
- [ ] Long 类型字段使用 `@JsonSerialize(using = ToStringSerializer.class)`

### 示例

```java
@Getter
@Setter
@Entity
public class Customer extends JpaCommonBean {

    @JsonView(Views.Public.class)
    private String loginName;

    @JsonIgnore  // 永不序列化
    private String password;

    @JsonView(Views.Internal.class)  // 仅内部接口可见
    private String phone;
}
```

---

## 🔧 自动化验证脚本

创建一个验证脚本 `check-code.sh`：

```bash
#!/bin/bash

echo "=== 检查代码规范 ==="

echo "1. 检查 VO/DTO 后缀..."
grep -r "class.*\(DTO\|VO\)\s" --include="*.java" . && echo "❌ 发现 VO/DTO 后缀" || echo "✅ 通过"

echo "2. 检查 @Data 注解..."
grep -r "@Data" --include="*.java" . && echo "❌ 发现 @Data 注解" || echo "✅ 通过"

echo "3. 检查 @RestController..."
grep -r "@RestController" --include="*.java" controller/ && echo "❌ 应使用 @PathRestController" || echo "✅ 通过"

echo "4. 检查 @Autowired..."
grep -r "@Autowired" --include="*.java" . && echo "⚠️ 建议使用构造器注入" || echo "✅ 通过"

echo "=== 检查完成 ==="
```

---

## ✅ 改进步骤

1. **运行检查清单**：逐项验证代码
2. **修复不符合规范的代码**：
   - 重命名类（去除 VO/DTO 后缀）
   - 替换 @Data 为具体注解
   - 修改 @RestController 为 @PathRestController
   - 添加缺失的注解
3. **重新验证**：确保所有检查项通过
4. **测试功能**：确保修改后功能正常

---

## 📚 相关参考

- 架构规范：[../standards/architecture.md](../standards/architecture.md)
- 命名规范：[../standards/naming.md](../standards/naming.md)
- Lombok 规范：[../standards/lombok.md](../standards/lombok.md)
- 完整示例：[../examples/complete-module.md](../examples/complete-module.md)
