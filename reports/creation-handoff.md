# qiaomu-prd-writer 创建交接

> 版本：0.1.0
>
> 日期：2026-08-19
>
> 模式：Production（本地全局 Skill，未发布公共仓库）

## 1. 目标与边界

本 Skill 服务产品、设计、研发之间的人工协作，并让管理层在同一份 PRD 的开头完成方向、范围、风险和待决策事项判断。支持新建、审查、更新；不负责技术架构、API/数据模型、任务拆解、排期、原型制作或默认外部发布。

## 2. 参考机制与落点

| 参考 | 学到的机制 | 在本包中的落点 |
|---|---|---|
| chituai/prd-writer | 中文对话、多角色视角、概念到详细、状态/异常意识 | `SKILL.md` 工作流、`prd-standard.md` 功能梳理、Standard 模板 |
| phuryn/create-prd | Why now、用户分层、价值主张、战略和假设 | 产品判断链、管理层摘要、访谈 P0 问题 |
| github/awesome-copilot/prd | 发现—分析—成文的简洁主流程与可衡量要求 | Compact Workflow、成功/验收标准分离 |
| anatasof/NatPRD | 新建/审查/更新、反幻觉、TBD、模板与验证 | Router Rules、证据五分法、校验脚本和评测 |

## 3. 明确拒绝

- 不在运行时串联三个 Skill，避免口径冲突、重复追问和上下文漂移；
- 不照搬任何候选的完整模板或大段文本；
- 不默认生成技术架构、任务拆解或研发计划；
- 不使用任意“质量分数”制造精确感，结构校验仅返回通过状态、错误与警告；
- 不强制填写不适用章节，不为了完整度编造数据或结论。

## 4. 优势声明与证据等级

### Design advantage

- 单文档双层阅读路径：管理层摘要在前、跨职能正文在后，减少两套真相；
- 事实、来源证据、推断、建议、待确认五分法；
- Lean / Standard 两档与新建/审查/更新三模式；
- 以用户任务/业务能力而非页面控件组织功能；
- 方向、范围、协作、决策、证据五道门。

### Validated advantage（仅限本地机械验证范围）

- 触发边界记录式评测：16/16 样例通过；
- 输出固定样例断言：3/3 `with_skill` 样例通过，3 个简化 baseline 均未通过；
- PRD 校验器单元测试：4/4 通过，覆盖 Standard、Lean、失败文档和自动档位降级防护；
- 输出评测证据类型为 `recorded_fixture`，不能推导真实模型质量优势。

### Hypothesis / missing evidence

- 假设：管理层能更快定位决策点；缺少真实管理者限时阅读对照。
- 假设：产品/设计/研发歧义与返工会减少；缺少跨角色盲评和项目复盘。
- provider-backed 新旧提示词对照：missing evidence。
- 真人跨职能评审：missing evidence。

## 5. 本地验证记录

```text
python3 -m unittest discover -s tests -p 'test_*.py'  -> 4/4 passed
python3 scripts/evaluate_output_cases.py ...         -> 3/3 with_skill passed
python3 qiaomu-meta-skill/scripts/trigger_eval.py ... -> 16/16 passed
python3 qiaomu-meta-skill/scripts/validate_skill.py . -> passed, 0 warnings
```

包级验证已通过且无警告。安装到 `~/.codex/skills/qiaomu-prd-writer/` 后从全局路径复验：包校验通过、单元测试 4/4、触发样例 16/16、记录式输出样例 3/3、Standard PRD 示例通过结构校验；仅发现根目录一个可发现的 `SKILL.md`。安装内容与暂存包对比一致（忽略 Python 测试缓存）。`skills-catalog.md` 已登记为 active。

## 6. 对抗式审查与修正

- **高风险：自动降档**。原实现可能把缺少 FR 编号的 Standard PRD 推断为 Lean，造成漏报。已改为只有标题明确标注 Lean 才使用轻量门，其余自动按 Standard 检查。
- **中风险：数字证据误放行**。原实现只要全文任一处出现待确认标记，就可能放行其他位置的无来源数字。已改为逐行检查数字与来源/基线/不确定性标记。
- **中风险：管理层摘要缺少决策结构**。已补推荐/备选方案、投入与影响边界、选项和不决策影响；未知资源不得自行承诺。
- **剩余风险**。结构校验仍无法判断产品判断是否正确；触发评测是规则烟雾测试，不代表所有自然语言表达；真人协作效果仍缺证据。

## 7. 资源说明

- 根入口：`SKILL.md`
- 判断规则：`references/`
- 可复用模板：`assets/`
- 确定性工具：`scripts/`
- 回归样例：`evals/`、`tests/`
- 证据与交接：`reports/`

## 8. 后续建议

选择一份真实但可脱敏的产品材料，分别让产品负责人、设计负责人、研发负责人和一位管理者在不互相讨论的情况下评阅；记录他们能否找到目标、范围、主流程、异常、验收、风险和待决策项，再依据失败点迭代 0.2.0。
