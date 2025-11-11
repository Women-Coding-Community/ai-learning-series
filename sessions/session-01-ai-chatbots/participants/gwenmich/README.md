## Coachly - your personal AI career coach

---

### 🌟 Overview

<p align="center">
  <img src="/sessions/session-01-ai-chatbots/participants/gwenmich/coachly_interface.png" alt="Coachly interface" width="60%">
</p>


**Coachly** can offer you:
- personalised career advice
- resume tips & optimisation
- help with interview preparation
- guide you on your career journey

Coachly remembers what you've talked about in previous sessions and 
will follow <br>alongside you while you work towards your career goals providing
encouragement and advice.

---

### 🛠️ Coachly setup

1. Clone the repo or download the files in `sessions/session-01-as-chatbots/participants/gwenmich`.
2. Create a virtual environment and activate it with the following commands in the terminal:
    ```python
    python -m venv .venv
    source .venv/bin/activate
    ```
3. Install requirements by running: 
    ```python
    pip install -r requirements.txt
    ```
4. Create a `.env` file. You can either copy & paste the `.env.example` file or create your own.
5. Make sure your `.env` file is included in your `.gitignore` file.
6. Create an LLM API key and add it into your `.env` file (eg. `GEMINI_API_KEY = your_api_key`).
7. Run the chatbot with: 
    ```python
    streamlit run app.py
    ```
8. Happy prompting!

A data file will appear in your folder after your first session with saved data.<br>
Coachly will use this in future sessions to remember what you've talked about.

---

### 📚 Key takeaways

- Learned about important LLM parameters, such as temperature, Top-P and Top-K.
- Gained an understanding of a chatbot's structure and investigated how the code functions.
- Practiced using an external API securely.
- Understood how prompt design and parameters influence model responses.

---

### 🧗‍♀️ Challenges

- Interpreting and adapting existing code to fit my own project and use case.
- Getting familiar with how an LLM integrates into a chatbot structure.
- Revisiting Python after a break and getting comfortable with its syntax and commands again.
- Getting to grips with the Streamlit framework and understanding how it supports building interactive apps.

---

### 🚀 Future improvements

- Include conversation history in sidebar
- Let users choose a focus before starting the conversation, such as *resume help* or *confidence*.
- Store chat history in a database, like MySQL or PostgreSQL.
- Expand the prompt to include specific scenarios, such as *switching careers*, *first tech role*, *burnout*, etc.

---

