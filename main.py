import streamlit as st
import os
import httpx

# Set up environment variables
API_KEY = os.getenv("ANTHROPIC_API_KEY")
API_URL = "https://api.anthropic.com/v1/messages"
ANTHROPIC_VERSION = "2023-06-01"

st.title("Claude Haiku Chat")

def send_message(prompt):
    headers = {
        "Content-Type": "application/json",
        "X-API-Key": API_KEY,
        "anthropic-version": ANTHROPIC_VERSION
    }
    
    data = {
        "model": "claude-3-haiku-20240307",
        "max_tokens": 1000,
        "messages": [{"role": "user", "content": prompt}]
    }
    
    response = httpx.post(API_URL, json=data, headers=headers)
    
    if response.status_code == 200:
        return response.json()["content"][0]["text"]
    else:
        st.error(f"Error: {response.text}")
        return None

# Streamlit interface
prompt = st.text_input("Enter your prompt:")
if st.button("Send"):
    if prompt:
        response = send_message(prompt)
        if response:
            st.write("Claude:", response)
    else:
        st.error("Please enter a prompt.")
