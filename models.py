from pydantic import BaseModel
from typing import Optional, List



class UserItem(BaseModel):
    username : str