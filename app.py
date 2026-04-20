import streamlit as st
import random
from datetime import datetime

st.set_page_config(page_title="Тест: Кухар-Кондитер", page_icon="👨‍🍳")

# Функція завантаження
@st.cache_data
def load_questions():
    qs = []
    try:
        with open('questions.txt', 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 6:
                    qs.append({
                        "q": parts[0],
                        "options": parts[1:5],
                        "correct": int(parts[5])
                    })
        return qs
    except: return []

# Ініціалізація
if 'init' not in st.session_state:
    st.session_state.questions = load_questions()
    random.shuffle(st.session_state.questions)
    st.session_state.step = 0
    st.session_state.score = 0
    st.session_state.user = ""
    st.session_state.init = True

# Вхід
if not st.session_state.user:
    st.title("👨‍🍳 Екзаменаційний тест")
    name = st.text_input("Ваше Прізвище та Ім'я:")
    if st.button("Почати"):
        if name:
            st.session_state.user = name
            st.rerun()
    st.stop()

# Тест
if st.session_state.step < len(st.session_state.questions):
    q = st.session_state.questions[st.session_state.step]
    st.write(f"Питання {st.session_state.step + 1} з {len(st.session_state.questions)}")
    st.progress(st.session_state.step / len(st.session_state.questions))
    
    st.info(q['q'])
    ans = st.radio("Оберіть відповідь:", q['options'], key=f"q_{st.session_state.step}")
    
    if st.button("Далі"):
        if q['options'].index(ans) + 1 == q['correct']:
            st.session_state.score += 1
        st.session_state.step += 1
        st.rerun()
else:
    st.title("🏁 Результат")
    score = st.session_state.score
    total = len(st.session_state.questions)
    mark = round((score / total) * 12)
    st.success(f"{st.session_state.user}, ваша оцінка: {mark} балів ({score}/{total})")
    print(f"LOG: {st.session_state.user} - {mark} ({datetime.now()})")
    if st.button("Перездати"):
        st.session_state.clear()
        st.rerun()
        
