import redis
import os
class Database():
    def __init__(self):
        self.database = redis.from_url(os.getenv('REDIS_CONNECTION_STRING'))
    
    def set_token(self, user_email, jwt_token, expiration):
        return self.database.set(jwt_token, user_email, ex=expiration)

    def exists_user_token(self, token):
        exists_token = self.database.exists(token) == 1
        return exists_token
    
    def delete_user_token(self, token):
        return self.database.delete(token)

    def close_connection(self):
        self.database.close()