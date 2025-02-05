from fastapi import FastAPI
import uvicorn  # Import uvicorn
from enum import Enum

class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"




#FastAPI is a Python class that provides all the functionality for your API.
app = FastAPI()

@app.get("/")
async def hello_world():
    return {"hello": "world"}
#path parameter itemid will be passed to the function as the argument
@app.get("/items/{item_id}")
async def read_item(item_id):
    return {"item_id": item_id}
#path paramaters with type so we should respect this type or we will get an error
@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}
#order matter the path operation will be executed in the order they are defined
@app.get("/users/me")
async def read_user_me():
    return {"user_id": "the current user"}


@app.get("/users/{user_id}")
async def read_user(user_id: str):
    return {"user_id": user_id}
#predefined values u can use the standard python enum
@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name is ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}

    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}

    return {"model_name": model_name, "message": "Have some residuals"}


#openAPI could support the path parameter with the type path
@app.get("/files/{file_path:path}")
async def read_file(file_path: str):
    return {"file_path": file_path}
test

# Run the app using uvicorn programmatically
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)