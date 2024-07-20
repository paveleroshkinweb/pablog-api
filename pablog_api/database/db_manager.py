from pablog_api.constant import request_id_ctx_var

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    async_scoped_session,
    async_sessionmaker,
)


def bind_session_to_request_id():
    return request_id_ctx_var.get()


class MasterSlaveManager:

    master_engine: AsyncEngine
    master_session_factory: async_sessionmaker
    master_scoped_session_factory: async_scoped_session

    slave_engine: None | AsyncEngine
    slave_session_factory: None | async_sessionmaker
    slave_scoped_session_factory: None | async_scoped_session

    def __init__(self, master_engine: AsyncEngine, slave_engine: None | AsyncEngine):
        self.master_engine = master_engine
        self.master_session_factory = async_sessionmaker(bind=master_engine, expire_on_commit=False,
                                                         autocommit=False, autoflush=False)
        self.master_scoped_session_factory = async_scoped_session(session_factory=self.master_session_factory,
                                                                  scopefunc=bind_session_to_request_id)

        self.slave_engine = slave_engine
        if slave_engine:
            self.slave_session_factory = async_sessionmaker(bind=slave_engine, expire_on_commit=False,
                                                            autocommit=False, autoflush=False)

            self.slave_scoped_session_factory = async_scoped_session(session_factory=self.slave_session_factory,
                                                                     scopefunc=bind_session_to_request_id)
        else:
            self.slave_session_factory = None
            self.slave_scoped_session_factory = None

    def get_engine(self, use_master: bool = False):
        if use_master:
            return self.master_engine
        return self.slave_engine

    def get_session(self, use_master: bool = False, scoped: bool = True):
        # Make it context manager ???
        if use_master:
            return self.__get_master_session(scoped)
        return self.__get_slave_session(scoped)

    def __get_master_session(self, scoped: bool):
        if scoped:
            return self.master_scoped_session_factory()
        return self.master_session_factory()

    def __get_slave_session(self, scoped: bool):
        if not self.slave_scoped_session_factory or not self.slave_session_factory:
            raise RuntimeError("Slave was not configured")

        if scoped:
            return self.slave_scoped_session_factory()
        return self.slave_session_factory()

    async def close(self):
        await self.master_engine.dispose(close=True)
        await self.slave_engine.dispose(close=True)
