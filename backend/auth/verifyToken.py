from jose import jwt, JWTError
from jose.exceptions import ExpiredSignatureError, JWTClaimsError, JWKError
from jose.backends.rsa_backend import RSAKey
from auth.key import fetch_openid_config, get_signing_key
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Dict
from core.config import settings

bearer_scheme = HTTPBearer()

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)) -> Dict:
    token = credentials.credentials
    config = fetch_openid_config()
    issuer = config.get("issuer")

    jwk = get_signing_key(token)
    public_key = RSAKey(jwk, algorithm="RS256")

    try:
        payload = jwt.decode(
            token,
            public_key,
            algorithms=["RS256"],
            audience=settings.CLIENT_ID,
            issuer=issuer,
        )
    except ExpiredSignatureError:
        print('Token has expired')
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Access Denied",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except JWTClaimsError as e:
        print(f"Invalid token claims: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Access Denied",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except JWKError as e:
        print(f"Key error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Access Denied",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except JWTError as e:
        print(f"JWT error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Access Denied",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Optional: Ensure "sub" claim exists
    if "sub" not in payload:
        print("Token missing 'sub' claim")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Access Denied",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return payload  

