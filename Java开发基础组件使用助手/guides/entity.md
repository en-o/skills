# Entity 层代码生成指南

## ⚠️ 重要提醒：Import 语句处理

**生成代码时不要自动生成 import 语句**，让用户手动导入或由 IDE 自动处理。

原因：
- jdevelops 框架的包路径可能因项目而异
- 用户项目可能有自定义的基类实现
- IDE 可以自动识别并导入正确的包

**正确做法**：
- ✅ 只生成类的主体代码（注解、字段、方法）
- ✅ 让用户使用 IDE 的自动导入功能（如 IDEA 的 Alt+Enter）
- ❌ 不要自动生成 `import cn.tannn.jdevelops.*` 等语句

---

## 快速参考

Entity 类继承 `JpaCommonBean` 或 `JpaCommonBean2`，使用 JPA 注解映射数据库表。

---

## 基本模板

```java
@Getter
@Setter
@Entity
@Table(name = "sys_customer", indexes = {
    @Index(name = "idx_login_name", columnList = "loginName", unique = true)
})
@Comment("客户表")
@Schema(description = "客户信息")
@DynamicUpdate
@DynamicInsert
public class Customer extends JpaCommonBean {

    @Column(name = "login_name", nullable = false, unique = true, length = 50)
    @Comment("登录名")
    @Schema(description = "登录名")
    private String loginName;

    @Column(name = "password", nullable = false)
    @Comment("密码")
    @JsonIgnore
    private String password;

    @Column(name = "phone", length = 20)
    @Comment("手机号")
    @Schema(description = "手机号")
    private String phone;

    @Column(name = "role_id")
    @Comment("角色ID")
    @JsonSerialize(using = ToStringSerializer.class)
    private Long roleId;

    @Column(name = "status", columnDefinition = "smallint")
    @ColumnDefault("1")
    @Comment("状态：1-正常，2-锁定")
    private Integer status;
}
```

---

## 必需注解清单

- [ ] `@Entity`
- [ ] `@Table(name = "表名")`
- [ ] `@Getter @Setter`（禁止 @Data）
- [ ] `@Column` 指定字段属性
- [ ] `@Comment` 添加注释
- [ ] `@Schema` 添加 Swagger 文档
- [ ] Long 类型添加 `@JsonSerialize(using = ToStringSerializer.class)`
- [ ] 敏感字段添加 `@JsonIgnore` 或 `@JsonView`

---

## 字段类型映射

| Java 类型 | columnDefinition | 示例 |
|-----------|------------------|------|
| String | `varchar(length)` | `@Column(columnDefinition = "varchar(50)")` |
| Integer | `smallint` | `@Column(columnDefinition = "smallint")` |
| Long | `bigint` | `@Column(columnDefinition = "bigint")` + `@JsonSerialize` |
| Boolean | `boolean` | `@Column(columnDefinition = "boolean")` |
| LocalDateTime | `timestamp` | `@Column(columnDefinition = "timestamp")` + `@JsonFormat` |
| LocalDate | `date` | `@Column(columnDefinition = "date")` |
| BigDecimal | `decimal(10,2)` | `@Column(columnDefinition = "decimal(10,2)")` |
| Text | `text` | `@Column(columnDefinition = "text")` |

---

## 公共基类

Entity 继承框架基类，自动包含公共字段（id、createTime、updateTime等）：

```java
// 继承 JpaCommonBean
public class Customer extends JpaCommonBean {
    // 业务字段
}

// 或继承 JpaCommonBean2
public class Order extends JpaCommonBean2 {
    // 业务字段
}
```

**JpaCommonBean 自动包含的字段**：
- `id`：主键（Long类型，自动生成）
- `createTime`：创建时间
- `updateTime`：更新时间

查看源码确认：https://github.com/en-o/Jdevelops

### JpaCommonBean 实现示例

如果项目中没有 JpaCommonBean，**必须**在 `common/pojo` 包下创建自己的基类。参考以下实现：

```java
package com.example.project.common.pojo;

import com.fasterxml.jackson.databind.annotation.JsonSerialize;
import com.fasterxml.jackson.databind.ser.std.ToStringSerializer;
import com.sunway.jpa.generator.UuidCustomGenerator;
import com.sunway.jpa.modle.json.JpaAuditTimeFormatFields;
import jakarta.persistence.*;
import lombok.Getter;
import lombok.Setter;
import org.hibernate.annotations.*;

/**
 * 公共的实体类- 处理时间的 建议用这个
 * @author tn
 * @date 2021-01-21 14:20
 */
@MappedSuperclass
@DynamicInsert
@DynamicUpdate
@SelectBeforeUpdate
@Access(AccessType.FIELD)
@Getter
@Setter
public class JpaCommonBean<B> extends JpaAuditTimeFormatFields<B> {

    @Id
    @GeneratedValue(strategy = GenerationType.AUTO, generator = "uuidCustomGenerator")
    @GenericGenerator(name = "uuidCustomGenerator", type = UuidCustomGenerator.class)
    @Column(columnDefinition="bigint")
    @Comment("uuid")
    @JsonSerialize(using = ToStringSerializer.class)
    private Long id;

    @Override
    public String toString() {
        return "CommonBean{" +
               "id=" + id +
               '}';
    }
}
```

**重要提醒**：
- ⚠️ 这是一个参考实现，请根据项目实际情况调整包路径
- ⚠️ 生成Entity代码时，不要自动生成import语句，让用户或IDE自动处理
- 如果使用 JDevelops 框架，框架会提供标准的 JpaCommonBean
- 如果是纯 Spring Boot 项目，需要在项目中创建此基类

---

## 索引定义

```java
@Table(
    name = "sys_customer",
    indexes = {
        // 唯一索引
        @Index(name = "idx_login_name", columnList = "loginName", unique = true),
        // 普通索引
        @Index(name = "idx_phone", columnList = "phone"),
        // 组合索引
        @Index(name = "idx_status_type", columnList = "status,type")
    }
)
```

---

## 字段可见性控制

### 永久隐藏（@JsonIgnore）

```java
@JsonIgnore
private String password;
```

### 按场景控制（@JsonView）

```java
// 定义视图
public class Views {
    public interface Public {}
    public interface Internal extends Public {}
}

// Entity 中使用
@JsonView(Views.Public.class)
private String loginName;

@JsonView(Views.Internal.class)
private String phone;
```

---

## 枚举字段

```java
@Column(name = "status")
@Enumerated(EnumType.STRING)
private AccountStatus status;

// 枚举定义
public enum AccountStatus {
    NORMAL, LOCKED, DELETED
}
```

---

## 时间字段格式化

```java
@Column(name = "create_time", columnDefinition = "timestamp")
@JsonFormat(locale = "zh", timezone = "GMT+8", pattern = "yyyy-MM-dd HH:mm:ss")
private LocalDateTime createTime;
```

---

## 完整检查清单

生成 Entity 后验证：

- [ ] 继承 `JpaCommonBean` 或 `JpaCommonBean2`
- [ ] 使用 `@Entity @Table` 注解
- [ ] 使用 `@Getter @Setter`（禁止 @Data）
- [ ] 所有字段添加 `@Column`
- [ ] 所有字段添加 `@Comment`
- [ ] 所有字段添加 `@Schema`
- [ ] Long 类型添加 `@JsonSerialize`
- [ ] 敏感字段控制可见性
- [ ] 时间字段添加 `@JsonFormat`
- [ ] 枚举字段使用 `@Enumerated(EnumType.STRING)`

---

## 参考资源

- 注解规范：[../standards/annotations.md](../standards/annotations.md)
- Lombok 规范：[../standards/lombok.md](../standards/lombok.md)
- 框架源码：https://github.com/en-o/Jdevelops
- 官方文档：https://www.yuque.com/tanning/yg9ipo
