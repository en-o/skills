# Service 层代码生成指南

## 快速参考

Service 接口继承 `J2Service<Entity>`，Service 实现继承 `J2ServiceImpl<Entity>`。

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
@RequiredArgsConstructor
public class CustomerServiceImpl extends J2ServiceImpl<Customer>
    implements CustomerService {

    private final CustomerDao customerDao;

    @Override
    public Optional<Customer> findByLoginName(String loginName) {
        return findOne("loginName", loginName, SQLOperator.EQ);
    }

    @Override
    public List<Customer> findActiveCustomers() {
        return findList("status", 1, SQLOperator.EQ);
    }
}
```

---

## 框架提供的基础方法

继承 `J2Service` 后，自动拥有以下方法：

### 查询方法

```java
// 根据ID查询
Optional<Customer> findById(Long id);

// 条件查询单个
Optional<Customer> findOne(String field, Object value, SQLOperator operator);

// 条件查询列表
List<Customer> findList(String field, Object value, SQLOperator operator);

// 分页查询
Page<Customer> findPage(PageQuery query, Pageable pageable);

// 查询所有
List<Customer> findAll();
```

### 保存方法

```java
// 保存单个
Customer save(Customer entity);

// 批量保存
List<Customer> saveAll(List<Customer> entities);
```

### 更新方法

```java
// 更新（根据指定字段匹配）
void update(Customer entity, SQLOperator operator, String... fields);

// 示例
customerService.update(customer, SQLOperator.EQ, "id");
```

### 删除方法

```java
// 根据ID删除
void deleteById(Long id);

// 批量删除
void deleteAllById(List<Long> ids);
```

### 判断方法

```java
// 判断是否存在
boolean existsById(Long id);
```

查看完整 API：https://github.com/en-o/Jdevelops

---

## 自定义方法示例

### 简单查询

```java
@Override
public Optional<Customer> findByLoginName(String loginName) {
    return findOne("loginName", loginName, SQLOperator.EQ);
}

@Override
public List<Customer> findByStatus(Integer status) {
    return findList("status", status, SQLOperator.EQ);
}
```

### 复杂查询

```java
@Override
public List<Customer> findActiveCustomers() {
    // 使用 DAO 进行复杂查询
    return customerDao.findByStatusAndDeletedFalse(1);
}

@Override
public Page<Customer> searchCustomers(String keyword, Pageable pageable) {
    return customerDao.findByLoginNameContainingOrUserNameContaining(
        keyword, keyword, pageable);
}
```

### 业务逻辑处理

```java
@Override
@Transactional
public void registerCustomer(UserAdd add) {
    // 1. 检查用户名是否存在
    if (findByLoginName(add.getLoginName()).isPresent()) {
        throw new BusinessException("用户名已存在");
    }

    // 2. 转换对象
    Customer customer = SerializableBean.to2(add, Customer.class);

    // 3. 密码加密
    customer.setPassword(PasswordUtil.encode(add.getPassword()));
    customer.setStatus(1);

    // 4. 保存
    save(customer);

    // 5. 其他业务逻辑（如发送邮件）
    sendWelcomeEmail(customer);
}
```

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
- [ ] Service 实现继承 `J2ServiceImpl<Entity>`
- [ ] Service 实现使用 `@Service` 注解
- [ ] 使用构造器注入 DAO
- [ ] 方法命名遵循规范（findByXxx、saveXxx、updateXxx）
- [ ] 优先使用框架提供的基础方法
- [ ] 复杂查询通过 DAO 实现
- [ ] 需要事务的方法添加 `@Transactional`

---

## 参考资源

- 架构规范：[../standards/architecture.md](../standards/architecture.md)
- 框架源码：https://github.com/en-o/Jdevelops
- 官方文档：https://www.yuque.com/tanning/yg9ipo
