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
    async def master_session(self, nested: bool = False):
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

    @asynccontextmanager
    async def current_session(self, use_master_if_missing: bool = True, nested: bool = False):
        session = self.scoped_session.registry.registry.get(bind_session_to_request_id())

        if not session:

            if use_master_if_missing:
                async with self.master_session(nested) as master_session:
                    yield master_session

            else:
                async with self.slave_session() as slave_session:
                    yield slave_session

        else:

            try:
                yield session
            finally:
                await session.close()

    async def close(self):
        await self.scoped_session.close()
