# loqui ai

multilingual ai assistant that routes between gpt-4o and claude behind a single interface. supports 10 languages with voice input (web speech api) and voice output (aws polly). react frontend, fastapi backend.

## how it works

you type or speak, pick a model and language, and the backend routes your message to the right provider with a language-aware system prompt. responses stream back via sse so you see tokens appear in real time. click listen on any response to hear it read aloud through aws polly neural voices.

## features

- unified chat interface routing between gpt-4o and claude
- sse streaming for real-time token display
- 10 languages with native system prompts
- aws polly neural voices matched per language
- web speech api voice input
- dark glassmorphism ui
- request analytics
- 100% lighthouse seo and best practices
- docker + vercel deployment configs

## setup

### backend
```bash
cd server
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn main:app --reload
```

### frontend
```bash
cd client
npm install
npm run dev
```

## run tests
```bash
cd server && python -m pytest tests/ -v
```
