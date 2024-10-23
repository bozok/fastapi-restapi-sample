from fastapi import FastAPI, status


from database import engine, Base
from routers import auth, todos, admin, users

app = FastAPI()

Base.metadata.create_all(bind=engine)

@app.get("/health-check")
async def health_check():
    return {'status': 'Healthy'}

@app.get("/", status_code=status.HTTP_200_OK)
async def root():
    return {"message": "Hello World"}

app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(admin.router)
app.include_router(users.router)
