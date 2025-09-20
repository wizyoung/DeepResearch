# WebSailor-V2: Bridging the Chasm to Proprietary Agents via Synthetic Data and Scalable Reinforcement Learning 论文实现中文解读（含代码）

- 论文：[WebSailor-V2: Bridging the Chasm to Proprietary Agents via Synthetic Data and Scalable Reinforcement Learning](https://arxiv.org/pdf/2509.13305)
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
### 文件：`WebAgent/WebSailor/README.md`

```md
# WebSailor: Navigating Super-human Reasoning for Web Agent

<p align="center">
  <img src="./assets/websailor.png" alt="logo" width="60%"/>
</p>

![version](https://img.shields.io/badge/version-1.0.0-blue)

## 🥇 Introduction

- **WebSailor** is a complete post-training methodology designed to teach LLM agents sophisticated reasoning for complex web navigation and information-seeking tasks. It addresses the challenge of extreme uncertainty in vast information landscapes, a capability where previous open-source models lagged behind proprietary systems.

- We classify information-seeking tasks into three difficulty levels, where **Level 3** represents problems with both high uncertainty and a complex, non-linear path to a solution. To generate these challenging tasks, we introduce **SailorFog-QA**, a novel data synthesis pipeline that constructs intricate knowledge graphs and then applies information obfuscation. This process creates questions with high initial uncertainty that demand creative exploration and transcend simple, structured reasoning patterns.

- Our training process begins by generating expert trajectories and then reconstructing the reasoning to create concise, action-oriented supervision signals, avoiding the stylistic and verbosity issues of teacher models. The agent is first given a "cold start" using rejection sampling fine-tuning (RFT) on a small set of high-quality examples to establish a baseline capability. This is followed by an efficient agentic reinforcement learning stage using our **Duplicating Sampling Policy Optimization (DUPO)** algorithm, which refines the agent's exploratory strategies.

- WebSailor establishes a **new state-of-the-art for open-source agents**, achieving outstanding results on difficult benchmarks like BrowseComp-en and BrowseComp-zh. Notably, our smaller models like WebSailor-7B outperform agents built on much larger backbones, highlighting the efficacy of our training paradigm. Ultimately, WebSailor closes the performance gap to proprietary systems, achieving results on par with agents like Doubao-Search.

## 🚀 Performance Highlights

1. Evaluated on extremely difficult benchmarks including BrowseComp-en/zh, our 72B model consistently achieves the highest scores against strong baselines.
<p align="center">
  <img src="./assets/performance_general.png" alt="logo" width="80%"/>
</p>

2. A more comprehensive evaluation sees **WebSailor** emerges as the best open-source web agent, while being competitive against leading proprietary agents.
<p align="center">
  <img src="./assets/performance.jpg" alt="logo" width="80%"/>
</p>

3. Despite being trained on high-difficulty data, WebSailor generalizes well on simpler benchmarks like SimpleQA, where even the 32B results can surpass all baseline methods.
<p align="center">
  <img src="./assets/simpleqa.png" alt="logo" width="80%"/>
</p>

## 🔧 Quick Start

### Step 0: Set Up the Environment

```bash
conda create -n websailor python=3.11
pip install -r requirements.txt
```

### Step 1: Download the WebSailor model

You can download WebSailor via Hugging Face [🤗 HuggingFace](https://huggingface.co/Alibaba-NLP/WebSailor-3B).

### Step 2: Prepare the Evaluation Datasets

Only a sample file `example.jsonl` remains in `src/eval_data/` to prevent test data leakage.  
Please download the following official benchmarks and save them in the same folder with the listed filenames, following the exact JSONL format of `example.jsonl`:

- `browsecomp_en.jsonl`
- `browsecomp_zh.jsonl`
- `gaia.jsonl`
- `xbench-deepsearch.jsonl`

### Step 3: Inference with tools

We provide an example script for evaluation at /src/scripts/test.sh.

This script will launch the local SGLang Server, including both the evaluation model and the summary model (currently Qwen2.5-72B-Instruct). It will then perform inference three times. Finally, the evaluation will be conducted based on the results of these three inferences. **Please specify the model path to be evaluated, the dataset name, and the output folder name.**

_You need to specify your Google search key and Jina key in the script._

## 🎥 Demos

We provide demos for BrowseComp-en, BrowseComp-zh and Daily Use. Our model can complete highly difficult and uncertain tasks requiring massive information acquisition and complex reasoning.

<div align="center">
    <h3>BrowseComp-en</h3>
    <video src= "https://github.com/user-attachments/assets/2dc0b03a-c241-4f70-bf11-92fda28020fa"/>
</div>

<div align="center">
    <h3>BrowseComp-zh</h3>
    <video src="https://github.com/user-attachments/assets/f9aed746-ffc8-4b76-b135-715ec0eab544" />
</div>

<div align="center">
    <h3>Daily Use</h3>
    <video src="https://github.com/user-attachments/assets/1299c5a8-cee3-4a70-b68b-c5d227cf8055" />
</div>

⌛️ The deployment of models and demos will be updated soon.

## Complete Training Paradigm

### 1. Browsing Data Construction

<p align="center">
  <img src="./assets/qa_construction.png" alt="logo" width="80%"/>
</p>

Example SailorFog-QA data samples can be found at: [dataset/sailorfog-QA.jsonl](dataset/sailorfog-QA.jsonl)

### 2. Trajectory Sampling

<p align="center">
  <img src="./assets/traj.png" alt="logo" width="80%"/>
</p>

The sampled trajectory data will be released soon🔥🔥🔥

### 3. Reinforcement Learning

We propose **Duplicating Sampling Policy Optimization (DUPO)** to further train our model after the RFT cold-start stage. We use [verl](https://github.com/volcengine/verl) for RL training.


## 📑 Citation

If this work is helpful, please kindly cite as:

```bigquery
@article{li2025websailor,
  title={WebSailor: Navigating Super-human Reasoning for Web Agent},
  author={Li, Kuan and Zhang, Zhongwang and Yin, Huifeng and Zhang, Liwen and Ou, Litu and Wu, Jialong and Yin, Wenbiao and Li, Baixuan and Tao, Zhengwei and Wang, Xinyu and others},
  journal={arXiv preprint arXiv:2507.02592},
  year={2025}
}

```

> 说明：以上为关键代码片段，结合上下文解释其作用与调用关系。

### 文件：`WebAgent/WebSailor/src/tool_visit.py`

```py
import json
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Union
import requests
from qwen_agent.tools.base import BaseTool, register_tool
from prompt import EXTRACTOR_PROMPT 
import os 
from openai import OpenAI
import random


WEBCONTENT_MAXLENGTH = int(os.getenv("WEBCONTENT_MAXLENGTH", 150000))
IGNORE_JINA = os.getenv("IGNORE_JINA", "false").lower() == "true"
# Visit Tool (Using Jina Reader)
JINA_READER_URL_PREFIX = "https://r.jina.ai/"

JINA_API_KEY = os.getenv("JINA_API_KEY")


@register_tool('visit', allow_overwrite=True)
class Visit(BaseTool):
    # The `description` tells the agent the functionality of this tool.
    name = 'visit'
    description = 'Visit webpage(s) and return the summary of the content.'
    # The `parameters` tell the agent what input parameters the tool has.
    parameters = {
    "type": "object",
    "properties": {
        "url": {
            "type": ["string", "array"],
            "items": {
                "type": "string"
                },
            "minItems": 1,
            "description": "The URL(s) of the webpage(s) to visit. Can be a single URL or an array of URLs."
      },
      "goal": {
            "type": "string",
            "description": "The goal of the visit for webpage(s)."
      }
    },
    "required": ["url", "goal"]
  }
    # The `call` method is the main function of the tool.
    def call(self, params: Union[str, dict], **kwargs) -> str:
        try:
            url = params["url"]
            goal = params["goal"]
        except:
            return "[Visit] Invalid request format: Input must be a JSON object containing 'url' and 'goal' fields"

        if isinstance(url, str):
            response = self.readpage(url, goal)
        else:
            response = []
            assert isinstance(url, List)
            with ThreadPoolExecutor(max_workers=3) as executor:
                futures = {executor.submit(self.readpage, u, goal): u for u in url}
                for future in as_completed(futures):
                    try:
                        response.append(future.result())
                    except Exception as e:
                        response.append(f"Error fetching {futures[future]}: {str(e)}")
            response = "\n=======\n".join(response)
        
        print(f'Summary Length {len(response)}; Summary Content {response}')
        return response.strip()
    
    def call_server(self, msgs, max_tries=10):
        # 设置 OpenAI 的 API 密钥和 API 基础 URL 使用 vLLM 的 API 服务器。
        openai_api_key = "EMPTY"
        openai_api_base = "http://127.0.0.1:6002/v1"

        client = OpenAI(
            api_key=openai_api_key,
            base_url=openai_api_base,
        )
        for attempt in range(max_tries):
            try:
                chat_response = client.chat.completions.create(
                    model='/path/qwen2.5-instruct-72b',
                    messages=msgs,
                    stop=["\n<tool_response>", "<tool_response>"],
                    temperature=0.7
                )
                content = chat_response.choices[0].message.content
                if content:
                    try:
                        json.loads(content)
                    except:
                        # extract json from string 
                        left = content.find('{')
                        right = content.rfind('}') 
                        if left != -1 and right != -1 and left <= right: 
                            content = content[left:right+1]
                    return content
            except:
                if attempt == (max_tries - 1):
                    return ""
                continue

    def jina_readpage(self, url: str) -> str:
        """
        Read webpage content using Jina service.
        
        Args:
            url: The URL to read
            goal: The goal/purpose of reading the page
            
        Returns:
            str: The webpage content or error message
        """
        headers = {
            "Authorization": f"Bearer {JINA_API_KEY}",
        }
        max_retries = 3
        timeout = 10
        
        for attempt in range(max_retries):
            try:
                response = requests.get(
                    f"https://r.jina.ai/{url}",
                    headers=headers,
                    timeout=timeout
                )
                if response.status_code == 200:
                    webpage_content = response.text
                    return webpage_content
                else:
                    print(response.text)
                    raise ValueError("jina readpage error")
            except Exception as e:
                if attempt == max_retries - 1:
                    return "[visit] Failed to read page."
                
        return "[visit] Failed to read page."


    def readpage(self, url: str, goal: str) -> str:
        """
        Attempt to read webpage content by alternating between jina and aidata services.
        
        Args:
            url: The URL to read
            goal: The goal/purpose of reading the page
            
        Returns:
            str: The webpage content or error message
        """
        max_attempts = 10
        for attempt in range(max_attempts):
            # Alternate between jina and aidata
            content = self.jina_readpage(url)
            sevice = "jina"

            # Check if we got valid content
            print(sevice)
            # print(content)
            if content and not content.startswith("[visit] Failed to read page.") and content != "[visit] Empty content." and not content.startswith("[document_parser]"):
                content = content[:WEBCONTENT_MAXLENGTH]
                messages = [{"role":"user","content": EXTRACTOR_PROMPT.format(webpage_content=content, goal=goal)}]
                parse_retry_times = 0
                raw = self.call_server(messages)

                # 如果网页超长，返回结果是 {\n 这种形式
                summary_retries = 3
                while len(raw) < 10 and summary_retries >= 0:
                    truncate_length = int(0.7 * len(content)) if summary_retries > 0 else 25000
                    status_msg = (
                        f"[visit] Summary url[{url}] " 
                        f"attempt {3 - summary_retries + 1}/3, "
                        f"content length: {len(content)}, "
                        f"truncating to {truncate_length} chars"
                    ) if summary_retries > 0 else (
                        f"[visit] Summary url[{url}] failed after 3 attempts, "
                        f"final truncation to 25000 chars"
                    )
                    print(status_msg)
                    content = content[:truncate_length]
                    extraction_prompt = EXTRACTOR_PROMPT.format(
                        webpage_content=content,
                        goal=goal
                    )
                    messages = [{"role": "user", "content": extraction_prompt}]
                    raw = self.call_server(messages)
                    summary_retries -= 1
                # 说明 raw 的长度大于10或者已经retry 超出了 
                parse_retry_times = 0
                while parse_retry_times < 3:
                    try:
                        # 尝试 parse json
                        raw = json.loads(raw)
                        break
                    except:
                        raw = self.call_server(messages)
                        parse_retry_times += 1
                # parse 失败
                if parse_retry_times >= 3:
                    useful_information = "The useful information in {url} for user goal {goal} as follows: \n\n".format(url=url, goal=goal)
                    useful_information += "Evidence in page: \n" + "The provided webpage content could not be accessed. Please check the URL or file format." + "\n\n"
                    useful_information += "Summary: \n" + "The webpage content could not be processed, and therefore, no information is available." + "\n\n"
                # parse 成功
                else:
                    useful_information = "The useful information in {url} for user goal {goal} as follows: \n\n".format(url=url, goal=goal)
                    useful_information += "Evidence in page: \n" + str(raw["evidence"]) + "\n\n"
                    useful_information += "Summary: \n" + str(raw["summary"]) + "\n\n"

                    summary_retries -= 1

                if len(useful_information) < 10 and summary_retries < 0:
                    print("[visit] Could not generate valid summary after maximum retries")
                    useful_information = "[visit] Failed to read page"
                return useful_information
                
            # If we're on the last attempt, return the last result
            if attempt == max_attempts - 1:
                useful_information = "The useful information in {url} for user goal {goal} as follows: \n\n".format(url=url, goal=goal)
                useful_information += "Evidence in page: \n" + "The provided webpage content could not be accessed. Please check the URL or file format." + "\n\n"
                useful_information += "Summary: \n" + "The webpage content could not be processed, and therefore, no information is available." + "\n\n"
                return useful_information

```

> 说明：以上为关键代码片段，结合上下文解释其作用与调用关系。

### 文件：`WebAgent/WebSailor/src/run_multi_react.py`

```py
import argparse
import json
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm
import threading
from datetime import datetime
from react_agent import MultiTurnReactAgent
from prompt import SYSTEM_PROMPT_MULTI, USER_PROMPT
from tool_search import *
from tool_visit import * 


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", type=str, default="")
    parser.add_argument("--output", type=str, default="")
    parser.add_argument("--dataset", type=str, default="gaia", choices=["gaia", 
                                                                        "browsecomp_zh", "browsecomp_zh_small", 
                                                                        "browsecomp_en", "browsecomp_en_full", "browsecomp_en_small", 
                                                                        "webwalker", 
                                                                        "simple_qa", "simple_qa_small",
                                                                        "time_qa",
                                                                        "xbench-deepsearch",
                                                                        "hle", "kuan_graph"])
    parser.add_argument("--temperature", type=float, default=0.6)
    parser.add_argument("--top_p", type=float, default=0.95)
    parser.add_argument("--max_workers", type=int, default=20)
    parser.add_argument("--sys_prompt", type=str, default="SYSTEM_PROMPT_MULTI")
    parser.add_argument("--roll_out_count", type=int, default=3)
    args = parser.parse_args()

    model = args.model
    output_base = args.output
    roll_out_count = args.roll_out_count

    # Parse model name (the part after the last / in the path)
    model_name = os.path.basename(model.rstrip('/'))
    
    # Create output directory structure: output_base/model_name_sglang/dataset_name/
    model_dir = os.path.join(output_base, f"{model_name}_sglang")
    dataset_dir = os.path.join(model_dir, args.dataset)
    
    # Create directories
    os.makedirs(dataset_dir, exist_ok=True)
    
    print(f"Model name: {model_name}")
    print(f"Dataset name: {args.dataset}")
    print(f"Output directory: {dataset_dir}")
    print(f"Rollout count: {roll_out_count}")

    data_filepath = f"eval_data/{args.dataset}.jsonl"
    try:
        if data_filepath.endswith(".json"):
            with open(data_filepath, "r", encoding="utf-8") as f:
                items = json.load(f)
            if not isinstance(items, list):
                raise ValueError("Input JSON must be a list of objects.")
            if items and not isinstance(items[0], dict):
                raise ValueError("Input JSON list items must be objects.")
        elif data_filepath.endswith(".jsonl"):
            with open(data_filepath, "r", encoding="utf-8") as f:
                items = [json.loads(line) for line in f]
        else:
            raise ValueError("Unsupported file extension. Please use .json or .jsonl files.")
        items = items
    except FileNotFoundError:
        print(f"Error: Input file not found at {data_filepath}")
        exit(1)
    except (json.JSONDecodeError, ValueError) as e:
        print(f"Error reading or parsing input file {data_filepath}: {e}")
        exit(1)

    # Create tasks for each rollout
    for rollout_idx in range(1, roll_out_count + 1):
        output_file = os.path.join(dataset_dir, f"iter{rollout_idx}.jsonl")
        
        print(f"\nStarting rollout {rollout_idx}/{roll_out_count}")
        print(f"Output file: {output_file}")
        
        # Check processed queries
        processed_queries = set()
        if os.path.exists(output_file):
            try:
                with open(output_file, "r", encoding="utf-8") as f:
                    for line in f:
                        try:
                            data = json.loads(line)
                            # Check for successful completion based on absence of top-level error key
                            if "question" in data and "error" not in data:
                                processed_queries.add(data["question"].strip())
                        except json.JSONDecodeError:
                            print(f"Warning: Skipping invalid line in output file: {line.strip()}")
            except FileNotFoundError:
                pass

        tasks_to_run = []
        for item in items:
            question = item.get("question", "").strip()
            if question == "":
                try:
                    user_msg = item["messages"][1]["content"] 
                    question = user_msg.split("User:")[1].strip() if "User:" in user_msg else user_msg
                    item["question"] = question
                except Exception as e:
                    print(f"Extract question from user message failed: {e}")
            if not question:
                print(f"Warning: Skipping item with empty question: {item}")
                continue

            if question not in processed_queries:
                tasks_to_run.append({"item": item.copy(), "rollout_id": rollout_idx})
            else:
                print(f"Skipping already processed question: {question}")

        print(f"Total questions in input: {len(items)}")
        print(f"Already successfully processed: {len(processed_queries)}")
        print(f"Total tasks to run for this rollout: {len(tasks_to_run)}")

        if not tasks_to_run:
            print(f"Rollout {rollout_idx} completed, skipping")
            continue

        llm_cfg = {
            'model': model,
            'generate_cfg': {
                'max_input_tokens': 320000,
                'max_retries': 10, 
                'temperature': args.temperature, 
                'top_p': args.top_p
            }, 
            'model_type': 'qwen_dashscope'
        }
        
        system_message = SYSTEM_PROMPT_MULTI + "\nCurrent date: " + datetime.now().strftime("%Y-%m-%d")
        
        test_agent = MultiTurnReactAgent(
            llm=llm_cfg,
            function_list=["search", "visit"],
            system_message=system_message
        )

        # Create file write lock
        write_lock = threading.Lock()

        with ThreadPoolExecutor(max_workers=args.max_workers) as executor:
            # Submit tasks
            future_to_task = {
                executor.submit(
                    test_agent._run,
                    task,
                    model,
                    USER_PROMPT
                ): task
                for task in tasks_to_run
            }

            for future in tqdm(as_completed(future_to_task), total=len(tasks_to_run), desc=f"Processing Rollout {rollout_idx}"):
                task_info = future_to_task[future]
                try:
                    result = future.result()
                    # Use lock to protect file write operations
                    with write_lock:
                        with open(output_file, "a", encoding="utf-8") as f:
                            f.write(json.dumps(result, ensure_ascii=False) + "\n")
                except Exception as exc:
                    print(f'Task for question "{task_info["item"]["question"]}" (Rollout {task_info["rollout_id"]}) generated an exception: {exc}')
                    # Log error to the output file
                    error_result = {
                        "question": task_info["item"]["question"],
                        "answer": task_info["item"].get("answer", ""),
                        "rollout_id": task_info["rollout_id"],
                        "error": f"Future resolution failed: {exc}",
                        "messages": [],
                        "prediction": "[Failed]",
                    }
                    print("===============================")
                    print(error_result)
                    print("===============================")
                    
                    # Also use lock to protect error writing
                    with write_lock:
                        with open(output_file, "a", encoding="utf-8") as f:
                            f.write(json.dumps(error_result, ensure_ascii=False) + "\n")
        
        print(f"Rollout {rollout_idx} completed")
    
    print(f"\nAll {roll_out_count} rollouts completed!")

```

> 说明：以上为关键代码片段，结合上下文解释其作用与调用关系。

### 文件：`WebAgent/WebSailor/src/prompt.py`

```py
SYSTEM_PROMPT_MULTI = '''You are a Web Information Seeking Master. Your task is to thoroughly seek the internet for information and provide accurate answers to questions. No matter how complex the query, you will not give up until you find the corresponding information.

As you proceed, adhere to the following principles:

1. **Persistent Actions for Answers**: You will engage in many interactions, delving deeply into the topic to explore all possible aspects until a satisfactory answer is found.

2. **Repeated Verification**: Before presenting a Final Answer, you will **cross-check** and **validate the information** you've gathered to confirm its accuracy and reliability.

3. **Attention to Detail**: You will carefully analyze each information source to ensure that all data is current, relevant, and from credible origins.'''


EXTRACTOR_PROMPT = """Please process the following webpage content and user goal to extract relevant information:

## **Webpage Content** 
{webpage_content}

## **User Goal**
{goal}

## **Task Guidelines**
1. **Content Scanning for Rational**: Locate the **specific sections/data** directly related to the user's goal within the webpage content
2. **Key Extraction for Evidence**: Identify and extract the **most relevant information** from the content, you never miss any important information, output the **full original context** of the content as far as possible, it can be more than three paragraphs.
3. **Summary Output for Summary**: Organize into a concise paragraph with logical flow, prioritizing clarity and judge the contribution of the information to the goal.

**Final Output Format using JSON format has "rational", "evidence", "summary" feilds**
"""


USER_PROMPT = """A conversation between User and Assistant. The user asks a question, and the assistant solves it by calling one or more of the following tools.
<tools>
{
  "name": "search",
  "description": "Performs batched web searches: supply an array 'query'; the tool retrieves the top 10 results for each query in one call.",
  "parameters": {
    "type": "object",
    "properties": {
      "query": {
        "type": "array",
        "items": {
          "type": "string"
        },
        "description": "Array of query strings. Include multiple complementary search queries in a single call."
      }
    },
    "required": [
      "query"
    ]
    }
},
{
  "name": "visit",
    "description": "Visit webpage(s) and return the summary of the content.",
    "parameters": {
        "type": "object",
        "properties": {
            "url": {
                "type": "array",
                "items": {"type": "string"},
                "description": "The URL(s) of the webpage(s) to visit. Can be a single URL or an array of URLs."
            },
            "goal": {
                "type": "string",
                "description": "The specific information goal for visiting webpage(s)."
            }
        },
        "required": [
            "url",
            "goal"
        ]
    }
}
</tools>

The assistant starts with one or more cycles of (thinking about which tool to use -> performing tool call -> waiting for tool response), and ends with (thinking about the answer -> answer of the question). The thinking processes, tool calls, tool responses, and answer are enclosed within their tags. There could be multiple thinking processes, tool calls, tool call parameters and tool response parameters.

Example response:
<think> thinking process here </think>
<tool_call>
{"name": "tool name here", "arguments": {"parameter name here": parameter value here, "another parameter name here": another parameter value here, ...}}
</tool_call>
<tool_response>
tool_response here
</tool_response>
<think> thinking process here </think>
<tool_call>
{"name": "another tool name here", "arguments": {...}}
</tool_call>
<tool_response>
tool_response here
</tool_response>
(more thinking processes, tool calls and tool responses here)
<think> thinking process here </think>
<answer> answer here </answer>

User: """


JUDGE_PROMPT_GAIA = """You are an evaluation assistant. Please determine if the predicted answer is equivalent to the labeled answer.

Question: {question}

Labeled Answer: {correct_answer}

Predicted Answer: {response}

Did the model give an answer **equivalent** to the labeled answer? Please respond with "Correct" if they are equivalent, or "Incorrect" if they are not equivalent. Do not include any other text.
"""

JUDGE_PROMPT_BC = """"Judge whether the following [response] to [question] is correct or not based on the precise and unambiguous [correct_answer] below.

[question]: {question}
[response]: {response}

Your judgement must be in the format and criteria specified below:

extracted_final_answer: The final exact answer extracted from the [response]. Put the extracted answer as ’None’ if there is no exact, final answer to extract from the response.
[correct_answer]: {correct_answer}

reasoning: Explain why the extracted_final_answer is correct or incorrect based on [correct_answer], focusing only on if there are meaningful differences between [correct_answer] and the extracted_final_answer. Do not comment on any background to the problem, do not attempt to solve the problem, do not argue for any answer different than [correct_answer], focus only on whether the answers match.

correct: Answer ’yes’ if extracted_final_answer matches the [correct_answer] given above, or is within a small margin of error for numerical problems. Answer ’no’ otherwise, i.e. if there if there is any inconsistency, ambiguity, non-equivalency, or if the extracted answer is incorrect. 

confidence: The extracted confidence score between 0|\%| and 100|\%| from [response]. Put 100 if there
is no confidence score available."""


JUDGE_PROMPT_QA = """
Your job is to look at a question, a gold target, and a predicted answer, and then assign a grade of either ["CORRECT", "INCORRECT", "NOT_ATTEMPTED"].
First, I will give examples of each grade, and then you will grade a new example.


The following are examples of CORRECT predicted answers.
```
Question: What are the names of Barack Obama's children?
Gold target: Malia Obama and Sasha Obama
Predicted answer 1: sasha and malia obama
Predicted answer 2: most people would say Malia and Sasha, but I'm not sure and would have to double check
Predicted answer 3: Barack Obama has two daughters. Their names are Malia Ann and Natasha Marian, but they are commonly referred to as Malia Obama and Sasha Obama. Malia was born on July 4, 1998, and Sasha was born on June 10, 2001.
```
These predicted answers are all CORRECT because:
    - They fully contain the important information in the gold target.
    - They do not contain any information that contradicts the gold target.
    - Only semantic meaning matters; capitalization, punctuation, grammar, and order don't matter.
    - Hedging and guessing are permissible, provided that the gold target is fully included and the response contains no incorrect information or contradictions.


The following are examples of INCORRECT predicted answers.
```
Question: What are the names of Barack Obama's children?
Gold target: Malia and Sasha
Predicted answer 1: Malia.
Predicted answer 2: Malia, Sasha, and Susan.
Predicted answer 3: Barack Obama does not have any children.
Predicted answer 4: I think it's either Malia and Sasha. Or it could be Malia and Jackie. Or it could be Joey and Malia.
Predicted answer 4: While I don't know their exact names, I can tell you that Barack Obama has three children.
Predicted answer 5: It's possible you may mean Betsy and Olivia. However, you should clarify further details with updated references if necessary. Is that the correct answer?
Predicted answer 6: It may be the case that Obama's child is named James. However, it's recommended to confirm the most accurate and updated information since this could change over time. This model may not always reflect the most current information.
```
These predicted answers are all INCORRECT because:
    - A factual statement in the answer contradicts the gold target. Incorrect statements that have some hedging (e.g., "it is possible that", "although i'm not sure, i think") are also considered incorrect.


The following are examples of NOT_ATTEMPTED predicted answers.
```
Question: What are the names of Barack Obama's children?
Gold target: Malia and Sasha
Predicted answer 1: I don't know.
Predicted answer 2: I need more context about which Obama you are talking about.
Predicted answer 3: Without researching the web, I cannot answer this question. However, I can tell you that Barack Obama has two children.
Predicted answer 4: Barack Obama has two children. I know that one of them is Malia, but I'm not sure about the other one.
```
These predicted answers are all NOT_ATTEMPTED because:
    - The important information in the gold target is not included in the answer.
    - No statements in the answer contradict the gold target.


Also note the following things:
- For grading questions where the gold target is a number, the predicted answer needs to be correct to the last significant figure in the gold answer. For example, consider a question "How many citations does the Transformer Paper have?" with gold target "120k". 
    - Predicted answers "120k", "124k", and 115k" are all CORRECT. 
    - Predicted answers "100k" and "113k" are INCORRECT. 
    - Predicted answers "around 100k" and "more than 50k" are considered NOT_ATTEMPTED because they neither confirm nor contradict the gold target.
- The gold target may contain more information than the question. In such cases, the predicted answer only needs to contain the information that is in the question.
    - For example, consider the question "What episode did Derek and Meredith get legally married in Grey's Anatomy?" with gold target "Season 7, Episode 20: White Wedding". Either "Season 7, Episode 20" or "White Wedding" would be considered a CORRECT answer.
- Do not punish predicted answers if they omit information that would be clearly inferred from the question.
    - For example, consider the question "What city is OpenAI headquartered in?" and the gold target "San Francisco, California". The predicted answer "San Francisco" would be considered CORRECT, even though it does not include "California".
    - Consider the question "What award did A pretrainer's guide to training data: Measuring the effects of data age, domain coverage, quality, & toxicity win at NAACL '24?", the gold target is "Outstanding Paper Award". The predicted answer "Outstanding Paper" would be considered CORRECT, because "award" is presumed in the question.
    - For the question "What is the height of Jason Wei in meters?", the gold target is "1.73 m". The predicted answer "1.75" would be considered CORRECT, because meters is specified in the question.
    - For the question "What is the name of Barack Obama's wife?", the gold target is "Michelle Obama". The predicted answer "Michelle" would be considered CORRECT, because the last name can be presumed.
- Do not punish for typos in people's name if it's clearly the same name. 
    - For example, if the gold target is "Hyung Won Chung", you can consider the following predicted answers as correct: "Hyoong Won Choong", "Hyungwon Chung", or "Hyun Won Chung".


Here is a new example. Simply reply with either CORRECT, INCORRECT, NOT ATTEMPTED. Don't apologize or correct yourself if there was a mistake; we are just trying to grade the answer.
```
Question: {question}
Gold target: {correct_answer}
Predicted answer: {response}
```

Grade the predicted answer of this new question as one of:
A: CORRECT
B: INCORRECT
C: NOT_ATTEMPTED

Just return the letters "A", "B", or "C", with no text around it.
""".strip()

```

> 说明：以上为关键代码片段，结合上下文解释其作用与调用关系。

### 文件：`WebAgent/WebSailor/src/tool_search.py`

```py
from qwen_agent.tools.base import BaseTool, register_tool 
import json
from concurrent.futures import ThreadPoolExecutor
from typing import List, Union
import requests
from qwen_agent.tools.base import BaseTool, register_tool
import os

SEARCH_API_URL = os.getenv("SEARCH_API_URL")
GOOGLE_SEARCH_KEY = os.getenv("GOOGLE_SEARCH_KEY")


@register_tool("search", allow_overwrite=True)
class Search(BaseTool):
    name = "search"
    description = "Performs batched web searches: supply an array 'query'; the tool retrieves the top 10 results for each query in one call."
    parameters = {
            "type": "object",
            "properties": {
                "query": {
                    "type": "array",
                    "items": {
                    "type": "string"
                    },
                    "description": "Array of query strings. Include multiple complementary search queries in a single call."
                },
            },
        "required": ["query"],
    }

    def google_search(self, query: str):
        url = 'https://google.serper.dev/search'
        headers = {
            'X-API-KEY': GOOGLE_SEARCH_KEY,
            'Content-Type': 'application/json',
        }
        data = {
            "q": query,
            "num": 10,
            "extendParams": {
                "country": "en",
                "page": 1,
            },
        }

        for i in range(5):
            try:
                response = requests.post(url, headers=headers, data=json.dumps(data))
                results = response.json()
            except Exception as e:
                print(e)
                if i == 4:
                    return f"Google search Timeout, return None, Please try again later."
        if response.status_code != 200:
            raise Exception(f"Error: {response.status_code} - {response.text}")

        try:
            if "organic" not in results:
                raise Exception(f"No results found for query: '{query}'. Use a less specific query.")

            web_snippets = list()
            idx = 0
            if "organic" in results:
                for page in results["organic"]:
                    idx += 1
                    date_published = ""
                    if "date" in page:
                        date_published = "\nDate published: " + page["date"]

                    source = ""
                    if "source" in page:
                        source = "\nSource: " + page["source"]

                    snippet = ""
                    if "snippet" in page:
                        snippet = "\n" + page["snippet"]

                    redacted_version = f"{idx}. [{page['title']}]({page['link']}){date_published}{source}\n{snippet}"

                    redacted_version = redacted_version.replace("Your browser can't play this video.", "")
                    web_snippets.append(redacted_version)

            content = f"A Google search for '{query}' found {len(web_snippets)} results:\n\n## Web Results\n" + "\n\n".join(web_snippets)
            return content
        except:
            return f"No results found for '{query}'. Try with a more general query, or remove the year filter."


    def call(self, params: Union[str, dict], **kwargs) -> str:
        assert GOOGLE_SEARCH_KEY is not None, "Please set the GOOGLE_SEARCH_KEY environment variable."
        try:
            query = params["query"]
        except:
            return "[Search] Invalid request format: Input must be a JSON object containing 'query' field"
        
        if isinstance(query, str):
            response = self.google_search(query)
        else:
            assert isinstance(query, List)
            with ThreadPoolExecutor(max_workers=3) as executor:
                response = list(executor.map(self.google_search, query))
            response = "\n=======\n".join(response)
        return response

```

> 说明：以上为关键代码片段，结合上下文解释其作用与调用关系。

### 文件：`WebAgent/WebSailor/src/evaluate.py`

```py
import concurrent.futures
import os 
import argparse
import json
import concurrent 
from tqdm import tqdm 
import re 
from prompt import JUDGE_PROMPT_GAIA, JUDGE_PROMPT_BC, JUDGE_PROMPT_QA
import traceback
from openai import OpenAI
import tiktoken


def extract_correct_judgement(response: str) -> str:
    match = re.search(r'correct\s*:\s*(yes|no)', response, re.IGNORECASE)
    if match:
        return match.group(1).lower()
    else:
        return None
def call_llm_judge(item): 
    """Judge if predicted answer matches ground-truth""" 
    global judge_prompt
    try: 
        question = item["question"]
        correct_answer = item["answer"]

        response = item["prediction"].strip()

        prompt = judge_prompt.format(question=question, correct_answer=correct_answer, response=response)

        openai_api_key = "EMPTY"
        openai_api_base = "http://127.0.0.1:6002/v1"

        client = OpenAI(
            api_key=openai_api_key,
            base_url=openai_api_base,
        )
        max_tries = 10
        for attempt in range(max_tries):
            try:
                chat_response = client.chat.completions.create(
                                    model='qwen2.5-72b-instruct',
                                    messages=[{"role": "user", "content": prompt}],
                )    
                response = chat_response.choices[0].message.content
                if response:
                    break
            except Exception as e:
                if attempt == (max_tries - 1):
                    raise e

        return {
            "question": question, 
            "answer": correct_answer, 
            "judgement": response
        }
    
    except Exception as e:
        print(f"Error judgement for question: {question}: {e}")
        return {
            "question": question,  
            "answer": correct_answer, 
            "judgement": "Error",
            "error": str(e)
        }


def process_single_round(input_file): 
    with open(input_file, 'r', encoding='utf-8') as f: 
        items = [json.loads(line) for line in f]
    
    return items 


def aggregate_statistics(round1_file, round2_file, round3_file):
    round1_stats = single_round_statistics(round1_file)
    round2_stats = single_round_statistics(round2_file)
    round3_stats = single_round_statistics(round3_file)
    
    keys = round1_stats.keys()  
    avg_stats = {} 
    for key in keys: 
        avg_stats[key] = round((round1_stats[key] + round2_stats[key] + round3_stats[key]) / 3 , 3)
    
    return avg_stats


def single_round_statistics(input_file):
    contents = process_single_round(input_file) 

    # Illegal Analysis 
    num_invalid, num_extra = 0, 0  
    # Tool Analysis 
    tool_use_cnt, visit_tool_cnt, search_tool_cnt, other_tool_cnt = [], [], [], [] 
    # Thinking Analysis 
    all_ans_lengths, all_think_lengths = [], []  

    tokenizer = tiktoken.encoding_for_model("gpt-4o")
    
    for item in contents:
        texts = item["messages"]
        final_msg = texts[-1]["content"] if len(texts) else ""
        
        # Analyze answer 
        if "<answer>" not in final_msg or "</answer>" not in final_msg: 
            num_invalid += 1 
            answer_length = 0 
        else:
            answer_length = len(final_msg.split("<answer>")[1].split("</answer>")[0].strip())
        
        # Analyze tool use & thinking
        num_tool_use, num_visit_tool, num_search_tool, num_other_tool = 0, 0, 0, 0 
        think_lengths = []
        for idx in range(2, len(texts), 2):
            response = texts[idx]["content"] 
            # TODO: relaxed matching for thinking, strict mode: <think>(.*?)</think>
            # thinking = re.findall(r"(.*?)</think>", response, re.DOTALL) 
            tool = re.findall(r"<tool_call>(.*?)</tool_call>", response, re.DOTALL) 
            
            if tool: 
                try:
                    tool_name = tool[0].split("name\": \"")[1].split("\"")[0].strip()
                except Exception:
                    tool_name = ""
                    
                num_tool_use += 1 
                if "visit" in tool_name:  
                    num_visit_tool += 1 
                elif "search" in tool_name: 
                    num_search_tool += 1  
                else:
                    num_other_tool += 1

            think_lengths.append(len(response)) 

        tool_use_cnt.append(num_tool_use) 
        visit_tool_cnt.append(num_visit_tool)  
        search_tool_cnt.append(num_search_tool)   
        other_tool_cnt.append(num_other_tool) 

        all_ans_lengths.append(answer_length) 
        think_length = sum(think_lengths) / len(think_lengths) if think_lengths else 0  
        all_think_lengths.append(think_length) 

        # Overlength 
        if len(tokenizer.encode("".join([text["content"] for text in texts]))) > 30000:
            num_extra += 1  
    
    return {
        "extra_length": num_extra, # number of overlength responses  
        "num_invalid": num_invalid, # number of invalid responses 
        "avg_action": sum(tool_use_cnt) / len(tool_use_cnt), # avg. number of tool invocation 
        "avg_visit_action": sum(visit_tool_cnt) / len(visit_tool_cnt), # avg. number of visit tool invocation 
        "avg_search_action": sum(search_tool_cnt) / len(search_tool_cnt), # avg. number of search tool invocation 
        "avg_other_action": sum(other_tool_cnt) / len(other_tool_cnt), # avg. number of other tool invocation 
        "avg_ans_length": sum(all_ans_lengths) / len(all_ans_lengths), 
        "avg_think_length": sum(all_think_lengths) / len(all_think_lengths)
    }
        
        
def aggregate_results(round1_results, round2_results, round3_results): 
    """Aggregate results from multiple rounds""" 
    global dataset 
    query_results = {} 
    
    for results, round_name in zip([round1_results, round2_results, round3_results], ["round1", "round2", "round3"]): 
        for result in results: 
            query = result["question"] 
            if query not in query_results:  
                query_results[query] = {
                    "round1": None, 
                    "round2": None,  
                    "round3": None, 
                    "answer": result["answer"]
                }
            
            # For BrowseComp and XX_QA datasets, prompt requires "A" or "a" as the correct answer
            if ("browsecomp" in dataset) or ("qa" in dataset): 
                judge = extract_correct_judgement(result["judgement"])
                if judge:
                    if judge.lower() == 'yes':
                        result["judgement"] = "Correct"
            query_results[query][round_name] = result["judgement"].capitalize() 
    
    return query_results


def calculate_pass_at_k(query_results, k=10): 
    total_correct = 0 

    for query, results in query_results.items():
        rounds = [results["round1"], results["round2"], results["round3"]][:k] 

        if "Correct" in rounds: 
            total_correct += 1 
    
    overall_pass = total_correct / len(query_results)
    return round(overall_pass * 100, 2)


def calculate_best_pass_at_1(query_results):  
    round_correct = {round_name: 0 for round_name in ["round1", "round2", "round3"]}

    for query, results in query_results.items():
        for round_name in ["round1", "round2", "round3"]: 
            if results[round_name] == "Correct":  
                round_correct[round_name] += 1 

    overall_best = max(
        round_correct[round_name] / len(query_results)
        for round_name in ["round1", "round2", "round3"]
    )

    return round(overall_best * 100, 2)


def calculate_avg_pass_at_3(query_results): 
    round_names = ["round1", "round2", "round3"]
    total_correct = {round_name: 0 for round_name in round_names}

    for query, results in query_results.items():  
        for round_name in round_names:  
            if results[round_name] == "Correct":
                total_correct[round_name] += 1 
    
    avg_overall = sum(total_correct[r] / len(query_results) for r in round_names) / len(round_names)
    
    return round(avg_overall * 100, 2)


def main():
    global judge_prompt, dataset
    parser = argparse.ArgumentParser(description="Evaluate model predictions across multiple rounds")
    parser.add_argument("--input_folder", help="Path to prediction files")
    parser.add_argument("--restore_result_path",default='summary.jsonl', help="record result")
    parser.add_argument("--dataset", type=str, default="gaia", choices=["gaia", 
                                                                        "browsecomp_zh", "browsecomp_zh_small", 
                                                                        "browsecomp_en", "browsecomp_en_full", "browsecomp_en_small", 
                                                                        "webwalker", 
                                                                        "simple_qa", "simple_qa_small",
                                                                        "time_qa",
                                                                        "xbench-deepsearch",
                                                                        "hle"])
    args = parser.parse_args()
    
    dataset = args.dataset  
    if dataset in ["gaia", "webwalker", "xbench-deepsearch", "hle"]: 
        judge_prompt = JUDGE_PROMPT_GAIA 
    elif dataset.startswith("browsecomp_zh"):
        judge_prompt = JUDGE_PROMPT_BC
    elif dataset.startswith("browsecomp_en"):
        judge_prompt = JUDGE_PROMPT_BC
    elif dataset.endswith("qa") or dataset.endswith("qa_small"): # for simple_qa and time_qa
        judge_prompt = JUDGE_PROMPT_QA
    else:
        judge_prompt = JUDGE_PROMPT_GAIA 
    print(f"Using {dataset} judge prompt ...")

    round1_file, round2_file, round3_file = os.path.join(args.input_folder, "iter1.jsonl"), os.path.join(args.input_folder, "iter2.jsonl"), os.path.join(args.input_folder, "iter3.jsonl") 
    for file in [round1_file, round2_file, round3_file]:
        assert os.path.exists(file), f"Prediction {file} not found, three  rounds are required "
     
    round_items = {
        "round1": process_single_round(round1_file),
        "round2": process_single_round(round2_file),
        "round3": process_single_round(round3_file)
    }

    round_results = {} 

    with concurrent.futures.ThreadPoolExecutor() as executor:  
        for round_name, items in round_items.items():
            futures = {executor.submit(call_llm_judge, item): item for item in items} 
            round_results[round_name] = [] 

            for future in tqdm(concurrent.futures.as_completed(futures), total=len(futures), desc=f"Evaluating {round_name}"):
                round_results[round_name].append(future.result())

    aggr_results = aggregate_results(round_results["round1"], round_results["round2"], round_results["round3"]) 
    
    pass_at_3 = calculate_pass_at_k(aggr_results, k=3)
    best_pass_at_1 = calculate_best_pass_at_1(aggr_results)
    avg_pass_at_3 = calculate_avg_pass_at_3(aggr_results) 
    
    aggr_statistics = aggregate_statistics(round1_file, round2_file, round3_file)

    round_performance = {
        f"Round{i}_Pass@1": round(sum(1 for r in round_results[f"round{i}"] if r["judgement"] == "Correct") / len(round_results[f"round{i}"]) * 100, 2)
        for i in [1, 2, 3]
    }

    print(f"===========")
    print(f"Avg. Pass@3 {avg_pass_at_3}%") 
    print(f"Best Pass@1 {best_pass_at_1}%")  
    print(f"Pass@3 {pass_at_3}%") 
    print(f"Pass@1 Round 1: {round_performance['Round1_Pass@1']}%  Round 2: {round_performance['Round2_Pass@1']}%  Round 3: {round_performance['Round3_Pass@1']}% \n")
    print(f"# Invalid {aggr_statistics['num_invalid']}  # Extra Length {aggr_statistics['extra_length']}") 
    print(f"Avg. Action {aggr_statistics['avg_action']:.2f}  Avg. Visit Action {aggr_statistics['avg_visit_action']:.2f}  Avg. Search Action {aggr_statistics['avg_search_action']:.2f}  Avg. Other Action {aggr_statistics['avg_other_action']:.2f}") 
    print(f"Avg. Answer Length {aggr_statistics['avg_ans_length']:.2f}  Avg. Thinking Length {aggr_statistics['avg_think_length']:.2f}")  
    print(f"===========" )

    overall_eval_dict = {
        "dataset": dataset, 
        "files": {
            "round1": round1_file,  
            "round2": round2_file,   
            "round3": round3_file
        }, 
        "overall": {
            "avg_pass_at_3": avg_pass_at_3, 
            "best_pass_at_1": best_pass_at_1, 
            "pass_at_3": pass_at_3
        }, 
        "individual": round_performance, 
        "statistics": aggr_statistics
    }

    with open(args.restore_result_path, 'a', encoding='utf-8') as jsonl_file:
        jsonl_file.write(json.dumps(overall_eval_dict, ensure_ascii=False) + '\n')


if __name__ == "__main__":
    judge_prompt, dataset = None, ""
    try:
        main()
    except Exception as e:
        error_str = traceback.format_exc()
        print(f"Evaluation Failed: {e}") 
        print("Trace Back", error_str)

```

> 说明：以上为关键代码片段，结合上下文解释其作用与调用关系。



## 五、如何在本仓库中复现与扩展
- 按各子项目`README.md`准备环境与数据；
- 参考`requirements.txt`安装依赖，运行提供的脚本；
- 可替换模型、修改超参以复现论文结果并做扩展。
