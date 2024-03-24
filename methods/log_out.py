from fastapi import Request, HTTPException
import json
from classes.database import Database

async def log_out(request: Request):
    try:
        request_body = await request.body()
        data = json.loads(request_body)
    except:
        raise HTTPException(400,detail="The body should be a valid JSON")
    
    token = data.get('token')

    database = Database()

    wasDeleted = database.delete_user_token(token)
    
    if (wasDeleted):
        return {
            'detail': 'log out succesfully'
        }
    else:
        return {
            'detail': 'token not found for sign out'
        }