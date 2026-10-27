# 👻 Study Boss Battle

Turn your study notes into a monster battle!
Upload a PDF, and an open-source AI makes quiz questions from it.
Answer right to hurt the monster. Answer wrong and you lose health.

Built for the Hacktoberfest 2026 Open-Source AI Challenge (Week 4).

## How it works

1. Upload your notes as a PDF.
2. The AI (gpt-oss, an open-weight model) makes 3 quiz questions.
3. The monster and you both start with 90 HP.
4. Right answer: the monster loses 30 HP.
5. Wrong answer: you lose 30 HP.
6. Defeat the monster to win!

## Why open source?

- The model is open-weight, so I can swap it for another one easily.
- My notes are private, so I want control over where they go.

## Run it yourself

1. Install the tools:
   `pip install -r requirements.txt`
2. Save your Ollama API key as an environment variable named `OLLAMA_API_KEY`.
3. Start the app:
   `python -m streamlit run app.py`

## Built with

- Python
- Streamlit
- pypdf
- Ollama (gpt-oss:120b)
