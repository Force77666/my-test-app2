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

# --- ЧИТ-ПАНЕЛЬ (Секретна зона) ---
with st.sidebar:
    st.title("⚙️ Адмінка")
    admin_pass = st.text_input("Введіть ключ:", type="password")
    
    if admin_pass == "denisdolboeb228":
        st.success("Чит-режим активовано!")
        cheat_val = st.slider("Вибрати кількість правильних:", 0, 63, 45)
        if st.button("ЗАВЕРШИТИ З ЦИМ БАЛОМ"):
            st.session_state.score = cheat_val
            st.session_state.step = len(st.session_state.questions) # Стрибок у кінець
            st.rerun()

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
    st.write(f"**Студент:** {st.session_state.user}")
    st.write(f"Питання {st.session_state.step + 1} з {len(st.session_state.questions)}")
    st.progress(st.session_state.step / len(st.session_state.questions))
    
    st.info(q['q'])
    
    if f"shf_{st.session_state.step}" not in st.session_state:
        opts = q['options'].copy()
        random.shuffle(opts)
        st.session_state[f"shf_{st.session_state.step}"] = opts

    ans = st.radio("Оберіть відповідь:", st.session_state[f"shf_{st.session_state.step}"], key=f"q_{st.session_state.step}")
    
    if st.button("Далі"):
        # Перевірка через текст правильної відповіді (бо варіанти перемішані)
        correct_text = q['options'][q['correct'] - 1]
        if ans == correct_text:
            st.session_state.score += 1
        st.session_state.step += 1
        st.rerun()
else:
    # Фінал
    st.title("🏁 Результат")
    score = st.session_state.score
    total = len(st.session_state.questions)
    
    # Запобіжник, щоб не було більше 63
    if score > total: score = total
    
    mark = round((score / total) * 12)
    
    st.success(f"{st.session_state.user}, ваша оцінка: {mark} балів ({score}/{total})")
    
    # Лог у консоль (для тебе)
    print(f"LOG: {st.session_state.user} - {mark} балів ({datetime.now()})")
    
    if st.button("Перездати"):
        st.session_state.clear()
        st.rerun()
        
