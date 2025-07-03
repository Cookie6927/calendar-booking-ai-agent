# AI Calendar Booking Agent 🤖📅

This project uses FastAPI, LangChain, and Google Gemini to build a conversational assistant that books meetings on Google Calendar.

## Features

- Conversational LLM agent using Gemini
- Google Calendar booking via Service Account
- Chat UI using Streamlit

## Tech Stack

- Python, FastAPI, Streamlit
- LangChain + Gemini Pro
- Google Calendar API

## Setup

1. `pip install -r requirements.txt`
2. Add your `.env` file and service_account.json
3. Run `uvicorn backend.main:app --reload`
4. Run `streamlit run streamlit_app.py`
