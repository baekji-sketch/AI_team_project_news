import json
import os
import re
import time
import openai
import streamlit as st


def get_openai_api_key():
    if st.session_state.get("openai_api_key_input"):
        return st.session_state.openai_api_key_input
    if os.getenv("OPENAI_API_KEY"):
        return os.getenv("OPENAI_API_KEY")
    if hasattr(st, "secrets") and st.secrets.get("OPENAI_API_KEY"):
        return st.secrets.get("OPENAI_API_KEY")
    return None


def initialize_session_state():
    if "story_history" not in st.session_state:
        st.session_state.story_history = []
    if "current_story" not in st.session_state:
        st.session_state.current_story = None
    if "timeline_step" not in st.session_state:
        st.session_state.timeline_step = 0
    if "current_age" not in st.session_state:
        st.session_state.current_age = None


def generate_openai_text(prompt, max_tokens=700):
    api_key = get_openai_api_key()
    if not api_key:
        raise ValueError("Missing OpenAI API key.")

    openai.api_key = api_key
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a professional future news writer."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.85,
        max_tokens=max_tokens,
        top_p=0.95,
        frequency_penalty=0.4,
        presence_penalty=0.3,
    )

    raw_text = response.choices[0].message["content"].strip()
    return parse_story_response(raw_text)


def parse_story_response(raw_text):
    try:
        parsed = json.loads(raw_text)
        return {
            "headline": parsed.get("headline", "Untitled future headline"),
            "article": parsed.get("article", ""),
        }
    except json.JSONDecodeError:
        headline_match = re.search(r'"headline"\s*:\s*"([^"]+)"', raw_text)
        article_match = re.search(r'"article"\s*:\s*"([\s\S]+)"', raw_text)
        headline = headline_match.group(1) if headline_match else "Future headline generated"
        article = article_match.group(1) if article_match else raw_text
        article = article.replace('\\n', '\n')
        return {"headline": headline, "article": article}


def generate_openai_image(prompt, size="1024x1024"):
    api_key = get_openai_api_key()
    if not api_key:
        raise ValueError("Missing OpenAI API key.")

    openai.api_key = api_key
    result = openai.Image.create(
        prompt=prompt,
        n=1,
        size=size,
    )
    return result["data"][0]["url"]


def render_typewriter_text(text, delay=0.02):
    placeholder = st.empty()
    lines = text.strip().split("\n")
    if len(lines) == 1:
        placeholder.markdown(f"<p style='color:#e2e8f0; white-space: pre-line;'>{text}</p>", unsafe_allow_html=True)
        return

    rendered = ""
    for line in lines:
        rendered += line + "\n"
        placeholder.markdown(f"<pre style='font-family: Inter, sans-serif; color:#e2e8f0; line-height:1.65;'>" \
                             f"{rendered}</pre>", unsafe_allow_html=True)
        time.sleep(delay)
