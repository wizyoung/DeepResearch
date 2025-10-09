# ReSum: Unlocking Long-Horizon Search Intelligence via Context Summarization 论文实现中文解读（含代码）

- 论文：[ReSum: Unlocking Long-Horizon Search Intelligence via Context Summarization](https://arxiv.org/pdf/2509.13313)
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
### 文件：`WebAgent/WebResummer/README.md`

```md
# ReSum: Unlocking Long-Horizon Search Intelligence via Context Summarization


## 🏅 Introduction

![workflow](./assets/workflow.jpg)

We introduce ReSum, a novel inference paradigm that enables **unlimited exploration** for web agents. Unlike classic ReAct paradigm that append all interaction history, ReSum periodically compresses conversation into compact, restartable reasoning states. Meanwhile, ReSum minimizes
modifications to ReAct to avoid additional architectural complexity, ensuring simplicity, efficiency, and plug-and-play compatibility with existing agents. Detailed contributions:

* **ReSumTool-30B** a specialized summarization model trained to extract key evidence, identify information gaps, and highlight next-step directions for continued exploration. This lightweight, open-source tool enables goal-oriented conversation compression tailored for web search contexts.
* **ReSum-GRPO** a tailored algorithm for paradigm adaptation. Specifically, ReSum-GRPO segments long trajectories and broadcasts trajectory-level advantages across all segments. Notably, with just 1K training samples, our ReSum-GRPO-trained WebSailor-30B-A3B achieves 33.3% Pass@1on BrowseComp-zh and 18.3% on BrowseComp-en, outperforming existing open-source web agents.



## 🚀 Performance Highlights 

1. **Universal Compatibility**: Direct application of the ReSum paradigm across three WebSailor agents achieves **4.5% average Pass@1 improvement**, demonstrating broad applicability.
2. **Specialized Summarization**: Our developed ReSumTool-30B achieves performance comparable to significantly larger models like Qwen3-235B and DeepSeek-R1-671B when serving as the summary tool, while maintaining lightweight deployment advantages.
3. **Effectiveness of Targeted RL Training**: The tailored ReSum-GRPO algorithm achieves higher training rewards and faster convergence compared to standard GRPO. Such paradigm-adapted reinforcement learning enables agents to reach **8.2% absolute improvement**.



## 📚 Citation 

If you find ReSum useful, please kindly cite as:

```bibtex
@article{wu2025resumun,
   title={ReSum: Unlocking Long-Horizon Search Intelligence via Context Summarization}, 
   author={Xixi Wu and Kuan Li and Yida Zhao and Liwen Zhang and Litu Ou and Huifeng Yin and Zhongwang Zhang and Yong Jiang and Pengjun Xie and Fei Huang and Minhao Cheng and Shuai Wang and Hong Cheng and Jingren Zhou},
   year={2025},
   journal={arXiv preprint arXiv:2509.13313},
}
```




```

> 说明：以上为关键代码片段，结合上下文解释其作用与调用关系。



## 五、如何在本仓库中复现与扩展
- 按各子项目`README.md`准备环境与数据；
- 参考`requirements.txt`安装依赖，运行提供的脚本；
- 可替换模型、修改超参以复现论文结果并做扩展。
