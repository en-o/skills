# Controller 层代码生成指南

## 快速参考

Controller 使用 `@PathRestController` 注解，统一返回 `ResultVO` 或 `ResultPageVO`。

---

## 基本模板

```java

import cn.tannn.jdevelops.annotations.web.mapping.PathRestController;
import cn.tannn.jdevelops.result.response.ResultVO;
import cn.tannn.jdevelops.result.response.ResultPageVO;
import cn.tannn.jdevelops.jpa.result.JpaPageResult;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.Parameter;
import io.swagger.v3.oas.annotations.tags.Tag;
import io.swagger.v3.oas.annotations.extensions.Extension;
import io.swagger.v3.oas.annotations.extensions.ExtensionProperty;
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
@Slf4j
@Validated
@RequiredArgsConstructor
public class CustomerController {

    private final CustomerService customerService;

    @PostMapping("add")
    @Operation(summary = "新增用户")
    public ResultVO<String> add(@RequestBody @Valid UserAdd add) {
        customerService.saveCustomer(add);
        return ResultVO.successMessage("新增成功");
    }

    @PutMapping("update")
    @Operation(summary = "更新用户")
    public ResultVO<String> update(@RequestBody @Valid UserEdit edit) {
        customerService.updateCustomer(edit);
        return ResultVO.successMessage("更新成功");
    }

    @GetMapping("detail/{id}")
    @Operation(summary = "用户详情")
    @Parameter(name = "id", description = "用户ID", required = true)
    public ResultVO<Customer> detail(@PathVariable Long id) {
        Customer customer = customerService.findOnly("id", id).orElseThrow();
        return ResultVO.success(customer);
    }

    @DeleteMapping("delete/{id}")
    @Operation(summary = "删除用户")
    @Parameter(name = "id", description = "用户ID", required = true)
    public ResultVO<String> delete(@PathVariable Long id) {
        int deleted = customerService.deleteEq("id", id);
        return ResultVO.resultMsg(deleted > 0, deleted > 0 ? "删除成功" : "删除失败");
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

## 必需注解清单

- [ ] `@PathRestController("{path}")`（不是 @RestController）
- [ ] `@Tag(name = "模块名称")`
- [ ] `@RequiredArgsConstructor`（构造器注入）
- [ ] 每个方法添加 `@Operation(summary = "接口说明")`
- [ ] **GET 请求**：使用 `@GetMapping`，参数使用 `@RequestParam` 或 `@PathVariable`，添加 `@Parameter` 注解
- [ ] **POST 请求**：使用 `@PostMapping`，参数使用 `@RequestBody @Valid` 注解
- [ ] **PUT 请求**：使用 `@PutMapping`，参数使用 `@RequestBody @Valid` 注解
- [ ] **DELETE 请求**：使用 `@DeleteMapping`，参数使用 `@PathVariable` 或 `@RequestParam`，添加 `@Parameter` 注解

---

## 返回值规范

Controller 统一返回 `ResultVO<T>` 或 `ResultPageVO<T, P>`，框架提供丰富的静态方法。

### ResultVO 成功返回

```java
// 1. 仅返回成功状态（无消息，无数据）
return ResultVO.success();

// 2. 返回数据（无消息）
return ResultVO.success(customer);

// 3. 返回消息（无数据）
return ResultVO.successMessage("操作成功");

// 4. 返回消息和数据
return ResultVO.success("新增成功", customer);
```

### ResultVO 失败返回

```java
// 1. 仅返回失败状态（无消息，无数据）
return ResultVO.fail();

// 2. 返回数据（无消息）
return ResultVO.fail(errorData);

// 3. 返回消息（无数据）
return ResultVO.failMessage("操作失败");

// 4. 返回消息和数据
return ResultVO.fail("删除失败", errorInfo);
```

### ResultVO 自定义返回

```java
// 1. 使用自定义错误码（ExceptionCode）
return ResultVO.of(CustomExceptionCode.INVALID_PARAM);

// 2. 使用自定义错误码和数据
return ResultVO.of(errorData, CustomExceptionCode.INVALID_PARAM);

// 3. 使用自定义状态码和消息
return ResultVO.of(400, "参数错误");

// 4. 使用自定义状态码、消息和数据
return ResultVO.of(customer, 201, "创建成功");
```

### ResultVO 条件返回

```java
// 根据布尔值返回成功或失败
boolean deleted = customerService.deleteById(id);
return ResultVO.resultMsg(deleted, deleted ? "删除成功" : "删除失败");
```

### ResultPageVO 分页返回

```java
// 1. 返回分页数据（无消息）
Page<Customer> result = customerService.findPage(page, page.getPage());
JpaPageResult<Customer> pageResult = JpaPageResult.toPage(result, Customer.class);
return ResultPageVO.success(pageResult);

// 2. 返回分页数据和消息
JpaPageResult<Customer> pageResult = JpaPageResult.toPage(result, Customer.class);
return ResultPageVO.success(pageResult, "查询成功");

// 3. 分页查询失败
return ResultPageVO.fail("查询失败");

// 4. 自定义状态码
return ResultPageVO.of(pageResult, CustomExceptionCode.PARTIAL_SUCCESS);

// 5. 自定义状态码和消息
return ResultPageVO.of(pageResult, 206, "部分数据查询成功");
```

### 实用示例

#### 新增操作

```java
@PostMapping("add")
@Operation(summary = "新增用户")
public ResultVO<String> add(@RequestBody @Valid UserAdd add) {
    customerService.saveCustomer(add);
    // 仅返回消息
    return ResultVO.successMessage("新增成功");
}
```

#### 查询详情

```java
@GetMapping("detail")
@Operation(summary = "用户详情")
public ResultVO<Customer> detail(@RequestParam Long id) {
    Customer customer = customerService.findById(id).orElseThrow();
    // 返回数据（无消息）
    return ResultVO.success(customer);
}
```

#### 更新操作

```java
@PostMapping("edit")
@Operation(summary = "编辑用户")
public ResultVO<Customer> edit(@RequestBody @Valid UserEdit edit) {
    Customer updated = customerService.updateCustomer(edit);
    // 返回消息和更新后的数据
    return ResultVO.success("编辑成功", updated);
}
```

#### 删除操作

```java
@PostMapping("delete")
@Operation(summary = "删除用户")
public ResultVO<String> delete(@RequestParam Long id) {
    boolean deleted = customerService.deleteById(id);
    // 根据结果返回成功或失败
    return ResultVO.resultMsg(deleted, deleted ? "删除成功" : "删除失败");
}
```

#### 分页查询

分页查询有两种实现模式，对应两种不同的 Service 调用方式。

**模式1：使用 @JpaSelectOperator 注解（自动查询）**

```java
@PostMapping("page")
@Operation(summary = "分页查询")
public ResultPageVO<LogEsInitData, JpaPageResult<LogEsInitData>> page(
    @RequestBody @Valid LogEsInitDataPage page) {
    // 直接传入 page 对象，框架根据 @JpaSelectOperator 注解自动构建查询
    Page<LogEsInitData> result = logEsInitDataService.findPage(page, page.getPage());
    JpaPageResult<LogEsInitData> pageResult = JpaPageResult.toPage(result);
    return ResultPageVO.success(pageResult, "查询成功");
}
```

**模式2：使用自定义 Specification（手动查询）**

```java
@PostMapping("page")
@Operation(summary = "分页查询资源日志")
public ResultPageVO<ResourceUseLog, JpaPageResult<ResourceUseLog>> page(
    @RequestBody @Valid ResourceUseLogPage page,
    HttpServletRequest request) {
    // 获取当前用户ID（从请求中获取）
    Long userId = getUserId(request);

    // 手动构建查询条件
    Specification<ResourceUseLog> spec = LogSpecQuery.logUserResourceSpec(page, userId, 1);

    // 传入 Specification 和分页参数
    Page<ResourceUseLog> result = resourceUseLogService.findPage(spec, page.getPage());
    JpaPageResult<ResourceUseLog> pageResult = JpaPageResult.toPage(result);
    return ResultPageVO.success(pageResult, "查询成功");
}
```

**两种模式的选择**：
- **模式1**：查询条件简单（等值、区间等标准条件），使用注解自动构建
- **模式2**：查询条件复杂（需要函数处理、动态组合），手动构建 Specification

**JpaPageResult 转换**：

```java
// 基本转换（不指定类型）
JpaPageResult<Customer> pageResult = JpaPageResult.toPage(result);

// 指定类型转换（推荐，类型安全）
JpaPageResult<Customer> pageResult = JpaPageResult.toPage(result, Customer.class);
```

#### 列表查询

```java
@GetMapping("list")
@Operation(summary = "用户列表")
public ResultVO<List<Customer>> list() {
    List<Customer> customers = customerService.findAll();
    // 返回列表数据
    return ResultVO.success(customers);
}
```

#### 异常处理

```java
@GetMapping("detail")
@Operation(summary = "用户详情")
public ResultVO<Customer> detail(@RequestParam Long id) {
    try {
        Customer customer = customerService.findById(id)
            .orElseThrow(() -> new RuntimeException("用户不存在"));
        return ResultVO.success(customer);
    } catch (Exception e) {
        log.error("查询用户详情失败", e);
        // 返回失败消息
        return ResultVO.failMessage("查询失败：" + e.getMessage());
    }
}
```

### 方法选择指南

| 场景 | 推荐方法 | 说明 |
|------|---------|------|
| 新增/编辑/删除成功 | `successMessage(String)` | 仅返回成功消息 |
| 查询单个对象 | `success(T body)` | 返回数据对象 |
| 查询列表 | `success(List<T> body)` | 返回列表数据 |
| 新增并返回对象 | `success(String, T)` | 返回消息和新增的对象 |
| 更新并返回对象 | `success(String, T)` | 返回消息和更新后的对象 |
| 条件操作 | `resultMsg(boolean, String)` | 根据布尔值返回成功或失败 |
| 分页查询 | `ResultPageVO.success(P, String)` | 返回分页数据和消息 |
| 操作失败 | `failMessage(String)` | 返回失败消息 |
| 自定义状态码 | `of(int, String)` | 自定义状态码和消息 |

---

## 鉴权控制

### 不需要鉴权

```java
@ApiMapping(value = "login", method = RequestMethod.POST, checkToken = false)
@Operation(summary = "用户登录")
public ResultVO<String> login(@RequestBody @Valid LoginRequest request) {
    // 登录逻辑
    return ResultVO.success(token);
}
```

### 平台限制

```java
@GetMapping("admin-list")
@Operation(summary = "管理员用户列表")
@ApiPlatform(platform = PlatformConstant.WEB_ADMIN)
public ResultVO<List<Customer>> adminList() {
    return ResultVO.success(customers);
}
```

---

## 参数验证

### GET 请求（使用 @RequestParam）

```java
@GetMapping("detail")
@Operation(summary = "用户详情")
@Parameter(name = "id", description = "用户ID", required = true)
@Parameter(name = "includeDeleted", description = "是否包含已删除", required = false)
public ResultVO<Customer> detail(
    @RequestParam Long id,
    @RequestParam(required = false, defaultValue = "false") Boolean includeDeleted) {
    return ResultVO.success(customer);
}
```

### GET 请求（使用 @PathVariable）

```java
@GetMapping("detail/{id}")
@Operation(summary = "用户详情")
@Parameter(name = "id", description = "用户ID", required = true)
public ResultVO<Customer> detail(@PathVariable Long id) {
    Customer customer = customerService.findOnly("id", id).orElseThrow();
    return ResultVO.success(customer);
}

// 多个路径变量
@GetMapping("{userId}/orders/{orderId}")
@Operation(summary = "用户订单详情")
@Parameter(name = "userId", description = "用户ID", required = true)
@Parameter(name = "orderId", description = "订单ID", required = true)
public ResultVO<Order> getUserOrder(
    @PathVariable Long userId,
    @PathVariable Long orderId) {
    return ResultVO.success(order);
}
```

### POST 请求

```java
@PostMapping("add")
@Operation(summary = "新增用户")
public ResultVO<String> add(@RequestBody @Valid UserAdd add) {
    // @Valid 触发参数验证
    customerService.saveOne(customer);
    return ResultVO.successMessage("新增成功");
}
```

### PUT 请求

```java
@PutMapping("update")
@Operation(summary = "更新用户")
public ResultVO<String> update(@RequestBody @Valid UserEdit edit) {
    // @Valid 触发参数验证
    customerService.update(customer, SQLOperator.EQ, "id");
    return ResultVO.successMessage("更新成功");
}

// 使用 @PathVariable
@PutMapping("update/{id}")
@Operation(summary = "更新用户")
@Parameter(name = "id", description = "用户ID", required = true)
public ResultVO<String> update(
    @PathVariable Long id,
    @RequestBody @Valid UserEdit edit) {
    edit.setId(id);
    customerService.update(edit, SQLOperator.EQ, "id");
    return ResultVO.successMessage("更新成功");
}
```

### DELETE 请求

```java
// 使用 @PathVariable（推荐）
@DeleteMapping("delete/{id}")
@Operation(summary = "删除用户")
@Parameter(name = "id", description = "用户ID", required = true)
public ResultVO<String> delete(@PathVariable Long id) {
    int deleted = customerService.deleteEq("id", id);
    return ResultVO.resultMsg(deleted > 0, deleted > 0 ? "删除成功" : "删除失败");
}

// 使用 @RequestParam
@DeleteMapping("delete")
@Operation(summary = "删除用户")
@Parameter(name = "id", description = "用户ID", required = true)
public ResultVO<String> delete(@RequestParam Long id) {
    int deleted = customerService.deleteEq("id", id);
    return ResultVO.resultMsg(deleted > 0, deleted > 0 ? "删除成功" : "删除失败");
}

// 批量删除
@DeleteMapping("batch-delete")
@Operation(summary = "批量删除用户")
public ResultVO<String> batchDelete(@RequestBody @Valid List<Long> ids) {
    ids.forEach(id -> customerService.deleteEq("id", id));
    return ResultVO.successMessage("批量删除成功");
}
```

### 混合参数

```java
// 路径变量 + 查询参数
@GetMapping("users/{userId}/orders")
@Operation(summary = "查询用户订单")
@Parameter(name = "userId", description = "用户ID", required = true)
@Parameter(name = "status", description = "订单状态", required = false)
public ResultVO<List<Order>> getUserOrders(
    @PathVariable Long userId,
    @RequestParam(required = false) Integer status) {
    return ResultVO.success(orders);
}

// 路径变量 + 请求体
@PutMapping("users/{userId}/password")
@Operation(summary = "修改用户密码")
@Parameter(name = "userId", description = "用户ID", required = true)
public ResultVO<String> updatePassword(
    @PathVariable Long userId,
    @RequestBody @Valid PasswordChange passwordChange) {
    passwordChange.setUserId(userId);
    customerService.updatePassword(passwordChange);
    return ResultVO.successMessage("密码修改成功");
}
```

---

## 完整检查清单

- [ ] 使用 `@PathRestController`
- [ ] 使用 `@Tag` 添加模块说明
- [ ] 使用构造器注入 Service
- [ ] 每个方法添加 `@Operation`
- [ ] **GET 请求**：
  - [ ] 使用 `@GetMapping`
  - [ ] 查询参数使用 `@RequestParam` 并添加 `@Parameter`
  - [ ] 路径变量使用 `@PathVariable` 并添加 `@Parameter`
- [ ] **POST 请求**：
  - [ ] 使用 `@PostMapping`
  - [ ] 请求体使用 `@RequestBody @Valid`
- [ ] **PUT 请求**：
  - [ ] 使用 `@PutMapping`
  - [ ] 请求体使用 `@RequestBody @Valid`
  - [ ] 路径变量使用 `@PathVariable` 并添加 `@Parameter`
- [ ] **DELETE 请求**：
  - [ ] 使用 `@DeleteMapping`
  - [ ] 路径变量使用 `@PathVariable`（推荐）或 `@RequestParam`
  - [ ] 添加 `@Parameter` 注解
- [ ] 统一返回 `ResultVO` 或 `ResultPageVO`
- [ ] 不直接操作数据库
- [ ] 不包含业务逻辑

---

## 参考资源

- 注解规范：[../standards/annotations.md](../standards/annotations.md)
- 请求/响应类：[./request-response.md](./request-response.md)
- 框架源码：https://github.com/en-o/Jdevelops
