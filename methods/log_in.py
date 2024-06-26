from fastapi import Request, HTTPException
import requests
import os
from jose import jwt
import json
import time

from security.APICryptContext import crypt_context
from classes.database import Database

async def log_in(request: Request):
    try:
        request_body = await request.body()
        data = json.loads(request_body)
    except:
        raise HTTPException(400,detail="The body should be a valid JSON")

    email = data.get('email')
    password = data.get('password')

    if email is None:
        raise HTTPException(status_code=404, detail="Body has to have an email")
    if password is None:
        raise HTTPException(status_code=404, detail="Body has to have a password")
    
    response = requests.get(f"{os.getenv('USERS_API_PATH')}/users/{email}",headers={
        'api-key': os.getenv('USERS_API_KEY')
    })

    print(response.status_code)

    if response.status_code == 200:

        user_data = response.json()

        if user_data['active'] is False:
            raise HTTPException(400, detail='An inactive user cannot be authenticated')
        if user_data['verified'] is False:
            raise HTTPException(400, detail='An unverified user cannot be authenticated')

        user_hashed_password = user_data['password']

        if crypt_context.verify(password, user_hashed_password):
            
            database = Database()

            one_day_on_seconds = 86400

            jwt_token = jwt.encode({
                    'email': user_data['email'],
                    'active': user_data['active'],
                    'expiration': time.time() + one_day_on_seconds
                },
                key= os.getenv('JWT_SECRET_KEY'),
                algorithm='HS256')
            
            database.set_token(user_data['email'], jwt_token, expiration=one_day_on_seconds)

            return {
                'jwt': jwt_token
            }
        else:
            raise HTTPException(403, detail='Invalid password or user')
    if response.status_code == 404:
        raise HTTPException(404, detail='Incorrect password or user')
    
    raise HTTPException(response.status_code, detail='Unhandled error') 