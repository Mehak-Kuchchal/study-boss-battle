import os
import json
import streamlit as st
from pypdf import PdfReader
from ollama import Client

st.title("👻 Study Boss Battle")

client = Client(
    host="https://ollama.com",
    headers={"Authorization": "Bearer " + os.environ["OLLAMA_API_KEY"]},
)

def make_questions(text):
    prompt = f"""Make 3 easy multiple choice questions from these notes.
Reply ONLY with JSON in this format:
[{{"question": "...", "options": ["...", "...", "...", "..."], "answer": "the correct option text"}}]

Notes:
{text[:3000]}"""
    response = client.chat(
        model="gpt-oss:120b",
        messages=[{"role": "user", "content": prompt}],
    )
    reply = response["message"]["content"]
    reply = reply.replace("```json", "").replace("```", "").strip()
    return json.loads(reply)

pdf = st.file_uploader("Upload your notes (PDF)", type="pdf")

if pdf and st.button("Summon the monster"):
    reader = PdfReader(pdf)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    st.session_state.questions = make_questions(text)
    st.session_state.current = 0
    st.session_state.monster_hp = 90
    st.session_state.player_hp = 90
    st.session_state.message = ""

if "questions" in st.session_state:
    s = st.session_state
    monster = max(s.monster_hp, 0)
    player = max(s.player_hp, 0)

    st.write("👹 Monster HP:", monster)
    st.progress(monster / 90)
    st.write("🧙 Your HP:", player)
    st.progress(player / 90)

    if s.message:
        st.info(s.message)

    if s.current < len(s.questions):
        q = s.questions[s.current]
        st.subheader(q["question"])
        for option in q["options"]:
            if st.button(option, key=f"{s.current}-{option}"):
                if option == q["answer"]:
                    s.monster_hp -= 30
                    s.message = "Hit! 💥"
                else:
                    s.player_hp -= 30
                    s.message = "Ouch! Right answer: " + q["answer"]
                s.current += 1
                st.rerun()
    else:
        if monster <= 0:
            st.success("You defeated the monster! 🎉")
            st.balloons()
        else:
            st.error("The monster survived. Study more! 💀")
            