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

    database.delete_user_token(token)

    return {
        'detail': 'log out succesfully'
    }
    pass