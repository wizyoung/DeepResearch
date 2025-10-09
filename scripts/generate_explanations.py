#!/usr/bin/env python3
import re
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

MAPPINGS = {
    "WebWalker": ROOT / "WebAgent" / "WebWalker",
    "WebDancer": ROOT / "WebAgent" / "WebDancer",
    "WebSailor": ROOT / "WebAgent" / "WebSailor",
    "WebShaper": ROOT / "WebAgent" / "WebShaper",
    "WebWatcher": ROOT / "WebAgent" / "WebWatcher",
    "WebResearcher": ROOT / "WebAgent" / "WebResearcher",
    "ReSum": ROOT / "WebAgent" / "WebResummer",
    "WebWeaver": ROOT / "WebAgent" / "WebWeaver",
    "WebSailor-V2": ROOT / "WebAgent" / "WebSailor-V2",
    "Scaling Agents via Continual Pre-training": ROOT / "Agent" / "AgentScaler",
    "Towards General Agentic Intelligence via Environment Scaling": ROOT / "Agent" / "AgentFounder",
}


def read_text_if_exists(path: Path, limit_bytes: int = 300_000) -> str:
    try:
        data = path.read_bytes()
        if len(data) > limit_bytes:
            data = data[:limit_bytes]
            return data.decode("utf-8", errors="ignore") + "\n\n... (truncated)\n"
        return data.decode("utf-8", errors="ignore")
    except Exception:
        return ""


def choose_key_files(base: Path):
    candidates = []
    if (base / "README.md").exists():
        candidates.append(base / "README.md")
    for rel in [
        "src/main.py",
        "src/__init__.py",
        "src/agent.py",
        "src/pipeline.py",
        "main.py",
        "agent.py",
        "pipeline.py",
        "run.py",
    ]:
        p = base / rel
        if p.exists():
            candidates.append(p)
    for p in list(base.rglob("*.py"))[:5]:
        if p not in candidates:
            candidates.append(p)
        if len(candidates) >= 8:
            break
    return candidates


CN_INTRO_TEMPLATE = (
    "# {title} 论文实现中文解读（含代码）\n\n"
    "- 论文：[{title}]({url})\n"
    "- 对象：有LLM SFT微调经验、对RL/Agent相对陌生的读者\n\n"
    "## 一、论文核心观点（通俗中文）\n{core_points}\n\n"
    "## 二、知识难点与背景补课\n{difficult_points}\n\n"
    "## 三、仓库结构与实现要点\n{impl_points}\n\n"
    "## 四、关键代码（粘贴原始代码并逐段解释）\n{code_blocks}\n\n"
    "## 五、如何在本仓库中复现与扩展\n{howto}\n"
)


def wrap_code_block(path: Path, content: str) -> str:
    lang = (path.suffix.lstrip(".") or "text")
    safe_rel = str(path.relative_to(ROOT))
    return (
        f"### 文件：`{safe_rel}`\n\n"
        f"```{lang}\n{content}\n```\n\n"
        "> 说明：以上为关键代码片段，结合上下文解释其作用与调用关系。\n"
    )


def generate_for_paper(title: str, url: str):
    key = None
    for k in MAPPINGS.keys():
        if k.lower() in title.lower():
            key = k
            break
    if key is None and title in MAPPINGS:
        key = title
    base = MAPPINGS.get(key)
    core_points = (
        "- 用中文精炼概括论文提出的问题、方法与贡献。\n"
        "- 方法如何提升长周期信息搜集能力与工具使用能力。"
    )
    difficult_points = (
        "- RL在Web/搜索环境中的回报设计与采样稳定性。\n"
        "- 任务分解、浏览器交互、记忆/检索的工程化实现要点。"
    )
    impl_points = (
        "- 目录结构、数据流、主要模块（策略、环境、工具、记忆）。\n"
        "- 训练/推理脚本与配置。"
    )
    code_blocks = ""
    if base and base.exists():
        files = choose_key_files(base)
        for f in files:
            text = read_text_if_exists(f)
            if text:
                code_blocks += wrap_code_block(f, text) + "\n"
    else:
        code_blocks = "> 提示：未检测到与该论文直接对应的实现目录，或目录结构发生变化。\n"

    howto = (
        "- 按各子项目`README.md`准备环境与数据；\n"
        "- 参考`requirements.txt`安装依赖，运行提供的脚本；\n"
        "- 可替换模型、修改超参以复现论文结果并做扩展。"
    )

    content = CN_INTRO_TEMPLATE.format(
        title=title,
        url=url,
        core_points=core_points,
        difficult_points=difficult_points,
        impl_points=impl_points,
        code_blocks=code_blocks,
        howto=howto,
    )
    safe_title = re.sub(r"[\\/:*?\"<>|]+", "_", title)
    out_path = ROOT / f"{safe_title}_explain_cn.md"
    out_path.write_text(content, encoding="utf-8")


def main():
    papers = json.loads((ROOT / "papers.json").read_text(encoding="utf-8"))
    for p in papers:
        generate_for_paper(p["title"], p["url"])


if __name__ == "__main__":
    main()

