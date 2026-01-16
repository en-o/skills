# Controller 层代码生成指南

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

## 登录管理示例

JDevelops 框架提供了两种登录方式：纯JWT登录和Redis+JWT登录。

### 方式1：纯JWT登录（无状态）

**适用场景**：小型应用、无需管理在线用户、不需要强制退出功能

**核心依赖**：`jdevelops-jwt-standalone`

**特点**：
- JWT完全无状态，服务端不存储token
- 无法实现强制退出（token在有效期内始终有效）
- 性能高，不依赖Redis

```java
@PathRestController("")
@Tag(name = "登录管理")
@RequiredArgsConstructor
@Slf4j
public class LoginController {

    private final UserInfoService userInfoService;
    private final LoginService loginService;  // JWT登录服务

    /**
     * 账户密码登录
     */
    @Operation(summary = "账户密码登录")
    @ApiMapping(value = "/login", checkToken = false, method = RequestMethod.POST)
    public ResultVO<LoginVO> login(
        @RequestBody @Valid LoginPassword login,
        HttpServletRequest request) throws IllegalAccessException {

        log.info("登录请求，登录名：{}", login.getLoginName());

        // 1. 验证用户名密码
        UserInfo userInfo = userInfoService.authenticateUser(login);

        // 2. 生成JWT token
        String token = loginUserSign(userInfo, request);

        return ResultVO.success("登录成功", new LoginVO(token));
    }

    /**
     * 退出（纯JWT无实际操作）
     */
    @Operation(summary = "退出")
    @GetMapping("/logout")
    public ResultVO<String> logout(HttpServletRequest request) {
        // 纯JWT模式下，退出只是客户端删除token
        // 服务端无法使token失效（除非维护黑名单）
        return ResultVO.successMessage("成功退出");
    }

    /**
     * 解析当前登录用户的token
     */
    @Operation(summary = "解析当前登录者的token")
    @ApiMapping(value = "parse")
    public ResultVO<SignEntity<String>> parseToken(HttpServletRequest request) {
        return ResultVO.success(JwtWebUtil.getTokenBySignEntity(request));
    }

    /**
     * 构造登录信息并生成token
     */
    private String loginUserSign(UserInfo account, HttpServletRequest request) {
        // 初始化签名实体
        SignEntity<LoginJwtExtendInfo<String>> init = SignEntity.init(account.getLoginName());

        // 设置扩展信息
        LoginJwtExtendInfo<String> extendInfo = new LoginJwtExtendInfo<>();
        extendInfo.setUserId(account.getId() + "");
        extendInfo.setUserNo(account.getId() + "");
        extendInfo.setUserName(account.getLoginName());
        extendInfo.setLoginName(account.getLoginName());
        init.setMap(extendInfo);

        // 生成token
        return loginService.login(init).getSign();
    }
}
```

### 方式2：Redis+JWT登录（有状态）

**适用场景**：中大型应用、需要管理在线用户、需要强制退出、防重复登录

**核心依赖**：`jdevelops-authentications-rjwt`

**特点**：
- JWT token存储在Redis中，支持管理和控制
- 可以实现强制退出、踢人下线、防重复登录
- 支持登录限制（错误次数限制）
- 支持验证码功能
- 支持登录日志记录
- 支持多平台登录控制

```java
@PathRestController
@Tag(name = "登录管理", extensions = {
    @Extension(properties = {
        @ExtensionProperty(name = "x-order", value = "1", parseValue = true)
    })
})
@RequiredArgsConstructor
@Slf4j
public class LoginController {

    private final RedisLoginService redisLoginService;  // Redis登录服务
    private final AccountService accountService;
    private final RoleAccountService roleAccountService;
    private final LoginLimitService loginLimitService;  // 登录限制服务
    private final AccountLoginPlatformService accountLoginPlatformService;
    private final CaptchaService captchaService;  // 验证码服务
    private final SysConfigService sysConfigService;

    /**
     * 管理端登录
     */
    @Operation(summary = "账户密码登录-admin")
    @ApiMapping(value = "/login", checkToken = false, method = RequestMethod.POST)
    @LoginLog(type = LoginType.ADMIN_ACCOUNT_PASSWORD)  // 记录登录日志
    public ResultVO<LoginVO> login(
        @RequestBody @Valid LoginPasswordCaptcha login,
        HttpServletRequest request) throws IllegalAccessException {

        // 1. 验证登录次数限制
        loginLimitService.verify(login.getLoginName(), false);

        // 2. 验证图形验证码（根据配置决定是否需要）
        SysLoginCaptcha captcha = sysConfigService.findCaptchaSetting_bean(PlatformType.ADMIN);
        if (captcha.green(login.getCaptcha())) {
            captchaService.verifyCaptcha(login.getCaptcha(), request);
        }

        try {
            // 3. 验证用户名密码
            List<String> platforms = Collections.singletonList(PlatformConstant.WEB_ADMIN);
            Account account = accountService.authenticateUser(platforms, login);

            // 4. 验证平台登录权限
            boolean isPlatformLogin = accountLoginPlatformService.isLoginPlatform(
                PlatformType.ADMIN, account.getId() + "");
            if (!isPlatformLogin) {
                throw new UserException(405, "无登录管理后台权限");
            }

            // 5. 生成token
            String token = loginUserSign(account, request, platforms, true);

            return ResultVO.success("登录成功",
                new LoginVO(token, account.verifyForcePasswordChange2()));
        } catch (Exception e) {
            // 6. 记录登录失败次数
            loginLimitService.limit(login.getLoginName());
            throw e;
        }
    }

    /**
     * 前台用户登录
     */
    @Operation(summary = "账户密码登录-利用端登录")
    @ApiMapping(value = "/login/web", checkToken = false, method = RequestMethod.POST)
    @LoginLog(type = LoginType.ADMIN_ACCOUNT_PASSWORD, platform = PlatformConstant.WEB_H5)
    public ResultVO<LoginVO> loginWeb(
        @RequestBody @Valid LoginPasswordCaptcha login,
        HttpServletRequest request) throws IllegalAccessException {

        loginLimitService.verify(login.getLoginName(), false);

        SysLoginCaptcha captcha = sysConfigService.findCaptchaSetting_bean(PlatformType.PC);
        if (captcha.green(login.getCaptcha())) {
            captchaService.verifyCaptcha(login.getCaptcha(), request);
        }

        try {
            List<String> platforms = Collections.singletonList(PlatformConstant.WEB_PC);
            Account account = accountService.authenticateUser(platforms, login);

            boolean isPlatformLogin = accountLoginPlatformService.isLoginPlatform(
                PlatformType.PC, account.getId() + "");
            if (!isPlatformLogin) {
                throw new UserException(405, "无登录权限,请联系管理员");
            }

            String token = loginUserSign(account, request, platforms, true);
            return ResultVO.success("登录成功", new LoginVO(token));
        } catch (Exception e) {
            loginLimitService.limit(login.getLoginName());
            throw e;
        }
    }

    /**
     * 游客登录
     */
    @Operation(summary = "利用端-游客登录")
    @ApiMapping(value = "/login/web/guest", checkToken = false, method = RequestMethod.POST)
    public ResultVO<LoginVO> loginGuest(HttpServletRequest request) {
        try {
            List<String> platforms = Collections.singletonList(PlatformConstant.WEB_PC);

            // 构造游客账号
            Account account = new Account();
            account.setId(0L);
            account.setLoginName(DefAccountLoginName.GUEST);
            account.setName("游客");
            account.setNickname("游客");
            account.setStatus(1);
            account.setType(0);
            account.setAvailable(2);
            account.setForcePasswordChange(false);

            String token = loginUserSign(account, request, platforms, false);
            return ResultVO.success("登录成功", new LoginVO(token));
        } catch (Exception e) {
            log.error("游客登录失败，错误消息{}", e.getMessage(), e);
            throw new BusinessException("登录失败！" + e.getMessage());
        }
    }

    /**
     * 退出（清除Redis中的token）
     */
    @Operation(summary = "退出")
    @GetMapping("/logout")
    public ResultVO<String> logout(HttpServletRequest request) {
        // Redis模式下，退出会清除Redis中的token，使其立即失效
        redisLoginService.loginOut(request);
        return ResultVO.successMessage("成功退出");
    }

    /**
     * 解析当前登录用户的token
     */
    @Operation(summary = "解析当前登录者的token")
    @ApiMapping(value = "parse")
    public ResultVO<SignEntity<String>> parseToken(HttpServletRequest request) {
        return ResultVO.success(JwtWebUtil.getTokenBySignEntity(request));
    }

    /**
     * 获取图形验证码
     */
    @Operation(summary = "获取图形验证码", description = "默认是PC的,data为空表示不需要验证码")
    @ApiMapping(value = "/captcha", checkToken = false, method = RequestMethod.GET)
    public ResultVO<CaptchaVO> imageShearCaptcha(
        @RequestParam(value = "platform", required = false) PlatformType platform,
        HttpServletRequest request) {

        if (platform == null) {
            platform = PlatformType.PC;
        }

        SysLoginCaptcha captcha = sysConfigService.findCaptchaSetting_bean(platform);
        if (!captcha.getOpen()) {
            return ResultVO.success(null);
        }

        CaptchaVO captchaVO = switchCaptcha(captcha, request);

        // 生产环境不返回答案
        if (!"mock".equals(profile)) {
            captchaVO.setCaptcha("你猜");
        }

        return ResultVO.success(captchaVO);
    }

    /**
     * 构造登录信息并生成token（Redis模式）
     */
    private String loginUserSign(Account account, HttpServletRequest request,
                                 List<String> platform, boolean log) {
        // 构造Redis签名实体
        RedisSignEntity<LoginJwtExtendInfo> redisSignEntity = new RedisSignEntity<>(
            account.getLoginName(),
            platform,
            false,  // 不允许多端登录
            false,  // 不强制下线旧token
            new StorageUserState(
                account.getLoginName(),
                account.getStatus(),
                account.getErrorMessage())
        );

        // 设置角色信息
        List<String> userRole = roleAccountService.getRoleCodeByUserId(account.getId());
        redisSignEntity.setUserRole(
            new StorageUserRole(
                account.getLoginName(),
                userRole,
                Collections.emptyList()));

        // 设置扩展信息
        LoginJwtExtendInfo<String> jwtExtendInfo = new LoginJwtExtendInfo<>();
        jwtExtendInfo.setUserId(account.getId() + "");
        jwtExtendInfo.setUserName(account.getName());
        jwtExtendInfo.setLoginName(account.getLoginName());
        redisSignEntity.setMap(jwtExtendInfo);

        // 生成token（存储到Redis）
        TokenSign login = redisLoginService.login(redisSignEntity);

        if (log) {
            LoginContextHolder.getContext()
                .setDescription(login.getDescription())
                .setToken(login.getSign(), false);
        }

        return login.getSign();
    }
}
```

### 登录请求类

```java
// 纯JWT登录请求类
@Getter
@Setter
@ToString
public class LoginPassword {
    @NotBlank(message = "登录名不能为空")
    @Schema(description = "登录名")
    private String loginName;

    @NotBlank(message = "密码不能为空")
    @Schema(description = "密码")
    private String password;
}

// Redis+JWT登录请求类（带验证码）
@Getter
@Setter
@ToString
public class LoginPasswordCaptcha extends LoginPassword {
    @Schema(description = "验证码")
    private String captcha;
}
```

### 登录响应类

```java
@Getter
@Setter
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class LoginVO {
    @Schema(description = "JWT Token")
    private String token;

    @Schema(description = "是否需要强制修改密码")
    private Boolean forcePasswordChange;

    public LoginVO(String token) {
        this.token = token;
    }
}
```

### 两种方式对比

| 特性 | 纯JWT登录 | Redis+JWT登录 |
|-----|----------|--------------|
| **依赖** | `jdevelops-jwt-standalone` | `jdevelops-authentications-rjwt` |
| **存储** | 无状态，不存储token | token存储在Redis |
| **强制退出** | ❌ 不支持 | ✅ 支持 |
| **踢人下线** | ❌ 不支持 | ✅ 支持 |
| **防重复登录** | ❌ 不支持 | ✅ 支持 |
| **登录限制** | ❌ 需自行实现 | ✅ 内置支持 |
| **验证码** | ❌ 需自行实现 | ✅ 内置支持 |
| **登录日志** | ❌ 需自行实现 | ✅ 内置支持 |
| **性能** | ⚡ 高（无IO操作） | 💾 依赖Redis性能 |
| **适用场景** | 小型应用、API网关 | 中大型应用、管理后台 |

### Service 层实现（用户认证）

```java
@Service
public class AccountServiceImpl extends J2ServiceImpl<AccountDao, Account, Long>
    implements AccountService {

    public AccountServiceImpl() {
        super(Account.class);
    }

    @Override
    public Account authenticateUser(List<String> platforms, LoginPassword login) {
        // 1. 查询用户
        Optional<Account> accountOpt = this.findOnly("loginName", login.getLoginName());
        if (accountOpt.isEmpty()) {
            throw new UserException(404, "用户不存在");
        }

        Account account = accountOpt.get();

        // 2. 验证密码
        if (!PasswordUtil.matches(login.getPassword(), account.getPassword())) {
            throw new UserException(401, "密码错误");
        }

        // 3. 验证账号状态
        if (account.getStatus() != 1) {
            throw new UserException(403, "账号已被禁用");
        }

        // 4. 验证平台权限（Redis模式）
        if (platforms != null && !platforms.isEmpty()) {
            boolean hasPermission = accountLoginPlatformService.hasPermission(
                account.getId(), platforms);
            if (!hasPermission) {
                throw new UserException(405, "无访问该平台的权限");
            }
        }

        return account;
    }
}
```

### 获取当前登录用户信息

```java
@PathRestController("user")
@Tag(name = "用户管理")
@RequiredArgsConstructor
public class UserController {

    private final AccountService accountService;

    /**
     * 获取当前登录用户信息
     */
    @GetMapping("current")
    @Operation(summary = "获取当前登录用户信息")
    public ResultVO<Account> getCurrentUser(HttpServletRequest request) {
        // 从token中获取用户ID
        SignEntity<String> signEntity = JwtWebUtil.getTokenBySignEntity(request);
        String userId = signEntity.getMap();

        // 查询用户信息
        Account account = accountService.findOnly("id", Long.parseLong(userId))
            .orElseThrow(() -> new UserException(404, "用户不存在"));

        return ResultVO.success(account);
    }
}
```

---

## 参考资源

- 注解规范：[../standards/annotations.md](../standards/annotations.md)
- 请求/响应类：[./request-response.md](./request-response.md)
- 框架源码：https://github.com/en-o/Jdevelops
