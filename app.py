import os
import json
import re
import streamlit as st
from pypdf import PdfReader
from ollama import Client

# -----------------------------
# Page setup
# -----------------------------
st.set_page_config(
    page_title="Study Boss Battle",
    page_icon="👻",
    layout="centered",
    initial_sidebar_state="expanded",
)

# -----------------------------
# Styling
# -----------------------------
st.markdown(
    """
    <style>
    .stApp {
        background: radial-gradient(circle at top, #20263a 0%, #0d1018 55%, #080a0f 100%);
    }
    .block-container { max-width: 950px; padding-top: 2rem; padding-bottom: 3rem; }
    .hero { text-align: center; padding: 1rem 0 1.5rem; }
    .hero h1 { font-size: 3rem; margin-bottom: .2rem; }
    .hero p { color: #b9c0d0; font-size: 1.1rem; }
    .card {
        background: rgba(24, 28, 40, .92);
        border: 1px solid rgba(255,255,255,.10);
        border-radius: 18px;
        padding: 1.2rem;
        margin: .8rem 0;
        box-shadow: 0 12px 35px rgba(0,0,0,.22);
    }
    .boss-name { font-size: 1.7rem; font-weight: 800; text-align:center; }
    .boss-desc { color:#b9c0d0; text-align:center; margin-top:.2rem; }
    .stat { text-align:center; font-weight:700; }
    .question-count { color:#aeb6c8; font-weight:700; text-transform:uppercase; letter-spacing:.08em; }
    .feedback-good { background: rgba(25, 135, 84, .18); border: 1px solid rgba(25, 135, 84, .45); padding: 1rem; border-radius: 14px; }
    .feedback-bad { background: rgba(220, 53, 69, .16); border: 1px solid rgba(220, 53, 69, .45); padding: 1rem; border-radius: 14px; }
    .result-score { font-size: 3.2rem; font-weight: 900; text-align:center; }
    </style>
    """,
    unsafe_allow_html=True,
)

# -----------------------------
# Helpers
# -----------------------------

def init_state():
    defaults = {
        "questions": [],
        "current": 0,
        "monster_hp": 100,
        "player_hp": 100,
        "score": 0,
        "correct": 0,
        "wrong": 0,
        "combo": 0,
        "best_combo": 0,
        "feedback": None,
        "battle_started": False,
        "battle_finished": False,
        "won": False,
        "boss_name": "Study Demon",
        "boss_emoji": "👹",
        "boss_description": "A monster made from your toughest notes.",
        "pdf_name": "",
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def reset_battle():
    for key in [
        "questions", "current", "monster_hp", "player_hp", "score", "correct",
        "wrong", "combo", "best_combo", "feedback", "battle_started",
        "battle_finished", "won", "boss_name", "boss_emoji", "boss_description", "pdf_name"
    ]:
        st.session_state.pop(key, None)
    init_state()


def get_client():
    api_key = os.getenv("OLLAMA_API_KEY")
    if not api_key:
        raise RuntimeError("OLLAMA_API_KEY is not set. Add your Ollama API key before starting a battle.")
    return Client(
        host="https://ollama.com",
        headers={"Authorization": "Bearer " + api_key},
    )


def clean_json(text):
    text = text.strip()
    text = re.sub(r"^```(?:json)?\s*", "", text, flags=re.IGNORECASE)
    text = re.sub(r"\s*```$", "", text)

    # If the model adds extra text, keep the largest JSON object/array.
    first_array = text.find("[")
    last_array = text.rfind("]")
    if first_array != -1 and last_array > first_array:
        text = text[first_array:last_array + 1]
    return text


def validate_questions(data, expected_count):
    if not isinstance(data, list):
        raise ValueError("AI did not return a list of questions.")

    valid = []
    seen = set()
    for item in data:
        if not isinstance(item, dict):
            continue
        question = str(item.get("question", "")).strip()
        options = item.get("options", [])
        answer = str(item.get("answer", "")).strip()
        explanation = str(item.get("explanation", "")).strip()

        if not question or not isinstance(options, list) or len(options) != 4 or not answer:
            continue

        options = [str(x).strip() for x in options]
        if len(set(options)) != 4 or answer not in options:
            continue

        key = question.lower()
        if key in seen:
            continue
        seen.add(key)

        valid.append({
            "question": question,
            "options": options,
            "answer": answer,
            "explanation": explanation or "Review this concept in your notes and try again.",
        })

    if len(valid) < expected_count:
        raise ValueError(f"Only {len(valid)} reliable questions were generated; {expected_count} were needed.")
    return valid[:expected_count]


def make_questions(text, difficulty, count):
    client = get_client()
    difficulty_rules = {
        "Easy": "Focus on definitions, facts, and direct understanding.",
        "Medium": "Test understanding and simple application of concepts.",
        "Hard": "Use application, comparison, reasoning, and tricky but fair questions.",
    }

    prompt = f"""
You are an educational quiz generator.
Create exactly {count} multiple-choice questions from the study notes below.
Difficulty: {difficulty}.
Difficulty rule: {difficulty_rules[difficulty]}

IMPORTANT:
- Use ONLY information supported by the notes.
- Do not invent facts that are not in the notes.
- Every question must have exactly 4 distinct options.
- The answer must exactly match one option.
- Give a short, useful explanation for the correct answer.
- Avoid duplicate or nearly duplicate questions.
- Return ONLY valid JSON. No markdown and no extra text.

JSON format:
[
  {{
    "question": "...",
    "options": ["...", "...", "...", "..."],
    "answer": "...",
    "explanation": "..."
  }}
]

STUDY NOTES:
{text[:12000]}
"""

    response = client.chat(
        model="gpt-oss:120b",
        messages=[{"role": "user", "content": prompt}],
        format="json",
    )
    raw = response["message"]["content"]
    data = json.loads(clean_json(raw))
    return validate_questions(data, count)


def make_boss(text, difficulty):
    client = get_client()
    prompt = f"""
Create a fun boss for a study game based on these notes.
Difficulty: {difficulty}.
Return ONLY valid JSON with exactly these keys:
{{"name":"...","emoji":"👹","description":"..."}}
Keep the name short and the description under 20 words.
Notes:
{text[:5000]}
"""
    response = client.chat(
        model="gpt-oss:120b",
        messages=[{"role": "user", "content": prompt}],
        format="json",
    )
    data = json.loads(clean_json(response["message"]["content"]))
    return (
        str(data.get("name", "Study Demon")).strip() or "Study Demon",
        str(data.get("emoji", "👹")).strip() or "👹",
        str(data.get("description", "A monster made from your toughest notes.")).strip()
        or "A monster made from your toughest notes.",
    )


def extract_pdf_text(uploaded_file):
    reader = PdfReader(uploaded_file)
    if reader.is_encrypted:
        raise ValueError("This PDF is password-protected. Please upload an unlocked PDF.")

    chunks = []
    for page in reader.pages:
        page_text = page.extract_text() or ""
        if page_text.strip():
            chunks.append(page_text.strip())

    text = "\n\n".join(chunks).strip()
    if len(text) < 100:
        raise ValueError("I could not find enough readable text in this PDF. Try a text-based PDF.")
    return text


def start_battle(pdf, difficulty, count):
    with st.status("👻 Preparing your boss battle...", expanded=True) as status:
        st.write("📄 Reading your notes...")
        text = extract_pdf_text(pdf)
        st.write("🧠 Creating quiz questions...")
        questions = make_questions(text, difficulty, count)
        st.write("👹 Summoning your boss...")
        boss_name, boss_emoji, boss_description = make_boss(text, difficulty)
        status.update(label="⚔️ Battle ready!", state="complete")

    st.session_state.questions = questions
    st.session_state.current = 0
    st.session_state.monster_hp = 100
    st.session_state.player_hp = 100
    st.session_state.score = 0
    st.session_state.correct = 0
    st.session_state.wrong = 0
    st.session_state.combo = 0
    st.session_state.best_combo = 0
    st.session_state.feedback = None
    st.session_state.battle_started = True
    st.session_state.battle_finished = False
    st.session_state.won = False
    st.session_state.boss_name = boss_name
    st.session_state.boss_emoji = boss_emoji
    st.session_state.boss_description = boss_description
    st.session_state.pdf_name = pdf.name


def answer_question(option):
    s = st.session_state
    q = s.questions[s.current]
    if option == q["answer"]:
        s.monster_hp = max(0, s.monster_hp - 20)
        s.correct += 1
        s.combo += 1
        s.best_combo = max(s.best_combo, s.combo)
        s.score += 100 + (s.combo - 1) * 25
        s.feedback = {"correct": True, "answer": q["answer"], "explanation": q["explanation"]}
    else:
        s.player_hp = max(0, s.player_hp - 20)
        s.wrong += 1
        s.combo = 0
        s.feedback = {"correct": False, "answer": q["answer"], "explanation": q["explanation"]}


def continue_after_feedback():
    s = st.session_state
    if s.monster_hp <= 0:
        s.battle_finished = True
        s.won = True
        return
    if s.player_hp <= 0:
        s.battle_finished = True
        s.won = False
        return
    s.current += 1
    s.feedback = None
    if s.current >= len(s.questions):
        s.battle_finished = True
        s.won = s.monster_hp <= 0


init_state()

# -----------------------------
# Header
# -----------------------------
st.markdown(
    '<div class="hero"><h1>👻 Study Boss Battle</h1>'
    '<p>Turn your study notes into an AI-powered boss fight.</p></div>',
    unsafe_allow_html=True,
)

# -----------------------------
# Sidebar controls
# -----------------------------
with st.sidebar:
    st.header("⚙️ Battle Settings")
    difficulty = st.selectbox("Difficulty", ["Easy", "Medium", "Hard"], index=1)
    count = st.selectbox("Questions", [5, 10, 20], index=1)
    st.divider()
    st.caption("💡 Tip: Use a clear, text-based PDF for the best questions.")
    if st.session_state.battle_started and st.button("🏠 Start New Battle", use_container_width=True):
        reset_battle()
        st.rerun()

# -----------------------------
# Home screen
# -----------------------------
if not st.session_state.battle_started:
    st.markdown(
        '<div class="card"><div class="boss-name">📚 Your notes → 👹 A boss battle</div>'
        '<div class="boss-desc">Upload your notes, choose a difficulty, and defeat the boss by answering correctly.</div></div>',
        unsafe_allow_html=True,
    )

    pdf = st.file_uploader("📄 Upload your notes (PDF)", type=["pdf"])
    if pdf:
        st.success(f"Ready: {pdf.name}")
        st.info(f"🎯 {count} questions • {difficulty} difficulty")

    if st.button("⚔️ SUMMON THE BOSS", type="primary", use_container_width=True, disabled=pdf is None):
        try:
            start_battle(pdf, difficulty, count)
            st.rerun()
        except Exception as exc:
            st.error("I couldn't prepare this battle.")
            st.warning(str(exc))
            st.caption("Check your PDF and make sure OLLAMA_API_KEY is configured.")

# -----------------------------
# Battle screen
# -----------------------------
elif not st.session_state.battle_finished:
    s = st.session_state
    total = len(s.questions)
    current_number = min(s.current + 1, total)

    st.markdown(
        f'<div class="card"><div class="boss-name">{s.boss_emoji} {s.boss_name}</div>'
        f'<div class="boss-desc">{s.boss_description}</div></div>',
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="stat">👹 Boss HP</div>', unsafe_allow_html=True)
        st.progress(s.monster_hp / 100)
        st.caption(f"{s.monster_hp} / 100 HP")
    with col2:
        st.markdown('<div class="stat">🧙 Your HP</div>', unsafe_allow_html=True)
        st.progress(s.player_hp / 100)
        st.caption(f"{s.player_hp} / 100 HP")

    st.progress(current_number / total)
    st.markdown(f'<div class="question-count">Question {current_number} of {total}</div>', unsafe_allow_html=True)

    if s.feedback is None:
        q = s.questions[s.current]
        st.subheader(q["question"])
        for i, option in enumerate(q["options"]):
            if st.button(option, key=f"answer-{s.current}-{i}", use_container_width=True):
                answer_question(option)
                st.rerun()
    else:
        feedback = s.feedback
        if feedback["correct"]:
            st.markdown(
                f'<div class="feedback-good"><b>⚔️ CRITICAL HIT!</b><br>'
                f'You dealt 20 damage!<br><br><b>🔥 Combo: {s.combo}</b><br><br>'
                f'<b>💡 Why?</b> {feedback["explanation"]}</div>',
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                f'<div class="feedback-bad"><b>💀 The boss hit you!</b><br>'
                f'<b>Correct answer:</b> {feedback["answer"]}<br><br>'
                f'<b>💡 Why?</b> {feedback["explanation"]}</div>',
                unsafe_allow_html=True,
            )
        if st.button("➡️ Continue Battle", type="primary", use_container_width=True):
            continue_after_feedback()
            st.rerun()

# -----------------------------
# Results screen
# -----------------------------
else:
    s = st.session_state
    total = len(s.questions)
    accuracy = round((s.correct / total) * 100) if total else 0

    if s.won:
        st.balloons()
        st.success(f"🏆 You defeated {s.boss_name}!")
    else:
        st.error(f"💀 {s.boss_name} survived this battle.")

    st.markdown(f'<div class="result-score">{accuracy}%</div><p style="text-align:center">Accuracy</p>', unsafe_allow_html=True)

    a, b, c, d = st.columns(4)
    a.metric("Correct", s.correct)
    b.metric("Wrong", s.wrong)
    c.metric("Score", s.score)
    d.metric("Best Combo", s.best_combo)

    st.markdown('<div class="card"><b>📊 Battle Summary</b><br>'
                f'Questions: {total}<br>'
                f'Correct answers: {s.correct}<br>'
                f'Boss HP remaining: {s.monster_hp}<br>'
                f'Your HP remaining: {s.player_hp}</div>', unsafe_allow_html=True)

    if accuracy >= 90:
        st.success("🧠 Brain Master! Excellent understanding.")
    elif accuracy >= 70:
        st.info("🔥 Great work! A little more practice can make you unstoppable.")
    else:
        st.warning("📚 Review the weak topics and challenge the boss again.")

    if st.button("🔄 Battle Again", type="primary", use_container_width=True):
        reset_battle()
        st.rerun()
