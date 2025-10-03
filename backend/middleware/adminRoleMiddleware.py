from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.responses import JSONResponse
from fastapi import  Request, HTTPException, status

class AdminRoleMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Only enforce admin role for specific paths
        admin_paths = ["/secure-endpoint"]

        if request.url.path in admin_paths:
            user = getattr(request.state, "user", None)

            if not user:
                return JSONResponse(
                    status_code=401,
                    content={"detail": "Access Denied."},
                )

            roles = user.get("roles", [])
            if "admin" not in roles:
                print("Admin role required")
                return JSONResponse(
                    status_code=403,
                    content={"detail": "Forbidden"},
                )

        return await call_next(request)
