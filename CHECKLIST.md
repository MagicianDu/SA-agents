# ✅ 4+2 架构 Agent 工作流检查清单

## 📂 启动文件
- [ ] project_init.yaml
- [ ] workflow.yaml
- [ ] prompts/*.xml
- [ ] runner.py

## 📂 工作流产出文件
### A. 立项与编排（ORC → G0_CHARter）
- [ ] out/G0_CHARter/project_charter.md
- [ ] out/G0_CHARter/solution_arch.md
- [ ] out/G0_CHARter/interface_freeze.md（草案）
- [ ] out/G0_CHARter/risk_register.md
- [ ] out/G0_CHARter/ADRs/0001-interface-freeze.md

### B. 策略-业务-领域（SBD → SBD_CORE）
- [ ] out/SBD_CORE/capability_map.yaml
- [ ] out/SBD_CORE/domain_model.yaml
- [ ] out/SBD_CORE/glossary.md
- [ ] out/SBD_CORE/openapi.yaml
- [ ] out/SBD_CORE/asyncapi.yaml
- [ ] out/SBD_CORE/data_contracts/core.yaml
- [ ] out/SBD_CORE/context_diagram.mmd

### C. 平台与非功能（PNF → PNF_CORE）
- [ ] out/PNF_CORE/nfr.yaml
- [ ] out/PNF_CORE/platform_blueprint.md
- [ ] out/PNF_CORE/slo_sli.yaml
- [ ] out/PNF_CORE/security_controls.md
- [ ] out/PNF_CORE/finops.md
- [ ] out/PNF_CORE/deploy_topology.mmd

### D. Gate 评审（Critics）
- [ ] out/G1_SECURITY/gates/G1_security_report.xml
- [ ] out/G1_COSTPERF/gates/G1_costperf_report.xml

### E. 接口冻结与复核（ORC → ORC_FREEZE）
- [ ] out/ORC_FREEZE/interface_freeze.md（最终版）
- [ ] out/ORC_FREEZE/ADRs/0001-interface-freeze.md

### F. 实现与可运行（SWA → SWA_SKELETON）
- [ ] out/SWA_SKELETON/code_skeleton/
- [ ] out/SWA_SKELETON/module_interfaces.md
- [ ] out/SWA_SKELETON/contract_tests/
- [ ] out/SWA_SKELETON/observability_hooks.md
