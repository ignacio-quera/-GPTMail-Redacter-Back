from fastapi import HTTPException, Body, FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from openai import OpenAI
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


print(os.getenv("OPENAI_API_KEY"))
API_KEY = os.getenv("OPENAI_API")

client = OpenAI(
    api_key = API_KEY
)

@app.post("/generate", )
async def generate_text(event_data: dict = Body(...)):
    try:
        prompt = event_data["email_data"]
        language = event_data["language"]
        response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a service which uses the Montoya method to create valuable email given a greeting, a sender name, a case and a request."},
            {"role": "user", "content": f"Compose an email in {language} in which the sender name is {prompt['name']}, the greeting is {prompt['greeting']}, the case {prompt['case']} and the request {prompt['request']}."}
        ]
        )
        generated_text = response.choices[0].message
        print(generated_text)
        return generated_text
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def root():
    return {"message": "Hello world"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

