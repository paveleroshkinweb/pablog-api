from contextvars import ContextVar


REQUEST_ID_HEADER: str = "X-Request-Id"

request_id_ctx_var: ContextVar[str] = ContextVar(REQUEST_ID_HEADER, default='')
