# Tool-Star 数学工具 Agent：SFT 与 GRPO 复现实验

> 这是对 [Tool-Star](https://github.com/RUC-NLPIR/Tool-Star) 的个人复现与实验扩展，不是原项目官方结果。原始上游 README 快照保留在 [README_UPSTREAM.md](README_UPSTREAM.md)。

本项目将 Qwen2.5-1.5B-Instruct 用于带 Python 工具调用的数学推理，完成从 SFT 数据处理、LoRA 微调、真实 Python 执行评测，到 GRPO Pilot 和奖励函数审计的一整套实验链路。

## 结果摘要

在 98 题调试保留集上，三组模型使用相同提示词、温度、工具预算和解码配置评测。严格自动评分结果如下：

| 模型 | 正确数 | 自动正确率 | 缺失最终输出 | 含 `<answer>` 的输出 |
| --- | ---: | ---: | ---: | ---: |
| Qwen2.5-1.5B-Instruct Base | 28 / 98 | 28.57% | 38 | 21 |
| 5k 数学工具轨迹 LoRA SFT | 58 / 98 | 59.18% | 2 | 88 |
| SFT + GRPO Pilot | 59 / 98 | 60.20% | 0 | 93 |

SFT 是这组实验中的主要增益来源：相对 Base，严格自动正确率提高 30.61 个百分点，并显著降低了缺失最终输出。GRPO 以 128 条训练样本、32 个训练步进行，仅作为训练链路和奖励函数的 Pilot；它改善了答案输出完成率，但尚未证明稳定的数学准确率提升。

对 SFT 与 GRPO 的 19 个自动评分分歧案例进行人工复核后，GRPO 有 8 个真实增益、8 个真实回退、3 个仅由最终答案格式解析差异造成的假分歧。因此，本实验不将自动评分的 `+1` 写作 GRPO 的稳定准确率提升。

详细配置、审计边界和结果见 [实验结果](docs/EXPERIMENT_RESULTS.md)，代表性失败模式见 [Bad Case 分析](docs/BAD_CASES.md)。

## 我完成了什么

- 构建 5,000 条数学工具轨迹 SFT 集，并完成 Qwen2.5-1.5B 的 LoRA 微调与权重合并。
- 接入真实 Python 执行器：模型生成 `<python>` 后执行代码，将 `<result>` 写回上下文，再继续生成最终答案。
- 建立统一 Base / SFT / GRPO 评测流程，固定解码参数并按分段恢复方式运行，避免长评测因 GPU 进程异常丢失结果。
- 定位并修复 GRPO 奖励中的数学等价误判：避免将不同多项式、不同变量或空答案判为正确；回归集覆盖 17 个边界用例。
- 完成 128 条样本、32 步的 GRPO Pilot，导出 Hugging Face 格式权重，并进行统一评测与人工分歧审计。

## 系统流程

```text
数学问题
  │
  ├─ 模型生成 <think> / <python>
  │
  ├─ PythonExecutor 执行代码
  │       └─ 将 <result> 注入下一轮上下文
  │
  ├─ 模型生成 <answer>
  │
  └─ 严格自动评分 + 人工分歧复核
```

## 实验设置

| 项目 | 设置 |
| --- | --- |
| 基座模型 | Qwen2.5-1.5B-Instruct |
| SFT | 5,000 条数学工具轨迹；LoRA，rank 16，alpha 32 |
| RL | GRPO Pilot：128 条训练样本、32 步；修复后的数学奖励函数 |
| 评测集 | 98 题调试保留集；已排除与 SFT 训练集重合的 2 题 |
| 推理 | temperature=0；单轮最大生成 2048；最多 3 次 Python 调用 |
| 执行 | vLLM + 真实 PythonExecutor；单题批处理 |

## 可复现实验产物

以下路径来自实验服务器，上传个人仓库时建议将结果 JSON、配置文件和本目录的文档一并保留：

```text
outputs/toolstar-math-lora-5k/                     # 5k SFT LoRA checkpoint
outputs/toolstar-math-5k-merged/                   # 合并后的 SFT 模型
outputs/grpo_models/math_grpo_rewardfixed_pilot32_hf/  # GRPO Pilot 导出模型
outputs/evaluations/unified_training_prompt_holdout98_gpu1_recovery_v1/
  ├── base.json
  ├── sft.json
  ├── grpo.json
  ├── summary.json
  └── comparison_audit_v1.json
```

## 结论与边界

本实验验证了小模型在真实 Python 工具环境中完成 SFT 与 GRPO 后训练的完整链路。SFT 对答案格式与工具使用的提升明确；GRPO Pilot 的价值在于验证奖励修复、训练、导出和评测链路可用，并暴露了 RL 阶段对计数边界、几何建模和格式约束的不足。

当前 98 题集合在提示词和评分器调试中使用过，因此它是**调试保留集**，不是新鲜盲测集。后续应在未参与任何调试的独立题集上复测，并扩大 GRPO 训练数据与随机种子，才可对 RL 的准确率增益作更强结论。

## 致谢

本实验基于 Tool-Star 的公开代码、数据格式与训练框架完成。请引用或使用原始项目时遵循其许可证与引用要求。
