import streamlit as st
import random

st.set_page_config(page_title="Тест: Кондитер 3-го розряду", page_icon="🍰")

# --- База ---
def load_questions():
    questions = []
    try:
        with open('questions.txt', 'r', encoding='utf-8') as f:
            for line in f:
                if '|' in line:
                    parts = line.strip().split('|')
                    questions.append({
                        "q": parts[0],
                        "options": parts[1:len(parts)-1],
                        "correct": int(parts[-1])
                    })
        return questions
    except Exception as e:
        st.error(f"Помилка: {e}")
        return []

if 'questions' not in st.session_state:
    st.session_state.questions = load_questions()
    random.shuffle(st.session_state.questions)
    st.session_state.current_step = 0
    st.session_state.score = 0
    st.session_state.finished = False
    st.session_state.user_name = ""

# --- ЧИТ-ПАНЕЛЬ (Скрытая в сайдбаре) ---
with st.sidebar:
    st.title("⚙️ Налаштування")
    use_cheat = st.checkbox("Активувати швидкий режим")
    if use_cheat:
        cheat_score = st.slider("Виберіть кількість правильних відповідей:", 40, 63, 55)
        if st.button("Завершити тест негайно"):
            st.session_state.score = cheat_score
            st.session_state.finished = True
            st.rerun()

# --- 1. ВВОД ИМЕНИ ---
if st.session_state.user_name == "":
    st.title("🍰 Тестування: Кондитер 3 розряду")
    name = st.text_input("Введіть ваше Прізвище та Ім'я:")
    if st.button("Почати"):
        if name.strip():
            st.session_state.user_name = name.strip()
            st.rerun()
        else:
            st.error("Введіть ім'я!")
    st.stop()

# --- 2. ПРОЦЕСС ТЕСТА ---
if not st.session_state.finished:
    q_idx = st.session_state.current_step
    if q_idx < len(st.session_state.questions):
        item = st.session_state.questions[q_idx]
        st.write(f"**Курсант:** {st.session_state.user_name}")
        st.write(f"**Питання {q_idx + 1} з {len(st.session_state.questions)}**")
        st.info(item["q"])
        
        ans = st.radio("Оберіть відповідь:", item["options"], key=f"q_{q_idx}")
        
        if st.button("Далі"):
            if (item["options"].index(ans) + 1) == item["correct"]:
                st.session_state.score += 1
            st.session_state.current_step += 1
            if st.session_state.current_step >= len(st.session_state.questions):
                st.session_state.finished = True
            st.rerun()
else:
    # --- 3. ФИНАЛ ---
    st.title("🏁 Результат тестування")
    total = 63 # Фиксируем общее число
    score = st.session_state.score
    mark = round((score / total) * 12)
    
    st.header(f"Прізвище: {st.session_state.user_name}")
    st.write("---")
    st.subheader(f"Правильних відповідей: {score} з {total}")
    st.subheader(f"Ваша оцінка: {mark} балів")
    
    if st.button("Пройти ще раз"):
        for key in list(st.session_state.keys()): del st.session_state[key]
        st.rerun()
        
