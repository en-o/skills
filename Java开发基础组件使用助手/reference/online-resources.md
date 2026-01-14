# 在线参考资源

## 框架源码

**GitHub 仓库**：https://github.com/en-o/Jdevelops

### 用途
- 查看最新 API 实现
- 确认包路径和方法签名
- 理解框架设计思路
- 查看示例项目

### 常用目录
- `jdevelops-dals-jpa`：JPA 数据访问层封装
- `jdevelops-apis-result`：统一返回格式（ResultVO）
- `jdevelops-authentications-rjwt`：Redis + JWT 鉴权

---

## 官方文档

**语雀知识库**：https://www.yuque.com/tanning/yg9ipo

### 用途
- API 使用说明
- 配置指南
- 最佳实践
- 常见问题解答

### 如何查阅
1. 访问文档首页
2. 查找对应模块（如"数据访问层"、"鉴权模块"）
3. 查看 API 说明和示例

---

## 下载文档到本地

如需离线查阅文档，可以使用提供的脚本下载：

```bash
# 下载完整文档
bash scripts/download-docs.sh

# 查看下载的文档
ls docs/
```

脚本使用 yuque-dl 工具：https://github.com/gxr404/yuque-dl

---

## 查阅优先级

```
遇到 API 不确定
    ↓
1. 查阅官方文档
   https://www.yuque.com/tanning/yg9ipo
    ↓ 找到了？
    ↓ 是 → 按文档说明使用
    ↓ 否 ↓
2. 查看 GitHub 源码
   https://github.com/en-o/Jdevelops
    ↓
确认方法签名和包路径
    ↓
生成符合规范的代码
```

---

## 常见问题

### Q1：如何查找某个类的包路径？

**A**：在 GitHub 仓库中搜索类名，例如搜索 `J2Service`：
1. 访问 https://github.com/en-o/Jdevelops
2. 按 `/` 键打开搜索
3. 输入类名查找

### Q2：如何确认最新版本号？

**A**：查看 GitHub Releases：
https://github.com/en-o/Jdevelops/releases

### Q3：文档和源码不一致怎么办？

**A**：以源码为准。文档可能存在更新延迟，源码始终是最新的。

---

## 相关参考

- 查阅策略：[./lookup-strategy.md](./lookup-strategy.md)
- 架构规范：[../standards/architecture.md](../standards/architecture.md)
