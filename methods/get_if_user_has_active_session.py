from fastapi import Request, HTTPException
from classes.database import Database
import json

async def get_if_user_has_active_session(request: Request):
    request_body = await request.body()
    request_data = json.loads(request_body)

    token = request_data.get('token')

    if token is None:
        raise HTTPException(404, 'You should provide a token to check')
    
    database = Database()

    isOnDatabase = database.exists_user_token(token)

    return {
        'is_active_token': isOnDatabase
    }
    