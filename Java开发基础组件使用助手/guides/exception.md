# 全局异常处理指南

## 组件介绍

`jdevelops-apis-exception` 是 JDevelops 框架中**最核心的组件之一**，提供：
- 全局异常捕获和处理
- 统一的 API 返回格式（ResultVO、ResultPageVO）
- 多种内置异常类（BusinessException、TokenException 等）
- @DisposeException 自定义异常处理
- **自动引入 jdevelops-apis-result**，无需单独添加

## 依赖配置

### Maven 依赖

```xml
<dependency>
    <groupId>cn.tannn.jdevelops</groupId>
    <artifactId>jdevelops-apis-exception</artifactId>
    <version>${jdevelops.version}</version>
</dependency>
```

**重要**：
- 添加 `jdevelops-apis-exception` 后，会自动引入 `jdevelops-apis-result`
- 无需再单独添加 `jdevelops-apis-result` 依赖

### 包含的依赖

jdevelops-apis-exception 自动引入：
- `jdevelops-apis-result` (1.0.3): 统一返回格式
- `jdevelops-utils-aop` (1.0.3): AOP 工具
- Spring Boot 相关依赖

---

## 默认异常格式

### 默认返回格式

全局异常会自动转换为统一的 JSON 格式：

```json
{
  "code": 500,
  "message": "具体的错误信息",
  "success": false,
  "data": null,
  "traceId": "trace-id-12345"
}
```

**字段说明**：
- `code`: 错误码（如 500、401、403）
- `message`: 错误信息
- `success`: 是否成功（异常时固定为 false）
- `data`: 数据（异常时为 null）
- `traceId`: 链路追踪 ID（用于日志查询）

### 自定义异常格式

如需修改默认格式，可以通过配置类自定义：

```java
@Configuration
public class ExceptionConfig {

    @Bean
    public GlobalExceptionHandler globalExceptionHandler() {
        return new GlobalExceptionHandler() {
            @Override
            protected ResultVO<Object> buildErrorResponse(int code, String message) {
                // 自定义返回格式
                return ResultVO.error(code, message);
            }
        };
    }
}
```

---

## 配置选项

在 `application.yml` 中可配置异常处理行为：

```yaml
jdevelops:
  exception:
    # 是否打印异常堆栈（默认 true）
    print-stack-trace: true

    # 是否返回异常详情给前端（默认 false，生产环境建议关闭）
    return-stack-trace: false

    # 默认错误信息
    default-message: "系统异常，请联系管理员"

    # 是否启用异常处理（默认 true）
    enabled: true
```

---

## 项目自定义异常（重要）

### 创建项目专属异常类

**在构建新项目时，必须在 `common/exception` 包下创建项目专属的异常类**，例如：
- 图书管理系统 → `BookException`
- 订单系统 → `OrderException`
- 用户系统 → `UserException`

### 项目异常类模板

**重要提醒**：
- ⚠️ 生成异常类代码时，不要自动生成import语句，让用户或IDE自动处理
- ⚠️ BusinessException需要从 jdevelops-apis-exception 依赖中导入
- ⚠️ ExceptionCode为自定义枚举类，需要根据项目自行创建

```java
package com.example.project.common.exception;

import lombok.AllArgsConstructor;
import lombok.Getter;

/**
 * 项目专属业务异常
 * 用于处理本项目特定的业务逻辑异常
 *
 * @author tn
 * @date 2021-01-22 14:15
 */
@AllArgsConstructor
@Getter
public class BookException extends BusinessException {

    public BookException(int code, String message) {
        super(code, message);
    }

    public BookException(String message) {
        super(message);
    }

    public BookException(ExceptionCode errorCode) {
        super(errorCode.getCode(), errorCode.getMessage());
    }
}
```

**说明**：
- 继承 `BusinessException` 而非 `RuntimeException`，使用框架统一的异常处理机制
- 支持三种构造方法：
  1. `BookException(int code, String message)` - 自定义错误码和消息
  2. `BookException(String message)` - 使用默认错误码(500)
  3. `BookException(ExceptionCode errorCode)` - 使用错误码枚举

### 配套异常处理器

创建异常类后，需要在同一包下创建对应的异常处理器：

**重要提醒**：
- ⚠️ 生成异常处理器代码时，不要自动生成import语句，让用户或IDE自动处理

```java
package com.example.project.common.exception;

/**
 * 项目异常处理器
 */
@Slf4j
@Component
public class BookExceptionHandler {

    @DisposeException(BookException.class)
    public ResultVO<Object> handleBookException(BookException e) {
        log.error("业务异常: {}", e.getMessage(), e);
        return ResultVO.error(e.getCode(), e.getMessage());
    }
}
```

### 使用示例

```java
@Service
public class BookServiceImpl extends J2Service<Book> implements BookService {

    @Override
    public void borrowBook(Long bookId, Long userId) {
        Book book = findById(bookId)
            .orElseThrow(() -> new BookException("图书不存在"));

        if (book.getStock() <= 0) {
            throw new BookException("图书库存不足");
        }

        // 业务逻辑...
    }
}
```

**为什么需要项目专属异常？**
- ✅ 更好的异常分类和管理
- ✅ 便于统一处理项目特定的业务异常
- ✅ 提高代码可读性和可维护性
- ✅ 支持自定义错误码和错误信息格式

---

## 内置异常类

### 1. BusinessException（业务异常）

**适用场景**：业务规则验证失败

```java
// 抛出异常
if (user == null) {
    throw new BusinessException("用户不存在");
}

// 带错误码
throw new BusinessException(404, "用户不存在");

// 使用枚举
throw new BusinessException(ErrorCode.USER_NOT_FOUND);
```

**返回示例**：
```json
{
  "code": 500,
  "message": "用户不存在",
  "success": false
}
```

### 2. TokenException（Token 异常）

**适用场景**：Token 验证失败

```java
// Token 无效
throw new TokenException("Token 无效");

// Token 过期
throw new TokenException(TokenCode.TOKEN_EXPIRED);
```

**返回示例**：
```json
{
  "code": 401,
  "message": "Token 无效",
  "success": false
}
```

### 3. UserException（用户异常）

**适用场景**：用户相关操作失败

```java
// 用户未登录
throw new UserException("用户未登录");

// 用户无权限
throw new UserException(403, "无权访问该资源");
```

### 4. ParamException（参数异常）

**适用场景**：请求参数验证失败

```java
// 参数为空
if (StringUtils.isBlank(name)) {
    throw new ParamException("用户名不能为空");
}

// 参数格式错误
throw new ParamException("邮箱格式不正确");
```

### 5. AuthException（认证异常）

**适用场景**：认证失败

```java
// 认证失败
throw new AuthException("用户名或密码错误");

// 账号被禁用
throw new AuthException("账号已被禁用");
```

### 6. NotFoundException（资源未找到）

**适用场景**：请求的资源不存在

```java
Customer customer = customerRepository.findById(id)
    .orElseThrow(() -> new NotFoundException("用户不存在"));
```

---

## @DisposeException 自定义异常处理

### 基本用法

使用 `@DisposeException` 注解可以自定义特定异常的处理逻辑：

```java
@Component
public class CustomExceptionHandler {

    /**
     * 处理自定义业务异常
     */
    @DisposeException(CustomBusinessException.class)
    public ResultVO<Object> handleCustomException(CustomBusinessException e) {
        // 记录日志
        log.error("业务异常: {}", e.getMessage());

        // 返回自定义格式
        return ResultVO.error(e.getCode(), e.getMessage());
    }

    /**
     * 处理数据库异常
     */
    @DisposeException(DataAccessException.class)
    public ResultVO<Object> handleDataAccessException(DataAccessException e) {
        log.error("数据库异常", e);
        return ResultVO.error(500, "数据库操作失败");
    }

    /**
     * 处理第三方 API 异常
     */
    @DisposeException(HttpClientErrorException.class)
    public ResultVO<Object> handleHttpException(HttpClientErrorException e) {
        log.error("HTTP 请求失败: {}", e.getMessage());
        return ResultVO.error(502, "外部服务调用失败");
    }
}
```

### 高级用法：异常链处理

```java
@Component
public class AdvancedExceptionHandler {

    /**
     * 处理异常链（当异常嵌套时）
     */
    @DisposeException(SQLException.class)
    public ResultVO<Object> handleSQLException(SQLException e) {
        // 判断具体的 SQL 异常类型
        if (e instanceof SQLIntegrityConstraintViolationException) {
            return ResultVO.error(400, "数据重复，违反唯一约束");
        } else if (e instanceof SQLTimeoutException) {
            return ResultVO.error(504, "数据库查询超时");
        }

        return ResultVO.error(500, "数据库操作失败");
    }

    /**
     * 返回不同的错误码
     */
    @DisposeException(IllegalArgumentException.class)
    public ResultVO<Object> handleIllegalArgument(IllegalArgumentException e) {
        return ResultVO.error(400, "参数错误: " + e.getMessage());
    }
}
```

---

## 特殊错误码说明（前端处理）

以下错误码需要前端特殊处理，通常会触发跳转登录页或提示用户重新登录。

### 错误码列表

| code | 内置枚举 | 说明 | 前端处理建议 |
|------|---------|------|------------|
| **401** | TOKEN_ERROR | Token 验证失败（格式错误、签名错误） | 清除本地 Token，跳转登录页 |
| **401** | REDIS_EXPIRED_USER | 登录过期（Redis 中 Token 已失效） | 提示"登录已过期"，跳转登录页 |
| **401** | REDIS_NO_USER | 非法登录（Token 已被替换，如异地登录） | 提示"账号已在其他地方登录"，跳转登录页 |
| **402** | SYS_AUTHORIZED_PAST | 授权过期（权限有效期已过） | 提示"授权已过期，请联系管理员" |
| **403** | UNAUTHENTICATED | 系统未授权（无权访问系统） | 提示"无访问权限"，返回首页或跳转登录 |
| **403** | UNAUTHENTICATED_PLATFORM | Token 平台不匹配（Web Token 访问 App 接口） | 提示"Token 无效"，跳转登录页 |

### 前端处理示例

```javascript
// Axios 拦截器示例
axios.interceptors.response.use(
  response => response,
  error => {
    const { code, message } = error.response.data;

    // 401: Token 相关错误，跳转登录
    if (code === 401) {
      if (message.includes('REDIS_NO_USER')) {
        Toast('账号已在其他地方登录');
      } else if (message.includes('REDIS_EXPIRED_USER')) {
        Toast('登录已过期');
      } else {
        Toast('Token 验证失败');
      }
      // 清除本地 Token
      localStorage.removeItem('token');
      // 跳转登录页
      router.push('/login');
    }

    // 402: 授权过期
    else if (code === 402) {
      Toast('授权已过期，请联系管理员');
      router.push('/unauthorized');
    }

    // 403: 无权限
    else if (code === 403) {
      if (message.includes('UNAUTHENTICATED_PLATFORM')) {
        Toast('Token 无效');
        router.push('/login');
      } else {
        Toast('无访问权限');
      }
    }

    return Promise.reject(error);
  }
);
```

### 后端抛出示例

```java
@Service
public class TokenServiceImpl implements TokenService {

    @Autowired
    private RedisTemplate<String, Object> redisTemplate;

    @Override
    public User validateToken(String token, String platform) {
        // 1. Token 格式验证
        if (!JwtUtil.validate(token)) {
            throw new TokenException(401, "TOKEN_ERROR", "Token 格式错误");
        }

        // 2. Redis 中查询用户信息
        String userId = JwtUtil.getUserId(token);
        User user = (User) redisTemplate.opsForValue().get("user:" + userId);

        if (user == null) {
            // Token 已失效
            throw new TokenException(401, "REDIS_EXPIRED_USER", "登录已过期");
        }

        // 3. 校验 Token 是否是最新的
        String redisToken = (String) redisTemplate.opsForValue().get("token:" + userId);
        if (!token.equals(redisToken)) {
            // Token 已被替换（异地登录）
            throw new TokenException(401, "REDIS_NO_USER", "账号已在其他地方登录");
        }

        // 4. 校验平台
        String tokenPlatform = JwtUtil.getPlatform(token);
        if (!platform.equals(tokenPlatform)) {
            throw new TokenException(403, "UNAUTHENTICATED_PLATFORM", "Token 平台不匹配");
        }

        // 5. 校验授权有效期
        if (user.getAuthExpireTime() != null &&
            user.getAuthExpireTime().before(new Date())) {
            throw new TokenException(402, "SYS_AUTHORIZED_PAST", "授权已过期");
        }

        // 6. 校验系统权限
        if (!user.hasSystemAccess()) {
            throw new TokenException(403, "UNAUTHENTICATED", "无系统访问权限");
        }

        return user;
    }
}
```

---

## 常用异常场景

### 场景 1: Controller 参数验证

```java
@PostMapping("add")
@Operation(summary = "新增用户")
public ResultVO<String> add(@RequestBody @Valid UserAdd add) {
    // @Valid 自动验证，失败抛出 MethodArgumentNotValidException
    // 框架自动捕获并返回验证失败信息

    customerService.saveCustomer(add);
    return ResultVO.success("新增成功");
}
```

### 场景 2: Service 业务逻辑验证

```java
@Service
public class CustomerServiceImpl implements CustomerService {

    @Override
    public void saveCustomer(UserAdd add) {
        // 检查用户名是否存在
        Optional<Customer> existing = findOnly("loginName", add.getLoginName());
        if (existing.isPresent()) {
            throw new BusinessException("用户名已存在");
        }

        // 检查手机号是否重复
        if (StringUtils.isNotBlank(add.getPhone())) {
            Optional<Customer> phoneExists = findOnly("phone", add.getPhone());
            if (phoneExists.isPresent()) {
                throw new BusinessException("手机号已被使用");
            }
        }

        // 保存用户
        Customer customer = SerializableBean.to2(add, Customer.class);
        saveOne(customer);
    }
}
```

### 场景 3: 资源未找到

```java
@GetMapping("detail")
@Operation(summary = "用户详情")
public ResultVO<Customer> detail(@RequestParam Long id) {
    // 方式1: 使用 orElseThrow
    Customer customer = customerService.findById(id)
        .orElseThrow(() -> new NotFoundException("用户不存在"));

    return ResultVO.success(customer);
}

// 方式2: 在 Service 中处理
@Override
public Customer getCustomerById(Long id) {
    return findById(id)
        .orElseThrow(() -> new BusinessException(404, "用户不存在"));
}
```

### 场景 4: 权限验证

```java
@DeleteMapping("delete/{id}")
@Operation(summary = "删除用户")
public ResultVO<String> delete(@PathVariable Long id, HttpServletRequest request) {
    // 获取当前用户
    Long currentUserId = TokenUtil.getUserId(request);
    Customer currentUser = customerService.findById(currentUserId).orElseThrow();

    // 权限验证
    if (!currentUser.isAdmin()) {
        throw new AuthException(403, "无权删除用户");
    }

    // 不能删除自己
    if (id.equals(currentUserId)) {
        throw new BusinessException("不能删除自己的账号");
    }

    customerService.deleteById(id);
    return ResultVO.success("删除成功");
}
```

### 场景 5: 数据库约束异常

```java
@Service
public class CustomerServiceImpl implements CustomerService {

    @Override
    @Transactional(rollbackFor = Exception.class)
    public void deleteCustomer(Long id) {
        try {
            // 删除用户
            deleteById(id);
        } catch (DataIntegrityViolationException e) {
            // 违反外键约束
            throw new BusinessException("该用户存在关联数据，无法删除");
        }
    }
}
```

---

## 完整示例

### 自定义异常类

```java
// 自定义业务异常
public class OrderException extends RuntimeException {
    private final int code;

    public OrderException(String message) {
        super(message);
        this.code = 500;
    }

    public OrderException(int code, String message) {
        super(message);
        this.code = code;
    }

    public int getCode() {
        return code;
    }
}
```

### 异常处理器

```java
@Component
public class OrderExceptionHandler {

    @DisposeException(OrderException.class)
    public ResultVO<Object> handleOrderException(OrderException e) {
        log.error("订单异常: {}", e.getMessage());
        return ResultVO.error(e.getCode(), e.getMessage());
    }
}
```

### 使用示例

```java
@Service
public class OrderServiceImpl implements OrderService {

    @Override
    @Transactional(rollbackFor = Exception.class)
    public void createOrder(OrderAdd add) {
        // 检查商品库存
        Product product = productService.findById(add.getProductId())
            .orElseThrow(() -> new OrderException("商品不存在"));

        if (product.getStock() < add.getQuantity()) {
            throw new OrderException("库存不足");
        }

        // 检查用户余额
        Customer customer = customerService.findById(add.getCustomerId())
            .orElseThrow(() -> new OrderException("用户不存在"));

        BigDecimal totalPrice = product.getPrice().multiply(new BigDecimal(add.getQuantity()));
        if (customer.getBalance().compareTo(totalPrice) < 0) {
            throw new OrderException("余额不足");
        }

        // 创建订单
        Order order = new Order();
        order.setCustomerId(add.getCustomerId());
        order.setProductId(add.getProductId());
        order.setQuantity(add.getQuantity());
        order.setTotalPrice(totalPrice);

        // 扣减库存
        product.setStock(product.getStock() - add.getQuantity());
        productService.saveOne(product);

        // 扣减余额
        customer.setBalance(customer.getBalance().subtract(totalPrice));
        customerService.saveOne(customer);

        // 保存订单
        saveOne(order);
    }
}
```

---

## 最佳实践

### 1. 异常分层

```
Controller 层：
  - 参数验证异常（@Valid 自动处理）
  - 不抛出业务异常，由 Service 层抛出

Service 层：
  - 业务逻辑验证（抛出 BusinessException）
  - 资源未找到（抛出 NotFoundException）
  - 权限验证（抛出 AuthException）

DAO 层：
  - 不抛出异常，返回 Optional
  - 数据库异常由框架自动处理
```

### 2. 异常信息规范

```java
// ✅ 正确：信息明确、友好
throw new BusinessException("用户名已存在");
throw new BusinessException("手机号格式不正确");

// ❌ 错误：信息模糊、不友好
throw new BusinessException("错误");
throw new BusinessException("save failed");
```

### 3. 避免过度捕获

```java
// ✅ 正确：让框架处理
@Override
public void saveCustomer(UserAdd add) {
    if (exists("loginName", add.getLoginName())) {
        throw new BusinessException("用户名已存在");
    }
    saveOne(customer);
}

// ❌ 错误：不必要的 try-catch
@Override
public void saveCustomer(UserAdd add) {
    try {
        if (exists("loginName", add.getLoginName())) {
            throw new BusinessException("用户名已存在");
        }
        saveOne(customer);
    } catch (Exception e) {
        throw new BusinessException("保存失败");
    }
}
```

### 4. 使用合适的异常

```java
// 业务验证失败
throw new BusinessException("用户名已存在");

// 资源未找到
throw new NotFoundException("用户不存在");

// 权限不足
throw new AuthException("无权访问该资源");

// 参数错误
throw new ParamException("用户名不能为空");

// Token 无效
throw new TokenException("Token 已过期");
```

---

## 参考资源

- 组件清单：[../reference/components.md](../reference/components.md)
- Controller 指南：[./controller.md](./controller.md)
- Service 指南：[./service.md](./service.md)
- 官方文档：https://www.yuque.com/tanning/yg9ipo
