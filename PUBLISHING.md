# 发布到 GitHub

本仓库是 Tool-Star 的个人复现与实验扩展。发布时应保留代码、实验文档、配置和小型演示样例；不要提交模型权重、训练数据、评测原始输出、缓存或实验日志。

`.gitignore` 已排除这些大文件和本机文件。发布前先检查：

```powershell
git status --short
git check-ignore -v LLaMA-Factory-main/data/final_sft_edition9.json
```

确认状态中没有模型权重、完整数据集、服务器绝对路径或密钥后，初始化并创建首个本地提交：

```powershell
git init -b main
git add README.md README_UPSTREAM.md PUBLISHING.md docs .gitignore `
  evaluation Tool_Star_RL LLaMA-Factory-main requirements.txt environment.yaml
git commit -m "docs: publish Tool-Star SFT and GRPO experiment"
```

若要减少仓库体积，可只提交本次实验新增内容：

```powershell
git add README.md README_UPSTREAM.md PUBLISHING.md docs .gitignore `
  evaluation/run.py evaluation/python_executor.py `
  Tool_Star_RL/src/verl/verl/utils/reward_score/re_search_math.py `
  Tool_Star_RL/src/verl/verl/workers/rollout/vllm_rollout/python_executor.py `
  requirements.txt environment.yaml
git commit -m "docs: add Tool-Star math agent experiment report"
```

创建 GitHub 远程仓库后，将 `<YOUR_GITHUB_NAME>` 替换为自己的账号：

```powershell
git remote add origin https://github.com/<YOUR_GITHUB_NAME>/toolstar-math-agent-rl.git
git push -u origin main
```

上传前请保留 Tool-Star 和 LLaMA-Factory 的原始许可证、引用信息和来源链接；`README_UPSTREAM.md` 保存了本地快照的原始项目说明。
