import uuid

from contextlib import asynccontextmanager

from pablog_api.constant import request_id_ctx_var

from sqlalchemy.ext.asyncio import async_scoped_session, async_sessionmaker


def bind_session_to_request_id():
    request_id = request_id_ctx_var.get()
    # In shell environment
    if not request_id:
        request_id = uuid.uuid4()
    return request_id


class MasterSlaveManager:

    def __init__(self, session_factory: async_sessionmaker):
        self.session_factory: async_sessionmaker = session_factory
        self.scoped_session: async_scoped_session = async_scoped_session(
            session_factory=self.session_factory, scopefunc=bind_session_to_request_id
        )

    @asynccontextmanager
    async def master_session(self, nested=False):
        async with self.scoped_session(use_master=True) as session:
            try:
                if nested and session.in_transaction():
                    async with session.begin_nested():
                        yield session
                else:
                    yield session
            finally:
                await session.close()

    @asynccontextmanager
    async def slave_session(self):
        async with self.scoped_session(use_master=False) as session:
            try:
                yield session
            finally:
                await session.close()

    async def close(self):
        await self.scoped_session.close()
