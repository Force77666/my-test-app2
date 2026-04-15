import streamlit as st
import random
import time
from datetime import datetime

# --- 1. ГЛУБОКАЯ НАСТРОЙКА СТИЛЯ (CSS) ---
st.set_page_config(page_title="Атестація кондитерів", page_icon="🧁", layout="centered")

st.markdown("""
    <style>
    /* Основной фон и шрифты */
    .main { background-color: #f9f9f9; }
    h1 { color: #4E342E; font-family: 'Helvetica Neue', sans-serif; }
    
    /* Стиль карточки вопроса */
    .stAlert { border-radius: 15px; border: none; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
    
    /* Красивые кнопки */
    .stButton>button {
        width: 100%;
        border-radius: 25px;
        background-color: #8D6E63;
        color: white;
        font-weight: bold;
        transition: 0.3s;
        border: none;
    }
    .stButton>button:hover {
        background-color: #5D4037;
        border: none;
        color: #FFECB3;
    }
    
    /* Прогресс-бар */
    .stProgress > div > div > div > div { background-color: #A1887F; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. ЗАГРУЗКА ДАННЫХ (ОПТИМИЗИРОВАНО) ---
@st.cache_data
def get_all_questions():
    qs = []
    try:
        with open('questions.txt', 'r', encoding='utf-8') as f:
            for line in f:
                if '|' in line:
                    parts = line.strip().split('|')
                    options = parts[1:-1]
                    qs.append({
                        "question": parts[0],
                        "options": options,
                        "correct": options[int(parts[-1])-1]
                    })
        return qs
    except:
        return []

# --- 3. ЛОГИКА СЕССИИ ---
if 'init' not in st.session_state:
    all_qs = get_all_questions()
    random.shuffle(all_qs)
    st.session_state.questions = all_qs
    st.session_state.step = 0
    st.session_state.score = 0
    st.session_state.name = ""
    st.session_state.start_time = 0
    st.session_state.init = True

# --- 4. ПРИВЕТСТВЕННЫЙ ЭКРАН ---
if not st.session_state.name:
    st.image("https://img.freepik.com/free-vector/bakery-logo-template-design_23-2148450148.jpg", width=150)
    st.title("👨‍🍳 Система професійної атестації")
    st.write("Вітаємо! Цей тест розроблено для перевірки знань кондитерів 3-го розряду.")
    
    with st.container():
        name_input = st.text_input("Введіть ваше Прізвище та Ім'я:", placeholder="Н-р: Мельник Олександр")
        if st.button("ПОЧАТИ ТЕСТУВАННЯ"):
            if len(name_input.strip()) > 2:
                st.session_state.name = name_input.strip()
                st.session_state.start_time = time.time()
                print(f"START: {st.session_state.name} @ {datetime.now()}")
                st.rerun()
            else:
                st.warning("Будь ласка, вкажіть прізвище.")
    st.stop()

# --- 5. ЭКРАН ТЕСТА ---
if st.session_state.step < len(st.session_state.questions):
    q_num = st.session_state.step
    curr = st.session_state.questions[q_num]
    
    # Шапка
    col_l, col_r = st.columns([4, 1])
    col_l.markdown(f"**Студент:** `{st.session_state.name}`")
    col_r.markdown(f"⏳ **{int(time.time() - st.session_state.start_time)}с**")
    
    st.progress(q_num / len(st.session_state.questions))
    
    # Карточка вопроса
    st.info(f"### Питання №{q_num + 1}\n{curr['question']}")
    
    # Рандомизация ответов внутри сессии
    if f"shf_{q_num}" not in st.session_state:
        opts = curr['options'].copy()
        random.shuffle(opts)
        st.session_state[f"shf_{q_num}"] = opts

    ans = st.radio("Оберіть правильний варіант:", st.session_state[f"shf_{q_num}"], key=f"ans_{q_num}")
    
    st.write("---")
    if st.button("ПІДТВЕРДИТИ ТА ДАЛІ →"):
        if ans == curr['correct']:
            st.session_state.score += 1
        
        st.session_state.step += 1
        st.toast("Відповідь прийнята!", icon="🍩")
        time.sleep(0.3) # Маленькая пауза для анимации
        st.rerun()

# --- 6. ЭКРАН РЕЗУЛЬТАТОВ ---
else:
    st.balloons()
    st.title("🏁 Тестування завершено")
    
    total = len(st.session_state.questions)
    score = st.session_state.score
    mark = round((score / total) * 12)
    duration = int(time.time() - st.session_state.start_time)
    
    # Красивая карточка финала
    with st.expander("📊 Подивитися деталі звіту", expanded=True):
        st.write(f"### Студент: {st.session_state.name}")
        
        c1, c2, c3 = st.columns(3)
        c1.metric("Правильно", f"{score}/{total}")
        c2.metric("Оцінка", f"{mark}/12")
        c3.metric("Час", f"{duration//60}хв {duration%60}с")
        
    # Комплимент от Шефа
    if mark >= 10:
        st.success("🌟 Відмінний результат! Ви справжній майстер своєї справи.")
    elif mark >= 7:
        st.warning("👍 Добре! Але є куди рости. Повторіть технологію приготування кремів.")
    else:
        st.error("📚 Треба підтягнути теорію. Спробуйте ще раз після вивчення конспектів.")

    # Лог для учителя
    print(f"RESULT: {st.session_state.name} | {mark}/12 | {duration}s")
    
    if st.button("ЗДАТИ РОБОТУ ТА ВИЙТИ"):
        st.session_state.clear()
        st.rerun()
        
