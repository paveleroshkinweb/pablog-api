import hashlib
import hmac
import secrets

from http import HTTPStatus

from pablog_api.apps.auth.database.models import User
from pablog_api.apps.auth.exception import AuthUserAlreadyExistException
from pablog_api.apps.auth.role import Role
from pablog_api.apps.auth.service import UserService, get_user_service
from pablog_api.exception.http import BadGatewayException, BadRequestException
from pablog_api.settings.app import get_app_settings

import httpx

from fastapi import APIRouter, Depends
from fastapi.responses import RedirectResponse


settings = get_app_settings()

GITHUB_CLIENT_ID = settings.oauth.github_client_id
GITHUB_CALLBACK = settings.oauth.github_redirect_uri
GITHUB_CLIENT_SECRET = settings.oauth.github_client_secret
GITHUB_AUTH_URL = 'https://github.com/login/oauth/authorize'
GITHUB_TOKEN_URL = 'https://github.com/login/oauth/access_token'
GITHUB_USER_API = 'https://api.github.com/user'
GITHUB_BASE_REDIRECT_URL = (
        f"{GITHUB_AUTH_URL}?client_id={GITHUB_CLIENT_ID}"
        f"&redirect_uri={GITHUB_CALLBACK}"
)

AUTH_ENCODED_PRIVATE_KEY = settings.oauth.private_key.encode()


router = APIRouter(prefix="/auth", tags=["auth"])


@router.get(
    path="/login",
    summary="Redirects to github oauth"
)
def login() -> RedirectResponse:
    random_state = secrets.token_urlsafe(16)
    signature = hmac.new(AUTH_ENCODED_PRIVATE_KEY, random_state.encode(), hashlib.sha256).hexdigest()
    url = f'{GITHUB_BASE_REDIRECT_URL}&state={random_state}:{signature}'
    return RedirectResponse(url)


@router.get(
    path="/callback",
    summary="Handles auth callback from github"
)
async def callback(state: str | None = None, code: str | None = None,
                   user_service: UserService = Depends(get_user_service)):
    if not state or not code:
        raise BadRequestException

    provided_state, signature = state.split(':')
    expected_signature = hmac.new(AUTH_ENCODED_PRIVATE_KEY, provided_state.encode(), hashlib.sha256).hexdigest()
    if signature != expected_signature:
        raise BadRequestException

    async with httpx.AsyncClient() as client:
        token_response = await client.post(
            GITHUB_TOKEN_URL,
            data={
                "client_id": GITHUB_CLIENT_ID,
                "client_secret": GITHUB_CLIENT_SECRET,
                "code": code,
                "redirect_uri": GITHUB_CALLBACK
            },
            headers={"Accept": "application/json"},
            timeout=8.0
        )

    if token_response.status_code != HTTPStatus.OK:
        raise BadGatewayException

    token_json = token_response.json()
    access_token = token_json.get('access_token')
    if access_token is None:
        raise BadGatewayException

    async with httpx.AsyncClient() as client:
        user_response = await client.get(
            GITHUB_USER_API,
            headers={"Authorization": f"Bearer {access_token}", "Accept": "application/vnd.github.v3+json"},
            timeout=8.0,
        )

    if user_response.status_code != HTTPStatus.OK:
        raise BadGatewayException

    user_json = user_response.json()
    github_user_id = user_json.get('id')
    if github_user_id is None:
        raise BadGatewayException

    user = await user_service.find_by_github_id(github_user_id)
    if not user:
        try:
            user = await user_service.save_user(User(
                github_id=github_user_id,
                username=user_json['login'],
                email="",
                roles=[Role.READER]
            ))
        except AuthUserAlreadyExistException:
            pass