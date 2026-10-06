import streamlit as st
import requests
import pandas as pd

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3.2:3b"

st.set_page_config(
    page_title="AI Social Media Content Planner",
    page_icon="📱",
    layout="wide"
)

st.title("📱 AI Social Media Content Planner")
st.write("Generate content ideas, captions, hashtags, and a posting calendar using Ollama.")

def generate_content(prompt):
    payload = {
        "model": MODEL,
        "prompt": prompt,
        "stream": False
    }

    response = requests.post(OLLAMA_URL, json=payload)

    if response.status_code == 200:
        data = response.json()
        return data.get("response", "No response generated.")
    else:
        return f"Error: {response.text}"

platform = st.selectbox(
    "Select Platform",
    ["Instagram", "LinkedIn", "Facebook", "Twitter/X"]
)

niche = st.text_input(
    "Enter Niche",
    placeholder="Example: AI, Education, Fitness, Travel"
)

days = st.slider(
    "Number of Days",
    min_value=3,
    max_value=30,
    value=7
)

if st.button("Generate Content Plan"):
    if niche.strip() == "":
        st.warning("Please enter a niche.")
    else:

        prompt = f"""
        Create a {days}-day social media content plan.

        Platform: {platform}
        Niche: {niche}

        For each day provide:
        1. Content Idea
        2. Caption
        3. Hashtags

        Format clearly.
        """

        with st.spinner("Generating content plan..."):
            result = generate_content(prompt)

        st.subheader("Generated Content Plan")
        st.write(result)

st.markdown("---")

st.subheader("📅 Quick Content Calendar")

if niche:
    calendar_prompt = f"""
    Create a {days}-day content calendar for
    {platform} in the {niche} niche.

    Return a simple table:
    Day | Topic
    """

    if st.button("Generate Calendar"):
        with st.spinner("Creating calendar..."):
            calendar = generate_content(calendar_prompt)

        st.text(calendar)

st.markdown("---")

st.subheader("🏷️ Hashtag Generator")

topic = st.text_input(
    "Enter Topic",
    placeholder="Example: AI Resume Analyzer"
)

if st.button("Generate Hashtags"):
    prompt = f"""
    Generate 20 trending hashtags for:
    {topic}

    Return only hashtags.
    """

    tags = generate_content(prompt)
    st.write(tags)

st.markdown("---")

st.subheader("✍️ Caption Generator")

caption_topic = st.text_input(
    "Caption Topic",
    placeholder="Example: AI Startup Analyzer"
)

if st.button("Generate Caption"):
    prompt = f"""
    Write a professional social media caption for:
    {caption_topic}

    Platform: {platform}
    """

    caption = generate_content(prompt)
    st.write(caption)