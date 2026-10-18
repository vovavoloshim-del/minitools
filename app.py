import streamlit as st
import random
import string
import qrcode
from io import BytesIO
from PIL import Image

# Налаштування сторінки
st.set_page_config(
    page_title="MiniTools — Корисні міні-інструменти",
    page_icon="🛠️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Красивий заголовок
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    .subheader {
        text-align: center;
        color: #666;
        margin-bottom: 2rem;
    }
    </style>
    <div class="main-header">🛠️ MiniTools</div>
    <div class="subheader">Набір корисних міні-інструментів. Безкоштовно і швидко.</div>
""", unsafe_allow_html=True)

# Бічне меню
st.sidebar.title("Обери інструмент")
tool = st.sidebar.selectbox(
    "Що хочеш зробити?",
    [
        "Калькулятор середнього балу",
        "Генератор паролів",
        "Текстові інструменти",
        "Генератор QR-кодів",
        "Конвертер одиниць",
        "Калькулятор відсотків",
        "Таймер Помодоро"
    ]
)

st.sidebar.markdown("---")
st.sidebar.info("""
**Як заробляти на цьому?**

- Додай Google AdSense
- Зроби Pro-версію (більше функцій)
- Пропонуй кастомні інструменти
- Залий на GitHub і просувай

Цей сайт уже можна задеплоїти безкоштовно на Streamlit Cloud.
""")

# ==================== ІНСТРУМЕНТИ ====================

if tool == "Калькулятор середнього балу":
    st.header("📊 Калькулятор середнього балу")
    st.write("Введи оцінки і отримай середній бал. Підходить для школи та університету.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        grades_input = st.text_area(
            "Оцінки (через кому або пробіл)",
            placeholder="5, 4, 5, 3, 5, 4",
            height=150
        )
    
    with col2:
        st.subheader("Результат")
        if grades_input:
            try:
                grades = [float(g.strip().replace(',', '.')) for g in grades_input.replace(',', ' ').split() if g.strip()]
                if grades:
                    average = sum(grades) / len(grades)
                    st.metric("Середній бал", f"{average:.2f}")
                    st.metric("Кількість оцінок", len(grades))
                    st.metric("Сума", f"{sum(grades):.1f}")
                    
                    if average >= 4.5:
                        st.success("Відмінно! 🎉")
                    elif average >= 3.5:
                        st.info("Добре")
                    elif average >= 2.5:
                        st.warning("Задовільно")
                    else:
                        st.error("Потрібно підтягнути")
                else:
                    st.warning("Введи хоча б одну оцінку")
            except:
                st.error("Помилка: введи числа через кому або пробіл")
        else:
            st.info("Введи оцінки зліва")

elif tool == "Генератор паролів":
    st.header("🔐 Генератор паролів")
    
    length = st.slider("Довжина пароля", 8, 64, 16)
    use_upper = st.checkbox("Великі літери (A-Z)", value=True)
    use_lower = st.checkbox("Малі літери (a-z)", value=True)
    use_digits = st.checkbox("Цифри (0-9)", value=True)
    use_symbols = st.checkbox("Символи (!@#$%^&*)", value=True)
    
    if st.button("Згенерувати пароль", type="primary"):
        chars = ""
        if use_upper: chars += string.ascii_uppercase
        if use_lower: chars += string.ascii_lowercase
        if use_digits: chars += string.digits
        if use_symbols: chars += "!@#$%^&*()_+-=[]{}|;:,.<>?"
        
        if not chars:
            st.error("Обери хоча б один тип символів")
        else:
            password = ''.join(random.choice(chars) for _ in range(length))
            st.code(password, language=None)
            st.success("Скопіюй пароль вище ↑")

elif tool == "Текстові інструменти":
    st.header("✍️ Текстові інструменти")
    
    text = st.text_area("Встав текст", height=200, placeholder="Напиши або встав будь-який текст...")
    
    if text:
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Символів", len(text))
        col2.metric("Символів без пробілів", len(text.replace(" ", "")))
        col3.metric("Слів", len(text.split()))
        col4.metric("Речень", text.count('.') + text.count('!') + text.count('?'))
        
        st.subheader("Перетворення")
        c1, c2, c3 = st.columns(3)
        with c1:
            if st.button("ВЕРХНІЙ РЕГІСТР"):
                st.code(text.upper())
        with c2:
            if st.button("нижній регістр"):
                st.code(text.lower())
        with c3:
            if st.button("З Великої Літери"):
                st.code(text.title())
        
        if st.button("Прибрати зайві пробіли"):
            cleaned = ' '.join(text.split())
            st.code(cleaned)
            st.info(f"Було символів: {len(text)} → Стало: {len(cleaned)}")

elif tool == "Генератор QR-кодів":
    st.header("📱 Генератор QR-кодів")
    
    qr_text = st.text_input("Що закодувати?", placeholder="https://example.com або будь-який текст")
    qr_size = st.slider("Розмір", 200, 800, 400)
    
    if qr_text and st.button("Створити QR-код", type="primary"):
        qr = qrcode.QRCode(version=1, box_size=10, border=4)
        qr.add_data(qr_text)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        
        buf = BytesIO()
        img.save(buf, format="PNG")
        buf.seek(0)
        
        st.image(buf, width=qr_size, caption="Твій QR-код")
        st.download_button(
            "Завантажити QR-код",
            data=buf.getvalue(),
            file_name="qrcode.png",
            mime="image/png"
        )

elif tool == "Конвертер одиниць":
    st.header("🔄 Конвертер одиниць")
    
    category = st.selectbox("Категорія", ["Довжина", "Вага", "Температура", "Об'єм"])
    
    if category == "Довжина":
        units = {"Метри": 1, "Кілометри": 1000, "Сантиметри": 0.01, "Міліметри": 0.001, 
                 "Милі": 1609.34, "Фути": 0.3048, "Дюйми": 0.0254}
    elif category == "Вага":
        units = {"Кілограми": 1, "Грами": 0.001, "Тонни": 1000, "Фунти": 0.453592, "Унції": 0.0283495}
    elif category == "Температура":
        units = {"Цельсій": "C", "Фаренгейт": "F", "Кельвін": "K"}
    else:
        units = {"Літри": 1, "Мілілітри": 0.001, "Галони": 3.78541, "Кубометри": 1000}
    
    col1, col2 = st.columns(2)
    with col1:
        from_unit = st.selectbox("З", list(units.keys()))
        value = st.number_input("Значення", value=1.0)
    with col2:
        to_unit = st.selectbox("У", list(units.keys()))
    
    if category == "Температура":
        def convert_temp(val, from_u, to_u):
            if from_u == to_u:
                return val
            if from_u == "Фаренгейт":
                c = (val - 32) * 5/9
            elif from_u == "Кельвін":
                c = val - 273.15
            else:
                c = val
            if to_u == "Фаренгейт":
                return c * 9/5 + 32
            elif to_u == "Кельвін":
                return c + 273.15
            return c
        result = convert_temp(value, from_unit, to_unit)
    else:
        base = value * units[from_unit]
        result = base / units[to_unit]
    
    st.metric("Результат", f"{result:.6g} {to_unit}")

elif tool == "Калькулятор відсотків":
    st.header("💯 Калькулятор відсотків")
    
    mode = st.radio("Що рахуємо?", [
        "Скільки відсотків становить A від B",
        "Знайти A% від числа B",
        "Збільшити/зменшити число на відсоток"
    ])
    
    if mode == "Скільки відсотків становить A від B":
        a = st.number_input("Число A", value=25.0)
        b = st.number_input("Число B", value=100.0)
        if b != 0:
            st.metric("Результат", f"{(a/b)*100:.2f}%")
    elif mode == "Знайти A% від числа B":
        a = st.number_input("Відсоток", value=20.0)
        b = st.number_input("Число", value=150.0)
        st.metric("Результат", f"{b * a / 100:.2f}")
    else:
        number = st.number_input("Число", value=1000.0)
        percent = st.number_input("Відсоток", value=15.0)
        direction = st.radio("Напрямок", ["Збільшити", "Зменшити"])
        if direction == "Збільшити":
            result = number * (1 + percent/100)
        else:
            result = number * (1 - percent/100)
        st.metric("Результат", f"{result:.2f}")

elif tool == "Таймер Помодоро":
    st.header("🍅 Таймер Помодоро")
    st.write("Техніка Помодоро: 25 хвилин роботи + 5 хвилин відпочинку.")
    
    work_min = st.slider("Хвилин роботи", 5, 60, 25)
    break_min = st.slider("Хвилин відпочинку", 1, 30, 5)
    
    if st.button("Запустити таймер (просто показує час)", type="primary"):
        st.info(f"""
        **Робота:** {work_min} хвилин  
        **Відпочинок:** {break_min} хвилин
        
        Постав таймер на телефоні або використай онлайн-таймер.  
        Цей інструмент допомагає швидко налаштувати інтервали.
        """)
        st.success(f"Готово! Працюй {work_min} хв, потім відпочинь {break_min} хв.")

# Футер
st.markdown("---")
st.caption("MiniTools • Зроблено на Streamlit • Можна монетизувати через рекламу та Pro-функції")
