# IF : 다른 선택의 미래

A Streamlit-powered cinematic alternate life simulator. Users enter a past choice they did not make, and the app generates a future news headline, a dramatic image, and an emotional alternate-life article. The story can continue 10 years later in the same parallel universe.

## Features

- Alternate life input form with age, personality, interests, and reason
- AI-generated future headlines and immersive news-style articles
- Cinematic image generation for the alternate future
- Continue the story 10 years later with timeline continuity
- Modern dark UI with glassmorphism cards and futuristic styling

## Files

- `app.py` — Streamlit application entry point
- `prompts.py` — Prompt templates for text and image generation
- `utils.py` — OpenAI API helpers, session state management, and display utilities
- `requirements.txt` — Python dependencies

## Setup

1. Create a Python environment and install dependencies:

```bash
pip install -r requirements.txt
```

2. Set your OpenAI API key:

```bash
export OPENAI_API_KEY="your_api_key_here"
```

Or add it to Streamlit secrets using `secrets.toml`.

3. Run the app:

```bash
streamlit run app.py
```

## Deployment

This app is ready for Streamlit Cloud. Ensure the `OPENAI_API_KEY` secret is configured in your Streamlit Cloud project settings.

## Notes

- The app uses session state to preserve timeline continuity and story history.
- The story generator is designed to simulate a parallel world rather than predict a real future.
- For best results, provide a detailed alternate choice and emotional context.
