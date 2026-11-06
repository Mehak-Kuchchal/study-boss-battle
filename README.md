# 👻 Study Boss Battle

> **Turn your study notes into an AI-powered boss battle! ⚔️**

Study Boss Battle is an interactive learning application that converts your **PDF study notes into AI-generated quiz questions** and turns them into a fun boss fight.

Instead of simply reading notes and taking a boring quiz, you fight a virtual boss by answering questions correctly. 🎮

---

## 🎮 How It Works

```text
📄 Upload Study Notes
        ↓
🧠 AI Reads Your Notes
        ↓
❓ AI Generates Quiz Questions
        ↓
👹 Boss Is Summoned
        ↓
⚔️ Answer Questions
        ↓
💥 Correct Answer → Damage the Boss
❌ Wrong Answer → Lose HP
        ↓
🏆 Get Your Final Score
```

---

## ✨ Features

### 📚 AI-Powered Quiz Generation
Upload a PDF and the application automatically creates questions based on your study material.

### 🎯 Multiple Difficulty Levels

Choose the difficulty that matches your preparation:

- 🟢 **Easy** — Basic concepts and definitions
- 🟡 **Medium** — Concept-based questions
- 🔴 **Hard** — More challenging questions

### ❓ Flexible Number of Questions

Choose how many questions you want:

- 5 Questions
- 10 Questions
- 20 Questions

### 👹 Boss Battles

Every study session becomes a battle against an AI-generated boss.

The boss has:

- ❤️ Health Points
- 👹 A unique name
- 📖 A description related to your study topic

### ⚔️ Battle System

Answer questions to attack the boss.

```text
✅ Correct Answer
       ↓
⚔️ Attack Boss
       ↓
💥 Boss loses HP

❌ Wrong Answer
       ↓
👹 Boss attacks
       ↓
❤️ You lose HP
```

### 🔥 Combo System

Answer consecutive questions correctly to build your combo.

### 💡 Explanations

After answering, the application provides an explanation so you can understand **why the answer is correct**.

### 🏆 Final Results

At the end of the battle, you can see:

- Accuracy
- Correct answers
- Wrong answers
- Score
- Best combo
- Remaining player HP
- Remaining boss HP

---

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| 🐍 Python | Application logic |
| 🎈 Streamlit | Web interface |
| 🧠 Ollama | AI question generation |
| 📄 pypdf | PDF text extraction |

---

## 📂 Project Structure

```text
study-boss-battle/
│
├── app.py
├── requirements.txt
└── README.md
```

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/Mehak-Kuchchal/study-boss-battle.git
```

### 2. Open the project

```bash
cd study-boss-battle
```

### 3. Install the required packages

```bash
pip install -r requirements.txt
```

### 4. Set up your Ollama API key

The application uses an Ollama API key to generate quiz questions.

**Do not put your API key directly inside `app.py` or commit it to GitHub.**

Set it as an environment variable on your computer.

### 5. Run the application

```bash
streamlit run app.py
```

The application will open in your browser.

---

## 🔐 Security

Your API key should be stored securely as an environment variable or through your deployment platform's secrets manager.

Never commit secrets such as:

```text
OLLAMA_API_KEY=your-secret-key
```

to a public GitHub repository.

---

## 🎯 Example

Imagine you upload:

```text
📄 Computer Networks - Unit 3.pdf
```

The application can generate a battle such as:

```text
👹 Router Rex

"Master of packets, routing through
subnets and virtual circuits!"

Question 1:

What is the primary function
of the network layer?

A. Moving frames between devices
B. Delivering packets end-to-end
C. Encrypting data
D. Providing power to routers
```

Answer correctly:

```text
⚔️ CRITICAL HIT!

💥 You dealt damage!
🔥 Combo increased!
```

At the end:

```text
🏆 BATTLE COMPLETE

Accuracy: 80%
Correct: 8
Wrong: 2
Score: 800
```

---

## 💡 Why Study Boss Battle?

Traditional studying can become repetitive.

Study Boss Battle combines:

**📚 Learning + 🧠 AI + 🎮 Gamification**

to make revision more interactive and engaging.

The goal is simple:

> **Don't just study your notes. Fight them. ⚔️**

---

## 🚀 Future Improvements

Planned improvements include:

- 📊 Study progress dashboard
- 📈 Performance tracking
- 🏆 Achievements and badges
- 🔥 Study streaks
- 🧠 Weak-topic detection
- 📚 Practice mode
- 🎮 More boss types
- 🖼️ Custom boss artwork
- 📱 Improved mobile experience

---

## 👩‍💻 Author

**Mehak Kuchchal**

B.Tech Computer Science & Engineering

---

## ⭐ Support

If you find this project useful, consider giving the repository a ⭐ on GitHub!

**Happy studying — and good luck defeating the boss! 👻⚔️**
