from fastapi import FastAPI, Request, Form
from pydantic import BaseModel
import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = FastAPI()

class FormData(BaseModel):
    name: str
    email: str
    phone: str = None
    message: str

@app.post("/submit-form")
async def submit_form(
    name: str = Form(...),
    email: str = Form(...),
    phone: str = Form(None),
    message: str = Form(...),
):
    # Retrieve the Web3Forms API key from environment variables
    api_key = os.getenv('W3_FORMS_API')

    form_data = {
        'access_key': api_key,
        'subject': 'New Contact Form Submission',
        'from_name': 'My Website',
        'name': name,
        'email': email,
        'phone': phone,
        'message': message
    }

    # Make the POST request to Web3Forms
    try:
        response = requests.post('https://api.web3forms.com/submit', json=form_data)
        data = response.json()

        if data.get('success'):
            return {"message": "Form submitted successfully"}
        else:
            return {"message": "Failed to submit the form"}

    except Exception as e:
        return {"message": "Server Error", "error": str(e)}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
