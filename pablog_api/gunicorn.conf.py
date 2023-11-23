from pablog_api.settings.app import settings


bind = settings.service_settings.dsn()

workers = settings.service_settings.workers

worker_class = "uvicorn.workers.UvicornWorker"

reload = settings.is_development()

preload_app = True

reuse_port = True

# Increase default (30) timeout in case of long sync or third party sync requests
timeout = 45

# As gunicorn will be deployed behind the load balancer we should increase default (2) value
keepalive = 4

pidfile = settings.service_settings.pidfile

max_requests = 20000

max_requests_jitter = 10000

# logging
disable_redirect_access_to_syslog = True

enable_stdio_inheritance = True

errorlog = "-"

loglevel = settings.logging.log_level.value.lower()

capture_output = True

logconfig_dict = settings.logging.get_config(settings.environment)
