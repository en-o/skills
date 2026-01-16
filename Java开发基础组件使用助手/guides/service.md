# Service 层代码生成指南

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

Service 接口继承 `J2Service<Entity>`，Service 实现继承 `J2ServiceImpl<DAO, Entity, ID>`。

**关键注意**：`J2ServiceImpl` 需要三个泛型参数：
1. **DAO**: DAO 接口类型
2. **Entity**: 实体类类型
3. **ID**: 主键类型（通常是 Long 或 String）

---

## 基本模板

### Service 接口

```java
public interface CustomerService extends J2Service<Customer> {
    // 自定义方法
    Optional<Customer> findByLoginName(String loginName);
    List<Customer> findActiveCustomers();
}
```

### Service 实现

```java
@Service
public class CustomerServiceImpl extends J2ServiceImpl<CustomerDao, Customer, Long>
    implements CustomerService {

    public CustomerServiceImpl() {
        super(Customer.class);
    }

    @Override
    public Optional<Customer> findByLoginName(String loginName) {
        // ⚠️ 重要：使用 getJpaBasicsDao() 而不是 getDao()
        return getJpaBasicsDao().findByLoginName(loginName);
    }

    @Override
    public List<Customer> findActiveCustomers() {
        return findList("status", 1, SQLOperator.EQ);
    }
}
```

**核心要点**：
- 继承 `J2ServiceImpl<CustomerDao, Customer, Long>`（三个泛型参数）
- 构造函数调用 `super(Customer.class)`
- 使用 `@Service` 注解
- DAO 会通过框架自动注入，无需手动注入

---

## ⚠️ 重要：DAO 访问规范

### 使用 getJpaBasicsDao() 而非 getDao()

在 ServiceImpl 中访问 DAO 时，**必须使用 `getJpaBasicsDao()` 方法**：

```java
// ✅ 正确：使用 getJpaBasicsDao()
@Override
public Optional<Account> findByLoginName(String loginName) {
    return getJpaBasicsDao().findByLoginName(loginName);
}

@Override
public Optional<Account> findById(Long id) {
    return getJpaBasicsDao().findById(id);
}

@Override
public Account save(Account account) {
    return getJpaBasicsDao().save(account);
}

// ❌ 错误：没有 getDao() 方法
// return getDao().findById(id);  // 编译错误！
```

### ServiceImpl 中调用其他 DAO

**重要规范**：ServiceImpl 中**不允许调用其他 Service**，只能注入和使用其他 DAO。

```java
@Service
public class AccountServiceImpl extends J2ServiceImpl<AccountDao, Account, Long>
    implements AccountService {

    // ✅ 正确：注入其他 DAO
    private final RoleAccountDao roleAccountDao;
    private final AccountSensitiveDao accountSensitiveDao;
    private final AccountLoginPlatformDao accountLoginPlatformDao;

    // 构造函数注入
    public AccountServiceImpl(RoleAccountDao roleAccountDao,
                             AccountSensitiveDao accountSensitiveDao,
                             AccountLoginPlatformDao accountLoginPlatformDao) {
        super(Account.class);
        this.roleAccountDao = roleAccountDao;
        this.accountSensitiveDao = accountSensitiveDao;
        this.accountLoginPlatformDao = accountLoginPlatformDao;
    }

    @Override
    public void updateEmail(String userId, String email) {
        // ✅ 正确：直接使用其他 DAO
        AccountSensitive sensitive = accountSensitiveDao.findByUserId(userId)
            .orElseGet(() -> {
                AccountSensitive newSensitive = new AccountSensitive();
                newSensitive.setUserId(userId);
                return newSensitive;
            });

        // 验证邮箱是否被其他用户使用
        accountSensitiveDao.findByEmail(email)
            .ifPresent(entity -> {
                if (!entity.getUserId().equals(userId)) {
                    throw new UserException("邮箱已被其他用户使用");
                }
            });

        sensitive.setEmail(email);
        accountSensitiveDao.save(sensitive);
    }
}
```

```java
// ❌ 错误示例：不要在 ServiceImpl 中注入其他 Service
@Service
public class AccountServiceImpl extends J2ServiceImpl<AccountDao, Account, Long> {

    // ❌ 错误：不要注入其他 Service
    private final RoleService roleService;  // 禁止！
    private final OrgService orgService;    // 禁止！

    // ❌ 错误：ServiceImpl 中调用其他 Service
    public void someMethod() {
        roleService.findById(roleId);  // 禁止！应该使用 RoleDao
    }
}
```

**为什么这样设计？**
- ✅ 避免 Service 层循环依赖
- ✅ 保持 Service 层的清晰职责
- ✅ DAO 层直接操作数据，性能更好
- ✅ 简化依赖关系，降低复杂度

---

## 框架提供的基础方法

继承 `J2Service` 后，自动拥有以下方法：

### 查询方法

```java
// 查询单个（等值条件）
Optional<Customer> findOnly(String fieldName, Object value);

// 查询单个（两个等值条件）
Optional<Customer> findOnly(String fieldName, Object value, String fieldName2, Object value2);

// 查询单个（自定义条件）
Optional<Customer> findOnly(Specification<Customer> spec);

// 查询所有
List<Customer> finds();

// 查询所有（带排序）
List<Customer> finds(Sorteds sort);

// 条件查询列表
List<Customer> finds(String fieldName, SQLOperator operator, Object... value);

// 条件查询列表（带排序）
List<Customer> finds(String fieldName, SQLOperator operator, Sorteds sort, Object... value);

// 自定义条件查询列表（带排序）
List<Customer> finds(Specification<Customer> spec, Sorteds sort);

// 异体Entity查询（使用注解）
<T> List<Customer> finds(T req);

// 异体Entity查询（使用注解，带排序）
<T> List<Customer> finds(T req, Sorteds sort);

// 分页查询（无条件）
Page<Customer> findPage(Pagings pageable);
Page<Customer> findPage(PagingSorteds pageable);

// 分页查询（使用注解）
<T> Page<Customer> findPage(T req, Pagings pageable);
<T> Page<Customer> findPage(T req, PagingSorteds pageable);
<T> Page<Customer> findPage(T req, Pagings pageable, Sorteds sort);

// 分页查询（自定义条件）
Page<Customer> findPage(Specification<Customer> spec, Pageable pageable);

// FluentQuery 查询（灵活查询）
<S extends Customer, C> C findBy(Specification<Customer> spec,
    Function<FluentQuery.FetchableFluentQuery<S>, C> queryFunction);
```

### 保存方法

```java
// 保存单个
Customer saveOne(Customer entity);

// 批量保存
List<Customer> saves(List<Customer> entities);

// 通过 VO 保存（自动转换为 Entity）
<V> Customer saveOneByVo(V bean);
```

### 更新方法

```java
// 更新（根据指定字段匹配）
<T> Boolean update(T bean, SQLOperator operator, String... uniqueKey);

// 示例：根据 id 更新
customerService.update(customer, SQLOperator.EQ, "id");
```

### 删除方法

```java
// 等值删除
int deleteEq(String fieldName, Object value);

// 条件删除
int delete(String fieldName, SQLOperator operator, Object... value);

// 自定义条件删除
int delete(Specification<Customer> spec);

// 使用注解删除
<T> int delete(T wheres);
```

### 其他方法

```java
// 获取 DAO
<ID, R extends JpaBasicsRepository<Customer, ID>> R getJpaBasicsDao();

// 获取 EntityManager
EntityManager getEntityManager();
```

**重要说明**：
- 所有这些方法都可以直接在 Controller 中通过注入的 Service 调用
- 例如：`customerService.findOnly("loginName", "zhangsan")`
- 这些方法内部都是通过 DAO 实现的，框架已经封装好了

查看完整 API：https://github.com/en-o/Jdevelops

---

## 自定义方法示例

### 直接使用继承的方法

**在 Controller 中直接调用**（推荐）：

```java
@PathRestController("user")
public class CustomerController {
    private final CustomerService customerService;

    @GetMapping("detail")
    public ResultVO<Customer> detail(@RequestParam String loginName) {
        // 直接调用 Service 继承的方法
        Optional<Customer> customer = customerService.findOnly("loginName", loginName);
        return ResultVO.success(customer.orElse(null));
    }

    @GetMapping("list")
    public ResultVO<List<Customer>> list(@RequestParam Integer status) {
        // 直接调用 Service 继承的方法
        List<Customer> customers = customerService.finds("status", SQLOperator.EQ, status);
        return ResultVO.success(customers);
    }
}
```

### 需要自定义业务逻辑时

当需要添加业务逻辑时，在 ServiceImpl 中实现。

#### 方式1：使用继承的方法

```java
// Service 接口
public interface CustomerService extends J2Service<Customer> {
    Optional<Customer> findByLoginName(String loginName);
}

// ServiceImpl 实现
@Service
public class CustomerServiceImpl extends J2ServiceImpl<CustomerDao, Customer, Long>
    implements CustomerService {

    public CustomerServiceImpl() {
        super(Customer.class);
    }

    @Override
    public Optional<Customer> findByLoginName(String loginName) {
        // 调用继承的方法
        return this.findOnly("loginName", loginName);
    }
}
```

#### 方式2：通过 DAO 实现（推荐）

**复杂查询应该在 DAO 中定义方法**：

```java
// DAO 接口
public interface CustomerDao extends JpaRepository<Customer, Long> {
    // 自定义查询方法（JPA 方法命名规范）
    Optional<Customer> findByLoginName(String loginName);

    List<Customer> findByStatusAndDeletedFalse(Integer status);

    Page<Customer> findByLoginNameContainingOrUserNameContaining(
        String loginName, String userName, Pageable pageable);

    // 使用 @Query 注解自定义 SQL
    @Query("SELECT c FROM Customer c WHERE c.status = :status AND c.deleted = false")
    List<Customer> findActiveCustomers(@Param("status") Integer status);
}

// ServiceImpl 实现
@Service
public class CustomerServiceImpl extends J2ServiceImpl<CustomerDao, Customer, Long>
    implements CustomerService {

    public CustomerServiceImpl() {
        super(Customer.class);
    }

    @Override
    public Optional<Customer> findByLoginName(String loginName) {
        // 通过 getJpaBasicsDao() 获取 DAO
        return getJpaBasicsDao().findByLoginName(loginName);
    }

    @Override
    public List<Customer> findActiveCustomers() {
        // 调用 DAO 的自定义方法
        return getJpaBasicsDao().findByStatusAndDeletedFalse(1);
    }

    @Override
    public Page<Customer> searchCustomers(String keyword, Pageable pageable) {
        // 调用 DAO 的复杂查询方法
        return getJpaBasicsDao().findByLoginNameContainingOrUserNameContaining(
            keyword, keyword, pageable);
    }
}
```

### 使用 DAO 的复杂查询

```java
@Override
public Page<Customer> searchCustomers(String keyword, Pageable pageable) {
    return getJpaBasicsDao().findByLoginNameContainingOrUserNameContaining(
        keyword, keyword, pageable);
}
```

### 业务逻辑处理

```java
@Override
@Transactional(rollbackFor = Exception.class)
public void registerCustomer(UserAdd add) {
    // 1. 检查用户名是否存在（调用继承的方法）
    Optional<Customer> existing = this.findOnly("loginName", add.getLoginName());
    if (existing.isPresent()) {
        throw new BusinessException("用户名已存在");
    }

    // 2. 转换对象
    Customer customer = SerializableBean.to2(add, Customer.class);

    // 3. 密码加密
    customer.setPassword(PasswordUtil.encode(add.getPassword()));
    customer.setStatus(1);

    // 4. 保存（调用继承的方法）
    this.saveOne(customer);

    // 5. 其他业务逻辑
    sendWelcomeEmail(customer);
}

private void sendWelcomeEmail(Customer customer) {
    // 邮件发送逻辑
}
```

### 方法选择建议

| 场景 | 推荐方式 | 说明 |
|------|---------|------|
| 简单查询，无业务逻辑 | Controller 直接调用 | `customerService.findOnly()` |
| 需要添加业务逻辑 | ServiceImpl 中实现 | 可调用继承的方法 |
| 复杂查询 | DAO 中定义方法 | JPA 方法命名或 @Query |
| 多表关联查询 | DAO 中使用 @Query | 自定义 JPQL 或 SQL |
| 需要事务控制 | ServiceImpl 中实现 | 添加 @Transactional |

### 分页查询示例

#### 模式1：使用 @JpaSelectOperator 注解（自动查询）

**在 Controller 中直接调用**（推荐）：

```java
@PostMapping("page")
@Operation(summary = "分页查询")
public ResultPageVO<LogEsInitData, JpaPageResult<LogEsInitData>> page(
    @RequestBody @Valid LogEsInitDataPage page) {
    // 直接调用 Service 继承的方法，框架根据注解自动构建查询
    Page<LogEsInitData> result = logEsInitDataService.findPage(page, page.getPage());
    JpaPageResult<LogEsInitData> pageResult = JpaPageResult.toPage(result);
    return ResultPageVO.success(pageResult, "查询成功");
}
```

**或在 ServiceImpl 中封装**：

```java
@Service
public class LogEsInitDataServiceImpl extends J2ServiceImpl<LogEsInitDataDao, LogEsInitData, Long>
    implements LogEsInitDataService {

    public LogEsInitDataServiceImpl() {
        super(LogEsInitData.class);
    }

    @Override
    public Page<LogEsInitData> queryPage(LogEsInitDataPage page) {
        // 调用继承的方法
        return this.findPage(page, page.getPage());
    }
}
```

#### 模式2：使用自定义 Specification（手动查询）

**在 ServiceImpl 中实现**：

```java
@Service
public class ResourceUseLogServiceImpl extends J2ServiceImpl<ResourceUseLogDao, ResourceUseLog, Long>
    implements ResourceUseLogService {

    public ResourceUseLogServiceImpl() {
        super(ResourceUseLog.class);
    }

    @Override
    public Page<ResourceUseLog> queryPage(ResourceUseLogPage page, Long userId, Integer status) {
        // 使用 Specification 构建复杂查询条件
        Specification<ResourceUseLog> spec = LogSpecQuery.logUserResourceSpec(page, userId, status);
        // 调用继承的方法
        return this.findPage(spec, page.getPage());
    }
}
```

**在 Controller 中调用**：

```java
@PostMapping("page")
@Operation(summary = "分页查询资源日志")
public ResultPageVO<ResourceUseLog, JpaPageResult<ResourceUseLog>> page(
    @RequestBody @Valid ResourceUseLogPage page,
    HttpServletRequest request) {
    Long userId = getUserId(request);
    // 调用 Service 的自定义方法
    Page<ResourceUseLog> result = resourceUseLogService.queryPage(page, userId, 1);
    JpaPageResult<ResourceUseLog> pageResult = JpaPageResult.toPage(result);
    return ResultPageVO.success(pageResult, "查询成功");
}
```

**两种模式的选择**：
- **模式1**：查询条件简单（等值、模糊、区间等），直接在 Controller 中调用 `service.findPage(page, page.getPage())`
- **模式2**：查询条件复杂（需要函数处理、多表关联、动态组合），在 ServiceImpl 中实现并使用 `Specification`

---

## 事务控制

```java
@Override
@Transactional
public void batchUpdate(List<Customer> customers) {
    // 批量更新操作
    customers.forEach(customer -> {
        update(customer, SQLOperator.EQ, "id");
    });
}

@Override
@Transactional(rollbackFor = Exception.class)
public void complexOperation() {
    // 复杂业务逻辑，任何异常都回滚
}
```

---

## 完整检查清单

- [ ] Service 接口继承 `J2Service<Entity>`
- [ ] Service 实现继承 `J2ServiceImpl<DAO, Entity, ID>`（三个泛型参数）
- [ ] Service 实现的构造函数调用 `super(Entity.class)`
- [ ] Service 实现使用 `@Service` 注解
- [ ] 不需要手动注入 DAO（框架自动注入）
- [ ] 方法命名遵循规范（findByXxx、saveXxx、updateXxx）
- [ ] 优先使用框架提供的基础方法
- [ ] 复杂查询通过 DAO 实现
- [ ] 需要事务的方法添加 `@Transactional(rollbackFor = Exception.class)`

---

## 参考资源

- 架构规范：[../standards/architecture.md](../standards/architecture.md)
- 框架源码：https://github.com/en-o/Jdevelops
- 官方文档：https://www.yuque.com/tanning/yg9ipo
