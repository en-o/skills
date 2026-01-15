# 需求分析和确认流程

## 📋 流程概述

在开始任何代码生成前，必须完成需求分析和确认流程。此流程确保：
- AI 完全理解用户需求
- 生成的代码符合用户期望
- 避免返工和重复修改

---

## 🔄 完整流程

```
┌─────────────────────────┐
│  1. 收集用户需求描述    │
└──────────┬──────────────┘
           ↓
┌─────────────────────────┐
│  2. AI 总结提炼需求     │
│   - 业务目标            │
│   - 核心功能            │
│   - 数据模型            │
│   - 接口定义            │
│   - 技术选型            │
└──────────┬──────────────┘
           ↓
┌─────────────────────────┐
│  3. 展示需求总结        │
│   询问：是否满意？      │
└──────────┬──────────────┘
           ↓
      满意？───NO──┐
           │       │
          YES      ↓
           │  ┌─────────────────────────┐
           │  │  4. 询问需要调整的内容  │
           │  │     或新增需求          │
           │  └──────────┬──────────────┘
           │             ↓
           │  ┌─────────────────────────┐
           │  │  5. 收集补充信息        │
           │  └──────────┬──────────────┘
           │             │
           │             ↓
           │  ┌─────────────────────────┐
           │  │  6. 重新总结提炼        │
           │  │   （整合新需求）        │
           │  └──────────┬──────────────┘
           │             │
           └─────────────┘
                   ↓
        ┌─────────────────────────┐
        │ 3.5. 包结构选择         │ ← 新增步骤
        │   - 询问选择 A/B/C      │
        │   - 提供推荐建议        │
        │   - 记录用户选择        │
        └──────────┬──────────────┘
                   ↓
        ┌─────────────────────────┐
        │ 6.5. Entity 字段设计确认│
        │   - 展示每个 Entity 字段│
        │   - 询问是否需要调整    │
        │   - 支持新增/删除/修改  │
        │   - 迭代直到满意        │
        └──────────┬──────────────┘
                   ↓
           ┌───────────────┐
           │ 所有 Entity   │
           │ 都已确认？    │
           └───┬───────┬───┘
              YES     NO
               │       │
               │       └──→ 继续确认下一个 Entity
               ↓
        ┌─────────────────────────┐
        │  7. 制定开发计划        │
        │   - 文件清单            │
        │   - 开发顺序            │
        │   - 依赖关系            │
        └──────────┬──────────────┘
                   ↓
        ┌─────────────────────────┐
        │  8. 征得确认后开始执行  │
        └─────────────────────────┘
```

---

## 📝 步骤详解

### 步骤 1: 收集用户需求描述

**目标**：让用户详细描述需求，获取足够的信息进行分析。

#### 如何引导用户

**创建新项目时**：
```
"请详细描述您要创建的项目：
1. 项目的业务场景是什么？
2. 需要实现哪些核心功能？
3. 预计有哪些主要模块？
4. 有什么特殊的技术要求吗？（如认证方式、缓存、文件上传等）
5. 使用什么数据库？

请尽可能详细地描述，这将帮助我更好地理解您的需求。"
```

**⚠️ 重要：框架选择（仅创建新项目时）**

如果用户在需求描述中**没有明确说明使用 JDevelops 框架**，必须询问：

```
"请问您希望使用哪种技术方案？

【选项 A】JDevelops 框架（推荐）
  - 基于 Spring Boot 3.x + JPA
  - 提供开箱即用的组件和工具类
  - 统一的开发规范和最佳实践
  - 内置认证、异常处理、分页等功能
  - 适合：快速开发、团队协作、企业级应用

【选项 B】纯 Spring Boot
  - 标准 Spring Boot + JPA
  - 使用 Spring 官方组件
  - 自定义架构和规范
  - 适合：对框架有特殊要求、需要完全控制

请选择 A 或 B（如不确定，推荐选择 A - JDevelops 框架）"
```

**根据用户选择决定后续流程**：
- 选择 A → 使用 JDevelops 框架规范
- 选择 B → 使用纯 Spring Boot 规范

**添加业务模块时**：

**不需要询问框架选择**，而是通过以下步骤自动检测：

1. **确认项目路径**
2. **读取 pom.xml 文件**
3. **自动检测框架类型**：
   - 查找 `<groupId>cn.tannn.jdevelops</groupId>` → JDevelops 框架
   - 只有标准 Spring 依赖 → 纯 Spring Boot
4. **通知用户检测结果**：
   ```
   "检测到项目使用 JDevelops 框架！
   将按照 JDevelops 规范生成代码。"

   或

   "检测到项目为纯 Spring Boot 项目！
   将按照标准 Spring Boot 规范生成代码。"
   ```

**引导用户描述模块需求**：
```
"请详细描述您要添加的模块：
1. 模块的业务功能是什么？
2. 需要管理哪些数据？（实体、字段）
3. 需要提供哪些接口？（增删改查、搜索、导出等）
4. 有什么特殊的业务逻辑？
5. 是否有权限控制？
6. 是否需要与其他模块关联？

请尽可能详细地描述，包括您能想到的所有细节。"
```

#### 用户描述示例

**示例 1 - 创建项目**：
```
用户输入：
"我要创建一个在线教育平台的后台管理系统，主要功能包括：
1. 课程管理（课程分类、课程信息、章节管理）
2. 讲师管理（讲师信息、课程绑定）
3. 学员管理（学员信息、学习记录）
4. 订单管理（课程订单、支付记录）
5. 统计分析（学员统计、课程统计、销售统计）
使用 MySQL 数据库，需要 JWT 认证，支持文件上传（课程视频、课件），
需要生成 API 文档方便前端对接"
```

**示例 2 - 添加模块**：
```
用户输入：
"我需要添加一个试题库管理模块，功能包括：
1. 试题管理（选择题、判断题、填空题、简答题）
2. 试题分类（按科目、难度、知识点）
3. 试卷管理（组卷、设置分值）
4. 考试管理（创建考试、发布考试、收集答卷）
5. 成绩管理（自动批改、成绩统计、成绩导出）
需要支持富文本编辑（试题内容可能包含图片、公式）"
```

---

### 步骤 2: AI 总结提炼需求

**目标**：将用户的自然语言描述转换为结构化的需求文档。

#### 总结模板

```markdown
【需求总结】

## 项目/模块概述
- 名称：
- 类型：
- 业务领域：
- 技术栈：

## 核心功能
1. 功能模块1
   - 子功能1
   - 子功能2
   - 子功能3

2. 功能模块2
   ...

## 数据模型设计

### Entity1（实体名称）
- 字段清单
- 字段类型
- 字段说明
- 特殊标注（主键、外键、索引、唯一约束）

### Entity2
...

## 接口定义

### Controller1（路径）
- HTTP方法 /路径 - 功能说明
- 请求参数
- 响应格式

### Controller2
...

## 请求/响应类

### 请求类（dto）
- 类名 - 用途

### 响应类（vo）
- 类名 - 用途

## 技术选型
- 认证方式：
- 缓存：
- 文件存储：
- 文档：

## 推荐组件
🔴 核心组件：
  - 组件列表

🟡 推荐组件：
  - 组件列表

🟢 可选组件：
  - 组件列表

## 特殊说明
- 业务规则
- 技术约束
- 性能要求
```

#### 总结示例

**基于示例 2 的总结**：

```markdown
【需求总结】

## 模块概述
- 名称：试题库管理模块（Question Bank）
- 业务领域：在线考试
- 关联模块：讲师模块（出题人）、学员模块（考生）

## 核心功能

1. 试题管理
   - 新增试题（选择题、判断题、填空题、简答题）
   - 编辑试题
   - 删除试题
   - 试题查询（分页、搜索）
   - 试题导入/导出

2. 试题分类
   - 按科目分类
   - 按难度分级（简单、中等、困难）
   - 按知识点标签

3. 试卷管理
   - 创建试卷
   - 添加试题到试卷
   - 设置试题分值
   - 设置试卷总分和时长
   - 试卷预览

4. 考试管理
   - 创建考试
   - 关联试卷
   - 设置考试时间
   - 发布考试
   - 考生答卷收集

5. 成绩管理
   - 自动批改（选择题、判断题）
   - 手动批改（填空题、简答题）
   - 成绩统计分析
   - 成绩导出（Excel）

## 数据模型设计

### Question（试题表）
- id: Long（主键）
- questionType: Integer（题型：1-选择题，2-判断题，3-填空题，4-简答题）
- content: Text（题目内容，富文本）
- options: String（选项，JSON 格式，仅选择题）
- answer: String（标准答案）
- analysis: Text（答案解析）
- subjectId: Long（科目ID）
- difficultyLevel: Integer（难度：1-简单，2-中等，3-困难）
- tags: String（知识点标签，逗号分隔）
- creatorId: Long（出题人ID）
- 继承 JpaCommonBean

### Paper（试卷表）
- id: Long
- paperName: String（试卷名称）
- totalScore: BigDecimal（总分）
- duration: Integer（时长，分钟）
- description: String（描述）
- 继承 JpaCommonBean

### PaperQuestion（试卷-试题关联表）
- id: Long
- paperId: Long
- questionId: Long
- score: BigDecimal（该题分值）
- sortOrder: Integer（排序）

### Exam（考试表）
- id: Long
- examName: String（考试名称）
- paperId: Long（试卷ID）
- startTime: LocalDateTime（开始时间）
- endTime: LocalDateTime（结束时间）
- status: Integer（状态：0-未发布，1-进行中，2-已结束）
- 继承 JpaCommonBean

### ExamAnswer（考生答卷表）
- id: Long
- examId: Long
- studentId: Long（学员ID）
- paperId: Long
- answers: Text（答案，JSON 格式）
- score: BigDecimal（成绩）
- gradeStatus: Integer（批改状态：0-未批改，1-已批改）
- submitTime: LocalDateTime

## 接口定义

### QuestionController（/question）
- POST /question/add - 新增试题
- PUT /question/update - 更新试题
- DELETE /question/delete/{id} - 删除试题
- GET /question/detail/{id} - 试题详情
- POST /question/page - 分页查询（支持按科目、难度、标签搜索）
- POST /question/import - 批量导入
- GET /question/export - 导出试题库

### PaperController（/paper）
- POST /paper/add - 新建试卷
- PUT /paper/update - 更新试卷
- DELETE /paper/delete/{id} - 删除试卷
- GET /paper/detail/{id} - 试卷详情
- POST /paper/add-question - 添加试题到试卷
- DELETE /paper/remove-question/{id} - 移除试题
- GET /paper/preview/{id} - 预览试卷

### ExamController（/exam）
- POST /exam/add - 创建考试
- PUT /exam/update - 更新考试
- PUT /exam/publish/{id} - 发布考试
- GET /exam/detail/{id} - 考试详情
- POST /exam/page - 分页查询
- GET /exam/paper/{id} - 获取考试试卷（考生）
- POST /exam/submit - 提交答卷

### GradeController（/grade）
- POST /grade/auto - 自动批改
- POST /grade/manual - 手动批改
- GET /grade/detail/{examAnswerId} - 成绩详情
- POST /grade/statistics/{examId} - 成绩统计
- GET /grade/export/{examId} - 导出成绩

## 请求/响应类

### 请求类（dto）
- QuestionAdd（新增试题）
- QuestionEdit（编辑试题）
- QuestionPage（试题查询）
- PaperAdd（新建试卷）
- PaperAddQuestion（添加试题到试卷）
- ExamAdd（创建考试）
- ExamSubmit（提交答卷）
- GradeManual（手动批改）

### 响应类（vo）
- QuestionInfo（试题详情，包含出题人信息）
- PaperInfo（试卷详情，包含试题列表）
- ExamInfo（考试详情，包含试卷信息）
- GradeInfo（成绩详情，包含答题详情）

## 技术要点
- 富文本编辑：需要前端支持（如 TinyMCE、CKEditor）
- 文件上传：需要 jdevelops-files-sdk（试题中的图片）
- Excel 导入导出：需要 jdevelops-utils-excel
- 自动批改：选择题、判断题比对答案
- 手动批改：填空题、简答题需要教师批阅
- 成绩统计：使用 JPA 聚合查询或原生 SQL

## 推荐组件
🟢 可选组件：
  - jdevelops-files-sdk（试题图片上传）
  - jdevelops-utils-excel（试题导入、成绩导出）
```

---

### 步骤 3: 确认需求

**展示总结并询问**：

```
"以上是我对您需求的总结，请您确认：

【需求总结】
（粘贴总结内容）

请问：
1. 需求总结是否准确？
2. 功能点是否完整？
3. 数据模型设计是否合理？
4. 接口定义是否符合预期？
5. 是否满意此需求总结？

如果有任何需要调整或补充的地方，请告诉我。"
```

---

### 步骤 3.5: 包结构选择（重要）

**⚠️ 需求确认后，必须询问用户选择包结构方式**

参考文档：[../reference/package-structure.md](../reference/package-structure.md)

#### 为什么需要确认包结构？

- 包结构直接影响项目的组织方式和未来的可维护性
- 不同规模的项目适合不同的包结构
- 提前确定可避免后期大规模重构

#### 询问方式

```
"现在需要确定项目的包结构方式。根据您的项目规模和需求，有以下三种选择：

【包结构选择】

【选项 A】传统三层架构（推荐小型项目）

结构示例：
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

✅ 优点：
  - 结构清晰，易于理解
  - 快速定位某一层的所有类
  - 代码复用方便
  - 适合团队快速开发

⚠️ 缺点：
  - 大型项目中单个包类数量可能过多
  - 跨层修改需要在多个包之间切换

📊 适用场景：
  - 小型项目（< 50 个实体）
  - 团队规模较小（< 10 人）
  - 业务模块耦合度较高
  - 希望快速开发、结构简单

---

【选项 B】垂直切分（模块化）（推荐中型项目）

结构示例：
```
src/main/java/{basePackage}/
├── controller/{domain}/     # 控制器层（统一管理）
│   ├── dto/
│   └── vo/
├── {module}/               # 业务模块（垂直切分）
│   ├── entity/            # 模块内所有实体
│   ├── dao/               # 模块内所有 DAO
│   ├── service/           # 模块内所有 Service 接口
│   └── service/impl/      # 模块内所有 Service 实现
```

✅ 优点：
  - 模块独立，职责清晰
  - 易于拆分成独立的微服务
  - 模块边界明确，减少耦合
  - 适合大型项目多模块并行开发
  - 利于团队分工

⚠️ 缺点：
  - 目录层次较深，需要更多导航
  - 跨模块复用代码相对困难
  - 小型项目可能显得过度设计

📊 适用场景：
  - 中大型项目（50-100 个实体）
  - 团队规模较大（> 10 人）
  - 业务模块独立性强
  - 未来可能拆分成微服务

---

【选项 C】标准目录结构（推荐大型项目）

结构示例：
```
src/main/java/{basePackage}/
├── controller/{domain}/     # 控制器层（统一管理）
├── common/                 # 公共组件层
│   ├── annotations/        # 自定义注解
│   ├── constant/           # 公共常量
│   ├── pojo/              # 公共 POJO
│   └── util/              # 工具类
├── core/                   # 核心配置层
│   ├── config/            # 配置类
│   ├── exception/         # 全局异常处理
│   └── initialize/        # 初始化类
└── modules/                # 业务模块层（细粒度垂直切分）
    ├── {module}/          # 大模块
    │   ├── constant/      # 模块常量
    │   └── {submodule}/   # 子模块
    │       ├── entity/
    │       ├── dao/
    │       ├── service/
    │       └── service/impl/
```

✅ 优点：
  - 高度模块化，业务边界清晰
  - 可扩展性强，易于维护
  - 支持大型项目和复杂业务
  - 便于拆分为微服务
  - 公共组件统一管理

⚠️ 缺点：
  - 目录层次最深（3-4 层）
  - 需要良好的模块规划
  - 小型项目过度设计

📊 适用场景：
  - 大型企业项目（> 100 个实体）
  - 多团队协作开发
  - 业务模块复杂且独立性强
  - 需要良好的模块边界
  - 未来可能演进为微服务架构

---

【快速决策参考】

根据您的项目规模：
- 小型项目（< 50 个实体）→ 推荐选择 A
- 中型项目（50-100 个实体）→ 推荐选择 B
- 大型项目（> 100 个实体）→ 推荐选择 C

请选择 A、B 或 C（如不确定，可以告诉我您的实体数量或项目规模，我来帮您推荐）"
```

#### 用户选择后的处理

**记录用户选择**：
```
用户: "选择 B，垂直切分"

AI: "好的，已记录您的包结构选择：

【包结构】垂直切分（模块化）

项目将采用以下结构：
- Controller 统一管理（controller/{domain}）
- 业务模块垂直切分（{module}/entity、{module}/dao、{module}/service）

后续代码生成将按照此结构进行。"
```

**如果用户不确定**：
```
用户: "不确定，你帮我推荐吧。我预计有 User、Role、Permission、Menu、Department、LoginLog、OperationLog 这些模块"

AI: "好的，让我分析一下：

【项目分析】
- 预计实体数量：7-10 个左右（算上关联实体）
- 业务特点：管理后台系统，模块关联紧密
- 模块规模：中小型

【推荐方案】选项 A - 传统三层架构

推荐理由：
1. 实体数量在 50 个以内，适合传统三层架构
2. 管理后台的模块通常耦合度较高（如用户-角色-权限-菜单）
3. 结构简单，开发效率高
4. 易于理解和维护

请问是否采用此方案？或者您有其他偏好？"
```

#### 确认清单

在进入 Entity 字段确认前，确保：
- [ ] 用户已选择包结构方式（A/B/C）
- [ ] 包结构选择已记录
- [ ] 用户理解所选包结构的特点

---

### 步骤 4-6: 迭代优化

如果用户不满意，进入迭代流程：

#### 步骤 4: 询问调整内容

```
"请说明需要调整的地方，或者是否有新的需求要加入？
您可以：
- 指出总结中不准确的地方
- 补充遗漏的功能
- 调整数据模型设计
- 修改接口定义
- 添加新的需求"
```

#### 步骤 5: 收集补充信息

记录用户的反馈和新需求。

**示例**：
```
用户: "基本准确，但还需要添加：
1. 试题收藏功能（教师可以收藏其他教师的试题）
2. 试题使用记录（记录试题被使用的次数和场景）
3. 错题本功能（学员可以查看自己的错题）"
```

#### 步骤 6: 重新总结提炼

整合新需求，更新总结：

```
"好的，我来更新需求总结：

【需求总结（更新版）】

## 核心功能（更新）
... （保留原有内容）

6. 试题收藏功能  ← 新增
   - 收藏试题
   - 取消收藏
   - 我的收藏列表

7. 试题使用记录  ← 新增
   - 记录试题被使用情况
   - 使用统计分析

8. 错题本功能  ← 新增
   - 自动收集错题
   - 错题分类
   - 错题重做

## 数据模型设计（更新）
新增：
  - QuestionFavorite（试题收藏表）
    - id, questionId, teacherId, createTime
  - QuestionUsage（试题使用记录表）
    - id, questionId, examId, usageTime
  - WrongQuestion（错题本表）
    - id, questionId, studentId, examId, wrongCount, createTime

## 接口定义（更新）
新增：
  - POST /question/favorite/add - 收藏试题
  - DELETE /question/favorite/remove/{id} - 取消收藏
  - GET /question/favorite/my - 我的收藏
  - GET /question/usage/{id} - 试题使用记录
  - GET /wrong-question/my - 我的错题本
  - POST /wrong-question/redo - 错题重做

请问现在是否满意？"
```

---

### 步骤 6.5: Entity 字段设计确认（重要）

**⚠️ 在制定开发计划前，必须对每个 Entity 的字段设计进行详细确认**

需求总结确认后，针对每个 Entity 进行字段设计的详细确认。

#### 为什么需要 Entity 字段确认？

- Entity 是数据模型的核心，字段设计直接影响后续开发
- 提前确认可避免后期大量修改
- 用户可能在看到详细字段设计后，发现遗漏或需要调整的地方

#### 确认流程

**对于每个 Entity，执行以下流程**：

##### 1. 展示详细字段设计

```
"现在让我们确认 {Entity名称} 的字段设计。

【{Entity名称} 字段设计详情】

基础字段（继承自 JpaCommonBean）：
- id: Long（主键，自动生成）
- createBy: Long（创建人ID）
- createTime: LocalDateTime（创建时间）
- updateBy: Long（修改人ID）
- updateTime: LocalDateTime（修改时间）
- delFlag: Integer（删除标志：0-正常，1-删除）
- remark: String（备注）

业务字段：
┌─────────────────┬──────────────┬──────────┬─────────────────────────┐
│ 字段名          │ 类型         │ 长度/约束│ 说明                     │
├─────────────────┼──────────────┼──────────┼─────────────────────────┤
│ loginName       │ String       │ 50/唯一  │ 登录名（必填）           │
│ password        │ String       │ 255      │ 密码（必填、敏感字段）   │
│ userName        │ String       │ 100      │ 用户姓名                 │
│ email           │ String       │ 100/唯一 │ 邮箱                     │
│ phone           │ String       │ 20/唯一  │ 手机号                   │
│ roleId          │ Long         │ -        │ 角色ID（外键）           │
│ status          │ Integer      │ -        │ 状态：0-禁用，1-启用     │
│ avatar          │ String       │ 255      │ 头像URL                  │
│ lastLoginTime   │ LocalDateTime│ -        │ 最后登录时间             │
└─────────────────┴──────────────┴──────────┴─────────────────────────┘

特殊标注：
- 敏感字段：password（使用 @JsonIgnore）
- 唯一约束：loginName, email, phone
- 索引建议：roleId, status
- Long 类型：id, roleId（需要 @JsonSerialize(using = ToStringSerializer.class)）

请问：
1. 字段设计是否完整？有无遗漏的字段？
2. 字段类型和长度是否合理？
3. 约束条件（必填、唯一、索引）是否合适？
4. 是否满意此字段设计？

如果需要调整，请告诉我需要【新增】或【删除】哪些字段，或者需要【修改】哪些字段的属性。"
```

##### 2. 收集用户反馈

**用户可能的回复类型**：

**类型 A - 满意，无需调整**：
```
用户: "满意，没有问题"
AI: "好的，{Entity名称} 字段设计确认完成！"
→ 继续下一个 Entity 的确认
```

**类型 B - 需要新增字段**：
```
用户: "需要新增以下字段：
1. gender（性别：0-女，1-男）
2. birthday（生日）
3. idCard（身份证号，需要唯一约束）"

AI: "好的，我来更新字段设计..."
→ 重新展示更新后的字段设计
→ 再次询问是否满意
```

**类型 C - 需要删除字段**：
```
用户: "不需要 avatar 和 lastLoginTime 字段"

AI: "好的，我来更新字段设计，删除这两个字段..."
→ 重新展示更新后的字段设计
→ 再次询问是否满意
```

**类型 D - 需要修改字段属性**：
```
用户: "phone 字段不需要唯一约束，可以为空；loginName 长度改为 30"

AI: "好的，我来更新字段设计：
- phone: 移除唯一约束，允许为空
- loginName: 长度从 50 调整为 30"
→ 重新展示更新后的字段设计
→ 再次询问是否满意
```

**类型 E - 混合调整**：
```
用户: "需要新增 deptId（部门ID），删除 avatar，修改 email 为非必填"

AI: "好的，我来更新字段设计：
【新增】deptId: Long（部门ID，外键）
【删除】avatar
【修改】email: 改为非必填"
→ 重新展示更新后的字段设计
→ 再次询问是否满意
```

##### 3. 更新字段设计

根据用户反馈，更新字段设计并重新展示：

```
"好的，我已更新 {Entity名称} 的字段设计。

【{Entity名称} 字段设计详情（更新版）】

基础字段（继承自 JpaCommonBean）：
（同上）

业务字段：
┌─────────────────┬──────────────┬──────────┬─────────────────────────┐
│ 字段名          │ 类型         │ 长度/约束│ 说明                     │
├─────────────────┼──────────────┼──────────┼─────────────────────────┤
│ loginName       │ String       │ 30/唯一  │ 登录名（必填）← 长度已调整│
│ password        │ String       │ 255      │ 密码（必填、敏感字段）   │
│ userName        │ String       │ 100      │ 用户姓名                 │
│ email           │ String       │ 100/唯一 │ 邮箱（可选）← 改为非必填  │
│ phone           │ String       │ 20       │ 手机号（可选）← 移除唯一  │
│ roleId          │ Long         │ -        │ 角色ID（外键）           │
│ deptId          │ Long         │ -        │ 部门ID（外键）← 新增     │
│ status          │ Integer      │ -        │ 状态：0-禁用，1-启用     │
│ gender          │ Integer      │ -        │ 性别：0-女，1-男 ← 新增   │
│ birthday        │ LocalDate    │ -        │ 生日 ← 新增               │
│ idCard          │ String       │ 18/唯一  │ 身份证号 ← 新增           │
└─────────────────┴──────────────┴──────────┴─────────────────────────┘

变更说明：
✅ 新增字段：deptId, gender, birthday, idCard
❌ 删除字段：avatar, lastLoginTime
✏️ 修改字段：loginName（长度 50→30），email（必填→可选），phone（移除唯一约束）

请问现在是否满意？"
```

##### 4. 迭代确认直到满意

重复步骤 1-3，直到用户满意为止。

##### 5. 多 Entity 处理

**如果项目包含多个 Entity，依次确认每一个**：

```
"✅ User Entity 字段设计已确认！

接下来确认 Role Entity 的字段设计...

【Role 字段设计详情】
（展示 Role 的字段设计）

请问是否满意 Role Entity 的字段设计？"
```

**确认顺序建议**：
- 先确认核心 Entity（如 User、Product）
- 再确认关联 Entity（如 Role、Category）
- 最后确认辅助 Entity（如 LoginLog、OperationLog）

##### 6. 所有 Entity 确认完成

```
"✅ 所有 Entity 字段设计确认完成！

【字段设计总结】
- User Entity: 12 个业务字段（已确认）
- Role Entity: 5 个业务字段（已确认）
- Permission Entity: 8 个业务字段（已确认）
- Menu Entity: 10 个业务字段（已确认）

现在进入开发计划制定阶段..."
```

#### 完整示例

**示例对话流程**：

```
AI: "现在让我们确认 Product（商品）Entity 的字段设计。

【Product 字段设计详情】

基础字段（继承自 JpaCommonBean）：
- id, createBy, createTime, updateBy, updateTime, delFlag, remark

业务字段：
┌─────────────────┬──────────────┬──────────┬─────────────────────────┐
│ 字段名          │ 类型         │ 长度/约束│ 说明                     │
├─────────────────┼──────────────┼──────────┼─────────────────────────┤
│ productName     │ String       │ 200      │ 商品名称（必填）         │
│ categoryId      │ Long         │ -        │ 分类ID（外键）           │
│ price           │ BigDecimal   │ 10,2     │ 价格（必填）             │
│ stock           │ Integer      │ -        │ 库存（必填）             │
│ status          │ Integer      │ -        │ 状态：0-下架，1-上架     │
│ description     │ String       │ 1000     │ 商品描述                 │
│ mainImage       │ String       │ 255      │ 主图URL                  │
└─────────────────┴──────────────┴──────────┴─────────────────────────┘

请问是否满意此字段设计？"

用户: "需要添加以下字段：
1. brand（品牌）
2. unit（单位，如：件、个、箱）
3. weight（重量）
另外，stock 需要添加库存预警阈值字段 lowStockThreshold"

AI: "好的，我来更新字段设计：

【Product 字段设计详情（更新版）】

业务字段：
┌─────────────────┬──────────────┬──────────┬─────────────────────────┐
│ 字段名          │ 类型         │ 长度/约束│ 说明                     │
├─────────────────┼──────────────┼──────────┼─────────────────────────┤
│ productName     │ String       │ 200      │ 商品名称（必填）         │
│ categoryId      │ Long         │ -        │ 分类ID（外键）           │
│ brand           │ String       │ 100      │ 品牌 ← 新增               │
│ price           │ BigDecimal   │ 10,2     │ 价格（必填）             │
│ stock           │ Integer      │ -        │ 库存（必填）             │
│ lowStockThreshold│ Integer     │ -        │ 库存预警阈值 ← 新增      │
│ unit            │ String       │ 20       │ 单位（件、个、箱）← 新增 │
│ weight          │ BigDecimal   │ 8,2      │ 重量（kg）← 新增          │
│ status          │ Integer      │ -        │ 状态：0-下架，1-上架     │
│ description     │ String       │ 1000     │ 商品描述                 │
│ mainImage       │ String       │ 255      │ 主图URL                  │
└─────────────────┴──────────────┴──────────┴─────────────────────────┘

变更说明：
✅ 新增字段：brand, unit, weight, lowStockThreshold

请问现在是否满意？"

用户: "满意！"

AI: "✅ Product Entity 字段设计确认完成！

接下来确认 ProductImage（商品图片）Entity 的字段设计..."
```

#### 确认清单

在进入开发计划前，确保：
- [ ] 每个 Entity 的字段设计都已详细展示
- [ ] 用户已确认每个 Entity 的字段设计
- [ ] 所有字段的类型、长度、约束都已明确
- [ ] 敏感字段、唯一约束、索引都已标注
- [ ] 用户对所有 Entity 的字段设计都满意

---

### 步骤 7: 制定开发计划

需求确认后，制定详细的开发计划：

```markdown
【开发计划】

## 开发阶段

### 阶段 1: 项目准备
- [ ] 确认项目路径
- [ ] 检查并添加必要组件
  - jdevelops-files-sdk（图片上传）
  - jdevelops-utils-excel（导入导出）

### 阶段 2: 核心数据模型
- [ ] 创建 Question Entity + Dao + Service
- [ ] 创建 Paper Entity + Dao + Service
- [ ] 创建 PaperQuestion Entity + Dao + Service
- [ ] 创建 Exam Entity + Dao + Service
- [ ] 创建 ExamAnswer Entity + Dao + Service

### 阶段 3: 扩展功能数据模型
- [ ] 创建 QuestionFavorite Entity + Dao + Service
- [ ] 创建 QuestionUsage Entity + Dao + Service
- [ ] 创建 WrongQuestion Entity + Dao + Service

### 阶段 4: 请求/响应类
- [ ] 创建所有请求类（dto）
- [ ] 创建所有响应类（vo）

### 阶段 5: Controller 接口
- [ ] 创建 QuestionController（试题管理）
- [ ] 创建 PaperController（试卷管理）
- [ ] 创建 ExamController（考试管理）
- [ ] 创建 GradeController（成绩管理）

### 阶段 6: 业务逻辑
- [ ] 实现自动批改逻辑
- [ ] 实现成绩统计逻辑
- [ ] 实现导入导出功能

### 阶段 7: 验证和测试
- [ ] 验证代码规范
- [ ] 测试基础功能
- [ ] 验证 API 文档

## 预计工作量
- Entity 层：8 个实体
- Service 层：8 个 Service
- Controller 层：4 个 Controller，约 30 个接口
- 请求/响应类：约 20 个类

确认开始执行？
```

---

### 步骤 8: 开始执行

获得用户确认后，开始按计划执行：

```
"好的，开始执行开发计划！

【当前进度】
✓ 需求分析和确认完成
→ 正在执行：阶段 1 - 项目准备

步骤 1: 确认项目路径...
（进入具体的工作流）"
```

---

## 🎯 关键要点

1. **不要急于动手**：先确保需求完全理解
2. **结构化总结**：使用统一的模板进行总结
3. **主动询问**：对模糊的需求主动澄清
4. **迭代优化**：允许用户多次调整，直到满意
5. **包结构选择**：需求确认后，必须询问用户选择包结构方式（A/B/C）
6. **Entity 字段确认**：在开发计划前，必须逐个确认每个 Entity 的字段设计
7. **支持字段调整**：允许用户新增、删除、修改字段，迭代直到满意
8. **计划先行**：制定详细计划再开始编码
9. **持续沟通**：在关键节点及时反馈进度

---

## 📚 相关文档

- 创建项目工作流：[../workflows/create-project.md](../workflows/create-project.md)
- 新增模块工作流：[../workflows/add-module.md](../workflows/add-module.md)
- SKILL 主文档：[../SKILL.md](../SKILL.md)
