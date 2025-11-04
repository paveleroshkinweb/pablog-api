from pablog_api.settings.base import BaseAppSettings

import pydantic


class OAuthSettings(BaseAppSettings):

    class Config:
        env_prefix: str = "oauth_"

    github_client_id: str = pydantic.Field()
    github_client_secret: str = pydantic.Field()
    github_redirect_uri: str = pydantic.Field()
