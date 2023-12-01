"""
Helper functions for the CLI
"""

from __future__ import annotations

from pathlib import Path
from textwrap import dedent
from typing import Iterator

from click.exceptions import ClickException
from langchain.chat_models import ChatAnthropic, ChatOpenAI
from langchain.llms import GPT4All
from langchain.llms.base import BaseLLM
from langchain.schema import AIMessage, BaseMessage, HumanMessage, SystemMessage
from langchain_core.language_models import BaseChatModel
from langchain_core.messages import BaseMessageChunk
from prompt_toolkit import PromptSession
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.history import FileHistory
from rich.columns import Columns
from rich.console import Console
from rich.live import Live
from rich.markdown import Markdown
from rich.panel import Panel
from rich.spinner import Spinner

from llm_term.__about__ import __application__, __version__
from llm_term.base import NoPadding


def print_header(console: Console, model: str) -> None:
    """
    Print the header
    """
    console.print(
        Panel(
            f"[bold red]{__application__} "
            f"is a command line interface for OpenAI's Chat API[/bold red]",
            title=f"[blue bold]{__application__} v{__version__}[/blue bold]",
            subtitle=f"[yellow bold]{model}[/yellow bold]",
            style="green bold",
            expand=False,
        ),
    )
    console.print("")


def get_llm(provider: str, api_key: str, model: str | None) -> tuple[BaseChatModel | BaseLLM, str]:
    """
    Check the credentials
    """
    if provider == "openai":
        chat_model = model or "gpt-3.5-turbo"
        return ChatOpenAI(openai_api_key=api_key, model_name=chat_model), chat_model
    elif provider == "anthropic":
        chat_model = model or "claude-2.1"
        return ChatAnthropic(anthropic_api_key=api_key, model_name=chat_model), chat_model
    elif provider == "gpt4all":
        chat_model = model or "mistral-7b-openorca.Q4_0.gguf"
        return GPT4All(model=chat_model, allow_download=True), chat_model
    else:
        msg = f"Provider {provider} is not supported... yet"
        raise ClickException(msg)


def setup_system_message(message: str | None = None) -> SystemMessage:
    """
    Set up the system message
    """
    setup = f"""
        You are a helpful AI assistant named {__application__}. Help the user by responding to
        their request, the output should be concise and always written in markdown format.
        Answer questions only if you know the answer or can make a well-informed guess;
        otherwise tell the you don't know or ask for more information.
        """
    system_message = message or dedent(setup).strip()
    return SystemMessage(content=system_message)


def chat_session(
    client: BaseChatModel | BaseLLM,
    console: Console,
    system_message: SystemMessage,
    stream: bool,
    panel: bool,
    chat_message: str,
    avatar: str,
) -> None:
    """
    Chat session with ChatGPT
    """
    history_file = Path().home() / ".llm-term-history.txt"
    history = FileHistory(str(history_file))
    session: PromptSession = PromptSession(history=history, erase_when_done=True)
    messages: list[BaseMessage] = [system_message]
    if chat_message.strip() != "":
        messages.append(HumanMessage(content=chat_message))
    message_counter = 0
    while True:
        if message_counter == 0 and len(messages) == 2:  # noqa: PLR2004
            console.print(f"{avatar}: {chat_message}")
            history.append_string(chat_message)
            if panel is False:
                console.print("")
                console.rule()
        else:
            text = session.prompt(f"{avatar}: ", auto_suggest=AutoSuggestFromHistory())
            if not text:
                continue
            console.print(f"{avatar}: {text}")
            if panel is False:
                console.print("")
                console.rule()
            messages.append(HumanMessage(content=text))
        console.print("")
        streamed_message = print_response(
            client=client,
            console=console,
            messages=messages,
            stream=stream,
            panel=panel,
        )
        if panel is False:
            console.print("")
            console.rule()
        messages.append(streamed_message)
        console.print("")
        message_counter += 1


def print_response(
    client: BaseChatModel | BaseLLM,
    console: Console,
    messages: list[BaseMessage],
    stream: bool,
    panel: bool,
) -> AIMessage:
    """
    Stream the response
    """
    panel_class = Panel if panel is True else NoPadding
    if stream is False:
        with Live(Spinner("aesthetic"), refresh_per_second=15, console=console, transient=True):
            response = client.invoke(input=messages)
            if isinstance(response, BaseMessage):
                text = response.content or ""
            else:
                text = response or ""
            console.print(panel_class(Markdown(response.content), title="🤖", title_align="left"))
        message = AIMessage(content=text)
    else:
        response = client.stream(input=messages)
        message = render_streamed_response(response=response, console=console, panel=panel)
    return message


def render_streamed_response(
    response: Iterator[BaseMessageChunk | str], console: Console, panel: bool
) -> AIMessage:
    """
    Render the streamed response and a spinner
    """
    panel_class = Panel if panel is True else NoPadding
    complete_message = ""
    rich_response = Columns(
        [
            panel_class(Markdown(complete_message), title="🤖", title_align="left"),
            Spinner("aesthetic"),
        ]
    )
    with Live(
        rich_response,
        refresh_per_second=15,
        console=console,
    ) as live:
        for chunk in response:
            if isinstance(chunk, BaseMessageChunk):
                chunk_text = chunk.content or ""
            else:
                chunk_text = chunk or ""
            complete_message += chunk_text
            updated_response = Columns(
                [
                    panel_class(Markdown(complete_message), title="🤖", title_align="left"),
                    Spinner("aesthetic"),
                ]
            )
            live.update(updated_response)
        live.update(panel_class(Markdown(complete_message), title="🤖", title_align="left"))
    return AIMessage(content=complete_message)