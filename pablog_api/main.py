if __name__ == "__main__":
    from pablog_api.apps.hot_config.commands.app import *  # type: ignore # noqa: F403
    from pablog_api.commands.app import app
    app()
