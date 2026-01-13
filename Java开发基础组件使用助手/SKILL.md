---
name: Java开发基础组件使用助手
description: 该技能是用于开发java项目的基础依赖使用参考和说明，辅助更好的生成符合代码习惯的代码和风格
---

# Java开发基础组件使用助手

## 基础规则
- 必须使用 jdk17
- 必须使用 spring boot 3.x, 默认使用3.2.7版本
- 数据库操作必须使用 spring boot jpa 方式操作数据库
- 接口参数类不允许以vo dto结尾，尽量以意图名，比如 UserEdit, UserAdd, UserDelete 等
- 接口返回参数处理必要的包裹类，不允许以vo dto结尾，尽量以意图名，非必要则以直接返回实体，如需要脱敏等处理则返回意图如：UserInfo


## 接口类结构规则
- 必须使用`ResultVO<T>`包裹返回结果，其中T为具体数据类型
- 必须使用 `@Operation(summary = "接口说明")` 注解标注接口说明
- 如果是`GET`请求，必须使用 `@Parameter(name = "参数名", description = "说明")` 注解标注接口参数
- 如果是`POST`请求，必须使用 `@RequestBody`和`@Valid` 注解标注接口参数
- 如果接口不用鉴权 `@ApiMapping(value = "接口路径", method = RequestMethod.GET/POST, checkToken = true/false)` 注解标注接口路径和请求方式
- 如果正常鉴权则可以使用常规的`@GetMapping` `@PostMapping` 等注解标注接口路径和请求方式
- 类上必须使用 `@Tag(name = "模块名称", description = "模块说明")` 注解标注接口模块
- 类上使用 `@PathRestController("访问前缀")` 代替 `@RestController`和`@RequestMapping`  注解标注访问前缀和JSON接口返回格式
- 类上必须使用 `@RequiredArgsConstructor` 注解标注，使用构造器注入依赖
- 类上必须使用 `@Slf4j` 注解标注，用于日志记录
- 类上看情况使用 `@Validated` 注解标注，用于参数校验
- 分页接口必须使用`ResultPageVO<T, JpaPageResult<T>>`包裹返回结果，其中T为具体数据类型


## 实体类结构规则
- 使用spring boot jpa的方式定义实体类，包括主键、字段、索引、约束等
- 使用 `@Entity` 注解标注实体类
- 使用 `@Id` 注解标注主键字段
- 使用 `@GeneratedValue(strategy = GenerationType.IDENTITY)` 注解标注主键生成策略
- 使用 `@Column` 注解标注字段，包括字段名、是否唯一、是否允许为空、是否索引等
- 使用 `@Index` 注解标注索引，包括索引名、字段名、是否唯一等
- 使用 `@Constraint` 注解标注约束，包括约束名、字段名、约束类型、约束参数等
- 使用 `@Table` 注解标注表名，包括表名、是否唯一等
- 使用 `@EntityListeners(AuditingEntityListener.class)` 注解标注实体类，用于自动记录创建时间、更新时间等
- 使用`jakarta.persistence.Column` `@Comment("登录日志")` 注解标注字段和表注释
- 使用`io.swagger.v3.oas.annotations.media.Schema` `@Schema` 标注swagger文档的实体和字段注释信息
- 使用`com.fasterxml.jackson.annotation` `@JsonFormat(locale = "zh", timezone = "GMT+8", pattern = "yyyy-MM-dd HH:mm:ss")` 对时间类型字段进行标记格式化
- 使用 `@Enumerated(EnumType.STRING)` 标记枚举类型字段，用于数据库存储枚举值的字符串表示
- 使用 `@ColumnDefault("0")` 标注字的段默认值,注意如果是字符串需要加上引号，例如`@ColumnDefault("'0'")`
- 如果是自定义类必须继承`SerializableBean<T>`类，用于序列化和反序列化,T为泛型类型，例如`SerializableBean<User>`
- 如果需要公共字段，例如创建时间、更新时间等，必须继承`JpaCommonBean2`,如果没有可以实现一个
- 如果是

## 示例

### 接口示例
```java
/**
 * 邮箱接口
 *
 * @author <a href="https://t.tannn.cn/">tan</a>
 * @version V1.0
 * @date 2025/3/17 15:44
 */
@Tag(name = "邮箱管理", description = "邮箱管理")
@PathRestController("email")
@RequiredArgsConstructor
@Slf4j
@Validated
public class EmailController {


    private final RedisOperateService redisOperateService;
    private final EmailService emailService;


    @Operation(summary = "获取邮箱验证码")
    @ApiMapping(value = "verificationCode", method = RequestMethod.GET, checkToken = false)
    @Parameter(name = "toEmail", description = "邮箱", required = true)
    @Parameter(name = "type", description = "验证码类型 1:注册，2修改密码,3.邮箱换绑", required = true)
    public ResultVO<String> verificationCode(@RequestParam("toEmail") String toEmail, @RequestParam("type") Integer type) {
        emailService.emailVerificationCode(toEmail, type);
        return ResultVO.successMessage("验证码发送成功");
    }

    @PostMapping("select")
    @Operation(summary = "分页查询角色")
    @ApiOperationSupport(order = 1)
    @ApiPlatform(platform = PlatformConstant.WEB_ADMIN)
    public ResultPageVO<Role, JpaPageResult<Role>> selectRole(@RequestBody @Valid RolePage role) {
        Page<Role> roles = roleService.findPage(role, role.getPage());
        JpaPageResult<Role> pageResult = JpaPageResult.toPage(roles);
        return ResultPageVO.success(pageResult, "查询成功");
    }
}
```


### 实体示例
```java

/**
 * 账户基础信息表
 *
 * @author tnnn
 * @version V1.0
 * @date 2023-10-25
 */
@Entity
@Table(name = "tb_account",
        indexes = {
                @Index(name = "idx_loginName", columnList = "loginName", unique = true)
        }
)
@Comment("账户基础信息表")
@Getter
@Setter
@ToString
@DynamicUpdate
@DynamicInsert
@Schema(description = "账户基础信息表")
@JsonView({Views.Public.class})
public class Account extends JpaCommonBean2<Account> {
    /**
     * 登录名
     */
    @Column(columnDefinition = " varchar(100)  not null ")
    @Comment("登录名")
    @Schema(description = "登录名")
    private String loginName;

    /**
     * 登录密码
     */
    @Column(columnDefinition = " varchar(100) not null ")
    @Comment("登录密码")
    @Schema(description = "登录密码")
    @JsonView(Views.UserPassword.class)
    private String password;


    /**
     * 性别:0[未知]，1[男性]，2[女性]
     */
    @Column(columnDefinition = "smallint")
    @ColumnDefault("0")
    @Comment("性别:0[未知]，1[男性]，2[女性]")
    @Schema(description = "性别:0[未知]，1[男性]，2[女性]")
    private Integer gender;

    /**
     * 用户真实姓名
     */
    @Column(columnDefinition = " varchar(200)")
    @Schema(description = "用户真实姓名")
    @Comment("用户真实姓名")
    private String name;

    /**
     * 用户昵称
     */
    @Column(columnDefinition = " varchar(200)")
    @Comment("用户昵称")
    @Schema(description = "用户昵称")
    private String nickname;


    /**
     * 账号状态:1[正常],2[锁定],3[回收站-逻辑删除]
     *
     * @see AccountStatus
     */
    @Column(columnDefinition = "smallint")
    @ColumnDefault("2")
    @Comment("账号状态:1[正常],2[锁定],3[回收站-逻辑删除]")
    @Schema(description = "账号状态:1[正常],2[锁定],3[回收站-逻辑删除]")
    private Integer status;

    /**
     * 账号类型:0[内置]，1[添加]，2[注册]，3[同步]
     *
     * @see AccountType
     */
    @Column(columnDefinition = "smallint")
    @ColumnDefault("2")
    @Comment("账号类型:0[内置]，1[添加]，2[注册]，3[同步]")
    @Schema(description = "账号类型:0[内置]，1[添加]，2[注册]，3[同步]")
    private Integer type;


    /**
     * 可用状态:-1[待激活](数据不支持)，0[已激活](数据不支持)，1[审核中](默认)，2[审核通过]，3[审核不通过]
     *
     * @see AccountAvailableStatus
     */
    @Column(columnDefinition = "smallint")
    @ColumnDefault("1")
    @Comment("可用状态:-1[待激活](数据不支持)，0[已激活](数据不支持)，1[审核中]，2[审核通过]，3[审核不通过]")
    @Schema(description = "可用状态:-1[待激活](数据不支持)，0[已激活](数据不支持)，1[审核中]，2[审核通过]，3[审核不通过]")
    private Integer available;

    /**
     * 错误消息备注
     * <p>比如被设置删除后，设置当前账户被回收</p>
     * <p>审核不通过时，设置不通过原因等</p>
     */
    @Column(columnDefinition = " varchar(200)")
    @Comment("错误消息备注")
    @Schema(description = "错误消息备注")
    private String errorMessage;


    /**
     * 最后登录时间
     */
    @Column(columnDefinition = "timestamp")
    @Comment("最后登录时间")
    @Schema(description = "最后登录时间")
    @JsonFormat(locale = "zh", timezone = "GMT+8", pattern = "yyyy-MM-dd HH:mm:ss")
    public LocalDateTime lastLoginTime;


    /**
     * 密码过期时间[为空永不过期]
     * <p>todo 后期考虑系统设置全局过期时间例如三个月，这里就可以选择使用系统全局还是自定义</p>
     * <p>todo 后期需要做线程处理过期密码的自动退出</p>
     */
    @Column(columnDefinition = "timestamp")
    @Comment("密码过期时间[为空永不过期]")
    @Schema(description = "密码过期时间[为空永不过期]")
    @JsonFormat(locale = "zh", timezone = "GMT+8", pattern = "yyyy-MM-dd HH:mm:ss")
    public LocalDateTime passwordExpireTime;

    /**
     * 用户过期时间[为空永不过期]
     * <p>todo 后期考虑系统设置全局过期时间例如三个月，这里就可以选择使用系统全局还是自定义</p>
     * <p>todo 后期需要做线程处理过期账户的自动退出</p>
     */
    @Column(columnDefinition = "timestamp")
    @Comment("用户过期时间[为空永不过期]")
    @Schema(description = "用户过期时间[为空永不过期]")
    @JsonFormat(locale = "zh", timezone = "GMT+8", pattern = "yyyy-MM-dd HH:mm:ss")
    public LocalDateTime userExpireTime;

    /**
     * 是否为默认密码:0[否]，1[是]
     * <p> todo 后期将默认密码的设置配置文件移到SysConfig书就看
     */
    @Column(nullable = false, columnDefinition = "boolean default false")
    @Comment("是否为默认密码:0[否]，1[是]")
    @Schema(description = "是否为默认密码:0[否]，1[是]")
    private Boolean defaultPassword;

    /**
     * 是否强制修改默认密码:0[否]，1[是]
     * <p>默认密码的情况下是否需要强制修改密码</p>
     */
    @Column(nullable = false, columnDefinition = "boolean default false")
    @Comment("是否强制修改默认密码:0[否]，1[是]")
    @Schema(description = "是否强制修改默认密码:0[否]，1[是]")
    private Boolean forcePasswordChange;


    /**
     * 注册IP
     */
    @Column(columnDefinition = " varchar(200)")
    @Comment("注册IP")
    @Schema(description = "注册IP")
    private String registerIp;

    /**
     * 注册平台
     *
     * @see PlatformType
     */
    @Comment("注册平台")
    @Schema(description = "注册平台")
    @Column(columnDefinition = "varchar(20) default 'PC'")
    @Enumerated(EnumType.STRING)
    private PlatformType registerPlatform;


    /**
     * 组织编码
     *
     * @see Organization#getNo()
     */
    @Comment("组织编码")
    @Schema(description = "组织编码")
    @Column(columnDefinition = "varchar(100) ")
    private String orgNo;

    /**
     * 冗余组织名
     *
     * @see Organization#getName()
     */
    @Comment("冗余组织名")
    @Schema(description = "冗余组织名")
    @Column(columnDefinition = "varchar(200) ")
    private String orgName;


    /**
     * 备注
     */
    @Column(columnDefinition = " varchar(200)")
    @Comment("备注")
    private String remark;

}
```
实体公共字段
```java
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
public class JpaCommonBean2<B> extends JpaAuditTimeFormatFields<B> {

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
