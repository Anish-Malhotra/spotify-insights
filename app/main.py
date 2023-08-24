from fastapi import FastAPI


app = FastAPI()

@app.get("/test")
def get_test():
    return "Hello test!"