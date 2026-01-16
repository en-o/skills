# 请求/响应类生成指南

## ⚠️ 重要提醒：Import 语句处理

**生成代码时不要自动生成 import 语句**，让用户手动导入或由 IDE 自动处理。

原因：
- jdevelops 框架的包路径可能因项目而异
- 用户项目可能有自定义的实现
- IDE 可以自动识别并导入正确的包

**正确做法**：
- ✅ 只生成类的主体代码（注解、字段、方法）
- ✅ 让用户使用 IDE 的自动导入功能（如 IDEA 的 Alt+Enter）
- ❌ 不要自动生成 `import cn.tannn.jdevelops.*` 等语句

---

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

分页查询有两种实现模式：

#### 模式1：使用 @JpaSelectOperator 注解（自动查询）

**适用场景**：简单的等值查询、区间查询等标准条件

**特点**：框架自动根据注解构建查询条件

```java
// controller/logs/dto/LogEsInitDataPage.java
import cn.tannn.jdevelops.annotations.jpa.JpaSelectIgnoreField;
import cn.tannn.jdevelops.annotations.jpa.JpaSelectOperator;
import cn.tannn.jdevelops.annotations.jpa.enums.SQLConnect;
import cn.tannn.jdevelops.annotations.jpa.enums.SQLOperatorWrapper;
import cn.tannn.jdevelops.jpa.request.PagingSorteds;
import cn.tannn.jdevelops.result.bean.SerializableBean;

@Schema(description = "ES初始化数据日志 分页查询参数")
@ToString
@Getter
@Setter
public class LogEsInitDataPage extends SerializableBean<LogEsInitDataPage> {

    /**
     * 数据库表英文名称（等值查询）
     */
    @Schema(description = "数据库表英文名称")
    @JpaSelectOperator(operatorWrapper = SQLOperatorWrapper.EQ, connect = SQLConnect.AND)
    private String tableEnName;

    /**
     * 索引名称（等值查询）
     */
    @Schema(description = "索引名称")
    @JpaSelectOperator(operatorWrapper = SQLOperatorWrapper.EQ, connect = SQLConnect.AND)
    private String indexName;

    /**
     * 分页排序（不参与查询条件）
     */
    @Schema(description = "分页排序")
    @JpaSelectIgnoreField
    @Valid
    private PagingSorteds page;

    /**
     * 设置默认排序
     */
    public PagingSorteds getPage() {
        if (page == null) {
            return new PagingSorteds().fixSort(1, "createTime");
        }
        page.fixSort(1, "createTime");
        return page;
    }
}
```

**常用查询操作符**：

```java
// 等值查询
@JpaSelectOperator(operatorWrapper = SQLOperatorWrapper.EQ, connect = SQLConnect.AND)
private String status;

// 模糊查询
@JpaSelectOperator(operatorWrapper = SQLOperatorWrapper.LIKE, connect = SQLConnect.AND)
private String keyword;

// 区间查询（BETWEEN）
@JpaSelectOperator(
    operatorWrapper = SQLOperatorWrapper.BETWEEN,
    connect = SQLConnect.AND,
    function = SpecBuilderDateFun.DATE_FORMAT
)
private String operatorTime;  // 格式：开始时间,结束时间

// 大于等于
@JpaSelectOperator(operatorWrapper = SQLOperatorWrapper.GE, connect = SQLConnect.AND)
private Integer minAge;

// 小于等于
@JpaSelectOperator(operatorWrapper = SQLOperatorWrapper.LE, connect = SQLConnect.AND)
private Integer maxAge;

// IN 查询
@JpaSelectOperator(operatorWrapper = SQLOperatorWrapper.IN, connect = SQLConnect.AND)
private List<String> types;
```

#### 模式2：使用 @JpaSelectIgnoreField + 自定义 Specification（手动查询）

**适用场景**：复杂的动态查询、多条件组合、需要函数处理等

**特点**：手动构建查询条件，灵活性高

**步骤1：定义分页请求类**

```java
// controller/front/dto/ResourceUseLogPage.java
import cn.tannn.jdevelops.annotations.jpa.JpaSelectIgnoreField;
import cn.tannn.jdevelops.annotations.jpa.JpaSelectOperator;
import cn.tannn.jdevelops.annotations.jpa.enums.SQLConnect;
import cn.tannn.jdevelops.annotations.jpa.enums.SQLOperatorWrapper;
import cn.tannn.jdevelops.annotations.jpa.enums.SpecBuilderDateFun;
import cn.tannn.jdevelops.jpa.request.PagingSorteds;

@Schema(description = "资源利用日志分页查询")
@ToString
@Getter
@Setter
@Valid
public class ResourceUseLogPage {

    /**
     * 资源类型（参与自动查询）
     */
    @Schema(description = "资源类型")
    @JpaSelectOperator(operatorWrapper = SQLOperatorWrapper.EQ)
    private String dataType;

    /**
     * 关键词（不参与自动查询，在 Specification 中手动处理）
     */
    @Schema(description = "关键词")
    @JpaSelectIgnoreField
    private String keyword;

    /**
     * 时间段（不参与自动查询，在 Specification 中手动处理）
     * 格式：开始时间,结束时间 eg. 2025-04-08 16:09:39,2025-04-09 16:09:39
     */
    @Schema(description = "时间段，格式YYYY-MM-DD HH:MM:SS[逗号隔开]，[开始,结束]")
    @JpaSelectIgnoreField
    private String operatorTime;

    /**
     * 分页排序（不参与查询条件）
     */
    @Schema(description = "分页排序")
    @JpaSelectIgnoreField
    @Valid
    private PagingSorteds page;

    public PagingSorteds getPage() {
        if (page == null) {
            return new PagingSorteds().fixSort(1, "id");
        }
        return page;
    }
}
```

**步骤2：继承扩展（可选）**

```java
// controller/front/dto/ResourceUseLogPage2.java
@Schema(description = "资源利用日志分页查询(扩展)")
@ToString
@Getter
@Setter
@Valid
public class ResourceUseLogPage2 extends ResourceUseLogPage {
    /**
     * 资源类型（额外的查询条件）
     */
    @JpaSelectIgnoreField
    @Schema(description = "资源类型 0:资源，1:来源，2:专题")
    private String resourceType;
}
```

**步骤3：创建 Specification 查询类**

```java
// modules/logs/query/LogSpecQuery.java
import cn.tannn.jdevelops.annotations.jpa.enums.SpecBuilderDateFun;
import cn.tannn.jdevelops.jpa.select.EnhanceSpecification;
import cn.tannn.jdevelops.jpa.utils.JpaUtils;
import cn.tannn.jdevelops.result.bean.SerializableBean;
import org.apache.commons.lang3.StringUtils;
import org.springframework.data.jpa.domain.Specification;

import java.util.Objects;

/**
 * 日志查询 Specification 工具类
 */
public class LogSpecQuery {

    /**
     * 用户资源相关日志查询
     */
    public static <T extends SerializableBean> Specification<T> logUserResourceSpec(
            ResourceUseLogPage page, Long userId, Integer status) {

        return EnhanceSpecification.where(e -> {
            // 模糊查询
            e.like(StringUtils.isNotBlank(page.getKeyword()),
                   "dataTitle", "%" + page.getKeyword() + "%");

            // 等值查询
            e.eq(Objects.nonNull(userId), "userId", userId);
            e.eq(StringUtils.isNotBlank(page.getDataType()), "dataType", page.getDataType());
            e.eq(status != null, "status", status);

            // 时间区间查询（带函数处理）
            String operateTime = page.getOperatorTime();
            if (StringUtils.isNotBlank(operateTime)) {
                String[] split = operateTime.split(",");
                if (split.length >= 2) {
                    // 大于等于开始时间
                    if (StringUtils.isNotBlank(split[0])) {
                        e.ge(JpaUtils.functionTimeFormat(
                                SpecBuilderDateFun.DATE_FORMAT_DATE,
                                e.getRoot(),
                                e.getBuilder(),
                                "operatorTime"), split[0]);
                    }
                    // 小于等于结束时间
                    if (StringUtils.isNotBlank(split[1])) {
                        e.le(JpaUtils.functionTimeFormat(
                                SpecBuilderDateFun.DATE_FORMAT_DATE,
                                e.getRoot(),
                                e.getBuilder(),
                                "operatorTime"), split[1]);
                    }
                }
            }
        });
    }

    /**
     * 用户收藏资源日志查询
     */
    public static <T extends SerializableBean> Specification<T> logUserFavoriteResourceSpec(
            ResourceUseLogPage2 page, Long userId) {

        return EnhanceSpecification.where(e -> {
            e.like(StringUtils.isNotBlank(page.getKeyword()),
                   "dataTitle", "%" + page.getKeyword() + "%");
            e.eq(Objects.nonNull(userId), "userId", userId);
            e.eq(StringUtils.isNotBlank(page.getDataType()), "dataType", page.getDataType());
            e.eq(Objects.nonNull(page.getResourceType()), "resourceType", page.getResourceType());
            e.eq(true, "status", "1");

            // ... 其他查询条件
        });
    }
}
```

**EnhanceSpecification 常用方法**：

```java
// 等值查询
e.eq(condition, "fieldName", value);

// 不等于
e.ne(condition, "fieldName", value);

// 模糊查询
e.like(condition, "fieldName", "%keyword%");

// 大于
e.gt(condition, "fieldName", value);

// 大于等于
e.ge(condition, "fieldName", value);

// 小于
e.lt(condition, "fieldName", value);

// 小于等于
e.le(condition, "fieldName", value);

// IN 查询
e.in(condition, "fieldName", valueList);

// IS NULL
e.isNull(condition, "fieldName");

// IS NOT NULL
e.isNotNull(condition, "fieldName");

// BETWEEN
e.between(condition, "fieldName", start, end);

// 自定义 Predicate
e.and(customPredicate);
e.or(customPredicate);
```

#### 两种模式对比

| 特性 | 模式1（注解自动查询） | 模式2（手动 Specification） |
|-----|---------------------|---------------------------|
| **适用场景** | 简单的等值、区间查询 | 复杂动态查询、多条件组合 |
| **实现方式** | `@JpaSelectOperator` 注解 | `@JpaSelectIgnoreField` + Query类 |
| **灵活性** | 低，仅支持标准操作符 | 高，可自由组合各种条件 |
| **代码量** | 少，仅需注解 | 多，需要单独的 Query 类 |
| **函数支持** | 有限（如 DATE_FORMAT） | 完全支持 JPA 函数 |
| **动态条件** | 支持（通过条件判断） | 完全支持（通过 EnhanceSpecification） |
| **维护性** | 高，声明式 | 中，命令式 |
| **Controller 调用** | `service.findPage(page, page.getPage())` | `service.findPage(spec, page.getPage())` |

#### 模式选择建议

```
需要分页查询？
  ├─ 查询条件简单（仅等值、区间）？
  │   └─ 是 → 使用模式1（@JpaSelectOperator）
  └─ 查询条件复杂（函数、动态组合）？
      └─ 是 → 使用模式2（Specification）
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
