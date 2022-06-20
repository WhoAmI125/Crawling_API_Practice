from typing import Optional
from fastapi import Body, FastAPI
from pydantic import BaseModel

app = FastAPI()

#Define the design of post and check if user returns the same type of data
class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

#contain post objects
my_posts = [{"title": "title post 1", "content": "content post 1 ", "rating": 10, "id": 1}, 
        {"title": "favorite food", "content": "food", "id": 2}]


# request Get method url: "/"

#referes to the path(route) operation
#decorator, changes to path operation, letting hit the end point and act as api
@app.get("/") # @decorlator.method("path")
def login_user(): #function()
    #whatever returns here is what it shows to the user
    return {"message": "welcome to my api!!!"}

@app.get("/posts") #use to retrieve data
def get_posts():
    return {"data": my_posts}

@app.post("/createposts")
#get the result from class of Post converted
def create_posts(new_post: Post): #saved as pydantic model
    print(new_post.rating)
    print(new_post.dict()) #converts the pydantic model to dictionary
    return {"data": new_post}
#title: str, content: str. We want user to send only two no other.