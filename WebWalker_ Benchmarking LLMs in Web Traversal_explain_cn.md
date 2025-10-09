# WebWalker: Benchmarking LLMs in Web Traversal 论文实现中文解读（含代码）

- 论文：[WebWalker: Benchmarking LLMs in Web Traversal](https://arxiv.org/pdf/2501.07572)
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
### 文件：`WebAgent/WebWalker/README.md`

```md
<div align="center">
<p align="center">
  <img src="assets/overall.jpg" width="50%" height="50%" />
</p>
</div>

<div align="center">
<h1>WebWalker: Benchmarking LLMs in Web Traversal</h1>
</div>

<div align="center">
<img src="https://img.shields.io/github/stars/Alibaba-NLP/WebWalker?color=yellow" alt="Stars">
<a href='https://huggingface.co/papers/2501.07572'><img src='https://img.shields.io/badge/%F0%9F%A4%97%20Hugging%20Face-Discussion-orange'></a>
<a href='https://huggingface.co/collections/callanwu/webwalker-677f6527407edfda44098b09'><img src='https://img.shields.io/badge/%F0%9F%A4%97%20Hugging%20Face-Colloectionss-blue'></a>
<a href='https://huggingface.co/datasets/callanwu/WebWalkerQA'><img src='https://img.shields.io/badge/%F0%9F%A4%97%20Hugging%20Face-Datasets-green'></a>
<a href='https://huggingface.co/spaces/callanwu/WebWalkerQALeadeboard'><img src='https://img.shields.io/badge/%F0%9F%A4%97%20Hugging%20Face-Leaderboard-yellow'></a><br>
<a href='https://arxiv.org/pdf/2501.07572'><img src='https://img.shields.io/badge/Paper-arXiv-red'></a>

<!-- **Authors:** -->
<br>

_**Jialong Wu, Wenbiao Yin, Yong Jiang, Zhenglin Wang, Zekun Xi, Runnan Fang**_

_**Linhai Zhang, Yulan He, Deyu Zhou, Pengjun Xie, Fei Huang<br>**_

<!-- **Affiliations:** -->

_Tongyi Lab <img src="./assets/tongyi.png" width="14px" style="display:inline;">, Alibaba Group_

👏 Welcome to try web traversal via our **[<img src="./assets/tongyi.png" width="14px" style="display:inline;"> Modelscope online demo](https://www.modelscope.cn/studios/iic/WebWalker/)** or **[🤗 Huggingface online demo](https://huggingface.co/spaces/callanwu/WebWalker)**!

<p align="center">
<a href="https://alibaba-nlp.github.io/WebWalker/">[🤖Project]</a>
<a href="https://arxiv.org/pdf/2501.07572">[📄Paper]</a>
<a href="## 🚩Citation">[🚩Citation]</a>

</div>

Repo for [_WebWalker: Benchmarking LLMs in Web Traversal_](https://arxiv.org/pdf/2501.07572)

# 📖 Quick Start

- 🌏 The **Online Demo** is available at [ModelScope](https://www.modelscope.cn/studios/jialongwu/WebWalker/) and [HuggingFace](https://huggingface.co/spaces/callanwu/WebWalker) now！

- 🤗 The **WebWalkerQA** dataset is available at[ HuggingFace Datasets](https://huggingface.co/datasets/callanwu/WebWalkerQA)!

- 🤗 The **WebWalkerQA** Leaderborad is available at[ HuggingFace Space](https://huggingface.co/spaces/callanwu/WebWalkerQALeadeboard)!

<img src="assets/demo.gif">

# 📌 Introduction

- We construct a challenging benchmark, **WebWalkerQA**, which is composed of **680** queries from four real-world scenarios across over **1373** webpages.
- To tackle the challenge of web-navigation tasks requiring long context, we propose **WebWalker**, which utilizes a multi-agent framework for effective memory management.
- Extensive experiments show that the WebWalkerQA is **challenging**, and for information-seeking tasks, **vertical exploration** within the page proves to be beneficial.

<div align="center">
    <img src="assets/method.jpg" width="80%" height="auto" />
</div>

# 📚 WebWalkerQA Dataset

The json item of WebWalkerQA dataset is organized in the following format:

```json
{
  "Question": "When is the paper submission deadline for the ACL 2025 Industry Track, and what is the venue address for the conference?",
  "Answer": "The paper submission deadline for the ACL 2025 Industry Track is March 21, 2025. The conference will be held in Brune-Kreisky-Platz 1.",
  "Root_Url": "https://2025.aclweb.org/",
  "Info": {
    "Hop": "multi-source",
    "Domain": "Conference",
    "Language": "English",
    "Difficulty_Level": "Medium",
    "Source_Website": [
      "https://2025.aclweb.org/calls/industry_track/",
      "https://2025.aclweb.org/venue/"
    ],
    "Golden_Path": ["root->call>student_research_workshop", "root->venue"]
  }
}
```

🤗 The WebWalkerQA Leaderboard is is available at[ HuggingFace](https://huggingface.co/spaces/callanwu/WebWalkerQALeadeboard)!

You can load the dataset via the following code:

```python
from datasets import load_dataset
ds = load_dataset("callanwu/WebWalkerQA", split="main")
```

Additionally, we possess a collection of approximately 14k silver QA pairs, which, although not yet carefully human-verified.
You can load the silver dataset by changing the split to `silver`.

## 💡 Perfomance

### 📊 Result on Web Agents

The performance on Web Agents are shown below:

<div align="center">
    <img src="assets/agent_result.jpg" width="80%" height="auto" />
</div>

### 📊 Result on RAG-Systems

<div align="center">
    <img src="assets/rag_result.jpg" width="80%" height="auto" />
</div>

🤗 The WebWalkerQA Leaderboard is is available at[ HuggingFace](https://huggingface.co/spaces/callanwu/WebWalkerQALeadeboard)!

🚩 Welcome to submit your method to the leaderboard!

# 🛠 Dependencies

```bash
conda create -n webwalker python=3.10
git clone https://github.com/alibaba-nlp/WebWalker.git
cd WebWalker

# Install requirements
pip install -r requirements.txt
# Run post-installation setup
crawl4ai-setup
# Verify your installation
crawl4ai-doctor
```

### 💻 Running WebWalker Demo Locally

🔑 Before running, please export the OPENAI API key or Dashscope API key as an environment variable:

```bash
export OPEN_AI_API_KEY=YOUR_API_KEY
export OPEN_AI_API_BASE_URL=YOUR_API_BASE_URL
```

or

```bash
export DASHSCOPE_API_KEY=YOUR_API_KEY
```

> You can use other supported API keys with Qwen-Agent. For more details, please refer to the [Qwen-Agent](https://github.com/QwenLM/Qwen-Agent/tree/main/qwen_agent/llm). To configure the API key, modify the code in lines 44-53 of [`src/app.py`](https://github.com/Alibaba-NLP/WebWalker/blob/main/src/app.py#L44-L53).

Then, run the `app.py` file with Streamlit:

```bash
cd src
streamlit run app.py
```

### Runing RAG-System on WebWalkerQA

```bash
cd src
python rag_system.py --api_name [API_NAME] --output_file [OUTPUT_PATH]
```

The details of environment setup can be found in the [README.md](./src/README.md) in the `src` folder.

# 🔍 Evaluation

The evaluation script for accuracy of the output answers using GPT-4 can be used as follows:

```bash
cd src
python evaluate.py --input_path [INPUT_PATH]--output_path [OUTPUT_PATH]
```

## 🌻Acknowledgement

- This work is implemented by [ReACT](https://github.com/ysymyth/ReAct), [Qwen-Agents](https://github.com/QwenLM/Qwen-Agent), [LangChain](https://github.com/langchain-ai/langchain). Sincere thanks for their efforts.
- We sincerely thank the contributors and maintainers of [Crawl4AI](https://github.com/unclecode/crawl4ai) for their open-source tool❤️, which helped us get web pages in a Markdown-like format.

  <a href="https://github.com/unclecode/crawl4ai">
  <img src="https://raw.githubusercontent.com/unclecode/crawl4ai/main/docs/assets/powered-by-disco.svg" alt="Powered by Crawl4AI" width="100"/>
</a>

- The repo is contributed by [Jialong Wu](https://callanwu.github.io/), if you have any questions, please feel free to contact via jialongwu@alibaba-inc.com or jialongwu@seu.edu.cn or create an issue.

## 🚩Citation

If this work is helpful, please kindly cite as:

```bigquery
@misc{wu2025webwalker,
      title={WebWalker: Benchmarking LLMs in Web Traversal},
      author={Jialong Wu and Wenbiao Yin and Yong Jiang and Zhenglin Wang and Zekun Xi and Runnan Fang and Deyu Zhou and Pengjun Xie and Fei Huang},
      year={2025},
      eprint={2501.07572},
      archivePrefix={arXiv},
      primaryClass={cs.CL},
      url={https://arxiv.org/abs/2501.07572},
}
```

## Star History

<div align="center">

[![Star History Chart](https://api.star-history.com/svg?repos=Alibaba-NLP/WebAgent&type=Date)](https://www.star-history.com/#Alibaba-NLP/WebAgent&Date)

</div>

```

> 说明：以上为关键代码片段，结合上下文解释其作用与调用关系。

## 六、补充注释与论文要点对齐（精细解读）

### 1）`src/agent.py` 总体逻辑与论文“探索-评审”范式对齐
- ReAct 主循环（`_run`）严格遵循论文的“Thought → Action → Observation”链；每次工具返回 Observation 后，调用两个阶段函数：
  - `observation_information_extraction`：判断 Observation 是否含与 Query 相关的“有效信息”，若有则结构化提取并存入 `self.momery`。
  - `critic_information`：对累计 `memory` 进行“能否回答”的判定；若足够则输出 `Final Answer` 并停止探索。
- 这一流程与论文中“横向/纵向整合”的思想一致：多步点击（纵向深入网页层级）+ 多条信息的聚合记忆（横向整合来源）。

注：`self.extra_generate_cfg` 中的 `stop=['Observation:', 'Observation:\n']` 对流式中止点尤为关键，可避免模型在应当让工具继续工作的时刻“跑偏”生成。

### 2）`src/app.py` 的工具抽象与动作空间约束
- `@register_tool('visit_page')` 将动作空间严格收敛为“点击按钮文本”。系统把 `<button>文本` → URL 的映射缓存在 `BUTTON_URL_ADIC.json` 中。
- 优点：
  - 将“浏览器复杂 DOM 操作”抽象为“点击一个按钮文本”，极大简化了模型决策空间，降低无关动作与失败率。
  - 工具返回 Markdown 化页面与新一轮按钮列表，为下一轮 ReAct 提供了结构化 Observation。

### 3）与 RAG 的结合位置与价值
- 论文中强调 RAG 与站点遍历的互补性：RAG 做外部横向检索，WebWalker 做站内纵向深挖；在代码中，这体现在：
  - ReAct Prompt（`prompts.py/SYSTEM_EXPLORER`）强制“每步必须行动”，避免“纯语言反刍”；
  - 工具在 Observation 中提供结构化内容，后续可被外部检索/记忆模块二次利用（虽然当前 demo 里未直接调用外部检索，但接口设计上是兼容的）。

### 4）工程注意点（给上手者）
- 建议对 `extract_links_with_text` 的规则再做细化（如适应更多 SPA 框架、懒加载、遮罩层等）。
- `momery` 命名应更正为 `memory`，同时考虑去重、合并策略，避免冗余。
- 若要训练/评估端到端智能体：将 `critic_information` 的“足够/不足”判定信号用于奖励设计，能更稳定地驱动 RL 采样。


### 文件：`WebAgent/WebWalker/src/agent.py`

```py
import json
from typing import Dict, Iterator, List, Literal, Optional, Tuple, Union

from qwen_agent.agents.fncall_agent import FnCallAgent
from qwen_agent.llm import BaseChatModel
from qwen_agent.llm.schema import ASSISTANT, DEFAULT_SYSTEM_MESSAGE, Message
from qwen_agent.settings import MAX_LLM_CALL_PER_RUN
from qwen_agent.tools import BaseTool
from qwen_agent.utils.utils import format_as_text_message, merge_generate_cfgs
from openai import OpenAI
import time
from prompts import *


TOOL_DESC = (
    '{name_for_model}: Call this tool to interact with the {name_for_human} API. '
    'What is the {name_for_human} API useful for? {description_for_model} Parameters: {parameters} {args_format}')

class WebWalker(FnCallAgent):
    """This explorer agent use ReAct format to call tools"""

    def __init__(self,
                 function_list: Optional[List[Union[str, Dict, BaseTool]]] = None,
                 llm: Optional[Union[Dict, BaseChatModel]] = None,
                 system_message: Optional[str] = DEFAULT_SYSTEM_MESSAGE,
                 name: Optional[str] = None,
                 description: Optional[str] = None,
                 files: Optional[List[str]] = None,
                 **kwargs):
        super().__init__(function_list=function_list,
                         llm=llm,
                         system_message=system_message,
                         name=name,
                         description=description,
                         files=files,
                         **kwargs)
        self.extra_generate_cfg = merge_generate_cfgs(
            base_generate_cfg=self.extra_generate_cfg,
            new_generate_cfg={'stop': ['Observation:', 'Observation:\n']},
        )
        self.client = OpenAI(
            api_key=llm['api_key'], 
            base_url=llm['model_server'],
        )
        self.llm_cfg = llm
        self.momery = []

    def observation_information_extraction(self, query, observation):
        user_prompt = "- Query: {query}\n- Observation: {observation}".format(query=query, observation=observation)
        messages = [
            {'role': 'system', 'content': STSTEM_CRITIIC_INFORMATION},
            {'role': 'user', 'content':  user_prompt}]
        max_retries = 10
        for attempt in range(max_retries):
            try:
                response = self.client.chat.completions.create(
                    model=self.llm_cfg['model'],
                    response_format={"type": "json_object"},
                    messages=messages
                )
                print(response.choices[0].message.content)
                # response_content = json.loads(response.choices[0].message.content)
                if "true" in response.choices[0].message.content:
                    try:
                        return json.loads(response.choices[0].message.content)["information"]
                    except:
                        return response.choices[0].message.content
                else:
                    return None
            except Exception as e:
                print(e)
                if attempt < max_retries - 1:
                    time.sleep(1 * (2 ** attempt))  # Exponential backoff
                else:
                    raise e  # Raise the exception if the last retry fails

    def critic_information(self, query, memory):  
        memory = "-".join(memory)
        user_prompt = "- Query: {query}\n- Accumulated Information: {memory}".format(query = query, memory=memory)
        messages = [
            {'role': 'system', 'content': STSTEM_CRITIIC_ANSWER},
            {'role': 'user', 'content': user_prompt}]
        response = self.client.chat.completions.create(
            model=self.llm_cfg['model'],
            response_format={"type": "json_object"},
            messages=messages
        )
        max_retries = 10
        for attempt in range(max_retries):
            try:
                response = self.client.chat.completions.create(
                    model=self.llm_cfg['model'],
                    response_format={"type": "json_object"},
                    messages=messages
                )
                print(response.choices[0].message.content)
                if "true" in response.choices[0].message.content:
                    try:
                        return json.loads(response.choices[0].message.content)["answer"]
                    except:
                        return response.choices[0].message.content
                else:
                    return None
            
            except Exception as e:
                print(e)
                if attempt < max_retries - 1:
                    time.sleep(1 * (2 ** attempt))  # Exponential backoff
                else:
                    raise e  # Raise the exception if the last retry fails

    def _run(self, messages: List[Message], lang: Literal['en', 'zh'] = 'en', **kwargs) -> Iterator[List[Message]]:
        text_messages = self._prepend_react_prompt(messages, lang=lang)
        num_llm_calls_available = MAX_LLM_CALL_PER_RUN
        response: str = 'Thought: '
        query = self.llm_cfg["query"]
        action_count = self.llm_cfg.get("action_count", MAX_LLM_CALL_PER_RUN)
        num_llm_calls_available = action_count
        while num_llm_calls_available > 0:
            num_llm_calls_available -= 1
            output = []
            for output in self._call_llm(messages=text_messages):
                if output:
                    yield [Message(role=ASSISTANT, content=output[-1].content)]
            # Accumulate the current response
            if output:
                response += output[-1].content

            has_action, action, action_input, thought = self._detect_tool("\n"+output[-1].content)
            if not has_action:
                if "Final Answer: " in output[-1].content:
                    break
                else:
                    continue

            # Add the tool result
            query = self.llm_cfg["query"]
            observation = self._call_tool(action, action_input, messages=messages, **kwargs)
            stage1 = self.observation_information_extraction(query, observation)
            if stage1:
                self.momery.append(stage1+"\n")
                if len(self.momery) > 1:
                    yield [Message(role=ASSISTANT, content= "Memory:\n" + "-".join(self.momery)+"\"}")]
                else:
                    yield [Message(role=ASSISTANT, content= "Memory:\n" + "-" + self.momery[0]+"\"}")]
                stage2 = self.critic_information(query, self.momery)
                if stage2:
                    response = f'Final Answer: {stage2}'
                    yield [Message(role=ASSISTANT, content=response)]
                    break


            observation = f'\nObservation: {observation}\nThought: '
            response += observation
            # yield [Message(role=ASSISTANT, content=response)]

            if (not text_messages[-1].content.endswith('\nThought: ')) and (not thought.startswith('\n')):
                # Add the '\n' between '\nQuestion:' and the first 'Thought:'
                text_messages[-1].content += '\n'
            if action_input.startswith('```'):
                # Add a newline for proper markdown rendering of code
                action_input = '\n' + action_input
            text_messages[-1].content += thought + f'\nAction: {action}\nAction Input: {action_input}' + observation
            # print(text_messages[-1].content)

    def _prepend_react_prompt(self, messages: List[Message], lang: Literal['en', 'zh']) -> List[Message]:
        tool_descs = []
        for f in self.function_map.values():
            function = f.function
            name = function.get('name', None)
            name_for_human = function.get('name_for_human', name)
            name_for_model = function.get('name_for_model', name)
            assert name_for_human and name_for_model
            args_format = function.get('args_format', '')
            tool_descs.append(
                TOOL_DESC.format(name_for_human=name_for_human,
                                 name_for_model=name_for_model,
                                 description_for_model=function['description'],
                                 parameters=json.dumps(function['parameters'], ensure_ascii=False),
                                 args_format=args_format).rstrip())
        tool_descs = '\n\n'.join(tool_descs)
        tool_names = ','.join(tool.name for tool in self.function_map.values())
        text_messages = [format_as_text_message(m, add_upload_info=True, lang=lang) for m in messages]
        text_messages[-1].content = SYSTEM_EXPLORER.format(
            tool_descs=tool_descs,
            tool_names=tool_names,
            query=text_messages[-1].content,
        )
        return text_messages

    def _detect_tool(self, text: str) -> Tuple[bool, str, str, str]:
        special_func_token = '\nAction:'
        special_args_token = '\nAction Input:'
        special_obs_token = '\nObservation:'
        func_name, func_args = None, None
        i = text.rfind(special_func_token)
        j = text.rfind(special_args_token)
        k = text.rfind(special_obs_token)
        if 0 <= i < j:  # If the text has `Action` and `Action input`,
            if k < j:  # but does not contain `Observation`,
                # then it is likely that `Observation` is ommited by the LLM,
                # because the output text may have discarded the stop word.
                text = text.rstrip() + special_obs_token  # Add it back.
            k = text.rfind(special_obs_token)
            func_name = text[i + len(special_func_token):j].strip()
            func_args = text[j + len(special_args_token):k].strip()
            text = text[:i]  # Return the response before tool call, i.e., `Thought`
        return (func_name is not None), func_name, func_args, text

```

> 说明：以上为关键代码片段，结合上下文解释其作用与调用关系。

### 文件：`WebAgent/WebWalker/src/rag_system.py`

```py
import asyncio
import json
import os
import aiohttp
import requests
import concurrent.futures
from tenacity import retry, stop_after_attempt, wait_exponential
from openai import AsyncOpenAI, OpenAI
from openai.types.chat.chat_completion import Choice
from volcenginesdkarkruntime import Ark
from tqdm.asyncio import tqdm
from typing import Dict, Any
from datasets import load_dataset

# openai_env
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL")
# gemini_env
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_BASE_URL = os.getenv("GEMINI_BASE_URL")
# ark_env
ARK_API_KEY = os.getenv("ARK_API_KEY")
ARK_MODEL = os.getenv("ARK_MODEL")
# moonshot_env
MOONSHOT_API_KEY = os.getenv("MOONSHOT_API_KEY")
# baidu_env
BAIDU_API_KEY = os.getenv("BAIDU_API_KEY")
BAIDU_SECRET_KEY = os.getenv("BAIDU_SECRET_KEY")

def o1_api(ds, output_path):
    if OPENAI_BASE_URL is None or OPENAI_API_KEY is None:
        print("Please set OPENAI_API_KEY and OPENAI_BASE_URL environment variables.")
        return
    client = AsyncOpenAI(base_url=OPENAI_BASE_URL, api_key=OPENAI_API_KEY)
    model = "o1-preview-2024-09-12"
    MAX_CONCURRENT = 16

    @retry(stop=stop_after_attempt(10), wait=wait_exponential(min=4, max=60))
    async def get_chat_completion(message, semaphore) -> str:
        try:
            async with semaphore:
                response = await client.chat.completions.create(
                    model=model,
                    messages=[{"role": "user", "content": message["question"]}],
                    timeout=80
                )
                message["pred"] = response.choices[0].message.content
                return message
        except Exception as e:
            print(f"Error in get_chat_completion for message  {type(e).__name__} - {str(e)}")
            raise

    async def request_model(prompts):
        semaphore = asyncio.Semaphore(MAX_CONCURRENT)
        tasks = [get_chat_completion(prompt, semaphore) for prompt in prompts]
        
        for future in tqdm.as_completed(tasks, total=len(tasks), desc="Processing prompts"):
            result = await future
            with open(output_path, "a", encoding="utf-8") as f:
                f.write(json.dumps(result, ensure_ascii=False) + "\n")

    visited = []
    if os.path.exists(output_path):
        with open(output_path, "r", encoding="utf-8") as f:
            visited = [json.loads(line)["question"] for line in f]
    prompts = []
    for item in ds["question"]:
        if item not in visited:
            temp = {"question": item}
            prompts.append(temp)

    asyncio.run(request_model(prompts))

def gemini_api(ds, output_path, search=False):
    if GEMINI_API_KEY is None or GEMINI_BASE_URL is None:
        print("Please set GEMINI_API_URL and GEMINI_AUTH_TOKEN environment variables.")
        return
    headers = {
        'Authorization': f'Bearer {GEMINI_API_KEY}',
        'Content-Type': 'application/json'
    }
    MAX_CONCURRENT = 16

    async def fetch(session, url, headers, data, semaphore, query_text):
        async with semaphore:
            return query_text, await _fetch_with_retry(session, url, headers, data)

    @retry(stop=stop_after_attempt(10), wait=wait_exponential(min=4, max=60), reraise=True)
    async def _fetch_with_retry(session, url, headers, data):
        async with session.post(url, headers=headers, json=data) as response:
            if response.status != 200:
                print(f"Error: {response.status} - {response.reason}")
            response.raise_for_status()
            return await response.json()

    async def run_gemini_api():
        if not os.path.exists(output_path):
            open(output_path, "w").close()
        with open(output_path, "r", encoding="utf-8") as f:
            visited = [json.loads(line)["question"] for line in f]
        data_list = []
        for item in ds["question"]:
            if item not in visited:
                data_list.append(item)
        semaphore = asyncio.Semaphore(MAX_CONCURRENT)
        async with aiohttp.ClientSession() as session:
            if search:
                tasks = [
                    fetch(session, GEMINI_BASE_URL, headers, {
                        "model": "gemini-1.5-pro",
                        "contents": [
                            {"role": "user", 
                             "parts": 
                                [   
                                    {"text": query}, 
                                    {"tools": {
                                        "google_search_retrieval": {
                                            "dynamic_retrieval_config": {
                                                "mode": "MODE_DYNAMIC",
                                                "dynamic_threshold": 0
                                                } 
                                            }
                                        }
                                    }
                                ]
                            }
                        ]
                    }, semaphore, query)
                    for query in data_list
                ]
            else:
                tasks = [
                    fetch(session, GEMINI_BASE_URL, headers, {
                        "model": "gemini-1.5-pro",
                        "contents": [{"role": "user", "parts": [{"text": query}]}],
                        "candidates": 1
                    }, semaphore, query)
                    for query in data_list
                ]
            for future in tqdm.as_completed(tasks, total=len(tasks), desc="Processing queries"):
                query_text, result = await future
                adic = {"question": query_text, "pred": result["candidates"][0]["content"]["parts"][0]["text"]}
                with open(output_path, "a", encoding="utf-8") as f:
                    f.write(json.dumps(adic, ensure_ascii=False) + "\n")

    asyncio.run(run_gemini_api())

def doubao_api(ds, output_path):
    if ARK_API_KEY is None or ARK_MODEL is None:
        print("Please set ARK_API_KEY environment variable.")
        return
    client = Ark(base_url="https://ark.cn-beijing.volces.com/api/v3", api_key=ARK_API_KEY)
    MAX_WORKERS = 10

    def call(data):
        try:
            completion = client.bot_chat.completions.create(
                model=ARK_MODEL,
                messages=[
                    {"role": "system", "content": "你是豆包，是由字节跳动开发的 AI 人工智能助手"},
                    {"role": "user", "content": data["question"]}
                ]
            )
            return completion.choices[0].message.content
        except Exception as e:
            print(f"Error: {e}")
            return

    if not os.path.exists(output_path):
        open(output_path, "w").close()
    visited = set()
    with open(output_path, "r", encoding="utf-8") as f:
        visited.update(json.loads(line)["question"] for line in f)
    data_list = []
    for item in ds["question"]:
        if item not in visited:
            temp = {"question": item}
            data_list.append(temp)

    with tqdm(total=len(data_list)) as pbar:
        with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            future_to_data = {executor.submit(call, data): data for data in data_list}
            for future in concurrent.futures.as_completed(future_to_data):
                outputs = future.result()
                data = future_to_data[future]
                if outputs:
                    data["pred"] = outputs
                with open(output_path, "a", encoding="utf-8") as f:
                    f.write(json.dumps(data, ensure_ascii=False) + "\n")
                pbar.update(1)

def kimi_api(ds, output_path):
    if MOONSHOT_API_KEY is None:
        print("Please set MOONSHOT_API_KEY environment variable.")
        return
    client = OpenAI(base_url="https://api.moonshot.cn/v1", api_key=MOONSHOT_API_KEY)
    MAX_WORKERS = 4

    def search_impl(arguments: Dict[str, Any]) -> Any:
        return arguments

    def chat(messages) -> Choice:
        try:
            completion = client.chat.completions.create(
                model="moonshot-v1-128k",
                messages=messages,
                temperature=0.3,
                tools=[{
                    "type": "builtin_function",
                    "function": {"name": "$web_search"}
                }]
            )
            return completion.choices[0]
        except Exception as e:
            print(f"Error: {e}")
            return

    if not os.path.exists(output_path):
        open(output_path, "w").close()
    
    visited = set()
    with open(output_path, "r", encoding="utf-8") as f:
        visited.update(json.loads(line)["question"] for line in f)

    data_list = []
    for item in ds["question"]:
        if item not in visited:
            temp = {"question": item}
            data_list.append(temp)
    def process_data(data):
        messages = [{"role": "system", "content": "你是 Kimi。"}, {"role": "user", "content": data["question"]}]
        finish_reason = None
        while finish_reason is None or finish_reason == "tool_calls":
            choice = chat(messages)
            finish_reason = choice.finish_reason
            if finish_reason == "tool_calls":
                messages.append(choice.message)
                for tool_call in choice.message.tool_calls:
                    tool_result = search_impl(json.loads(tool_call.function.arguments))
                    messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "name": tool_call.function.name,
                        "content": json.dumps(tool_result),
                    })
        data["pred"] = choice.message.content
        return data

    with tqdm(total=len(data_list)) as pbar:
        with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            future_to_data = {executor.submit(process_data, data): data for data in data_list}
            for future in concurrent.futures.as_completed(future_to_data):
                processed_data = future.result()
                with open(output_path, "a", encoding="utf-8") as f:
                    f.write(json.dumps(processed_data, ensure_ascii=False) + "\n")
                pbar.update(1)

def wenxin_api(ds, output_path):
    if BAIDU_API_KEY is None or BAIDU_SECRET_KEY is None:
        print("Please set BAIDU_API_KEY and BAIDU_SECRET_KEY environment variables.")
        return
    
    def get_access_token():
        url = f"https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={BAIDU_API_KEY}&client_secret={BAIDU_SECRET_KEY}"
        response = requests.post(url, headers={'Content-Type': 'application/json'})
        return response.json().get("access_token")

    url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/completions_pro?access_token=" + get_access_token()

    def call(data):
        payload = json.dumps({
            "messages": [{"role": "user", "content": data["question"]}]
        })
        headers = {'Content-Type': 'application/json'}
        response = requests.post(url, headers=headers, data=payload)
        return response.json()["result"]

    if not os.path.exists(output_path):
        open(output_path, "w").close()
    
    visited = set()
    with open(output_path, "r", encoding="utf-8") as f:
        visited.update(json.loads(line)["question"] for line in f)
    
    data_list = []
    for item in ds["question"]:
        if item not in visited:
            temp = {"question": item}
            data_list.append(temp)

    with tqdm(total=len(data_list)) as pbar:
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            future_to_data = {executor.submit(call, data): data for data in data_list}
            for future in concurrent.futures.as_completed(future_to_data):
                outputs = future.result(timeout=10)
                data = future_to_data[future]
                data["pred"] = outputs
                with open(output_path, "a", encoding="utf-8") as f:
                    f.write(json.dumps(data, ensure_ascii=False) + "\n")
                pbar.update(1)

def main(api_name, output_path):
    ds = load_dataset("callanwu/WebWalkerQA", split="main")
    api_functions = {
        "o1_api": o1_api,
        "gemini_api": gemini_api,
        "gemini_search_api": gemini_api,
        "doubao_api": doubao_api,
        "kimi_api": kimi_api,
        "wenxin_api": wenxin_api,
    }
    if api_name == "all":
        for api in api_functions:
            print(api)
            print(output_path + "/" + api+"_result.jsonl")
            os.makedirs(output_path, exist_ok=True)
            if api != "gemini_search_api":
                api_functions[api](ds, output_path + "/" + api+"_result.jsonl")
            else:
                api_functions[api](ds, output_path + "/" + api+"_result.jsonl", search=True)
    else:
        if api_name in api_functions:
            if api_name == "gemini_search_api":
                gemini_api(ds, output_path, search=True)
            asyncio.run(api_functions[api_name](ds, output_path))
        else:
            print(f"API {api_name} is not supported.")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Run different API models.")
    parser.add_argument("--api_name", type=str, help="Name of the API to run.")
    parser.add_argument("--output_path", type=str, help="Path to the output file. If api_name is 'all', this should be a directory. If api_name is others, this should be a file.")
    args = parser.parse_args()
    main(args.api_name, args.output_path)
```

> 说明：以上为关键代码片段，结合上下文解释其作用与调用关系。

### 文件：`WebAgent/WebWalker/src/app.py`

```py
import streamlit as st
import os
import json5
from agent import WebWalker
from qwen_agent.tools.base import BaseTool, register_tool
import os
import re
import json
import asyncio
from utils import *
import base64
from PIL import Image
from bs4 import BeautifulSoup



if 'DASHSCOPE_API_KEY' not in os.environ and 'OPENAI_API_KEY' not in os.environ:
    raise ValueError("Please set the environment variable 'DASHSCOPE_API_KEY' or 'OPENAI_API_KEY' to your API key.")
if 'DASHSCOPE_API_KEY' in os.environ:
    model = "qwen-plus"
    llm_cfg = {
        'model': model,
        'api_key': os.getenv('DASHSCOPE_API_KEY'),
        'model_server': "https://dashscope.aliyuncs.com/compatible-mode/v1" ,
        'generate_cfg': {
                'top_p': 0.8,
                'max_input_tokens': 120000,
                'max_retries': 20
        },
    }
if 'OPENAI_API_KEY' in os.environ and 'OPENAI_MODEL_SERVER' in os.environ:
    model = "gpt-4o"
    llm_cfg = {
        'model': model,
        'api_key': os.getenv('OPENAI_API_KEY'),
        'model_server': os.getenv('OPENAI_MODEL_SERVER'),
        'generate_cfg': {
                'top_p': 0.8,
                'max_input_tokens': 120000,
                'max_retries': 20
        },
    }
"""
llm_cfg = {
    'model': model,
    'api_key': api_key,
    'model_server': model_server,
    'generate_cfg': {
            'top_p': 0.8,
            'max_input_tokens': 120000,
            'max_retries': 20
    },
}
"""

def extract_links_with_text(html):
    """
    Args:
        html (str): html content
    
    Returns:
        str: clickable buttons
    """
    with open("ROOT_URL.txt", "r") as f:
        ROOT_URL = f.read()
    soup = BeautifulSoup(html, 'html.parser')
    links = []

    for a_tag in soup.find_all('a', href=True):
        url = a_tag['href']
        text = ''.join(a_tag.stripped_strings)
        
        if text and "javascript" not in url and not url.endswith(('.jpg', '.png', '.gif', '.jpeg', '.pdf')):
            if process_url(ROOT_URL, url).startswith(ROOT_URL):
                links.append({'url': process_url(ROOT_URL, url), 'text': text})

    for a_tag in soup.find_all('a', onclick=True):
        onclick_text = a_tag['onclick']
        text = ''.join(a_tag.stripped_strings)
        
        match = re.search(r"window\.location\.href='([^']*)'", onclick_text)
        if match:
            url = match.group(1)
            if url and text  and not url.endswith(('.jpg', '.png', '.gif', '.jpeg', '.pdf')):
                if process_url(ROOT_URL, url).startswith(ROOT_URL):
                    links.append({'url': process_url(ROOT_URL, url), 'text': text})

    for a_tag in soup.find_all('a', attrs={'data-url': True}):
        url = a_tag['data-url']
        text = ''.join(a_tag.stripped_strings)
        if url and text and not url.endswith(('.jpg', '.png', '.gif', '.jpeg', '.pdf')):
            if process_url(ROOT_URL, url).startswith(ROOT_URL):
                links.append({'url': process_url(ROOT_URL, url), 'text': text})

    for a_tag in soup.find_all('a', class_='herf-mask'):
        url = a_tag.get('href')
        text = a_tag.get('title') or ''.join(a_tag.stripped_strings)
        if url and text and not url.endswith(('.jpg', '.png', '.gif', '.jpeg', '.pdf')):
            if process_url(ROOT_URL, url).startswith(ROOT_URL):
                    links.append({'url': process_url(ROOT_URL, url), 'text': text})

    for button in soup.find_all('button', onclick=True):
        onclick_text = button['onclick']
        text = button.get('title') or button.get('aria-label') or ''.join(button.stripped_strings)
        match = re.search(r"window\.location\.href='([^']*)'", onclick_text)
        if match:
            url = match.group(1)
            if url and text:
                if process_url(ROOT_URL, url).startswith(ROOT_URL):
                    links.append({'url': process_url(ROOT_URL, url), 'text': text})

    unique_links = {f"{item['url']}_{item['text']}": item for item in links}  # 去重

    if not os.path.exists("BUTTON_URL_ADIC.json"):
        with open("BUTTON_URL_ADIC.json", "w") as f:
            json.dump({}, f)
    with open("BUTTON_URL_ADIC.json", "r") as f:
        BUTTON_URL_ADIC = json.load(f)
    for temp in list(unique_links.values()):
        BUTTON_URL_ADIC[temp["text"]] = temp["url"]
    with open("BUTTON_URL_ADIC.json", "w") as f:
        json.dump(BUTTON_URL_ADIC, f)
    info = ""
    for i in list(unique_links.values()):
        info += "<button>" + i["text"] + "<button>" + "\n"
    return info

if __name__ == "__main__":
    st.title('🤝WebWalker')
    st.markdown("### 📚Introduction")
    st.markdown("👋Welcome to WebWalker! WebWalker is a web-based conversational agent that can help you navigate websites and find information.")
    st.markdown("📑The paper of WebWalker is available at [arXiv]().")
    st.markdown("✨You can bulid your own WebWalker by following the [instruction](https://github.com/Alibaba-NLP/WebWalker).")
    st.markdown("🙋If you have any questions, please feel free to contact us via the [Github issue](https://github.com/Alibaba-NLP/WebWalker/issue).")
    st.markdown("### 🚀Let's start exploring the website!")
    if 'form_1_text' not in st.session_state:
        st.session_state.form_1_text = ""
    if 'form_2_text' not in st.session_state:
        st.session_state.form_2_text = ""

    with st.sidebar:
        MAX_ROUNDS = st.number_input('Max Count Count：', min_value=1, max_value=15, value=10, step=1)
        website_example = st.sidebar.selectbox('Example Website：', ['https://2025.aclweb.org/'])
        question_example = st.sidebar.selectbox('Example Query：', ["When is the paper submission deadline for ACL 2025 Industry Track, and what is the venue specific address?", "Who is the general chair of ACL 2025?", "What is the spcial theme of ACL 2025?"])

    col1, col2 = st.columns([3, 1]) 
    with col1:
        with st.form(key='my_form'):
            form_1_text = st.text_area("**🤯Memory**", value="No Memory", height=68)
            website = st.text_area('👉Website', value=website_example, placeholder='Input the website you want to walk through.')
            query = st.text_area('🤔Query', value=question_example, placeholder='Input the query you want to ask.')
            submit_button = st.form_submit_button('Start!!!!')
            
            if submit_button:
                if website and query:
                    tools = ["visit_page"]  
                    llm_cfg["query"] = query
                    llm_cfg["action_count"] = MAX_ROUNDS
                    bot = WebWalker(llm=llm_cfg,
                        function_list=tools
                        )
                    BUTTON_URL_ADIC = {}
                    ROOT_URL = website
                    with open("ROOT_URL.txt", "w") as f:
                        f.write("https://2025.aclweb.org/")
                    messages = []  # This stores the chat history.
                    visited_links = []
                    start_prompt = "query:\n{query} \nofficial website:\n{website}".format(query=query, website=website)
                    st.markdown('**🌐Now visit**')
                    st.write(website)
                    html, markdown, screenshot = asyncio.run(get_info(website))
                    with col2:
                        st.markdown('**📸Observation**')
                        if screenshot:
                            st.session_state.image_index = 0
                            print("get screenshot!")
                            image_folder = "images/"
                            if not os.path.exists(image_folder):
                                os.makedirs(image_folder)
                            with open(image_folder+str(st.session_state.image_index)+".png", "wb") as f:
                                f.write(base64.b64decode(screenshot))
                            image_files = os.listdir(image_folder)
                            image_files = [f for f in image_files if f.endswith(('.png', '.jpg', '.jpeg'))]
                            image_path = os.path.join(image_folder, image_files[st.session_state.image_index])
                            image = Image.open(image_folder+str(st.session_state.image_index)+".png")
                            st.image(image, caption='Start Obervation', width=400)
                        
                    buttons = extract_links_with_text(html)
                    response = "website information:\n\n" + markdown + "\n\n"
                    response += "clickable button:\n\n" + buttons + "\n\nEach button is wrapped in a <button> tag"
                    start_prompt += "\nObservation:" + response + "\n\n"
                    messages.append({'role': 'user', 'content':start_prompt})
                    cnt = 0
                    response = []
                    response = bot.run(messages=messages, lang = "zh")
                    for i in response:
                        if "\"}" in i[0]["content"] and "Memory" not in i[0]["content"]:
                            st.markdown('**💭Thoughts**')
                            st.markdown(i[0]["content"].split("Action")[0])
                        elif "\"}" in i[0]["content"] and "Memory" in i[0]["content"]:
                            st.text_area('**🤯Memory Update**', i[0]["content"][:-2])
                        if "Final Answer" in i[0]["content"]:
                            st.session_state.answer = i[0]["content"]
                            st.markdown('**🙋Anwser**')
                            st.write(st.session_state.answer)
                else:
                    st.error('Please input the website and query.')


@register_tool('visit_page',allow_overwrite=True)
class VisitPage(BaseTool):
    """
    description: A tool that visits a webpage and extracts the content of the page.
    parameters:
        - name: url
            type: string
            description: The URL of the webpage to visit.
            required: true
    """
    description = 'A tool analyzes the content of a webpage and extracts buttons associated with sublinks. Simply input the button which you want to explore, and the tool will return both the markdown-formatted content of the corresponding page of button and a list of new clickable buttons found on the new page.'
    parameters = [{
        'name': 'button',
        'type': 'string',
        'description': 'the button you want to click',
        'required': True
    }]

            
    def call(self, params: str, **kwargs) -> str:
        if not params.strip().endswith("}"):
            if "}" in params.strip():
                params = "{" + get_content_between_a_b("{","}",params) + "}"
            else:
                if not params.strip().endswith("\""):
                    params = params.strip() + "\"}"
                else:
                    params = params.strip() + "}"
        params = "{" + get_content_between_a_b("{","}",params) + "}"
        if 'button' in json5.loads(params):
            with open("BUTTON_URL_ADIC.json", "r") as f:
                BUTTON_URL_ADIC = json.load(f)
            if json5.loads(params)['button'].replace("<button>","") in BUTTON_URL_ADIC:
                st.markdown('**👆Click Button**')
                st.write(json5.loads(params)['button'].replace("<button>",""))
                url =  BUTTON_URL_ADIC[json5.loads(params)['button'].replace("<button>","")]
                html, markdown, screenshot = asyncio.run(get_info(url))
                st.markdown('**🌐Now Visit**')
                st.write(url)
                with col2:
                    st.write("")
                    st.markdown('**📸Observation**')
                    if screenshot:
                        print("get screenshot!")
                        image_folder = "images/"
                        with open(image_folder+str(st.session_state.image_index+1)+".png", "wb") as f:
                            f.write(base64.b64decode(screenshot))
                        st.session_state.image_index += 1
                        image = Image.open(image_folder+str(st.session_state.image_index)+".png")
                        st.image(image, caption='Step ' + str(st.session_state.image_index) + ' Obervation', width=400)
                response_bottons = extract_links_with_text(html)
                response_content = markdown
                if response_content:
                    response = "The web informtaion if:\n\n" + response_content + "\n\n"
                else:
                    response = "The information of the current page is not accessible\n\n"
                response += "Clickable buttons are wrapped in <button> tag" + response_bottons
                return response
            else:
                return "The button can not be clicked, please retry a new botton!"
        else:
            return "Your input is invalid, plase output the action input correctly!"

```

> 说明：以上为关键代码片段，结合上下文解释其作用与调用关系。

### 文件：`WebAgent/WebWalker/src/evaluate.py`

```py
import os
import json
import time
import concurrent.futures
from tqdm import tqdm
from datasets import load_dataset
from langchain.evaluation import load_evaluator

# Dictionary to store questions, answers, and additional information
info_adic = {}

# Load the dataset
ds = load_dataset("callanwu/WebWalkerQA", split="main")
for question, answer, info in zip(ds["question"], ds["answer"], ds["info"]):
    info_adic[question] = [answer, info]

def eval_result(input_path, output_path):
    """
    Evaluates prediction results against reference answers and generates a report.
    
    Parameters:
        input_path (str): Path to the input predictions file.
        output_path (str): Path to save the evaluation results and report.
    """
    evaluator = load_evaluator("cot_qa")
    data_list = []
    visited = []

    # Ensure output file exists
    if not os.path.exists(output_path):
        with open(output_path, "w", encoding="utf-8") as f:
            f.write("")

    # Load already processed questions
    with open(output_path, "r", encoding="utf-8") as f:
        for line in f:
            visited.append(json.loads(line)["question"])

    # Load and filter data
    with open(input_path, "r", encoding="utf-8") as f:
        for line in f:
            data = json.loads(line)
            if data["question"] not in visited:
                data["answer"] = info_adic.get(data["question"], [None, None])[0]
                if data["answer"] is not None:
                    data_list.append(data)

    def call(data):
        """Handles evaluation retries with exponential backoff."""
        max_retries = 10
        for attempt in range(max_retries):
            try:
                return evaluator.evaluate_strings(
                    prediction=data["pred"],
                    input=data["question"],
                    reference=data["answer"]
                )
            except Exception as e:
                print(f"Error during evaluation: {e}")
                if attempt < max_retries - 1:
                    time.sleep(1 * (2 ** attempt))  # Exponential backoff
                else:
                    raise e  # Raise the exception if the last retry fails

    s = 0
    cnt = 0

    with tqdm(total=len(data_list)) as pbar:
        with concurrent.futures.ThreadPoolExecutor(max_workers=16) as executor:
            future_to_data = {executor.submit(call, data): data for data in data_list}
            for future in concurrent.futures.as_completed(future_to_data):
                try:
                    outputs = future.result(timeout=4)
                    data = future_to_data[future]
                    data["score"] = outputs["score"]

                    cnt += data["score"]
                    s += 1

                    with open(output_path, "a", encoding="utf-8") as f:
                        f.write(json.dumps(data, ensure_ascii=False) + "\n")

                    pbar.update(1)
                    print("Current accuracy:", cnt / s)

                except Exception as e:
                    print(f"Error processing data: {e}")

    # Prepare statistics for the report
    single_source_easy, single_source_medium, single_source_hard = [], [], []
    multi_source_easy, multi_source_medium, multi_source_hard = [], [], []
    overall = []

    datas = []

    # Reload processed data
    with open(output_path, "r", encoding="utf-8") as f:
        for line in f:
            item = json.loads(line)
            if item["question"] in info_adic:
                item["info"] = info_adic[item["question"]][1]
                datas.append(item)

    for temp in datas:
        score = temp.get("score")
        if score is not None:
            info = temp.get("info", {})
            q_type = info.get("type")
            difficulty = info.get("difficulty_level")

            if q_type == "single_source":
                if difficulty == "easy":
                    single_source_easy.append(score)
                elif difficulty == "medium":
                    single_source_medium.append(score)
                elif difficulty == "hard":
                    single_source_hard.append(score)

            elif q_type == "multi_source":
                if difficulty == "easy":
                    multi_source_easy.append(score)
                elif difficulty == "medium":
                    multi_source_medium.append(score)
                elif difficulty == "hard":
                    multi_source_hard.append(score)

            overall.append(score)

    # Safely compute averages to avoid division by zero
    def safe_average(scores):
        return sum(scores) / len(scores) if scores else None

    result = {
        "single_source_easy": safe_average(single_source_easy),
        "single_source_medium": safe_average(single_source_medium),
        "single_source_hard": safe_average(single_source_hard),
        "multi_source_easy": safe_average(multi_source_easy),
        "multi_source_medium": safe_average(multi_source_medium),
        "multi_source_hard": safe_average(multi_source_hard),
        "overall": safe_average(overall)
    }

    # Save the report
    report_path = output_path.split(".jsonl")[0] + "_report.json"
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--input_path", type=str, help="Input prediction result path")
    parser.add_argument("--output_path", type=str, help="Evaluation output path")
    args = parser.parse_args()

    eval_result(args.input_path, args.output_path)

```

> 说明：以上为关键代码片段，结合上下文解释其作用与调用关系。

### 文件：`WebAgent/WebWalker/src/prompts.py`

```py
SYSTEM_EXPLORER = """Digging through the buttons to find quailty sources and the right information. You have access to the following tools:

{tool_descs}

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can be repeated zero or more 20 times)

Notice:
- You must take action at every step. When you take action, you must use the tool with the correct format and output the action input.
- When you can not find the information you need, you should visit page of previous page recursively until you find the information you need.
- You can not say "I'm sorry, but I cannot assist with this request."!!! You must explore.
- You do not need to provide the final answer, but you must explore.
- Action Input should be valid JSON.

Begin!

{query}
"""

STSTEM_CRITIIC_INFORMATION = """You are an information extraction agent. Your task is to analyze the given observation and extract information relevant to the current query. You need to decide if the observation contains useful information for the query. If it does, return a JSON object with a "usefulness" value of true and an "information" field with the relevant details. If not, return a JSON object with a "usefulness" value of false.

**Input:**
- Query: "<Query>"
- Observation: "<Current Observation>"

**Output (JSON):**
{
  "usefulness": true,
  "information": "<Extracted Useful Information> using string format"
}
Or, if the observation does not contain useful information:
{
  "usefulness": false
}
Only respond with valid JSON.

"""

STSTEM_CRITIIC_ANSWER = """You are a query answering agent. Your task is to evaluate whether the accumulated useful information is sufficient to answer the current query. If it is sufficient, return a JSON object with a "judge" value of true and an "answer" field with the answer. If the information is insufficient, return a JSON object with a "judge" value of false.

**Input:**
- Query: "<Query>"
- Accumulated Information: "<Accumulated Useful Information>"


**Output (JSON):**
{
    "judge": true,
    "answer": "<Generated Answer> using string format"
}
Or, if the information is insufficient to answer the query:
{
    "judge": false
}
Only respond with valid JSON.
"""
```

> 说明：以上为关键代码片段，结合上下文解释其作用与调用关系。



## 五、如何在本仓库中复现与扩展
- 按各子项目`README.md`准备环境与数据；
- 参考`requirements.txt`安装依赖，运行提供的脚本；
- 可替换模型、修改超参以复现论文结果并做扩展。
