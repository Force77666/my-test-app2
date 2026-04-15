import streamlit as st
import random

st.set_page_config(page_title="Тест: Кондитер 3-го розряду", page_icon="🍰")

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
        st.error(f"Помилка завантаження файлу: {e}")
        return []

if 'questions' not in st.session_state:
    base_qs = load_questions()
    random.shuffle(base_qs)
    st.session_state.questions = base_qs
    st.session_state.current_step = 0
    st.session_state.score = 0
    st.session_state.finished = False

st.title("🍰 Тест: Кондитер 3-го розряду")

if not st.session_state.finished:
    q_idx = st.session_state.current_step
    if q_idx < len(st.session_state.questions):
        item = st.session_state.questions[q_idx]
        
        st.write(f"### Питання {q_idx + 1} із {len(st.session_state.questions)}")
        st.info(item["q"])
        
        ans = st.radio("Оберіть варіант:", item["options"], key=f"q_{q_idx}")
        
        if st.button("Підтвердити відповідь"):
            selected_idx = item["options"].index(ans) + 1
            if selected_idx == item["correct"]:
                st.session_state.score += 1
                st.success("✅ Вірно!")
            else:
                correct_text = item["options"][item["correct"]-1]
                st.error(f"❌ Невірно. Правильна відповідь: {correct_text}")
            
            st.session_state.current_step += 1
            if st.session_state.current_step >= len(st.session_state.questions):
                st.session_state.finished = True
            st.rerun()
    else:
        st.session_state.finished = True
        st.rerun()
else:
    st.balloons()
    st.header("🎉 Тест завершено!")
    final_score = st.session_state.score
    total = len(st.session_state.questions)
    st.write(f"## Ваш результат: {final_score} з {total}")
    st.progress(final_score / total)
    
    if st.button("Спробувати ще раз"):
        for key in st.session_state.keys():
            del st.session_state[key]
        st.rerun()
