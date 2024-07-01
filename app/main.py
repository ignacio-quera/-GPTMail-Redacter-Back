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

API_KEY = ""

# Get key from environment variable
# API_KEY = os.getenv("OPENAI_API_KEY")

# 
# API_KEY = os.getenv("OPENAI_API_KEY")

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
            {"role": "system", "content": f'''You are a service which uses the Montoya method to create valuable email given a greeting, a sender name, a case and a request.
              The Montoya method needs to have the following structure: Greeting, presentation of the sender, exposion of case and requeriment. Do NOT generate the 
             The greeting will be recieved in spanish but it needs to be transalated to {language}.'''},
            {"role": "user", "content": f"Compose a short email in {language} from {prompt['name']} to {prompt['to']}, the greeting is {prompt['greeting']}, the case {prompt['case']} and the request {prompt['request']}. Make the email breif and concise using the Montoya method and write it all in {language}."}
        ]
        )
        generated_text = response.choices[0].message
        return generated_text
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def root():
    return {"message": "Hello world"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)