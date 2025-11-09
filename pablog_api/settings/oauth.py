import base64

from functools import cached_property

from pablog_api.settings.base import BaseAppSettings

import pydantic


class OAuthSettings(BaseAppSettings):

    class Config:
        env_prefix: str = "oauth_"

    github_client_id: str = pydantic.Field()
    github_client_secret: str = pydantic.Field()
    github_redirect_uri: str = pydantic.Field()

    rsa_private_key: str = pydantic.Field()
    rsa_public_key: str = pydantic.Field()
    rsa_is_encoded: bool = pydantic.Field(default=True)

    @cached_property
    def public_key(self) -> str:
        if self.rsa_is_encoded:
            return base64.b64decode(self.rsa_public_key).decode("UTF-8")
        return self.rsa_public_key

    @cached_property
    def private_key(self) -> str:
        if self.rsa_is_encoded:
            return base64.b64decode(self.rsa_private_key).decode("UTF-8")
        return self.rsa_private_key
