from abc import ABC, abstractmethod

from app.infra.integrations.notifications.dtos import Notification


class BaseNotificationClient(ABC):
    @abstractmethod
    async def _format_notification(self, notification: Notification): ...

    @abstractmethod
    async def send(self, notification: Notification): ...
