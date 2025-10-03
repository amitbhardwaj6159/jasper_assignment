import httpx
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from jose.exceptions import ExpiredSignatureError, JWTClaimsError, JWKError
from jose.backends.rsa_backend import RSAKey
import time
from typing import Dict, Optional
from core.config import settings

# === CACHING (optional) ===
_jwks: Optional[Dict] = None
_jwks_last_fetch: float = 0
_JWKS_TTL = 60 * 60  # 1 hour

DISCOVERY_URL = f"{settings.KEYCLOAK_BASE}/realms/{settings.REALM}/.well-known/openid-configuration"


def fetch_openid_config() -> Dict:
    try:
        response = httpx.get(DISCOVERY_URL, timeout=5.0)
        response.raise_for_status()
        return response.json()
    except httpx.RequestError as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error connecting to Keycloak: {str(e)}",
        )
    except httpx.HTTPStatusError as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve OIDC config: {e.response.text}",
        )


def fetch_jwks() -> Dict:
    global _jwks, _jwks_last_fetch
    now = time.time()
    if _jwks is None or (now - _jwks_last_fetch) > _JWKS_TTL:
        config = fetch_openid_config()
        jwks_uri = config.get("jwks_uri")
        if not jwks_uri:
            raise HTTPException(
                status_code=500,
                detail="jwks_uri not found in Keycloak discovery document",
            )
        try:
            response = httpx.get(jwks_uri, timeout=5.0)
            response.raise_for_status()
            _jwks = response.json()
            _jwks_last_fetch = now
        except httpx.RequestError as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to fetch JWKS from Keycloak: {str(e)}",
            )
        except httpx.HTTPStatusError as e:
            raise HTTPException(
                status_code=500,
                detail=f"Error response from Keycloak JWKS endpoint: {e.response.text}",
            )
    return _jwks

# === GET SIGNING KEY FROM JWKS ===
def get_signing_key(token: str) -> Dict:
    jwks = fetch_jwks()
    try:
        unverified_header = jwt.get_unverified_header(token)
    except JWTError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid token header: {str(e)}",
            headers={"WWW-Authenticate": "Bearer"},
        )

    kid = unverified_header.get("kid")
    if not kid:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing 'kid' in token header",
            headers={"WWW-Authenticate": "Bearer"},
        )

    for key in jwks.get("keys", []):
        if key.get("kid") == kid:
            return key

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Public key matching 'kid' not found",
        headers={"WWW-Authenticate": "Bearer"},
    )
