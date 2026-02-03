import json
import uuid
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, Generator, Optional
from netra.simulation import TaskResult

import requests


class EventType(Enum):
    """Enumeration of possible event types from the streaming API."""
    INIT = "init"
    FINAL = "final"
    FEEDBACK = "feedback"
    SUGGESTIONS = "suggestions"
    DONE = "done"


@dataclass
class APIResponse:
    """
    Structured response from the customer service API.

    Attributes:
        session_id: Unique identifier for the conversation session
        message: The final response message from the API
        metadata: Additional response metadata (run_id, feedback, suggestions, etc.)
    """
    session_id: str
    message: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class StreamEvent:
    """
    Represents a single event from the streaming API.

    Attributes:
        event_type: Type of the event
        data: Event payload data
        session_id: Session identifier for the conversation
    """
    event_type: str
    data: Optional[Dict[str, Any]]
    session_id: str


class CustomerServiceAPIClient:
    """
    Client for interacting with the customer service streaming API.

    This client handles communication with the customer service API,
    managing sessions, streaming responses, and parsing API events.
    """

    BASE_URL = "https://chatagent-ai-svc.milestoneinternet.com"
    SITE_ID = "5013"
    SITE_URL = "https://www.sunoutdoors.com/"

    def __init__(self, base_url: Optional[str] = None, site_id: Optional[str] = None):
        """
        Initialize the API client.

        Args:
            base_url: Optional custom base URL for the API
            site_id: Optional custom site ID
        """
        self.base_url = base_url or self.BASE_URL
        self.site_id = site_id or self.SITE_ID
        self.session = requests.Session()

    def _get_headers(self) -> Dict[str, str]:
        """
        Generate standard headers for API requests.

        Returns:
            Dictionary of HTTP headers
        """
        return {
            "accept": "text/event-stream",
            "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
            "cache-control": "no-cache",
            "content-type": "application/json",
            "origin": self.SITE_URL,
            "pragma": "no-cache",
            "priority": "u=1, i",
            "referer": self.SITE_URL,
            "sec-ch-ua": '"Google Chrome";v="143", "Chromium";v="143", "Not A(Brand";v="24"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"macOS"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "cross-site",
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36",
            "x-site-id": self.site_id,
            "x-site-url": self.SITE_URL
        }

    def _generate_session_id(self) -> str:
        """
        Generate a new unique session ID.

        Returns:
            UUID string for session identification
        """
        return str(uuid.uuid4())

    def _parse_sse_line(self, line: str) -> tuple[Optional[str], Optional[str]]:
        """
        Parse a Server-Sent Events (SSE) formatted line.

        Args:
            line: Raw SSE line text

        Returns:
            Tuple of (field_name, field_value) or (None, None) if invalid
        """
        if not line or line.startswith(('Connected', 'Connection')):
            return None, None

        if ':' not in line:
            return None, None

        field_name, field_value = line.split(':', 1)
        return field_name.strip(), field_value.strip()

    def _parse_final_event(self, data: Dict[str, Any]) -> Optional[str]:
        """
        Extract message from final event data.

        Args:
            data: Final event data dictionary

        Returns:
            Extracted message string or None
        """
        if not data:
            return None

        if data.get("type") == "markdown":
            content = data.get("content")
            return content if isinstance(content, str) else str(content)

        if data.get("type") == "json" and "content" in data:
            content = data["content"]
            prefix = content.get("prefixText")
            summary = content.get("summary")
            postfix = content.get("postfixText")

            summary_text: Optional[str]
            if summary is None:
                summary_text = None
            elif isinstance(summary, str):
                summary_text = summary
            else:
                summary_text = json.dumps(summary, ensure_ascii=False)

            parts = [
                prefix if isinstance(prefix, str) else None,
                summary_text,
                postfix if isinstance(postfix, str) else None,
            ]
            return "\n".join([p for p in parts if p])

        content = data.get("content")
        return str(content) if content is not None else str(data)

    def send_message(
        self,
        message: str,
        session_id: Optional[str] = None
    ) -> APIResponse:
        """
        Send a message to the customer service API and return the complete response.

        Args:
            message: User message to send to the API
            session_id: Optional session ID for conversation continuity.
                       If not provided, a new session will be created.

        Returns:
            APIResponse object containing the session ID, message, and metadata

        Raises:
            requests.HTTPError: If the API request fails
            requests.RequestException: If there's a network-related error
        """
        session_id = session_id or self._generate_session_id()

        url = f"{self.base_url}/stream"
        payload = {
            "thread_id": session_id,
            "message": message
        }

        try:
            response = self.session.post(
                url,
                headers=self._get_headers(),
                json=payload,
                stream=True,
                timeout=30
            )
            response.raise_for_status()
        except requests.RequestException as e:
            raise RuntimeError(f"Failed to send message to API: {e}") from e

        api_response = APIResponse(session_id=session_id)
        current_event_type = None

        for line in response.iter_lines():
            if not line:
                continue

            line_text = line.decode('utf-8').strip()
            field_name, field_value = self._parse_sse_line(line_text)

            if field_name is None:
                continue

            if field_name == "event":
                current_event_type = field_value
            elif field_name == "data":
                if field_value == "[DONE]":
                    break

                try:
                    data = json.loads(field_value)
                    self._process_event(current_event_type, data, api_response)
                except json.JSONDecodeError:
                    continue

        return api_response

    def _process_event(
        self,
        event_type: Optional[str],
        data: Any,
        response: APIResponse
    ) -> None:
        """
        Process an event and update the response object.

        Args:
            event_type: Type of the event being processed
            data: Event data payload
            response: APIResponse object to update
        """
        if not isinstance(data, dict):
            return

        if event_type == EventType.FINAL.value:
            final_text = self._parse_final_event(data)
            response.message = final_text
            response.metadata["raw_content"] = data.get("content")
            response.metadata["full_response"] = data.get("content")
            response.metadata["final_text"] = final_text

        elif event_type == EventType.FEEDBACK.value:
            if "run_id" in data:
                response.metadata["run_id"] = data["run_id"]
            if "shouldShowFeedback" in data:
                response.metadata["feedback"] = data["shouldShowFeedback"]

        elif event_type == EventType.SUGGESTIONS.value:
            if isinstance(data, list):
                response.metadata["suggestions"] = data

    def send_message_streaming(
        self,
        message: str,
        session_id: Optional[str] = None
    ) -> Generator[StreamEvent, None, None]:
        """
        Send a message and stream the response events in real-time.

        Args:
            message: User message to send to the API
            session_id: Optional session ID for conversation continuity.
                       If not provided, a new session will be created.

        Yields:
            StreamEvent objects containing event type, data, and session ID

        Raises:
            requests.HTTPError: If the API request fails
            requests.RequestException: If there's a network-related error
        """
        session_id = session_id or self._generate_session_id()

        url = f"{self.base_url}/stream"
        payload = {
            "thread_id": session_id,
            "message": message
        }

        try:
            response = self.session.post(
                url,
                headers=self._get_headers(),
                json=payload,
                stream=True,
                timeout=30
            )
            response.raise_for_status()
        except requests.RequestException as e:
            raise RuntimeError(f"Failed to send message to API: {e}") from e

        current_event_type = None

        for line in response.iter_lines():
            if not line:
                continue

            line_text = line.decode('utf-8').strip()
            field_name, field_value = self._parse_sse_line(line_text)

            if field_name is None:
                continue

            if field_name == "event":
                current_event_type = field_value
            elif field_name == "data":
                if field_value == "[DONE]":
                    yield StreamEvent(
                        event_type=EventType.DONE.value,
                        data=None,
                        session_id=session_id
                    )
                    break

                try:
                    data = json.loads(field_value)
                    yield StreamEvent(
                        event_type=current_event_type or EventType.INIT.value,
                        data=data,
                        session_id=session_id
                    )
                except json.JSONDecodeError:
                    continue

    def close(self) -> None:
        """Close the underlying session."""
        self.session.close()

    def __enter__(self) -> "CustomerServiceAPIClient":
        """Context manager entry."""
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """Context manager exit."""
        self.close()
        return None


# Legacy function wrappers for backward compatibility
def call_customer_service_api(
    message: str,
    session_id: Optional[str] = None
) -> Dict[str, Any]:
    """
    Legacy wrapper function for backward compatibility.

    Args:
        message: The user message to send to the API
        session_id: Optional session ID

    Returns:
        Dictionary containing session_id and message
    """
    # raise Exception("Not implemented")
    with CustomerServiceAPIClient() as client:
        response = client.send_message(message, session_id)
        return TaskResult(
            session_id=response.session_id,
            message=response.message or ""
        )

from netra.simulation import BaseTask

class MilestoneAgent(BaseTask):
    def __init__(self):
        super().__init__()

    async def run(self, message: str, session_id: Optional[str] = None):
        result = call_customer_service_api(message, session_id)
        return TaskResult(session_id=result.session_id, message=result.message)


def main():
    """Example usage of the customer service API client."""
    print("-" * 50)
    result = call_customer_service_api(
        message="I choose route 1", session_id="98d647a3-189c-40c8-a399-c8a4fe6f91c6")
    print(result)


if __name__ == "__main__":
    main()
