# Scaling Agents via Continual Pre-training 论文实现中文解读（含代码）

- 论文：[Scaling Agents via Continual Pre-training](https://arxiv.org/pdf/2509.13310)
- 对象：有LLM SFT微调经验、对RL/Agent相对陌生的读者

## 一、论文核心观点（通俗中文）
- 用中文精炼概括论文提出的问题、方法与贡献。
- 方法如何提升长周期信息搜集能力与工具使用能力。

## 二、知识难点与背景补课
- RL在Web/搜索环境中的回报设计与采样稳定性。
- 任务分解、浏览器交互、记忆/检索的工程化实现要点。

## 三、仓库结构与实现要点
- 目录结构、数据流、主要模块（策略、环境、工具、记忆）。
- 训练/推理脚本与配置。

## 四、关键代码（粘贴原始代码并逐段解释）
### 文件：`Agent/AgentScaler/README.md`

```md

<h1 align="center"> <img src="assets/caller.jpg" alt="AgentScaler Logo" width="35" style="vertical-align: middle; margin-right: px;">AgentScaler: 

Towards General Agentic Intelligence via Environment Scaling</h1>


## 🌟Overview

In this work, we scale up environments as a step towards advancing general agentic intelligence. This gives rise to two central challenges: (i) how to scale environments in a principled manner, and (ii) how to effectively train agentic capabilities from experiences derived through inter-actions with these environments. To address these, we design a scalable framework that automatically constructs heterogeneous environments that are fully simulated, systematically broadening the space of function-calling scenarios. We further adapt a two-phase agent fine-tuning strategy: first endowing agentswith fundamental agentic capabilities, then specializing them for domain-specific contexts. Extensive experiments on agentic benchmarks, τ-bench, τ2-Bench, and ACEBench, demonstrate that our trained model, AgentScaler, significantly enhances the models’ function-calling capability.

## 🔧Framework
We introduce a principled pipeline that comprises two central stages: (i) fully simulated
environment construction and scaling, which establishes and expands diverse agentic scenarios, and (ii)
agent experience learning, which exploits these environments to foster generalizable intelligence.
![Framework Overview](assets/env_build.png "Click to see the detailed architecture")

The process to obtain the agent trajectories
![Framework Overview](assets/infer.png "Click to see the detailed architecture")


## 📚MainResults
Main results on τ-bench, τ2-Bench, and ACEBench-en
![Main Results](assets/main.png "Click to see the detailed architecture")




## 🚩Citation

Please cite our repository if you think it's useful

```bibtex
@article{su2025agentfounder,
      title={Towards General Agentic Intelligence via Environment Scaling}, 
      author={Runnan Fang, Shihao Cai, Baixuan Li, Jialong Wu, Guangyu Li, Wenbiao Yin, Xinyu Wang, Xiaobin Wang, Liangcai Su, Zhen Zhang, Shibin Wu, Zhengwei Tao, Yong Jiang, Pengjun Xie, Fei Huang, Jingren Zhou},
      year={2025},
      journal={arXiv preprint arXiv:2509.13311},
}
```



## 🎉Contributors


We will offer long-term maintenance to fix bugs and solve issues. So if you have any problems, please put issues to us.
```

> 说明：以上为关键代码片段，结合上下文解释其作用与调用关系。



## 五、如何在本仓库中复现与扩展
- 按各子项目`README.md`准备环境与数据；
- 参考`requirements.txt`安装依赖，运行提供的脚本；
- 可替换模型、修改超参以复现论文结果并做扩展。
