# 新增业务模块工作流

## 🎯 开始之前

**重要**：在开始添加模块前，必须完成需求分析和确认流程。参考 [SKILL.md - 需求分析和确认流程](../SKILL.md#需求分析和确认流程首要步骤)

## 工作流清单

复制此清单并跟踪进度：

```
模块创建进度：
- [ ] 步骤0：需求分析和确认（首要步骤）
- [ ] 步骤1：分析需求（确定模块名、功能、字段）
- [ ] 步骤2：查阅参考资料（确认 API 和包路径）
- [ ] 步骤3：创建 Entity 类
- [ ] 步骤4：创建 DAO 接口
- [ ] 步骤5：创建 Service 接口和实现
- [ ] 步骤6：创建 Controller 和请求/响应类
- [ ] 步骤7：验证代码规范
```

---

## 步骤0：需求分析和确认（首要步骤）

### ⚠️ 必须首先完成需求分析

**在开始任何代码生成前，必须通过需求分析和确认流程**：

### 需求收集

**引导用户描述需求**：
- "请详细描述您要添加的模块：功能、字段、业务逻辑等"
- 鼓励用户提供尽可能多的细节

**示例用户输入**：
```
"我需要添加一个商品管理模块，包含：
1. 商品基本信息管理（名称、分类、价格、库存）
2. 商品上下架功能
3. 商品图片管理（支持多图）
4. 商品规格管理（颜色、尺寸等）
5. 商品搜索（支持按名称、分类、价格区间搜索）
6. 库存预警功能"
```

### 需求总结提炼

根据用户描述，进行结构化总结：

```markdown
【需求总结】

## 模块概述
模块名称：商品管理模块（Product）
业务领域：商品管理

## 核心功能
1. 商品信息管理
   - 新增商品
   - 编辑商品
   - 删除商品
   - 查询商品详情

2. 商品状态管理
   - 商品上架
   - 商品下架
   - 状态查询

3. 商品图片管理
   - 上传商品图片（多图）
   - 删除图片
   - 设置主图

4. 商品规格管理
   - 添加规格（颜色、尺寸）
   - 规格库存管理
   - 规格价格管理

5. 商品搜索
   - 按名称搜索
   - 按分类筛选
   - 价格区间筛选
   - 分页查询

6. 库存预警
   - 设置预警阈值
   - 库存不足提醒

## 数据模型设计

### Product（商品表）
- id: Long（主键）
- productName: String（商品名称）
- categoryId: Long（分类ID）
- price: BigDecimal（价格）
- stock: Integer（库存）
- status: Integer（状态：0-下架，1-上架）
- description: String（描述）
- mainImage: String（主图）
- lowStockThreshold: Integer（库存预警阈值）
- 继承 JpaCommonBean（创建时间、修改时间等）

### ProductImage（商品图片表）
- id: Long
- productId: Long（关联商品）
- imageUrl: String（图片URL）
- sortOrder: Integer（排序）
- isMain: Boolean（是否主图）

### ProductSpec（商品规格表）
- id: Long
- productId: Long
- specName: String（规格名：颜色/尺寸）
- specValue: String（规格值：红色/L）
- price: BigDecimal（规格价格）
- stock: Integer（规格库存）

## 接口定义

### ProductController（/product）
- POST /product/add - 新增商品
- PUT /product/update - 更新商品
- DELETE /product/delete/{id} - 删除商品
- GET /product/detail/{id} - 商品详情
- GET /product/list - 商品列表（分页）
- PUT /product/status/{id} - 上下架
- POST /product/search - 搜索商品（分页）
- GET /product/low-stock - 库存预警列表

### ProductImageController（/product/image）
- POST /product/image/upload - 上传图片
- DELETE /product/image/delete/{id} - 删除图片
- PUT /product/image/main/{id} - 设置主图

### ProductSpecController（/product/spec）
- POST /product/spec/add - 添加规格
- PUT /product/spec/update - 更新规格
- DELETE /product/spec/delete/{id} - 删除规格
- GET /product/spec/list/{productId} - 规格列表

## 请求/响应类

### 请求类（dto）
- ProductAdd（新增商品）
- ProductEdit（编辑商品）
- ProductSearch（搜索条件）
- ProductImageAdd（图片上传）
- ProductSpecAdd（规格添加）

### 响应类（vo）
- ProductInfo（商品详情，包含图片和规格）
- 或直接返回 Product Entity（如不需要脱敏）

## 技术要点
- 商品图片：需要 jdevelops-files-sdk 组件
- 搜索功能：使用 @JpaSelectOperator 注解或自定义 Specification
- 库存预警：可使用定时任务或实时检查
```

### 确认需求

**询问用户**：
```
"以上是我对您需求的总结。请问：
1. 需求总结是否准确？
2. 功能点是否完整？
3. 数据模型设计是否合理？
4. 是否满意此需求总结？"
```

### 迭代优化（如果不满意）

**如果用户不满意**：
```
用户: "基本满意，但我还需要添加商品评价功能和收藏功能"

AI: "好的，我来更新需求总结：

【需求总结（更新版）】
... （保留原有内容）

7. 商品评价功能  ← 新增
   - 用户评价
   - 评分（1-5星）
   - 评价列表

8. 商品收藏功能  ← 新增
   - 添加收藏
   - 取消收藏
   - 我的收藏列表

## 数据模型设计（更新）
新增：
  - ProductReview（商品评价表）
    - id, productId, userId, rating, content, createTime
  - ProductFavorite（商品收藏表）
    - id, productId, userId, createTime

## 接口定义（更新）
新增：
  - POST /product/review/add - 添加评价
  - GET /product/review/list/{productId} - 评价列表
  - POST /product/favorite/add - 添加收藏
  - DELETE /product/favorite/remove/{productId} - 取消收藏
  - GET /product/favorite/my - 我的收藏

请问现在是否满意？"
```

**继续询问直到用户满意**。

### 制定开发计划

**需求确认后，制定详细的开发计划**：

**⚠️ 重要：在制定开发计划前，必须完成 Entity 字段设计确认**

参考：[requirement-analysis.md - 步骤 6.5: Entity 字段设计确认](./requirement-analysis.md#步骤-65-entity-字段设计确认重要)

对每个 Entity 进行详细的字段设计确认：
- 展示完整的字段清单（字段名、类型、长度、约束）
- 询问用户是否满意
- 支持新增、删除、修改字段
- 迭代直到用户对所有 Entity 的字段设计都满意

**Entity 字段确认完成后，再制定开发计划**：

```markdown
【开发计划】

## 阶段 1: 项目准备
✓ 步骤 1.1: 确认项目路径
✓ 步骤 1.2: 检查是否需要添加文件上传组件（jdevelops-files-sdk）

## 阶段 2: 核心数据模型
✓ 步骤 2.1: 创建 Product Entity
  - 字段：productName, categoryId, price, stock, status...
  - 继承 JpaCommonBean
  - 添加注解：@Entity, @Table, @Comment, @Schema

✓ 步骤 2.2: 创建 ProductDao 接口
  - 继承 JpaRepository<Product, Long>
  - 自定义查询方法（如需要）

✓ 步骤 2.3: 创建 ProductService 和实现
  - 继承 J2Service<Product>
  - 实现基础 CRUD
  - 实现业务方法（上下架、库存预警）

## 阶段 3: 关联数据模型
✓ 步骤 3.1: 创建 ProductImage Entity + Dao + Service
✓ 步骤 3.2: 创建 ProductSpec Entity + Dao + Service
✓ 步骤 3.3: 创建 ProductReview Entity + Dao + Service
✓ 步骤 3.4: 创建 ProductFavorite Entity + Dao + Service

## 阶段 4: 请求/响应类
✓ 步骤 4.1: 创建请求类（dto）
  - ProductAdd, ProductEdit, ProductSearch
  - ProductImageAdd, ProductSpecAdd
  - ProductReviewAdd

✓ 步骤 4.2: 创建响应类（vo，如需要）
  - ProductInfo（包含图片、规格、评价统计）

## 阶段 5: Controller 接口
✓ 步骤 5.1: 创建 ProductController
  - 基础 CRUD 接口
  - 搜索接口
  - 上下架接口
  - 库存预警接口

✓ 步骤 5.2: 创建 ProductImageController
✓ 步骤 5.3: 创建 ProductSpecController
✓ 步骤 5.4: 创建 ProductReviewController
✓ 步骤 5.5: 创建 ProductFavoriteController

## 阶段 6: 验证
✓ 步骤 6.1: 验证代码规范
✓ 步骤 6.2: 测试基础功能
✓ 步骤 6.3: 验证 API 文档

确认开始执行？
```

### 获得确认后开始执行

用户确认后，进入步骤1开始执行。

---

## 步骤1：分析需求

### ⚠️ 交互式询问

**如果用户未提供以下信息，必须进行询问**：

#### 0. 项目路径确认（优先级最高）

**在开始任何代码生成前，必须首先确认项目路径**：

- **询问**: 是否是当前目录下的项目？
  - 当前工作目录：`/mnt/c/work/tan/code/skills/Java开发基础组件使用助手`

- **选项**:
  - **选项 A**: 是，当前目录就是项目根目录
    - 验证：检查当前目录是否包含 `pom.xml` 或 `build.gradle`
    - 验证：检查是否为 Spring Boot 项目

  - **选项 B**: 否，项目在其他位置
    - **继续询问**: 请提供项目的完整路径
    - **示例**:
      - Linux/Mac: `/home/user/projects/my-project`
      - Windows: `C:\work\tan\code\my-project`
      - 相对路径: `../my-project`

**路径验证**:
1. 检查路径是否存在
2. 检查是否有写入权限
3. 验证是否为 Spring Boot 项目：
   - 检查 `pom.xml` 或 `build.gradle` 文件
   - 检查 `src/main/java` 目录
4. 如果验证失败，提示用户并重新询问路径

**⚠️ 重要：自动检测项目框架**

路径确认后，**必须**读取 `pom.xml` 文件，检测项目使用的框架：

```bash
# 读取 pom.xml
cat pom.xml
```

**检测规则**：
1. **检查是否使用 JDevelops 框架**：
   - 查找依赖：`<groupId>cn.tannn.jdevelops</groupId>`
   - 查找组件：`jdevelops-spring-boot-starter`、`jdevelops-dals-jpa` 等

2. **如果找到 JDevelops 依赖**：
   ```
   "检测到项目使用 JDevelops 框架！

   【项目信息】
   - 框架：JDevelops
   - JDevelops 版本：{version}
   - 已安装组件：
     - jdevelops-spring-boot-starter
     - jdevelops-dals-jpa
     - jdevelops-apis-exception
     - ...

   将按照 JDevelops 框架规范生成代码：
   ✓ Entity 继承 JpaCommonBean
   ✓ Service 继承 J2Service
   ✓ Controller 使用 @PathRestController
   ✓ 统一返回格式 ResultVO
   "
   ```

3. **如果未找到 JDevelops 依赖**：
   ```
   "检测到项目为纯 Spring Boot 项目！

   【项目信息】
   - 框架：Spring Boot
   - Spring Boot 版本：{version}
   - JPA：Spring Data JPA

   将按照标准 Spring Boot 规范生成代码：
   ✓ Entity 使用标准 JPA 注解
   ✓ Repository 继承 JpaRepository
   ✓ Service 自定义接口
   ✓ Controller 使用 @RestController
   "
   ```

4. **记录框架类型供后续使用**：
   - 设置标记：`framework_type = "jdevelops"` 或 `"spring-boot"`
   - 后续代码生成根据此标记选择不同的模板和规范

**检测示例**：

```xml
<!-- 如果 pom.xml 包含这样的依赖 -->
<dependencies>
    <dependency>
        <groupId>cn.tannn.jdevelops</groupId>
        <artifactId>jdevelops-spring-boot-starter</artifactId>
        <version>1.0.3</version>
    </dependency>
    ...
</dependencies>

→ 判定为 JDevelops 框架项目
```

```xml
<!-- 如果 pom.xml 只包含标准 Spring 依赖 -->
<dependencies>
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-data-jpa</artifactId>
    </dependency>
    ...
</dependencies>

→ 判定为纯 Spring Boot 项目
```

**确认后的操作**:
- 记录项目根路径
- 记录框架类型（JDevelops 或 Spring Boot）
- 读取 `pom.xml` 或 `build.gradle` 确认项目信息
- 检查现有包结构，确定是否为首次添加模块
- 后续代码生成使用对应的规范和模板

#### 1. 项目描述和业务场景

如果用户未提供项目背景，必须先询问：
- **询问**: 请描述您的项目是做什么的？有哪些主要功能模块？
- **说明**: 了解项目整体情况，帮助规划模块结构
- **示例回答**:
  - "这是一个管理后台系统，需要基础的用户、字典、角色、权限、菜单等功能"
  - "这是一个电商平台，需要商品管理、订单管理、用户管理等模块"
  - "这是一个内容管理系统，需要文章、分类、标签、评论等功能"

#### 2. 包结构选择

**⚠️ 如果是首次添加业务模块，必须询问包结构偏好**

参考详细文档：[../reference/package-structure.md](../reference/package-structure.md)

**同时参考需求分析流程中的包结构选择步骤**：[./requirement-analysis.md - 步骤 3.5](./requirement-analysis.md#步骤-35-包结构选择重要)

如果是首次添加业务模块，需要询问包结构偏好：
- **询问**: 请选择您希望使用的包结构
- **选项**:

  - **选项 A - 传统三层架构（推荐小型项目）**:
    ```
    src/main/java/{basePackage}/
    ├── controller/{domain}/     # 控制器层（按业务域划分）
    │   ├── dto/                # 请求类
    │   └── vo/                 # 响应类
    ├── entity/                 # 实体层（所有实体集中）
    ├── dao/                    # DAO 层（所有 DAO 集中）
    ├── service/                # Service 接口层
    └── service/impl/           # Service 实现层
    ```
    - **优点**: 结构清晰、易于定位、适合中小型项目
    - **适用**: < 50 个实体的项目

  - **选项 B - 垂直切分（推荐中型项目）**:
    ```
    src/main/java/{basePackage}/
    ├── controller/{domain}/     # 控制器层（按业务域划分）
    │   ├── dto/
    │   └── vo/
    └── {module}/               # 业务模块（按功能垂直拆分）
        ├── entity/            # 模块内所有实体
        ├── dao/               # 模块内所有 DAO
        ├── service/           # 模块内所有 Service 接口
        └── service/impl/      # 模块内所有 Service 实现
    ```
    - **优点**: 模块独立、易于拆分微服务、适合大型项目
    - **适用**: 50-100 个实体，模块独立性强

  - **选项 C - 标准目录结构（推荐大型项目）**:
    ```
    src/main/java/{basePackage}/
    ├── controller/{domain}/     # 控制器层（统一管理）
    │   ├── dto/
    │   └── vo/
    ├── common/                 # 公共组件层
    ├── core/                   # 核心配置层
    └── modules/                # 业务模块层
        └── {module}/          # 大模块
            └── {submodule}/   # 子模块
                ├── entity/
                ├── dao/
                ├── service/
                └── service/impl/
    ```
    - **优点**: 高度模块化、支持大型项目、便于团队分工
    - **适用**: > 100 个实体，多团队协作，复杂业务场景

- **说明**:
  - 如果项目已有代码，则沿用现有结构
  - 新项目推荐根据项目规模选择：
    - 小型项目（< 50 实体）→ 传统三层架构（选项 A）
    - 中型项目（50-100 实体）→ 垂直切分（选项 B）
    - 大型项目（> 100 实体）→ 标准目录结构（选项 C）
  - 详细说明请参考 [../reference/package-structure.md](../reference/package-structure.md)

#### 3. 数据库结构提供方式

询问用户如何提供数据表结构：
- **询问**: 请选择如何定义数据表结构
- **选项**:
  - **选项 A**: 我已有数据库表结构（DDL 或表结构截图），请根据它生成 Entity
  - **选项 B**: 我提供字段清单，请帮我生成 Entity
  - **选项 C**: 我口头描述需求，请你设计数据表并生成 Entity
  - **选项 D**: 我自己已经写好了 Entity，跳过这步

- **说明**:
  - 选项 A 和 B：请在后续消息中提供表结构或字段清单
  - 选项 C：AI 将根据业务需求设计合理的数据表结构
  - 选项 D：直接进入 Service 和 Controller 创建

#### 4. 模块基本信息

明确以下信息：

**模块命名**：
- **选项 A（传统三层架构）**：
  - 作为类名前缀（如 Customer → CustomerDao、CustomerService）

- **选项 B（垂直切分）**：
  - 作为模块包名（如 `{basePackage}.customer`）
  - 模块内所有类都在该包下（customer.entity、customer.dao、customer.service）

- **选项 C（标准目录结构）**：
  - **大模块名**：业务领域（如 account、biz、file、logs）
  - **子模块名**：具体功能（如 account.suser、account.role、account.org）
  - 路径格式：`{basePackage}.modules.{module}.{submodule}`

**业务领域**（Controller 路径）：
- 用于：决定 Controller 所在包（controller.user、controller.sys、controller.logs）
- 无论采用哪种包结构，Controller 都统一按业务域划分

**核心字段**：
- 哪些字段必需
- 哪些字段敏感（密码、token 等）
- 哪些字段需要脱敏

**是否需要脱敏**：
- 决定是否创建单独的响应类（VO）

### 决策树：是否需要创建响应类？

```
需要返回数据？
  ├─ 包含敏感字段（密码、token）？
  │   ├─ 是 → 使用 @JsonIgnore 或创建单独响应类
  │   └─ 否 → 继续判断
  └─ 需要按场景控制可见性？
      ├─ 是 → 使用 @JsonView 定义视图
      └─ 否 → 直接返回 Entity
```

### 信息确认

在开始生成代码前，确认以下信息：
- [ ] **项目路径已确认并验证**（当前目录或指定路径）
- [ ] 项目描述和业务场景已明确
- [ ] 包结构选择已确定（A/B/C）
- [ ] 数据表结构提供方式已确定
- [ ] 模块命名已明确
  - 选项 A/B：模块名（如 customer、order）
  - 选项 C：大模块名和子模块名（如 account.suser）
- [ ] 业务领域已明确（Controller 路径）
- [ ] 核心字段需求已明确

---

## 步骤2：查阅参考资料

**关键：确认包路径和 API**

### 查阅顺序

1. **查官方文档**：https://www.yuque.com/tanning/yg9ipo
   - 查找 Entity 基类（JpaCommonBean、JpaCommonBean2）
   - 查找 Service 基类（J2Service、J2ServiceImpl）
   - 查找注解用法（@PathRestController、@ApiMapping）

2. **文档找不到** → 查 GitHub 源码：https://github.com/en-o/Jdevelops
   - 查看最新方法签名
   - 确认包路径

3. **下载文档到本地**（可选）：
   ```bash
   bash scripts/download-docs.sh
   ```

详细策略：[../reference/lookup-strategy.md](../reference/lookup-strategy.md)

---

## 步骤3：创建 Entity 类

查阅详细指南：[../guides/entity.md](../guides/entity.md)

### 快速检查清单

- [ ] 继承 `JpaCommonBean` 或 `JpaCommonBean2`
- [ ] 使用 `@Getter @Setter`（**禁止** @Data）
- [ ] 使用 `@Entity @Table` 注解
- [ ] Long 类型添加 `@JsonSerialize(using = ToStringSerializer.class)`
- [ ] 敏感字段添加 `@JsonIgnore` 或 `@JsonView`
- [ ] 使用 `@Column` 指定字段属性（columnDefinition、nullable 等）
- [ ] 使用 `@Comment` 添加注释
- [ ] 使用 `@Schema` 添加 Swagger 文档

### 最小示例

```java
@Getter
@Setter
@Entity
@Table(name = "sys_customer")
@Comment("客户表")
public class Customer extends JpaCommonBean {

    @Column(name = "login_name", nullable = false, unique = true, length = 50)
    @Comment("登录名")
    @Schema(description = "登录名")
    private String loginName;

    @Column(name = "password", nullable = false)
    @Comment("密码")
    @JsonIgnore  // 敏感字段
    private String password;

    @Column(name = "role_id")
    @JsonSerialize(using = ToStringSerializer.class)
    private Long roleId;
}
```

---

## 步骤4：创建 DAO 接口

DAO 接口继承 `JpaRepository`，由框架自动实现。

```java
// {module}/dao/CustomerDao.java
public interface CustomerDao extends JpaRepository<Customer, Long> {
    // 自定义查询方法（可选）
    Optional<Customer> findByLoginName(String loginName);
}
```

---

## 步骤5：创建 Service 接口和实现

查阅详细指南：[../guides/service.md](../guides/service.md)

### Service 接口

```java
// {module}/service/CustomerService.java
public interface CustomerService extends J2Service<Customer> {
    Optional<Customer> findByLoginName(String loginName);
}
```

### Service 实现

```java
// {module}/service/impl/CustomerServiceImpl.java
@Service
public class CustomerServiceImpl extends J2ServiceImpl<CustomerDao, Customer, Long>
    implements CustomerService {

    public CustomerServiceImpl() {
        super(Customer.class);
    }

    @Override
    public Optional<Customer> findByLoginName(String loginName) {
        return findOne("loginName", loginName, SQLOperator.EQ);
    }
}
```

**关键点**：
- 继承 `J2ServiceImpl<DAO, Entity, ID>`（**三个泛型参数**：DAO接口、Entity实体、ID类型）
- 使用无参构造器调用 `super(Entity.class)`
- DAO会通过框架自动注入，**无需手动注入**

---

## 步骤6：创建 Controller 和请求/响应类

查阅详细指南：
- Controller：[../guides/controller.md](../guides/controller.md)
- 请求/响应类：[../guides/request-response.md](../guides/request-response.md)

### Controller 类

```java
@PathRestController("user")
@Tag(name = "用户管理", extensions = {@Extension(properties = {
    @ExtensionProperty(name = "x-order", value = "3", parseValue = true)})})
public class CustomerController {

    private final CustomerService customerService;

    public CustomerController(CustomerService customerService) {
        this.customerService = customerService;
    }

    @PostMapping("add")
    @Operation(summary = "新增用户")
    public ResultVO<String> add(@RequestBody @Valid UserAdd add) {
        // 业务逻辑
        return ResultVO.success("新增成功");
    }

    @GetMapping("detail")
    @Operation(summary = "用户详情")
    public ResultVO<Customer> detail(@RequestParam Long id) {
        Customer customer = customerService.findById(id).orElseThrow();
        return ResultVO.success(customer);
    }
}
```

### 请求类（dto/）

命名规范：**UserAdd、UserEdit、UserPage**（禁止 VO/DTO 后缀）

```java
// controller/user/dto/UserAdd.java
@Getter
@Setter
@ToString
public class UserAdd {
    @NotBlank(message = "登录名不能为空")
    private String loginName;

    @NotBlank(message = "密码不能为空")
    private String password;
}
```

### 响应类（vo/）

**优先直接返回 Entity**，仅在需要脱敏时创建：

```java
// controller/user/vo/UserInfo.java
@Getter
@Setter
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class UserInfo {
    private Long id;
    private String loginName;
    private String userName;
    // 不包含密码等敏感字段
}
```

---

## 步骤7：验证代码规范

运行完整的检查清单：[./modify-code.md](./modify-code.md)

### 快速验证命令

```bash
# 检查命名规范
grep -r "DTO\|VO" --include="*.java" . | grep "class.*\(DTO\|VO\)"

# 检查 @Data 注解
grep -r "@Data" --include="*.java" .

# 检查框架注解
grep -r "@PathRestController" --include="*.java" controller/
grep -r "extends J2Service" --include="*.java" {module}/service/
grep -r "extends JpaCommonBean" --include="*.java" {module}/entity/
```

### 必须验证的项目

- [ ] 包路径符合规范（controller.{domain} 或 {module}.{layer}）
- [ ] 继承了正确的框架基类
- [ ] 使用了框架注解（@PathRestController、@ApiMapping）
- [ ] 统一返回格式（ResultVO/ResultPageVO）
- [ ] 命名无 VO/DTO 后缀
- [ ] 禁用了 @Data
- [ ] 敏感字段使用了 @JsonIgnore 或 @JsonView
- [ ] Long 类型字段添加了 @JsonSerialize
- [ ] 添加了 Swagger 注解

---

## ✅ 完成标志

当以下所有项都完成时，模块创建完成：

- [ ] 代码符合 [../standards/](../standards/) 中的所有强制规范
- [ ] 通过检查清单验证
- [ ] 可以成功编译
- [ ] API 文档生成正确（Swagger UI）
- [ ] 基础功能测试通过

---

## 📚 相关参考

- 完整示例：[../examples/complete-module.md](../examples/complete-module.md)
- 架构规范：[../standards/architecture.md](../standards/architecture.md)
- 命名规范：[../standards/naming.md](../standards/naming.md)
- Lombok 规范：[../standards/lombok.md](../standards/lombok.md)
