from pablog_api.settings.app import settings


bind = settings.service_settings.dsn()

workers = settings.service_settings.workers

worker_class = "uvicorn.workers.UvicornWorker"

reload = settings.is_development()
