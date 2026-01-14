# Controller 层代码生成指南

## 快速参考

Controller 使用 `@PathRestController` 注解，统一返回 `ResultVO` 或 `ResultPageVO`。

---

## 基本模板

```java
@PathRestController("user")
@Tag(name = "用户管理", extensions = {
    @Extension(properties = {
        @ExtensionProperty(name = "x-order", value = "3", parseValue = true)
    })
})
public CustomerServiceImpl() {
        super(Customer.class);
    }
@Slf4j
@Validated
public class CustomerController {

    private final CustomerService customerService;

    @PostMapping("add")
    @Operation(summary = "新增用户")
    public ResultVO<String> add(@RequestBody @Valid UserAdd add) {
        customerService.saveCustomer(add);
        return ResultVO.success("新增成功");
    }

    @PostMapping("edit")
    @Operation(summary = "编辑用户")
    public ResultVO<String> edit(@RequestBody @Valid UserEdit edit) {
        customerService.updateCustomer(edit);
        return ResultVO.success("编辑成功");
    }

    @GetMapping("detail")
    @Operation(summary = "用户详情")
    @Parameter(name = "id", description = "用户ID", required = true)
    public ResultVO<Customer> detail(@RequestParam Long id) {
        Customer customer = customerService.findById(id).orElseThrow();
        return ResultVO.success(customer);
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
- [ ] GET 请求使用 `@Parameter` 注解参数
- [ ] POST 请求使用 `@RequestBody @Valid` 注解参数

---

## 返回值规范

### 成功返回

```java
// 返回消息
return ResultVO.success("操作成功");

// 返回数据
return ResultVO.success(customer);

// 返回列表
return ResultVO.success(customerList);

// 返回分页
JpaPageResult<Customer> pageResult = JpaPageResult.toPage(result, Customer.class);
return ResultPageVO.success(pageResult, "查询成功");
```

### 失败返回

```java
return ResultVO.fail("操作失败");
return ResultVO.fail(500, "系统错误");
```

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

### GET 请求

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

### POST 请求

```java
@PostMapping("add")
@Operation(summary = "新增用户")
public ResultVO<String> add(@RequestBody @Valid UserAdd add) {
    // @Valid 触发参数验证
    return ResultVO.success();
}
```

---

## 完整检查清单

- [ ] 使用 `@PathRestController`
- [ ] 使用 `@Tag` 添加模块说明
- [ ] 使用构造器注入 Service
- [ ] 每个方法添加 `@Operation`
- [ ] GET 请求使用 `@Parameter`
- [ ] POST 请求使用 `@RequestBody @Valid`
- [ ] 统一返回 `ResultVO` 或 `ResultPageVO`
- [ ] 不直接操作数据库
- [ ] 不包含业务逻辑

---

## 参考资源

- 注解规范：[../standards/annotations.md](../standards/annotations.md)
- 请求/响应类：[./request-response.md](./request-response.md)
- 框架源码：https://github.com/en-o/Jdevelops
