from pydantic import BaseModel, ConfigDict
from datetime import datetime

class Post_Create(BaseModel):
    title: str
    content: str
    published: bool = True

class Post_Update(Post_Create):
    published: bool

class post_back(Post_Create):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)