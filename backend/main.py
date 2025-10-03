from typing import Dict
from auth.verifyToken import verify_token
from middleware.adminRoleMiddleware import AdminRoleMiddleware
from middleware.authMiddleware import AuthMiddleware
from fastapi import FastAPI, Request, Depends
from fastapi.responses import JSONResponse
from starlette.middleware import Middleware


app = FastAPI(middleware=[
        Middleware(AuthMiddleware),
        Middleware(AdminRoleMiddleware),
    ])


@app.get("/secure-endpoint")
def protected_endpoint(token_data: Dict = Depends(verify_token)):
    return JSONResponse(
                    status_code=200,
                    content={"detail": "Access Granted"},
                )
