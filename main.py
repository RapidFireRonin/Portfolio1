import streamlit as st
import os
import httpx

# Set up environment variables
API_KEY = os.getenv("ANTHROPIC_API_KEY")
API_URL = "https://api.anthropic.com/v1/messages"
ANTHROPIC_VERSION = "2023-06-01"

st.title("Claude Haiku Chat")

# System message to be included in the prompt
SYSTEM_MESSAGE = "You are an AI assistant. Provide helpful and accurate information."

def send_message(user_prompt):
    headers = {
        "Content-Type": "application/json",
        "X-API-Key": API_KEY,
        "anthropic-version": ANTHROPIC_VERSION
    }

    # Combine the system message with the user prompt
    full_prompt = f"{SYSTEM_MESSAGE}\n\nUser: {user_prompt}"

    data = {
        "model": "claude-3-haiku-20240307",
        "max_tokens": 1000,
        "messages": [{"role": "user", "content": full_prompt}]
    }

    try:
        response = httpx.post(API_URL, json=data, headers=headers)
        response.raise_for_status()
        return response.json()["content"][0]["text"]
    except httpx.HTTPStatusError as e:
        st.error(f"HTTP error occurred: {e.response.text}")
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
    return None

# Streamlit interface
user_prompt = st.text_input("Enter your prompt:")
if st.button("Send"):
    if user_prompt:
        response = send_message(user_prompt)
        if response:
            st.write("Claude:", response)
    else:
        st.error("Please enter a prompt.")
