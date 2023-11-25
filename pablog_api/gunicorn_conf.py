from pablog_api.settings.app import settings

from uvicorn.workers import UvicornH11Worker


class HeadlessUvicornWorker(UvicornH11Worker):
    CONFIG_KWARGS = {**UvicornH11Worker.CONFIG_KWARGS, "server_header": False}


bind = settings.service_settings.dsn()

workers = settings.service_settings.workers

worker_class = "pablog_api.gunicorn_conf.HeadlessUvicornWorker"

reload = settings.is_development()

preload_app = True

reuse_port = True

pidfile = settings.service_settings.pidfile

max_requests = 50000

max_requests_jitter = 10000

# logging
disable_redirect_access_to_syslog = True

enable_stdio_inheritance = True

errorlog = "-"

loglevel = settings.logging.log_level.value.lower()

capture_output = True

logconfig_dict = settings.logging.get_config(settings.environment)
