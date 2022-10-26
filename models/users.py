from pydantic import BaseModel


class userAuthModel(BaseModel):
    username: str
    password: str
