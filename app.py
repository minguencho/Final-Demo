from fastapi import FastAPI

from capstone.routers import map, authentication, user, menu


app = FastAPI()
      

app.include_router(authentication.router)
app.include_router(user.router)
app.include_router(menu.router)
app.include_router(map.router)

