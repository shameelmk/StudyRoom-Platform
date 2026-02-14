from fastapi import FastAPI

app = FastAPI(title="StudyRoom Platform", description="StudyRoom Platform API", version="0.0.1")

@app.get("/")
def read_root():
    return {"Hello": "World"}
