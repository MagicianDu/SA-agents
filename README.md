# 4+2 架构 Agent 工作流 · Demo 仓库

这是一个**完全可运行**的示例，基于“4+2 架构最小代理（SBD / PNF / ORC / SWA + 两个 Critics）”工作流。
目标：你只需填写 `project_init.yaml`，即可一键拉起从**立项 → 契约 → 平台/NFR → Gate → 接口冻结 → 代码骨架**的端到端流程。

## 🚀 快速开始

```bash
# 1) 准备环境
pip install openai pyyaml

# 2) 配置模型 Key（以 OpenAI 为例）
export OPENAI_API_KEY=sk-xxxx

# 3) 初始化起点输入
cp project_init.example.yaml project_init.yaml
# 编辑 project_init.yaml，填入你的项目目标/场景/NFR/约束等

# 4) 运行
python runner.py --init project_init.yaml --workflow workflow.yaml --model gpt-4o-mini
# 或者
make run
```

运行完成后，所有产物会写入 `out/` 目录，按任务 ID 分类。若 Gate（安全或成本/性能）返回 `red`，流程会自动中断。

## 📂 仓库结构

```
arch_agents_demo/
├─ prompts/                      # 六个 System Prompt（XML，可复用）
│  ├─ SBD.xml                    # 策略-业务-领域一体化
│  ├─ PNF.xml                    # 平台与非功能
│  ├─ ORC.xml                    # Orchestrator / 总编排
│  ├─ SWA.xml                    # 实现架构
│  ├─ CRITIC_SECURITY.xml        # 安全/合规 Gate
│  └─ CRITIC_COST.xml            # 成本/性能 Gate
├─ workflow.yaml                 # 工作流 DAG（任务/依赖/Gate）
├─ project_init.example.yaml     # 起点输入示例（复制为 project_init.yaml 使用）
├─ runner.py                     # 执行器（LLM 可替换，默认 OpenAI Chat Completions）
├─ CHECKLIST.md                  # 30 个关键文件/目录的核对清单
├─ Makefile                      # 一键运行/清理
├─ .gitignore                    # 忽略 out/ 等本地文件
└─ out/                          # 运行输出（执行后生成）
```

## 🧠 工作流角色（4+2）
- **SBD**：策略-业务-领域一体化（能力图、领域模型、接口契约、数据契约、上下文图）  
- **PNF**：平台与非功能（NFR、平台蓝图、SLO/SLI、安全、FinOps、部署拓扑）  
- **ORC**：编排端到端方案与 Gate/ADR，对 SBD/PNF 产物进行汇聚，输出接口冻结（Interface Freeze）  
- **SWA**：在冻结后生成可运行代码骨架、契约测试与可观测性方案  
- **Critics（Security / Cost-Perf）**：在 Gate 阶段给出绿/黄/红与整改意见

## ✅ 执行检查
对照根目录的 `CHECKLIST.md` 逐项勾选，确保产出完整且可用。
