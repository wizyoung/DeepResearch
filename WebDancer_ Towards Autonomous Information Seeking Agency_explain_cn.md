# WebDancer: Towards Autonomous Information Seeking Agency 论文实现中文解读（含代码）

- 论文：[WebDancer: Towards Autonomous Information Seeking Agency](https://arxiv.org/pdf/2505.22648)
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
### 文件：`WebAgent/WebDancer/demos/assistant_qwq_chat.py`

```py
"""An image generation agent implemented by assistant with qwq"""

import os

from qwen_agent.agents import Assistant
from qwen_agent.utils.output_beautify import typewriter_print

from demos.agents.search_agent import SearchAgent
from demos.llm.oai import TextChatAtOAI
from demos.llm.qwen_dashscope import QwenChatAtDS
from demos.gui.web_ui import WebUI
from demos.utils.date import date2str, get_date_now
from demos.tools import Visit, Search


ROOT_RESOURCE = os.path.join(os.path.dirname(__file__), 'resource')



def init_dev_search_agent_service(name: str = 'SEARCH', port: int = 8002, desc: str = '初版', reasoning: bool = True, max_llm_calls: int = 20, tools = ['search', 'visit'], addtional_agent = None):
    llm_cfg = TextChatAtOAI({
        'model': '',
        'model_type': 'oai',
        'model_server': f'http://127.0.0.1:{port}/v1',
        'api_key': 'EMPTY',
        'generate_cfg': {
            'fncall_prompt_type': 'nous',
            'temperature': 0.6,
            'top_p': 0.95,
            'top_k': -1,
            'repetition_penalty': 1.1,
            'max_tokens': 32768,
            'stream_options': {
                'include_usage': True,
            },
            'timeout': 3000
        },
    })
    def make_system_prompt():
        system_message="You are a Web Information Seeking Master. Your task is to thoroughly seek the internet for information and provide accurate answers to questions. with chinese language." \
                       "And you are also a Location-Based Services (LBS) assistant designed to help users find location-specific information." \
                        "No matter how complex the query, you will not give up until you find the corresponding information.\n\nAs you proceed, adhere to the following principles:\n\n" \
                        "1. **Persistent Actions for Answers**: You will engage in many interactions, delving deeply into the topic to explore all possible aspects until a satisfactory answer is found.\n\n" \
                        "2. **Repeated Verification**: Before presenting a Final Answer, you will **cross-check** and **validate the information** you've gathered to confirm its accuracy and reliability.\n\n" \
                        "3. **Attention to Detail**: You will carefully analyze each information source to ensure that all data is current, relevant, and from credible origins.\n\n" \
                        f"Please note that the current datetime is [{date2str(get_date_now(), with_week=True)}]. When responding, consider the time to provide contextually relevant information."
        return system_message
    
    bot = SearchAgent(
        llm=llm_cfg,
        function_list=tools,
        system_message="",
        name=f'WebDancer',
        description=f"I am WebDancer, a web information seeking agent, welcome to try!",
        extra={
            'reasoning': reasoning,
            'max_llm_calls': max_llm_calls,
        },
        addtional_agent = addtional_agent,
        make_system_prompt = make_system_prompt,
        custom_user_prompt='''The assistant starts with one or more cycles of (thinking about which tool to use -> performing tool call -> waiting for tool response), and ends with (thinking about the answer -> answer of the question). The thinking processes, tool calls, tool responses, and answer are enclosed within their tags. There could be multiple thinking processes, tool calls, tool call parameters and tool response parameters.

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

User: '''
    )

    return bot



def app_gui():
    agents = []
    for name, port, desc, reasoning, max_llm_calls, tools in [
        ('WebDancer-QwQ-32B', 8004, '...', True, 50, ['search', 'visit']),
    ]:
        search_bot_dev = init_dev_search_agent_service(
            name=name,
            port=port,
            desc=desc,
            reasoning=reasoning,
            max_llm_calls=max_llm_calls,
            tools=tools,
        )
        agents.append(search_bot_dev)


    chatbot_config = {
        'prompt.suggestions': [
            '中国国足的一场比赛，国足首先失球，由一名宿姓球员扳平了。后来还发生了点球。比分最终是平均。有可能是哪几场比赛',
            'When is the paper submission deadline for the ACL 2025 Industry Track, and what is the venue address for the conference?',
            'On June 6, 2023, an article by Carolyn Collins Petersen was published in Universe Today. This article mentions a team that produced a paper about their observations, linked at the bottom of the article. Find this paper. Under what NASA award number was the work performed by R. G. Arendt supported by?',
            '有一位华语娱乐圈的重要人物，与其兄弟共同创作并主演了一部在中国南方沿海城市上映的喜剧电影，这部电影成为该类型的开山之作。与此同时，这位人物还凭借两首极具影响力的本地方言歌曲在音乐领域取得突破，极大推动了本地方言流行音乐的发展。请问，这一切发生在20世纪70年代的哪一年？',
            '有一首欧洲国家的国歌自20世纪50年代初被正式采用，并只选用了其中的一部分歌词。同一年，一位中国文艺界的重要人物创作了一部以民间传说为基础的戏曲作品，并在当年担任了多个文化领域的重要职务。请问这位中国文艺界人物是谁？',
            '有一部英国文坛上极具影响力的长篇诗歌，由一位16世纪末的著名诗人创作，这位诗人在16世纪90年代末于伦敦去世后，被安葬在一个象征英国文学传统的著名场所，与多位文学巨匠为邻。请问，这位诗人安息之地是哪里？',
            '出一份三天两夜的端午北京旅游攻略',
            '对比下最新小米汽车和保时捷性能参数，然后根据最终的结果分析下性价比最高的车型，并给出杭州的供应商',
            '量子计算突破对现有加密体系的威胁',
            '人工智能伦理框架的全球差异',
            '老龄化社会对全球养老金体系的长期冲击',
            '全球碳中和目标下的能源转型路径差异',
            '塑料污染在海洋食物链中的累积效应',
            'AI生成内容（如AI绘画）对传统艺术价值的重构'
        ],
        'user.name': 'User',
        'verbose': True
    }
    messages = {'role': 'user', 'content': '介绍下你自己'}
    WebUI(
        agent=agents,
        chatbot_config=chatbot_config,
    ).run(
        message=messages,
        share=False,
        server_name='127.0.0.1',
        server_port=7860,
        concurrency_limit=20,
        enable_mention=False,
    )


if __name__ == '__main__':
    app_gui()

```

> 说明：以上为关键代码片段，结合上下文解释其作用与调用关系。

### 文件：`WebAgent/WebDancer/demos/__init__.py`

```py
# coding=utf-8

```

> 说明：以上为关键代码片段，结合上下文解释其作用与调用关系。

### 文件：`WebAgent/WebDancer/demos/gui/web_ui.py`

```py
import os
import pprint
import re
from typing import List, Optional, Union

from qwen_agent import Agent, MultiAgentHub
from qwen_agent.agents.user_agent import PENDING_USER_INPUT
from qwen_agent.gui.gradio_utils import format_cover_html
from qwen_agent.gui.utils import convert_fncall_to_text, convert_history_to_chatbot, get_avatar_image
from qwen_agent.llm.schema import AUDIO, CONTENT, FILE, IMAGE, NAME, ROLE, USER, VIDEO, Message
from qwen_agent.log import logger
from qwen_agent.utils.utils import print_traceback


class WebUI:
    """A Common chatbot application for agent."""

    def __init__(self, agent: Union[Agent, MultiAgentHub, List[Agent]], chatbot_config: Optional[dict] = None):
        """
        Initialization the chatbot.

        Args:
            agent: The agent or a list of agents,
                supports various types of agents such as Assistant, GroupChat, Router, etc.
            chatbot_config: The chatbot configuration.
                Set the configuration as {'user.name': '', 'user.avatar': '', 'agent.avatar': '', 'input.placeholder': '', 'prompt.suggestions': []}.
        """
        chatbot_config = chatbot_config or {}

        if isinstance(agent, MultiAgentHub):
            self.agent_list = [agent for agent in agent.nonuser_agents]
            self.agent_hub = agent
        elif isinstance(agent, list):
            self.agent_list = agent
            self.agent_hub = None
        else:
            self.agent_list = [agent]
            self.agent_hub = None

        user_name = chatbot_config.get('user.name', 'user')
        self.user_config = {
            'name': user_name,
            'avatar': chatbot_config.get(
                'user.avatar',
                get_avatar_image(user_name),
            ),
        }

        self.agent_config_list = [{
            'name': agent.name,
            'avatar': chatbot_config.get(
                'agent.avatar',
                get_avatar_image(agent.name),
            ),
            'description': agent.description or "I'm a helpful assistant.",
        } for agent in self.agent_list]

        self.input_placeholder = chatbot_config.get('input.placeholder', '请输入需要分析的问题，尽管交给我吧～')
        self.prompt_suggestions = chatbot_config.get('prompt.suggestions', [])
        self.verbose = chatbot_config.get('verbose', False)

    """
    Run the chatbot.

    Args:
        messages: The chat history.
    """

    def run(self,
            messages: List[Message] = None,
            share: bool = False,
            server_name: str = None,
            server_port: int = None,
            concurrency_limit: int = 10,
            enable_mention: bool = False,
            **kwargs):
        self.run_kwargs = kwargs

        from qwen_agent.gui.gradio_dep import gr, mgr, ms

        customTheme = gr.themes.Default(
            primary_hue=gr.themes.utils.colors.blue,
            radius_size=gr.themes.utils.sizes.radius_none,
        )

        if messages is not None:
            logger.info('web-ui messages.size %s' % len(messages))

        with gr.Blocks(
                css=os.path.join(os.path.dirname(__file__), 'assets/appBot.css'),
                theme=customTheme,
        ) as demo:
            history = gr.State([])
            with ms.Application():
                with gr.Row(elem_classes='container'):
                    with gr.Column(scale=4):
                        chatbot = mgr.Chatbot(value=convert_history_to_chatbot(messages=messages),
                                              avatar_images=[
                                                  self.user_config,
                                                  self.agent_config_list,
                                              ],
                                              height=850,
                                              avatar_image_width=80,
                                              flushing=False,
                                              show_copy_button=True,
                                              latex_delimiters=[{
                                                  'left': '\\(',
                                                  'right': '\\)',
                                                  'display': True
                                              }, {
                                                  'left': '\\begin{equation}',
                                                  'right': '\\end{equation}',
                                                  'display': True
                                              }, {
                                                  'left': '\\begin{align}',
                                                  'right': '\\end{align}',
                                                  'display': True
                                              }, {
                                                  'left': '\\begin{alignat}',
                                                  'right': '\\end{alignat}',
                                                  'display': True
                                              }, {
                                                  'left': '\\begin{gather}',
                                                  'right': '\\end{gather}',
                                                  'display': True
                                              }, {
                                                  'left': '\\begin{CD}',
                                                  'right': '\\end{CD}',
                                                  'display': True
                                              }, {
                                                  'left': '\\[',
                                                  'right': '\\]',
                                                  'display': True
                                              }])

                        input = mgr.MultimodalInput(
                            placeholder=self.input_placeholder,
                            show_copy_button=True,
                        )

                    with gr.Column(scale=1):
                        if len(self.agent_list) > 1:
                            agent_selector = gr.Dropdown(
                                [(agent.name, i) for i, agent in enumerate(self.agent_list)],
                                label='Agents',
                                info='请选择一个 Agent',
                                value=0,
                                interactive=True,
                            )

                        agent_info_block = self._create_agent_info_block()

                        agent_plugins_block = self._create_agent_plugins_block()

                        if self.prompt_suggestions:
                            gr.Examples(
                                label='推荐对话',
                                examples=self.prompt_suggestions,
                                inputs=[input],
                            )

                    if len(self.agent_list) > 1:
                        agent_selector.change(
                            fn=self.change_agent,
                            inputs=[agent_selector],
                            outputs=[agent_selector, agent_info_block, agent_plugins_block],
                            queue=False,
                        )

                    input.change(
                        fn=self.change_text,
                        inputs=[input],
                    )
                    input_promise = input.submit(
                        fn=self.add_text,
                        inputs=[input, chatbot, history],
                        outputs=[input, chatbot, history],
                        queue=True,
                        concurrency_limit=concurrency_limit,
                    )

                    if len(self.agent_list) > 1:
                        if enable_mention:
                            input_promise = input_promise.then(
                                self.add_mention,
                                [chatbot, agent_selector],
                                [chatbot, agent_selector],
                            ).then(
                                self.agent_run,
                                [chatbot, history, agent_selector],
                                [chatbot, history, agent_selector],
                            )
                        else:
                            input_promise = input_promise.then(
                                self.agent_run,
                                [chatbot, history, agent_selector],
                                [chatbot, history, agent_selector],
                            )
                    else:
                        input_promise = input_promise.then(
                            self.agent_run,
                            [chatbot, history],
                            [chatbot, history],
                        )

                    input_promise.then(self.flushed, None, [input])

            demo.load(None)

        demo.queue(default_concurrency_limit=concurrency_limit).launch(share=share,
                                                                       server_name=server_name,
                                                                       server_port=server_port)

    def change_agent(self, agent_selector):
        yield agent_selector, self._create_agent_info_block(agent_selector), self._create_agent_plugins_block(
            agent_selector)

    def change_text(self, _input):
        logger.info(f'agent_run change_text input:{_input.text}')

    def add_text(self, _input, _chatbot, _history):
        _history.append({
            ROLE: USER,
            CONTENT: [{
                'text': _input.text
            }],
        })

        if self.user_config[NAME]:
            _history[-1][NAME] = self.user_config[NAME]

        logger.info('agent_run add_text input:\n' + pprint.pformat(_history, indent=2))

        if _input.files:
            for file in _input.files:
                if file.mime_type.startswith('image/'):
                    _history[-1][CONTENT].append({IMAGE: 'file://' + file.path})
                elif file.mime_type.startswith('audio/'):
                    _history[-1][CONTENT].append({AUDIO: 'file://' + file.path})
                elif file.mime_type.startswith('video/'):
                    _history[-1][CONTENT].append({VIDEO: 'file://' + file.path})
                else:
                    _history[-1][CONTENT].append({FILE: file.path})

        _chatbot.append([_input, None])

        from qwen_agent.gui.gradio_dep import gr
        yield gr.update(interactive=False, value=''), _chatbot, _history

    def add_mention(self, _chatbot, _agent_selector):
        if len(self.agent_list) == 1:
            yield _chatbot, _agent_selector

        query = _chatbot[-1][0].text
        match = re.search(r'@\w+\b', query)
        if match:
            _agent_selector = self._get_agent_index_by_name(match.group()[1:])

        agent_name = self.agent_list[_agent_selector].name

        if ('@' + agent_name) not in query and self.agent_hub is None:
            _chatbot[-1][0].text = '@' + agent_name + ' ' + query

        yield _chatbot, _agent_selector

    def agent_run(self, _chatbot, _history, _agent_selector=None):
        # TODO 仅保持任务的单论对话
        if self.verbose:
            logger.info('agent_run input[all]:\n' + pprint.pformat(_history, indent=2))
        _history = _history[-1:]
        if self.verbose:
            logger.info('agent_run input[new]:\n' + pprint.pformat(_history, indent=2))

        if len(_history) == 0:
            if _agent_selector is not None:
                yield _chatbot, _history, _agent_selector
            else:
                yield _chatbot, _history
            logger.info('agent_run input with empty input, do nothing.')
            return

        num_input_bubbles = len(_chatbot) - 1
        num_output_bubbles = 1
        _chatbot[-1][1] = [None for _ in range(len(self.agent_list))]

        logger.info('agent_run input:_agent_selector %s' % _agent_selector)
        agent_runner = self.agent_list[_agent_selector or 0]
        if self.agent_hub:
            agent_runner = self.agent_hub
        agent_runner.function_map

        responses = []
        for responses in agent_runner.run(_history, **self.run_kwargs):
            if not responses:
                continue
            if responses[-1][CONTENT] == PENDING_USER_INPUT:
                logger.info('Interrupted. Waiting for user input!')
                break

            display_responses = convert_fncall_to_text(responses)
            if not display_responses:
                continue
            if display_responses[-1][CONTENT] is None:
                continue

            while len(display_responses) > num_output_bubbles:
                # Create a new chat bubble
                _chatbot.append([None, None])
                _chatbot[-1][1] = [None for _ in range(len(self.agent_list))]
                num_output_bubbles += 1

            assert num_output_bubbles == len(display_responses)
            assert num_input_bubbles + num_output_bubbles == len(_chatbot)

            for i, rsp in enumerate(display_responses):
                agent_index = self._get_agent_index_by_name(rsp[NAME])
                _chatbot[num_input_bubbles + i][1][agent_index] = rsp[CONTENT]

            if len(self.agent_list) > 1:
                _agent_selector = agent_index

            if _agent_selector is not None:
                yield _chatbot, _history, _agent_selector
            else:
                yield _chatbot, _history

        if responses:
            _history.extend([res for res in responses if res[CONTENT] != PENDING_USER_INPUT])

        if _agent_selector is not None:
            yield _chatbot, _history, _agent_selector
        else:
            yield _chatbot, _history

        if self.verbose:
            logger.info('agent_run response:\n' + pprint.pformat(responses, indent=2))

    def flushed(self):
        logger.info('agent_run flushed')
        from qwen_agent.gui.gradio_dep import gr
        return gr.update(interactive=True, value='')

    def _get_agent_index_by_name(self, agent_name):
        if agent_name is None:
            return 0

        try:
            agent_name = agent_name.strip()
            for i, agent in enumerate(self.agent_list):
                if agent.name == agent_name:
                    return i
            return 0
        except Exception:
            print_traceback()
            return 0

    def _create_agent_info_block(self, agent_index=0):
        from qwen_agent.gui.gradio_dep import gr

        agent_config_interactive = self.agent_config_list[agent_index]

        return gr.HTML(
            format_cover_html(
                bot_name=agent_config_interactive['name'],
                bot_description=agent_config_interactive['description'],
                bot_avatar=agent_config_interactive['avatar'],
            ))

    def _create_agent_plugins_block(self, agent_index=0):
        from qwen_agent.gui.gradio_dep import gr

        agent_interactive = self.agent_list[agent_index]

        if agent_interactive.function_map:
            capabilities = [key for key in agent_interactive.function_map.keys()]
            return gr.CheckboxGroup(
                label='插件',
                value=capabilities,
                choices=capabilities,
                interactive=False,
            )

        else:
            return gr.CheckboxGroup(
                label='插件',
                value=[],
                choices=[],
                interactive=False,
            )

```

> 说明：以上为关键代码片段，结合上下文解释其作用与调用关系。

### 文件：`WebAgent/WebDancer/demos/gui/html_decorate.py`

```py
from markdown_it import MarkdownIt
import html
import re

def get_style_css(style_name):
    """
    根据选择的样式名称获取对应的CSS样式文件
    
    Args:
        style_name (str): 样式名称，可选值为"Default"、"MBE"、"Glassmorphism"、"Apple"
    
    Returns:
        str: CSS样式内容
    """
    
    if style_name == "Default":
        return open("assets/demo.css", "r").read()
    elif style_name == "1":
        return open("assets/demo.1.css", "r").read()
    elif style_name == "MBE":
        return open("assets/demo_mbe.css", "r").read()
    elif style_name == "Glassmorphism":
        return open("assets/demo_glassmorphism.css", "r").read()
    elif style_name == "Apple":
        return open("assets/demo_apple.css", "r").read()
    elif style_name == "Paper":
        return open("assets/demo_paper.css", "r").read()
    else:
        return open("assets/demo.css", "r").read()

def decorate_writing(writing_result, style="Default"):
    if not writing_result:
        return writing_result
    
    cite_pattern = r'<qwen:cite\s+url=["\']([^"\']+)["\'](?:\s+[^>]*)?>(.*?)</qwen:cite>'
    takeaway_pattern = r'<qwen:takeaway(?:\s+class=["\'](?P<class>[^"\']+)["\'])?>(?P<content>[^<]*)</qwen:takeaway>'
    citation_map = {}

    def replace_cite(match):
        nonlocal citation_map
        urls = match.group(1).split(',')
        content = match.group(2)
        citation_html = []
        
        for url in urls:
            if url not in citation_map:
                citation_map[url] = len(citation_map) + 1
            current_index = citation_map[url]
            citation_html.append((f'<a href="{url}" title="点击查看引用来源: {url}">{current_index}</a>', current_index))
        
        citation_html = sorted(citation_html, key=lambda x: x[1])
        citation_html = ', '.join([x[0] for x in citation_html])

        cite_html = f'{content}<sup class="citation">[{citation_html}]</sup>'
        return cite_html
    
    decorated_result = re.sub(cite_pattern, replace_cite, writing_result, flags=re.S)

    def replace_takeaway(match):
        class_attr = match.group('class')
        content = match.group('content')
        
        if class_attr:
            return f'<div class="takeaway {class_attr}">{content}</div>'
        else:
            return f'<div class="takeaway">{content}</div>'
    
    decorated_result = re.sub(takeaway_pattern, replace_takeaway, decorated_result, flags=re.S)

    mermaid_pattern = r'```mermaid\n(.*?)\n```'
    def decorate_mermaid(match):
        return f"""
<pre class="mermaid">
{match.group(1)}
</pre>
"""
    decorated_result = re.sub(mermaid_pattern, decorate_mermaid, decorated_result, flags=re.S)

    echarts_pattern = r'```echarts\n(.*?)\n```'
    echarts_index = 0
    
    def replace_echarts(match):
        """
        将echarts代码块转换为HTML和JavaScript
        
        Args:
            match: 正则表达式匹配对象
        
        Returns:
            str: 包含HTML和JavaScript的echarts图表代码
        """
        nonlocal echarts_index 
        echarts_code = match.group(1)
        echarts_id = f'echarts-container-{echarts_index}'
        echarts_index += 1
        
        replace_code = f"""
<div class="echarts-container loading" id="{echarts_id}">Echarts Rendering...</div>
<script>
    var chartDom = document.getElementById('{echarts_id}');
    var myChart = echarts.init(chartDom);
    var option;
    option = {echarts_code};
    myChart.setOption(option);
    chartDom.classList.remove('loading');
</script>
        """
        return replace_code
    
    decorated_result = re.sub(echarts_pattern, replace_echarts, decorated_result, flags=re.S)

    md = MarkdownIt()
    body = md.render(decorated_result)
    
    selected_css = get_style_css(style)
    
    html_content = """
<html>
<head>
    <!-- KaTeX for mathematical formulas -->
    <link rel="stylesheet" href="https://s4.zstatic.net/npm/katex@0.16.0/dist/katex.min.css">
    <script src="https://s4.zstatic.net/npm/katex@0.16.0/dist/katex.min.js"></script>
    <script src="https://s4.zstatic.net/npm/katex@0.16.0/dist/contrib/auto-render.min.js"></script>
    <script src="https://s4.zstatic.net/npm/echarts@5.6.0/dist/echarts.min.js"></script>
    <style>
""" + selected_css + """
    </style>
</head>
<body>
<div class="generated-content">
""" + body + """</div>
<script type="module">
    import mermaid from 'https://unpkg.com/mermaid@11.6.0/dist/mermaid.esm.min.mjs';
</script>
<script>
    document.addEventListener('DOMContentLoaded', function() {
        renderMathInElement(document.body);
    });
</script>
</body>
</html>
"""
    # 转义HTML内容以便在iframe中安全使用
    # 这是必要的，因为HTML内容包含引号和其他特殊字符
    escaped_html_content = html.escape(html_content)
    
    # 定义iframe的样式属性
    iframe_style = "width: 100%; height: 1024px; transform-origin: top left; border-color: lightgrey; border-width: 1px; border-radius: 10px;"
    
    # 创建最终的iframe HTML，通过srcdoc属性注入转义后的HTML内容
    # 设置loading="eager"和importance="high"以优先加载
    # pointer-events="none"防止用户与iframe内容交互
    iframe_content = f'<iframe id="ai-ui-iframe" loading="eager" importance="high" pointer-events="none" style="{iframe_style}" srcdoc="{escaped_html_content}"></iframe>'

    # 返回最终的iframe HTML内容
    iframe_content = re.sub(r'\n\s*\n', '\n', iframe_content)
    return iframe_content

```

> 说明：以上为关键代码片段，结合上下文解释其作用与调用关系。

### 文件：`WebAgent/WebDancer/demos/gui/__init__.py`

```py
# coding=utf-8

```

> 说明：以上为关键代码片段，结合上下文解释其作用与调用关系。



## 五、如何在本仓库中复现与扩展
- 按各子项目`README.md`准备环境与数据；
- 参考`requirements.txt`安装依赖，运行提供的脚本；
- 可替换模型、修改超参以复现论文结果并做扩展。
