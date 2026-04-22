import streamlit as st
import random
from datetime import datetime

st.set_page_config(page_title="Тест: Кухар-Кондитер", page_icon="👨‍🍳")

# Функция загрузки
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

# Инициализация
if 'init' not in st.session_state:
    st.session_state.questions = load_questions()
    random.shuffle(st.session_state.questions)
    st.session_state.step = 0
    st.session_state.score = 0
    st.session_state.user = ""
    st.session_state.show_feedback = False # Для показа ошибок
    st.session_state.last_answer_correct = False
    st.session_state.init = True

# --- ЧИТ-ПАНЕЛЬ ---
with st.sidebar:
    st.title("⚙️ Адмінка")
    admin_pass = st.text_input("Введіть ключ:", type="password")
    if admin_pass == "denisdolboeb228":
        st.success("Чит-режим активовано!")
        cheat_val = st.slider("Кількість правильних:", 0, 63, 45)
        if st.button("ЗАВЕРШИТИ З ЦИМ БАЛОМ"):
            st.session_state.score = cheat_val
            st.session_state.step = len(st.session_state.questions)
            st.rerun()

# Вход
if not st.session_state.user:
    st.title("👨‍🍳 Екзаменаційний тест")
    name = st.text_input("Ваше Прізвище та Ім'я:")
    if st.button("Почати"):
        if name:
            st.session_state.user = name
            st.rerun()
    st.stop()

# ТЕСТ
if st.session_state.step < len(st.session_state.questions):
    q = st.session_state.questions[st.session_state.step]
    
    st.write(f"**Студент:** {st.session_state.user}")
    st.write(f"Питання {st.session_state.step + 1} з {len(st.session_state.questions)}")
    st.progress(st.session_state.step / len(st.session_state.questions))
    
    st.info(f"### {q['q']}")
    
    # Перемешиваем варианты один раз
    if f"shf_{st.session_state.step}" not in st.session_state:
        opts = q['options'].copy()
        random.shuffle(opts)
        st.session_state[f"shf_{st.session_state.step}"] = opts

    # Если мы НЕ показываем фидбек (ждем ответа)
    if not st.session_state.show_feedback:
        ans = st.radio("Оберіть відповідь:", st.session_state[f"shf_{st.session_state.step}"], key=f"q_{st.session_state.step}")
        
        if st.button("ПЕРЕВІРИТИ ✅"):
            correct_text = q['options'][q['correct'] - 1]
            if ans == correct_text:
                st.session_state.score += 1
                st.session_state.last_answer_correct = True
            else:
                st.session_state.last_answer_correct = False
                st.session_state.correct_text = correct_text # Сохраняем правильный текст
            
            st.session_state.show_feedback = True
            st.rerun()
    
    # Если мы показываем результат ответа (Работа над ошибками)
    else:
        if st.session_state.last_answer_correct:
            st.success("✨ **Правильно!**")
        else:
            st.error(f"❌ **Помилка!**\n\nПравильна відповідь була: **{st.session_state.correct_text}**")
        
        if st.button("НАСТУПНЕ ПИТАННЯ ➡️"):
            st.session_state.show_feedback = False
            st.session_state.step += 1
            st.rerun()

# ФИНАЛ
else:
    st.title("🏁 Результат")
    score = st.session_state.score
    total = len(st.session_state.questions)
    mark = round((score / total) * 12)
    
    st.success(f"### {st.session_state.user}, ваша оцінка: {mark} балів")
    st.metric("Правильних відповідей", f"{score} з {total}")
    
    print(f"LOG: {st.session_state.user} - {mark} ({datetime.now()})")
    
    if st.button("Скинути та вийти"):
        st.session_state.clear()
        st.rerun()
        
