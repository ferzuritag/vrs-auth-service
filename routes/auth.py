from fastapi import APIRouter, Request, Header

from methods.log_in import log_in
from methods.get_if_user_has_active_session import get_if_user_has_active_session
from methods.log_out import log_out

from security.checkAPIKey import check_api_key

auth = APIRouter()

@auth.post('/auth')
async def LogIn(request: Request):
    return await log_in(request)

@auth.delete('/auth')
async def LogOut(request: Request):
    return await log_out(request)

@auth.get('/auth/session')
async def getIfUserHasActiveSession(request: Request, api_key = Header()):
    check_api_key(api_key)
    return await get_if_user_has_active_session(request)
