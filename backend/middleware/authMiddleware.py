from fastapi import  Request, HTTPException, status
from fastapi.responses import  JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware 
from jose import jwt, JWTError
from jose.exceptions import ExpiredSignatureError, JWTClaimsError, JWKError
from auth.key import fetch_openid_config, get_signing_key
from core.config import settings


class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Allow open endpoints (optional)
        if request.url.path in ["/open", "/docs", "/openapi.json"]:
            return await call_next(request)

        
        unAuthenticatedMsg = "Access Denied."

        # Extract token from Authorization header
        auth_header: str = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            print("Missing or invalid Authorization header")
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"detail": unAuthenticatedMsg},
                headers={"WWW-Authenticate": "Bearer"},
            )

        token = auth_header.split(" ")[1]
        

        try:
            config = fetch_openid_config()
            issuer = config.get("issuer")
            key = get_signing_key(token)

            payload = jwt.decode(
                token,
                key,
                algorithms=["RS256"],
                audience=settings.CLIENT_ID,
                issuer=issuer,
            )

            # Attach user info to request state
            request.state.user = {
                "sub": payload.get("sub"),
                "email": payload.get("email"),
                "username": payload.get("preferred_username"),
                "roles": payload.get("realm_access", {}).get("roles", []),
                "raw": payload,
            }


        except ExpiredSignatureError:
            print("Token has expired")
            return JSONResponse(
                status_code=401,
                content={"detail": unAuthenticatedMsg},
                headers={"WWW-Authenticate": "Bearer"},
            )
        except JWTClaimsError as e:
            print(f"Invalid token claims: {str(e)}")
            return JSONResponse(
                status_code=401,
                content={"detail": unAuthenticatedMsg},
                headers={"WWW-Authenticate": "Bearer"},
            )
        except JWTError as e:
            print(f"JWT error: {str(e)}")
            return JSONResponse(
                status_code=401,
                content={"detail": unAuthenticatedMsg},
                headers={"WWW-Authenticate": "Bearer"},
            )
        except HTTPException as e:
            print(e.detail)
            return JSONResponse(
                status_code=e.status_code,
                content={"detail":unAuthenticatedMsg},
                headers={"WWW-Authenticate": "Bearer"},
            )
        except Exception as e:
            print(f"Internal server error: {str(e)}")
            return JSONResponse(
                status_code=500,
                content={"detail": unAuthenticatedMsg},
            )

        return await call_next(request)
        
    
