# qiaomu-prd-writer

面向中文产品团队的 PRD 写作、审查与更新 Skill。它把管理层决策摘要放在正文前部，并用同一份文档继续承载产品、设计、研发协作所需的功能结构、流程、规则、状态、异常和验收边界。

仓库：https://github.com/xiy12502-tech/qiaomu-prd-writing

## 适合解决什么

- 从模糊想法、会议记录、用户反馈或既有材料生成 Lean / Standard PRD；
- 梳理 Why now、目标用户、用户/业务价值、目标、范围与取舍；
- 以用户任务和业务能力组织功能，不停留在页面或控件清单；
- 审查既有 PRD 的方向、范围、证据、流程、异常、权限和可验收性；
- 对既有 PRD 做受控更新，附变更影响和遗留问题。

它不负责技术架构、API/数据库设计、研发任务拆解、排期、原型制作或外部项目管理工具操作。

## 前置条件

- [ ] 已安装 Node.js 与 npx：`node --version && npx --version`
- [ ] 使用支持 Agent Skills 的客户端，并了解安装 Skill 会授予其读取指令与调用本地工具的能力
- [ ] 安装前已审查本仓库的 `SKILL.md`、脚本和权限边界

## 安装

本地全局安装可将整个目录放入：

```text
~/.codex/skills/qiaomu-prd-writer/
```

从 GitHub 全局安装：

```bash
npx skills add xiy12502-tech/qiaomu-prd-writing --skill qiaomu-prd-writer -g
```

## 你可以直接这样说

- “根据这份会议记录写一份给上级评审的 PRD，重点梳理功能范围和取舍。”
- “审查这份 PRD，看看产品、设计、研发协作时还缺哪些状态、异常和验收边界。”
- “把这段用户反馈整理成 Lean PRD；不知道的数据不要编，列为待确认。”
- “只更新 PRD 的权限与异常处理章节，并给我变更影响摘要。”

## 默认输出

默认交付一份 Markdown 文档：

1. 前部是管理层决策摘要，呈现 Why now、目标用户、价值、目标、范围/非范围、风险和待拍板事项；
2. 后部是跨职能 PRD，呈现功能地图、核心流程、需求编号、规则、状态、异常、权限、验收标准、依赖与待确认项。

信息不足时会使用 `【假设】`、`【建议】`、`【待确认】`，不会将缺失的指标、调研结论、负责人或技术承诺补成事实。

## 结构验证

验证一个 PRD：

```bash
python3 scripts/validate_prd.py path/to/prd.md --profile auto
```

验证 Skill 包：

```bash
python3 /path/to/qiaomu-meta-skill/scripts/validate_skill.py .
python3 /path/to/qiaomu-meta-skill/scripts/trigger_eval.py . --output reports/trigger-eval.json
```

运行本地测试和记录式输出评测：

```bash
python3 -m unittest discover -s tests -p 'test_*.py'
python3 scripts/evaluate_output_cases.py --cases evals/output_cases.json --output reports/output-eval.json
```

这些检查证明结构规则和记录式样例能通过；它们不等同于真实模型提供方对照实验或人工盲评。

## Troubleshooting

### Skill 没有触发

在请求中明确写“PRD / 产品需求文档 / 产品方案”，并说明要新建、审查或更新。若只是技术设计、排期或开发实现，本 Skill 按设计不应触发。

### 追问太多

明确说“请基于现有材料直接出稿，把缺口标为待确认”。Skill 每轮最多问 1–3 个高信息量问题，材料足够时应停止访谈。

### 校验器报缺少章节

先确认文档档位。小改动使用 `--profile lean`；需要管理层评审或跨职能协作的文档使用 `--profile standard`。校验器只检查结构和部分可机械识别规则，不能代替产品判断。

### PRD 过长

保留管理层摘要、关键判断、范围与主流程；把证据、竞品、详细规则表等移到条件附录。不要删除非范围、风险和待确认项来缩短篇幅。

## 风险与限制

- 文档质量仍受输入材料真实性和关键决策完整度影响；
- 静态校验无法判断方案是否真正创造用户价值；
- 涉及法律、合规、安全、财务或医疗结论时必须由相应专家复核；
- 当前版本缺少 provider-backed 对照运行和跨角色人工盲评证据，相关优势仅作为设计优势或假设陈述。

## Credits

机制研究来源：`chituai/prd-writer; phuryn/create-prd; github/awesome-copilot/prd; anatasof/NatPRD`。本 Skill 重新设计了中文跨职能输出契约、管理层摘要、证据边界和结构校验，没有复制其成品文档。

<!-- qiaomu-profile:start -->
## 关于向阳乔木

向阳乔木（乔向阳 / Joe）是一位实践型 AI 产品与内容创作者，长期把前沿 AI 变化转译成可复用的工作流、产品判断、AI 编程实践、AI 搜索实践和 GEO/AI 营销方法。

- 个人网站: https://qiaomu.ai
- 博客: https://blog.qiaomu.ai
- X: https://x.com/vista8
- GitHub: https://github.com/joeseesun/
- 微信公众号: 向阳乔木推荐看

### 支持与关注

| 打赏支持 | 微信公众号 |
|---|---|
| <img src="assets/qiaomu-profile/qiaomu_reward_qr.png" alt="向阳乔木打赏二维码" width="180" /> | <img src="assets/qiaomu-profile/qiaomu_wechat_public_account_qr.jpg" alt="向阳乔木推荐看公众号二维码" width="180" /> |
| 感谢支持乔木持续分享 AI 实践 | 扫码关注「向阳乔木推荐看」 |

<!-- qiaomu-profile:end -->

## License

MIT License。Copyright (c) 向阳乔木。

- X: https://x.com/vista8
- GitHub: https://github.com/joeseesun/
