from jose import jwt

from core.config import settings
from core.security import create_access_token, get_password_hash, verify_password


def test_password_hashing():
    password = "secret_password_123"
    hashed = get_password_hash(password)
    assert hashed != password
    assert verify_password(password, hashed) is True
    assert verify_password("wrong_password", hashed) is False

def test_create_access_token():
    data = {"sub": "test@example.com"}
    token = create_access_token(data)
    assert isinstance(token, str)

    # Decode and verify
    payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    assert payload.get("sub") == "test@example.com"
    assert "exp" in payload
