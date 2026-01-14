# 完整模块示例

本示例展示如何创建一个完整的用户管理模块，包含 Entity、DAO、Service、Controller 的所有代码。

**示例包路径**: `cn.tannn.example` （实际项目中替换为你的包路径）

---

## 方式 A：传统三层架构

适用于小型项目（< 50 个实体）

```
src/main/java/cn/tannn/example/
├── controller/
│   └── user/
│       ├── dto/
│       │   ├── UserAdd.java
│       │   ├── UserEdit.java
│       │   └── UserPage.java
│       ├── vo/
│       │   └── UserInfo.java
│       └── UserController.java
│
├── entity/
│   └── User.java
│
├── dao/
│   └── UserDao.java
│
├── service/
│   └── UserService.java
│
└── service/impl/
    └── UserServiceImpl.java
```

---

## 方式 B：垂直切分（模块化）

适用于中型项目（50-100 个实体）

```
src/main/java/cn/tannn/example/
├── controller/
│   └── user/
│       ├── dto/
│       │   ├── UserAdd.java
│       │   ├── UserEdit.java
│       │   └── UserPage.java
│       ├── vo/
│       │   └── UserInfo.java
│       └── UserController.java
│
└── user/                      # 用户模块
    ├── entity/
    │   └── User.java
    ├── dao/
    │   └── UserDao.java
    ├── service/
    │   └── UserService.java
    └── service/impl/
        └── UserServiceImpl.java
```

---

## 方式 C：标准目录结构

适用于大型项目（> 100 个实体）

```
src/main/java/cn/tannn/example/
├── controller/
│   └── user/
│       ├── dto/
│       │   ├── UserAdd.java
│       │   ├── UserEdit.java
│       │   └── UserPage.java
│       ├── vo/
│       │   └── UserInfo.java
│       └── UserController.java
│
├── common/                    # 公共组件层
│   ├── pojo/
│   └── util/
│
├── core/                      # 核心配置层
│   ├── config/
│   └── exception/
│
└── modules/                   # 业务模块层
    └── account/              # 账户大模块
        └── user/             # 用户子模块
            ├── entity/
            │   └── User.java
            ├── dao/
            │   └── UserDao.java
            ├── service/
            │   └── UserService.java
            └── service/impl/
                └── UserServiceImpl.java
```

**以下示例代码适用于所有三种结构**（根据实际包路径调整 import）

---

## 1. Entity 层

```java
package com.example.userservice.customer.entity;

import cn.tannn.jdevelops.jpa.entity.JpaCommonBean;
import com.fasterxml.jackson.annotation.JsonFormat;
import com.fasterxml.jackson.annotation.JsonIgnore;
import com.fasterxml.jackson.annotation.JsonSerialize;
import com.fasterxml.jackson.databind.ser.std.ToStringSerializer;
import io.swagger.v3.oas.annotations.media.Schema;
import jakarta.persistence.*;
import lombok.Getter;
import lombok.Setter;
import org.hibernate.annotations.ColumnDefault;
import org.hibernate.annotations.Comment;
import org.hibernate.annotations.DynamicInsert;
import org.hibernate.annotations.DynamicUpdate;

import java.time.LocalDateTime;

@Getter
@Setter
@Entity
@Table(
    name = "sys_customer",
    indexes = {
        @Index(name = "idx_login_name", columnList = "loginName", unique = true)
    }
)
@Comment("客户表")
@Schema(description = "客户信息")
@DynamicUpdate
@DynamicInsert
public class Customer extends JpaCommonBean {

    @Column(name = "login_name", nullable = false, unique = true, length = 50)
    @Comment("登录名")
    @Schema(description = "登录名", example = "zhangsan")
    private String loginName;

    @Column(name = "user_name", nullable = false, length = 100)
    @Comment("用户名")
    @Schema(description = "用户名")
    private String userName;

    @Column(name = "password", nullable = false, length = 100)
    @Comment("密码")
    @JsonIgnore
    private String password;

    @Column(name = "phone", length = 20)
    @Comment("手机号")
    @Schema(description = "手机号")
    private String phone;

    @Column(name = "email", length = 100)
    @Comment("邮箱")
    @Schema(description = "邮箱")
    private String email;

    @Column(name = "role_id")
    @Comment("角色ID")
    @Schema(description = "角色ID")
    @JsonSerialize(using = ToStringSerializer.class)
    private Long roleId;

    @Column(name = "status", columnDefinition = "smallint")
    @ColumnDefault("1")
    @Comment("状态：1-正常，2-锁定，3-删除")
    @Schema(description = "状态：1-正常，2-锁定，3-删除")
    private Integer status;

    @Column(name = "last_login_time", columnDefinition = "timestamp")
    @Comment("最后登录时间")
    @Schema(description = "最后登录时间")
    @JsonFormat(locale = "zh", timezone = "GMT+8", pattern = "yyyy-MM-dd HH:mm:ss")
    private LocalDateTime lastLoginTime;
}
```

---

## 2. DAO 层

```java
package com.example.userservice.customer.dao;

import com.example.userservice.customer.entity.Customer;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.Optional;

public interface CustomerDao extends JpaRepository<Customer, Long> {

    /**
     * 根据登录名查询
     */
    Optional<Customer> findByLoginName(String loginName);

    /**
     * 根据手机号查询
     */
    Optional<Customer> findByPhone(String phone);
}
```

---

## 3. Service 层

### Service 接口

```java
package com.example.userservice.customer.service;

import cn.tannn.jdevelops.jpa.service.J2Service;
import com.example.userservice.customer.entity.Customer;
import com.example.userservice.controller.user.dto.UserAdd;
import com.example.userservice.controller.user.vo.UserInfo;

import java.util.Optional;

public interface CustomerService extends J2Service<Customer> {

    /**
     * 根据登录名查询
     */
    Optional<Customer> findByLoginName(String loginName);

    /**
     * 获取用户信息（脱敏）
     */
    UserInfo getUserInfo(Long id);

    /**
     * 注册用户
     */
    void registerUser(UserAdd add);
}
```

### Service 实现

```java
package com.example.userservice.customer.service.impl;

import cn.tannn.jdevelops.jpa.service.impl.J2ServiceImpl;
import cn.tannn.jdevelops.jpa.sql.SQLOperator;
import cn.tannn.jdevelops.utils.SerializableBean;
import com.example.userservice.customer.dao.CustomerDao;
import com.example.userservice.customer.entity.Customer;
import com.example.userservice.customer.service.CustomerService;
import com.example.userservice.controller.user.dto.UserAdd;
import com.example.userservice.controller.user.vo.UserInfo;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.util.StringUtils;

import java.util.Optional;

@Service
@RequiredArgsConstructor
public class CustomerServiceImpl extends J2ServiceImpl<Customer>
    implements CustomerService {

    private final CustomerDao customerDao;

    @Override
    public Optional<Customer> findByLoginName(String loginName) {
        return findOne("loginName", loginName, SQLOperator.EQ);
    }

    @Override
    public UserInfo getUserInfo(Long id) {
        Customer customer = findById(id)
            .orElseThrow(() -> new RuntimeException("用户不存在"));

        // 转换并脱敏
        UserInfo info = SerializableBean.to2(customer, UserInfo.class);

        // 手机号脱敏
        if (StringUtils.hasText(info.getPhone())) {
            info.setPhone(info.getPhone().replaceAll("(\\d{3})\\d{4}(\\d{4})", "$1****$2"));
        }

        return info;
    }

    @Override
    @Transactional(rollbackFor = Exception.class)
    public void registerUser(UserAdd add) {
        // 检查用户名是否存在
        if (findByLoginName(add.getLoginName()).isPresent()) {
            throw new RuntimeException("用户名已存在");
        }

        // 转换对象
        Customer customer = SerializableBean.to2(add, Customer.class);

        // 密码加密（这里简化处理，实际应使用加密工具）
        customer.setPassword(encryptPassword(add.getPassword()));
        customer.setStatus(1);

        // 保存
        save(customer);
    }

    private String encryptPassword(String password) {
        // 实际项目应使用 BCrypt 等加密算法
        return password; // 简化处理
    }
}
```

---

## 4. Controller 层

### 请求类（DTO）

```java
package com.example.userservice.controller.user.dto;

import io.swagger.v3.oas.annotations.media.Schema;
import jakarta.validation.constraints.Email;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Pattern;
import jakarta.validation.constraints.Size;
import lombok.Getter;
import lombok.Setter;
import lombok.ToString;

@Getter
@Setter
@ToString
public class UserAdd {

    @NotBlank(message = "登录名不能为空")
    @Size(min = 3, max = 50, message = "登录名长度必须在3-50之间")
    @Schema(description = "登录名", requiredMode = Schema.RequiredMode.REQUIRED)
    private String loginName;

    @NotBlank(message = "用户名不能为空")
    @Schema(description = "用户名", requiredMode = Schema.RequiredMode.REQUIRED)
    private String userName;

    @NotBlank(message = "密码不能为空")
    @Size(min = 6, max = 20, message = "密码长度必须在6-20之间")
    @Schema(description = "密码", requiredMode = Schema.RequiredMode.REQUIRED)
    private String password;

    @Pattern(regexp = "^1[3-9]\\d{9}$", message = "手机号格式不正确")
    @Schema(description = "手机号")
    private String phone;

    @Email(message = "邮箱格式不正确")
    @Schema(description = "邮箱")
    private String email;
}
```

```java
package com.example.userservice.controller.user.dto;

import io.swagger.v3.oas.annotations.media.Schema;
import jakarta.validation.constraints.NotNull;
import lombok.Getter;
import lombok.Setter;
import lombok.ToString;

@Getter
@Setter
@ToString
public class UserEdit {

    @NotNull(message = "ID不能为空")
    @Schema(description = "用户ID", requiredMode = Schema.RequiredMode.REQUIRED)
    private Long id;

    @Schema(description = "用户名")
    private String userName;

    @Schema(description = "手机号")
    private String phone;

    @Schema(description = "邮箱")
    private String email;
}
```

```java
package com.example.userservice.controller.user.dto;

import cn.tannn.jdevelops.jpa.query.PageQuery;
import io.swagger.v3.oas.annotations.media.Schema;
import lombok.Getter;
import lombok.Setter;
import lombok.ToString;

@Getter
@Setter
@ToString
public class UserPage extends PageQuery {

    @Schema(description = "登录名")
    private String loginName;

    @Schema(description = "状态")
    private Integer status;
}
```

### 响应类（VO）

```java
package com.example.userservice.controller.user.vo;

import com.fasterxml.jackson.databind.annotation.JsonSerialize;
import com.fasterxml.jackson.databind.ser.std.ToStringSerializer;
import io.swagger.v3.oas.annotations.media.Schema;
import lombok.*;

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

    @Schema(description = "邮箱")
    private String email;

    @JsonSerialize(using = ToStringSerializer.class)
    @Schema(description = "角色ID")
    private Long roleId;

    @Schema(description = "状态")
    private Integer status;
}
```

### Controller 类

```java
package com.example.userservice.controller.user;

import cn.tannn.jdevelops.annotations.web.path.PathRestController;
import cn.tannn.jdevelops.result.bean.ResultVO;
import cn.tannn.jdevelops.result.bean.ResultPageVO;
import cn.tannn.jdevelops.jpa.result.JpaPageResult;
import com.example.userservice.customer.entity.Customer;
import com.example.userservice.customer.service.CustomerService;
import com.example.userservice.controller.user.dto.UserAdd;
import com.example.userservice.controller.user.dto.UserEdit;
import com.example.userservice.controller.user.dto.UserPage;
import com.example.userservice.controller.user.vo.UserInfo;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.Parameter;
import io.swagger.v3.oas.annotations.extensions.Extension;
import io.swagger.v3.oas.annotations.extensions.ExtensionProperty;
import io.swagger.v3.oas.annotations.tags.Tag;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.data.domain.Page;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.bind.annotation.*;

@PathRestController("user")
@Tag(name = "用户管理", extensions = {
    @Extension(properties = {
        @ExtensionProperty(name = "x-order", value = "3", parseValue = true)
    })
})
@RequiredArgsConstructor
@Slf4j
@Validated
public class CustomerController {

    private final CustomerService customerService;

    @PostMapping("add")
    @Operation(summary = "新增用户")
    public ResultVO<String> add(@RequestBody @Valid UserAdd add) {
        log.info("新增用户：{}", add);
        customerService.registerUser(add);
        return ResultVO.success("新增成功");
    }

    @PostMapping("edit")
    @Operation(summary = "编辑用户")
    public ResultVO<String> edit(@RequestBody @Valid UserEdit edit) {
        log.info("编辑用户：{}", edit);
        // 更新逻辑
        return ResultVO.success("编辑成功");
    }

    @GetMapping("detail")
    @Operation(summary = "用户详情")
    @Parameter(name = "id", description = "用户ID", required = true)
    public ResultVO<Customer> detail(@RequestParam Long id) {
        Customer customer = customerService.findById(id)
            .orElseThrow(() -> new RuntimeException("用户不存在"));
        return ResultVO.success(customer);
    }

    @GetMapping("info")
    @Operation(summary = "用户信息（脱敏）")
    @Parameter(name = "id", description = "用户ID", required = true)
    public ResultVO<UserInfo> info(@RequestParam Long id) {
        UserInfo info = customerService.getUserInfo(id);
        return ResultVO.success(info);
    }

    @PostMapping("page")
    @Operation(summary = "分页查询用户")
    public ResultPageVO<Customer, JpaPageResult<Customer>> page(
        @RequestBody @Valid UserPage page) {
        Page<Customer> result = customerService.findPage(page, page.getPage());
        JpaPageResult<Customer> pageResult = JpaPageResult.toPage(result, Customer.class);
        return ResultPageVO.success(pageResult, "查询成功");
    }
}
```

---

## 5. 配置文件

### application.yml

```yaml
spring:
  application:
    name: user-service

  datasource:
    url: jdbc:mysql://localhost:3306/user_db?useUnicode=true&characterEncoding=utf8&serverTimezone=Asia/Shanghai
    username: root
    password: password
    driver-class-name: com.mysql.cj.jdbc.Driver

  jpa:
    hibernate:
      ddl-auto: update
    show-sql: true
    properties:
      hibernate:
        dialect: org.hibernate.dialect.MySQLDialect
        format_sql: true

springdoc:
  api-docs:
    enabled: true
  swagger-ui:
    enabled: true
    path: /swagger-ui.html
```

---

## 6. 启动类

```java
package com.example.userservice;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.data.jpa.repository.config.EnableJpaAuditing;

@SpringBootApplication
@EnableJpaAuditing
public class Application {
    public static void main(String[] args) {
        SpringApplication.run(Application.class, args);
    }
}
```

---

## 验证步骤

1. **启动项目**
   ```bash
   mvn spring-boot:run
   ```

2. **访问 Swagger UI**
   ```
   http://localhost:8080/swagger-ui.html
   ```

3. **测试接口**
   - 新增用户：POST `/user/add`
   - 查询详情：GET `/user/detail?id=1`
   - 分页查询：POST `/user/page`

---

## 总结

这个示例展示了：
- ✅ Entity 继承 `JpaCommonBean`
- ✅ Service 继承 `J2Service`
- ✅ Controller 使用 `@PathRestController`
- ✅ 统一返回 `ResultVO`
- ✅ 请求类使用意图命名（无 VO/DTO 后缀）
- ✅ 响应类优先返回 Entity，需要脱敏时创建 UserInfo
- ✅ 使用 `@Getter @Setter`（禁止 @Data）
- ✅ Long 类型添加 `@JsonSerialize`
- ✅ 敏感字段使用 `@JsonIgnore`

完全符合 JDevelops 框架规范。
