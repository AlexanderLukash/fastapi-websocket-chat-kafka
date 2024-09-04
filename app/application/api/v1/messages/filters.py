from pydantic import BaseModel

from app.infra.repositories.filters.messages import (
    GetMessagesFilters as GetMessagesInfraFilters,
    GetAllChatsFilters,
)


class GetMessagesFilters(BaseModel):
    limit: int = 10
    offset: int = 0

    def to_infra(self):
        return GetMessagesInfraFilters(
            limit=self.limit,
            offset=self.offset,
        )


class GetChatsFilters(BaseModel):
    limit: int = 10
    offset: int = 0

    def to_infra(self):
        return GetAllChatsFilters(
            limit=self.limit,
            offset=self.offset,
        )
