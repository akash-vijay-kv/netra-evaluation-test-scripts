import os
import asyncio
import argparse
import uuid
import json
from datetime import datetime
from typing import Dict, Any, List, Optional

from dotenv import load_dotenv
from netra import Netra
from netra.session_manager import ConversationType
from netra.decorators import agent, task
from netra.instrumentation.instruments import InstrumentSet
import openai
from utils.library_tool_schemas import LIBRARY_TOOLS_V1
from utils.library_tools import fetch_current_shelf_books, order_book, get_book_info


load_dotenv()

try:
    api_key = os.environ["NETRA_API_KEY"]
    headers = f"x-api-key={api_key}"
except KeyError:
    headers = None

Netra.init(
    app_name="openai-eval-feature",
    disable_batch=True,
    environment="dev",
    headers=headers,
    instruments={InstrumentSet.OPENAI},
)


OPENAI_MODEL = "gpt-4o-mini"

APP_NAME = "library_eval_feature_demo"
USER_ID = "user_eval"
SESSION_ID = "session_eval_library_001"


@agent(name="Library Assistant Bot")
async def ask_library_agent(query: str) -> str:
    system_prompt = (
        "You are a helpful library assistant. You can check current shelf books, get book info, and place orders. "
        "Use tools as needed and provide a concise final answer."
    )

    Netra.add_conversation(
        conversation_type=ConversationType.INPUT, role="System", content=system_prompt
    )
    Netra.add_conversation(
        conversation_type=ConversationType.INPUT, role="User", content=query
    )

    tools = LIBRARY_TOOLS_V1

    messages: List[Dict[str, Any]] = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": query},
    ]

    final_text = "Agent did not produce a final response."

    with Netra.start_span("chat_service"):
        cached_shelf: Optional[List[Dict[str, Any]]] = None
        for _ in range(4):
            with Netra.start_span(f"llm_generation"):
                resp = openai.chat.completions.create(
                    model=OPENAI_MODEL,
                    messages=messages,
                    tools=tools,
                    tool_choice="auto",
                    temperature=0.7,
                    max_tokens=300,
                )
                msg = resp.choices[0].message
                tool_calls = getattr(msg, "tool_calls", None)

                if tool_calls:
                    assistant_msg = {"role": "assistant", "content": msg.content or ""}
                    assistant_msg["tool_calls"] = [
                        {
                            "id": tc.id,
                            "type": tc.type,
                            "function": {
                                "name": tc.function.name,
                                "arguments": tc.function.arguments,
                            },
                        }
                        for tc in tool_calls
                    ]
                    messages.append(assistant_msg)

                    for tc in tool_calls:
                        name = tc.function.name
                        args = tc.function.arguments or "{}"
                        try:
                            parsed = json.loads(args)
                        except Exception:
                            parsed = {}

                        if name == "fetch_current_shelf_books":
                            if cached_shelf is None:
                                cached_shelf = await fetch_current_shelf_books()
                            content = json.dumps(cached_shelf)
                        elif name == "order_book":
                            res = await order_book(
                                book_id=parsed.get("book_id"),
                                title=parsed.get("title"),
                                quantity=int(parsed.get("quantity", 1) or 1),
                            )
                            content = json.dumps(res)
                        elif name == "get_book_info":
                            res = await get_book_info(
                                book_id=parsed.get("book_id"),
                                title=parsed.get("title"),
                            )
                            content = json.dumps(res)
                        else:
                            content = json.dumps({"error": f"Unknown tool: {name}"})

                        messages.append(
                            {
                                "role": "tool",
                                "tool_call_id": tc.id,
                                "name": name,
                                "content": content,
                            }
                        )
                    continue

            final_text = msg.content or final_text
            break

    Netra.add_conversation(
        conversation_type=ConversationType.OUTPUT, role="Assistant", content=final_text
    )
    return final_text


async def main_async(query: str):
    print(f"\n>>> User Query: {query}\n")
    response = await get_library_agent_response(query)
    print("--- Library Assistant Agent ---")
    print(response)


async def get_library_agent_response(query: str) -> str:
    session_id = str(uuid.uuid4())
    Netra.set_session_id(session_id)
    Netra.set_tenant_id("NextGen Software Corp.")
    Netra.set_user_id("Librarian")
    return await ask_library_agent(query)


def get_library_agent_response_sync(query: str) -> str:
    return asyncio.run(get_library_agent_response(query))


def parse_args():
    parser = argparse.ArgumentParser(description="Library Assistant Agent Demo")
    parser.add_argument(
        "--query",
        default="What books are on my shelf?",
        help="User query to send to the agent",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    asyncio.run(main_async(args.query))
