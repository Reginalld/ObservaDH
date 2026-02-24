from typing import Any
from typing import Optional

from datetime import datetime
from datetime import timedelta

from jwt import encode
from jwt import decode
from jwt.exceptions import InvalidTokenError

from odhbackend.models import TokenData

from odhbackend.utils.environment_variables import SECRET_KEY

ALGORITHM = "HS256"


def encode_payload(
        payload
) -> str:
    return encode(
        payload=payload,
        key=SECRET_KEY,
        algorithm=ALGORITHM
    )


def decode_jwt(
        jwt: str
) -> Any:
    try:
        return decode(
            jwt=jwt,
            key=SECRET_KEY,
            algorithms=[ALGORITHM]
        )
    except InvalidTokenError:
        return None


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
        expire = datetime.now() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_token_data(token: str) -> TokenData:
    payload = decode_jwt(jwt=token)
    if payload is None:
        return None
    email = payload.get("sub")
    if email is None:
        return None
    return TokenData(email=email)