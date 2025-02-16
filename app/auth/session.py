from fastapi import Request, Response
from itsdangerous import URLSafeSerializer
from fastapi.middleware import Middleware
from starlette.middleware.sessions import SessionMiddleware
from app.config.settings import settings
SECRET_KEY =  settings.SECRET_KEY



serializer = URLSafeSerializer(SECRET_KEY)

def create_session(response: Response, username: str):
    session_token = serializer.dumps({"username": username})
    response.set_cookie(key="session_token", value=session_token, httponly=True)


def get_session(request: Request):
    session_token = request.cookies.get("session_token")
    if session_token:
        try:
            data = serializer.loads(session_token)
            return data
        except Exception:
            return None
    return None


def clear_session(response: Response):
    response.delete_cookie("session_token")