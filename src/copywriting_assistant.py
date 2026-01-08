import os
import uuid
from typing import Optional
import asyncio

from dotenv import load_dotenv
from openai import OpenAI

from netra import Netra, ConversationType
from netra.decorators import agent, task, span
from netra.instrumentation.instruments import InstrumentSet


load_dotenv()

headers = f"x-api-key={os.getenv('NETRA_API_KEY')}"
Netra.init(
    app_name="Copywriting Assistant",
    disable_batch=True,
    environment="dev",
    headers=headers,
    instruments={InstrumentSet.OPENAI},
    debug_mode=True
)


@task
def brand_guidelines_check(text: str) -> str:
    emojis = [
        "😀",
        "😊",
        "😂",
        "😍",
        "👍",
        "🔥",
        "🎉",
        "😅",
        "😉",
        "🥳",
        "😭",
        "😎",
        "🤩",
        "💯",
        "✨",
        "😜",
        "😁",
        "🤣",
        "🤗",
        "🙌",
        "👏",
        "🤝",
        "🚀",
        "🤙",
    ]
    cleaned = text
    for e in emojis:
        cleaned = cleaned.replace(e, "")
    cleaned = " ".join(cleaned.split())
    return cleaned


@task
def word_limit_check(text: str) -> str:
    WORD_LIMIT = 120
    words = text.split()
    if len(words) <= WORD_LIMIT:
        return text
    return " ".join(words[:WORD_LIMIT])


def generate_copywrite(user_query: str, model: Optional[str] = None) -> str:
    client = OpenAI()
    model_name = model or os.getenv("OPENAI_MODEL", "gpt-4o-mini")

    system_prompt = (
            "You are an expert copywriting assistant with deep knowledge of persuasive writing, marketing psychology, and brand communication."
            "Your role is to help users create compelling, conversion-focused copy across all formats and channels."
            "Generate fun and engaging copy. Make the content engaging and easy to understand."
        )


    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_query},
    ]

    completion = client.chat.completions.create(
        model=model_name,
        messages=messages,
        temperature=1,
        max_tokens=700,
    )
    content = completion.choices[0].message.content

    Netra.add_conversation(
        conversation_type=ConversationType.INPUT,
        role="System",
        content=system_prompt,
    )
    Netra.add_conversation(
        conversation_type=ConversationType.INPUT,
        role="User",
        content=str(user_query),
    )
    Netra.add_conversation(
        conversation_type=ConversationType.OUTPUT,
        role="Assistant",
        content=str(content),
    )

    return content

@span
def refactoring_service(text: str, model: Optional[str] = None) -> str:
    client = OpenAI()
    model_name = model or os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    messages = [
        {
            "role": "system",
            "content": "Format the user input to a professional format. Remove any emojis or casual language. Follow brand guidelines and do not add any policy disclaimers. Expand the response to be more detailed and professional.",
        },
        {"role": "user", "content": text},
    ]
    completion = client.chat.completions.create(
        model=model_name,
        messages=messages,
        temperature=0.2,
        max_tokens=700,
    )
    content = completion.choices[0].message.content
    Netra.add_conversation(
        conversation_type=ConversationType.OUTPUT,
        role="Refactoring Assistant",
        content=str(content),
    )
    return content


@agent(name="Copywrite Generator")
async def ask_copywriting_agent(query: str, model: Optional[str] = None) -> str:
    with Netra.start_span("generation_pipeline"):
        with Netra.start_span("generate_copywrite"):

            # Generate copywrite
            content = generate_copywrite(query, model=model)

        # Branch Guidelines Check
        checked_content = brand_guidelines_check(content)

        # Word Limit Check
        limited_content = word_limit_check(checked_content)

        # Refactor Copywrite
        content = refactoring_service(limited_content, model=model)
        return content


async def get_copywriting_agent_response(
    query: str, model: Optional[str] = None
) -> str:
    if isinstance(query, dict):
        query = query.get("question")

    session_id = str(uuid.uuid4())
    Netra.set_session_id(session_id)
    Netra.set_user_id("Jerina")
    Netra.set_tenant_id("AceTech")
    content = await ask_copywriting_agent(query=query, model=model)
    return content


if __name__ == "__main__":
    asyncio.run(get_copywriting_agent_response(query="Write an interesting blurb about our healthy chopsticks."))