# 查阅策略

## 查阅流程图

```
遇到 API 不确定或需要参考
    ↓
步骤1：查阅官方文档
    ↓
找到了？
    ├─ 是 → 按文档说明使用 → 完成
    └─ 否 ↓
步骤2：查看 GitHub 源码
    ↓
确认方法签名和包路径
    ↓
生成符合规范的代码 → 完成
```

---

## 步骤1：查阅官方文档

**文档地址**：https://www.yuque.com/tanning/yg9ipo

### 适用场景
- 不确定某个 API 如何使用
- 需要查看配置说明
- 需要了解功能特性
- 查看示例代码

### 如何查阅

1. **访问文档首页**
   https://www.yuque.com/tanning/yg9ipo

2. **使用文档搜索**
   - 语雀支持全文搜索
   - 搜索关键词（如"J2Service"、"分页"、"鉴权"）

3. **浏览目录**
   - 数据访问层（JPA）
   - 鉴权模块（JWT）
   - 工具类
   - 配置说明

### 查找技巧

- **查 API 用法**：搜索类名或方法名
- **查配置**：搜索"配置"或"application.yml"
- **查示例**：浏览"快速开始"或"示例代码"章节

---

## 步骤2：查看 GitHub 源码

**仓库地址**：https://github.com/en-o/Jdevelops

### 适用场景
- 文档中找不到说明
- 需要确认方法签名
- 需要查看最新实现
- 理解框架设计思路

### 如何查阅

1. **使用 GitHub 搜索**
   - 访问仓库
   - 按 `/` 键打开搜索
   - 输入类名或方法名

2. **浏览模块目录**
   ```
   jdevelops-dals-jpa/          # JPA 数据访问
   jdevelops-apis-result/       # 统一返回格式
   jdevelops-authentications/   # 鉴权模块
   ```

3. **查看类定义**
   - 找到目标类
   - 查看方法签名
   - 查看注释说明

### 查找技巧

- **查基类**：搜索 `J2Service`、`JpaCommonBean`
- **查注解**：搜索 `@PathRestController`、`@ApiMapping`
- **查工具类**：搜索 `SerializableBean`、`ResultVO`

---

## 步骤3：下载文档到本地（可选）

如需离线查阅文档：

```bash
# 运行下载脚本
bash scripts/download-docs.sh

# 查看下载的文档
ls docs/
```

---

## 常见查阅场景

### 场景1：不确定 Service 基类

**查阅步骤**：
1. 查文档：搜索"Service"或"数据访问层"
2. 找到 `J2Service` 和 `J2ServiceImpl`
3. 查看示例代码

**或者**：
1. 查 GitHub：搜索 `J2Service`
2. 查看类定义和方法签名
3. 按照签名使用

### 场景2：不确定返回格式

**查阅步骤**：
1. 查文档：搜索"返回格式"或"ResultVO"
2. 查看使用说明

**或者**：
1. 查 GitHub：搜索 `ResultVO`
2. 查看类定义

### 场景3：不确定注解用法

**查阅步骤**：
1. 查文档：搜索注解名（如"@PathRestController"）
2. 查看使用示例

**或者**：
1. 查 GitHub：搜索注解定义
2. 查看注解参数和说明

### 场景4：不确定包路径

**查阅步骤**：
1. 查 GitHub：搜索类名
2. 查看完整包路径
3. 在代码中使用正确的 import

---

## 快速参考表

| 需求 | 查阅方式 | 资源 |
|-----|---------|------|
| API 用法 | 文档搜索 | https://www.yuque.com/tanning/yg9ipo |
| 方法签名 | GitHub 搜索 | https://github.com/en-o/Jdevelops |
| 配置说明 | 文档浏览 | 文档 → 配置章节 |
| 示例代码 | 文档浏览 | 文档 → 快速开始 |
| 包路径 | GitHub 搜索 | GitHub → 搜索类名 |
| 最新版本 | GitHub Releases | https://github.com/en-o/Jdevelops/releases |

---

## 注意事项

1. **优先查文档**：文档通常有更详细的说明和示例
2. **源码为准**：如果文档和源码不一致，以源码为准
3. **注意版本**：确保查看的是对应版本的文档和源码
4. **记录包路径**：查到包路径后记录下来，方便后续使用

---

## 相关资源

- 在线资源：[./online-resources.md](./online-resources.md)
- 架构规范：[../standards/architecture.md](../standards/architecture.md)
