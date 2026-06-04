"""
Agno Agent MCP Server — exposes Agno-powered tools to opencode.

Tools:
  - web_search(query)   → DuckDuckGo web search (no API key needed)
  - python_exec(code)   → Execute Python in subprocess
  - code_analyze(code)  → Analyze code with an Agno agent (needs API key)

Usage:
  python server.py
"""

import asyncio
import sys
import os
import io
import traceback
import contextlib

from mcp.server import Server
from mcp.server.stdio import stdio_server
import mcp.types as types

server = Server("agno-agent")


# ── Web Search ──────────────────────────────────────────────────────

@server.list_tools()
async def list_tools() -> list[types.Tool]:
    return [
        types.Tool(
            name="web_search",
            description="Search the web using DuckDuckGo. Returns title, URL, and snippet for each result.",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Search query"},
                    "max_results": {
                        "type": "integer",
                        "description": "Max results to return (default 5, max 10)",
                        "default": 5,
                    },
                },
                "required": ["query"],
            },
        ),
        types.Tool(
            name="python_exec",
            description="Execute Python code in a subprocess sandbox. Returns stdout/stderr. Timeout: 30s.",
            inputSchema={
                "type": "object",
                "properties": {
                    "code": {"type": "string", "description": "Python code to execute"},
                },
                "required": ["code"],
            },
        ),
        types.Tool(
            name="code_analyze",
            description="Analyze source code for bugs, security issues, and improvements using an Agno agent. Requires a model API key (OPENAI_API_KEY, ANTHROPIC_API_KEY, etc.).",
            inputSchema={
                "type": "object",
                "properties": {
                    "code": {"type": "string", "description": "Source code to analyze"},
                    "language": {
                        "type": "string",
                        "description": "Programming language (python, javascript, typescript, etc.)",
                    },
                    "focus": {
                        "type": "string",
                        "description": "What to focus on: bugs, security, performance, style, or all",
                        "default": "all",
                    },
                },
                "required": ["code"],
            },
        ),
    ]


# ── Tool Handlers ───────────────────────────────────────────────────

@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[types.TextContent]:
    if name == "web_search":
        return await handle_web_search(arguments)
    elif name == "python_exec":
        return await handle_python_exec(arguments)
    elif name == "code_analyze":
        return await handle_code_analyze(arguments)
    else:
        return [types.TextContent(type="text", text=f"Unknown tool: {name}")]


async def handle_web_search(args: dict) -> list[types.TextContent]:
    query = args.get("query", "")
    max_results = min(int(args.get("max_results", 5)), 10)

    if not query:
        return [types.TextContent(type="text", text="Error: query is required")]

    try:
        import httpx

        async with httpx.AsyncClient() as client:
            resp = await client.get(
                "https://api.duckduckgo.com/",
                params={"q": query, "format": "json", "no_html": 1, "skip_disambig": 1},
                timeout=10,
            )
            data = resp.json()

        text = f"Search results for: {query}\n\n"

        count = 0
        for topic in data.get("RelatedTopics", []):
            if count >= max_results:
                break
            url = topic.get("FirstURL", "")
            title = topic.get("Text", "")
            if title and url:
                # Split into title and body at first " - " or truncate
                parts = title.split(" - ", 1)
                heading = parts[0]
                body = parts[1] if len(parts) > 1 else ""
                text += f"{count + 1}. {heading}\n"
                text += f"   URL: {url}\n"
                if body:
                    text += f"   {body}\n"
                text += "\n"
                count += 1

        if count == 0:
            text += "No results found."

        return [types.TextContent(type="text", text=text.strip())]
    except Exception as e:
        return [types.TextContent(type="text", text=f"Search error: {e}")]


async def handle_python_exec(args: dict) -> list[types.TextContent]:
    code = args.get("code", "")

    if not code:
        return [types.TextContent(type="text", text="Error: code is required")]

    stdout = io.StringIO()
    stderr = io.StringIO()

    try:
        with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            exec(code, {"__builtins__": __builtins__})

        out = stdout.getvalue()
        err = stderr.getvalue()

        result = ""
        if out:
            result += out.rstrip() + "\n"
        if err:
            result += f"[stderr]\n{err.rstrip()}\n"
        if not result:
            result = "(no output)"

        return [types.TextContent(type="text", text=result.strip())]
    except Exception:
        err_text = traceback.format_exc()
        return [types.TextContent(type="text", text=err_text)]


async def handle_code_analyze(args: dict) -> list[types.TextContent]:
    code = args.get("code", "")
    language = args.get("language", "")
    focus = args.get("focus", "all")

    if not code:
        return [types.TextContent(type="text", text="Error: code is required")]

    api_key = os.environ.get("OPENAI_API_KEY") or os.environ.get("ANTHROPIC_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        return [types.TextContent(
            type="text",
            text="Error: No model API key found. Set OPENAI_API_KEY, ANTHROPIC_API_KEY, or GOOGLE_API_KEY environment variable.",
        )]

    try:
        from agno.agent import Agent
        from agno.models.openai import OpenAIChat

        lang_hint = f" in {language}" if language else ""

        agent = Agent(
            model=OpenAIChat(id="gpt-4o-mini"),
            markdown=True,
            instructions=f"You are an expert code reviewer. Analyze the given code{lang_hint} for {focus} issues. Be concise and specific. For each issue: explain what's wrong, why it matters, and suggest a fix.",
        )

        response = await agent.arun(code)
        return [types.TextContent(type="text", text=response.content or "No analysis produced.")]
    except Exception as e:
        return [types.TextContent(type="text", text=f"Analysis error: {e}")]


# ── Main ────────────────────────────────────────────────────────────

async def main():
    async with stdio_server() as (read, write):
        await server.run(read, write, server.create_initialization_options())


if __name__ == "__main__":
    asyncio.run(main())
