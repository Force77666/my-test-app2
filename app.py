import streamlit as st
import random
import time
from datetime import datetime

# --- НАСТРОЙКИ СТРАНИЦЫ ---
st.set_page_config(page_title="Атестація: Кондитер 3 розряду", page_icon="👨‍🍳")

# --- КОСТЫЛЬ: КЭШИРОВАНИЕ (чтобы не падал при нагрузке) ---
@st.cache_data
def load_questions():
    questions = []
    try:
        with open('questions.txt', 'r', encoding='utf-8') as f:
            for line in f:
                if '|' in line:
                    parts = line.strip().split('|')
                    # Сохраняем вопрос, варианты и текст правильного ответа
                    q_text = parts[0]
                    options = parts[1:-1]
                    correct_idx = int(parts[-1]) - 1
                    correct_text = options[correct_idx]
                    questions.append({
                        "q": q_text,
                        "options": options,
                        "correct_text": correct_text
                    })
        return questions
    except Exception as e:
        st.error(f"Помилка файлу: {e}")
        return []

# --- ИНИЦИАЛИЗАЦИЯ ---
if 'questions' not in st.session_state:
    qs = load_questions()
    random.shuffle(qs) # Рандомизация вопросов
    st.session_state.questions = qs
    st.session_state.current_step = 0
    st.session_state.score = 0
    st.session_state.finished = False
    st.session_state.user_name = ""
    st.session_state.start_time = None # Время старта

# --- АДМИН ПАНЕЛЬ (В сайдбаре) ---
with st.sidebar:
    st.title("🛡️ Admin Panel")
    # Секретный пароль для тебя
    admin_pass = st.text_input("Введіть код доступу:", type="password")
    
    # Чит-панель доступна только админу или по флагу
    if admin_pass == "chef777": # Твой пароль
        st.success("Доступ дозволено, Шеф!")
        cheat = st.checkbox("Активувати швидкий режим (Чит)")
        if cheat:
            val = st.slider("Бал:", 0, 63, 55)
            if st.button("Завершити негайно"):
                st.session_state.score = val
                st.session_state.finished = True
                st.rerun()
    
    st.write("---")
    st.write("v1.2 (Optimized)")

# --- 1. ЭКРАН РЕГИСТРАЦИИ ---
if st.session_state.user_name == "":
    st.title("🍰 Тестування: Кондитер 3 розряду")
    name = st.text_input("Введіть ваше Прізвище та Ім'я:")
    if st.button("Почати іспит"):
        if name.strip():
            st.session_state.user_name = name.strip()
            st.session_state.start_time = time.time() # Фиксируем время начала
            st.rerun()
        else:
            st.error("Будь ласка, введіть ім'я!")
    st.stop()

# --- 2. ПРОЦЕСС ТЕСТА ---
if not st.session_state.finished:
    q_idx = st.session_state.current_step
    if q_idx < len(st.session_state.questions):
        item = st.session_state.questions[q_idx]
        
        # Таймер (визуальный костыль)
        elapsed = int(time.time() - st.session_state.start_time)
        
        st.write(f"**Студент:** {st.session_state.user_name} | **Час:** {elapsed} сек.")
        st.progress(q_idx / len(st.session_state.questions))
        
        st.info(f"**Питання {q_idx + 1}:** {item['q']}")
        
        # Чтобы варианты не прыгали при обновлении таймера, 
        # фиксируем их порядок для текущего вопроса
        if f"opts_{q_idx}" not in st.session_state:
            shuffled_opts = item["options"].copy()
            random.shuffle(shuffled_opts)
            st.session_state[f"opts_{q_idx}"] = shuffled_opts

        ans = st.radio("Оберіть відповідь:", st.session_state[f"opts_{q_idx}"], key=f"q_{q_idx}")
        
        if st.button("Наступне питання ➡️"):
            # Проверка по тексту ответа (так как индексы перемешаны)
            if ans == item["correct_text"]:
                st.session_state.score += 1
            
            st.session_state.current_step += 1
            if st.session_state.current_step >= len(st.session_state.questions):
                st.session_state.finished = True
            st.rerun()

# --- 3. ФИНАЛЬНЫЙ ЭКРАН ---
else:
    st.title("🏁 Результат тестування")
    total = len(st.session_state.questions)
    score = st.session_state.score
    mark = round((score / total) * 12)
    
    # Считаем итоговое время
    end_time = int(time.time() - st.session_state.start_time)
    
    st.header(f"Курсант: {st.session_state.user_name}")
    st.write("---")
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Правильно", f"{score}/{total}")
    col2.metric("Оцінка", f"{mark}/12")
    col3.metric("Час", f"{end_time} сек")

    # КОСТЫЛЬ ЛОГИРОВАНИЯ (Смотри это в Logs на сайте Streamlit)
    log_msg = f"!!! [ОТЧЕТ] {st.session_state.user_name} | Оцінка: {mark} | Час: {end_time}с | {datetime.now()}"
    print(log_msg) 

    if st.button("Спробувати знову"):
        # Очистка всего, кроме вопросов (их заново грузить не надо, они в кэше)
        for key in ["user_name", "score", "current_step", "finished", "start_time"]:
            if key in st.session_state: del st.session_state[key]
        st.rerun()

