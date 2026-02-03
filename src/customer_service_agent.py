from netra.simulation import BaseTask
from netra import Netra
import json
import os
import uuid
from typing import Any, Dict, List, Optional, Annotated, TypedDict

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage, ToolMessage, BaseMessage
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import MemorySaver
from netra.simulation import TaskResult

from utils.refund_tools import TOOL_REGISTRY
from utils.refund_tool_schemas import REFUND_TOOLS

load_dotenv()


headers = f"x-api-key={os.getenv('NETRA_API_KEY')}"
Netra.init(
    app_name="Customer Service Agent",
    headers=headers,
)


class AgentState(TypedDict):
    """State for the customer service agent."""
    messages: Annotated[List[BaseMessage], add_messages]


SYSTEM_PROMPT = """You are a helpful and professional customer service agent for an e-commerce company. Your primary role is to assist customers with refund requests and order inquiries.

**Your Capabilities:**
- Look up customer orders using their user ID or email
- Check order details and status
- Verify refund eligibility based on company policies
- Process refund requests for eligible orders
- Explain refund policies to customers

**Guidelines:**
1. Always be polite, empathetic, and professional
2. Before processing a refund, always verify the order exists and check eligibility
3. Clearly explain the refund policy when relevant
4. If a refund is not possible, explain why and offer alternatives if applicable
5. Confirm important details with the customer before processing refunds
6. Provide refund IDs and estimated timelines after successful processing

**Available User IDs for testing:**
- U-001 (John Smith, Gold member)
- U-002 (Jane Doe, Silver member)  
- U-003 (Bob Wilson, Standard member)

When a customer provides their information, use the appropriate tools to look up their orders and assist with their refund request."""


class CustomerServiceAgent:
    """LangGraph-based customer service agent for handling refund requests."""

    def __init__(self, model_name: str = "gpt-4o-mini"):
        """Initialize the customer service agent.

        Args:
            model_name: OpenAI model to use for inference
        """
        self.llm = ChatOpenAI(
            model=model_name,
            temperature=0,
            api_key=os.getenv("OPENAI_API_KEY"),
        )
        self.llm_with_tools = self.llm.bind_tools(REFUND_TOOLS)
        self.memory = MemorySaver()
        self.graph = self._build_graph()

    def _build_graph(self) -> StateGraph:
        """Build the LangGraph workflow."""
        workflow = StateGraph(AgentState)

        workflow.add_node("agent", self._agent_node)
        workflow.add_node("tools", self._tool_node)

        workflow.set_entry_point("agent")

        workflow.add_conditional_edges(
            "agent",
            self._should_continue,
            {
                "continue": "tools",
                "end": END,
            },
        )

        workflow.add_edge("tools", "agent")

        return workflow.compile(checkpointer=self.memory)

    def _agent_node(self, state: AgentState) -> Dict[str, Any]:
        """Process the current state and generate a response."""
        messages = state["messages"]

        messages_with_system = [SystemMessage(
            content=SYSTEM_PROMPT)] + messages

        response = self.llm_with_tools.invoke(messages_with_system)

        return {"messages": [response]}

    def _tool_node(self, state: AgentState) -> Dict[str, Any]:
        """Execute tool calls from the agent."""
        messages = state["messages"]
        last_message = messages[-1]

        tool_messages = []

        if hasattr(last_message, "tool_calls") and last_message.tool_calls:
            for tool_call in last_message.tool_calls:
                tool_name = tool_call["name"]
                tool_args = tool_call["args"]
                tool_id = tool_call["id"]

                if tool_name in TOOL_REGISTRY:
                    try:
                        result = TOOL_REGISTRY[tool_name](**tool_args)
                        tool_messages.append(
                            ToolMessage(
                                content=json.dumps(result, indent=2),
                                tool_call_id=tool_id,
                            )
                        )
                    except Exception as e:
                        tool_messages.append(
                            ToolMessage(
                                content=json.dumps({"error": str(e)}),
                                tool_call_id=tool_id,
                            )
                        )
                else:
                    tool_messages.append(
                        ToolMessage(
                            content=json.dumps(
                                {"error": f"Unknown tool: {tool_name}"}),
                            tool_call_id=tool_id,
                        )
                    )

        return {"messages": tool_messages}

    def _should_continue(self, state: AgentState) -> str:
        """Determine if the agent should continue with tool execution or end."""
        messages = state["messages"]
        last_message = messages[-1]

        if hasattr(last_message, "tool_calls") and last_message.tool_calls:
            return "continue"
        return "end"

    def invoke(self, message: str, session_id: str) -> Dict[str, Any]:
        """Invoke the agent with a message and session ID.

        Args:
            message: The user's message
            session_id: Unique session identifier for conversation continuity

        Returns:
            Dictionary containing session_id and the agent's response message
        """
        config = {"configurable": {"thread_id": session_id}}

        input_state = {"messages": [HumanMessage(content=message)]}

        result = self.graph.invoke(input_state, config)

        final_message = result["messages"][-1]
        response_content = final_message.content if hasattr(
            final_message, "content") else str(final_message)

        return {
            "session_id": session_id,
            "message": response_content,
        }


_agent_instance: Optional[CustomerServiceAgent] = None


def get_agent() -> CustomerServiceAgent:
    """Get or create the singleton agent instance."""
    global _agent_instance
    if _agent_instance is None:
        _agent_instance = CustomerServiceAgent()
    return _agent_instance


def call_customer_service_bot(
    message: str,
    session_id: Optional[str] = None
) -> Dict[str, Any]:
    """
    Invoke the customer service bot with a message and session ID.

    This function provides a simple interface to interact with the LangGraph-based
    customer service agent. It handles session management and returns the agent's
    response.

    Args:
        message: The user's message to send to the bot
        session_id: Optional session ID for conversation continuity.
                   If not provided, a new session will be created.

    Returns:
        Dictionary containing:
            - session_id: The session identifier (existing or newly created)
            - message: The agent's response message

    Example:
        >>> result = call_customer_service_bot("I want to request a refund for order ORD-1001")
        >>> print(result["message"])
    """
    if session_id is None:
        session_id = str(uuid.uuid4())

    agent = get_agent()
    result = agent.invoke(message, session_id)
    return TaskResult(session_id=result.get("session_id"), message=result.get("message"))


class CustomerServiceBot(BaseTask):
    def __init__(self):
        super().__init__()

    async def run(self, message: str, session_id: Optional[str] = None):
        result = call_customer_service_bot(message, session_id)
        return TaskResult(session_id=result.session_id, message=result.message)


def main():
    """Example usage of the customer service bot."""
    print("=" * 60)
    print("Customer Service Bot - Refund Processing Demo")
    print("=" * 60)

    session_id = str(uuid.uuid4())
    print(f"\nSession ID: {session_id}\n")

    conversations = [
        "Hi, I'm John Smith with user ID U-001. I'd like to request a refund.",
        "I want to return the Wireless Bluetooth Headphones. The reason is that the product is defective.",
    ]

    for user_message in conversations:
        print(f"User: {user_message}")
        print("-" * 40)

        result = call_customer_service_bot(user_message, session_id)
        print(f"Bot: {result['message']}")
        print("=" * 60)


if __name__ == "__main__":
    main()
