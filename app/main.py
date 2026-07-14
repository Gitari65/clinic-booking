from fastapi import FastAPI 

app=FastAPI()

@app.get("/")

def home():
    return {"message": "clinic Bookings API is running"}