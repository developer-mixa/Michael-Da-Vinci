"""Port: Message broker interface (publish/consume abstraction)."""

from abc import ABC, abstractmethod
from typing import Any, Callable, Coroutine


class IMessageBroker(ABC):

    @abstractmethod
    async def publish(self, data: dict, queue_name: str) -> None:
        """Publish a message to the given queue."""

    @abstractmethod
    async def wait_response(
        self,
        queue_name: str,
        user_id: int,
        callback: Callable[[Any], Coroutine],
    ) -> None:
        """Wait for a response message for a specific user."""

