# Watermarker Pro v7.0

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.0+-FF4B4B.svg)](https://streamlit.io)
[![Pillow](https://img.shields.io/badge/Pillow-10+-green.svg)](https://python-pillow.org/)

**Потужний інструмент для пакетного додавання водяних знаків (текст + PNG-логотип) на зображення.**

Watermarker Pro — це швидкий, надійний і зручний веб-додаток на базі Streamlit + Pillow. Підтримує тисячі файлів, live-прев’ю, вбудований редактор, пресети та EXIF.

### ✨ Ключові можливості
- Текстова та графічна водяна мітка
- Вбудований редактор (crop, rotate, resize)
- Пресети налаштувань (збереження/завантаження)
- Багатопотокова обробка (до 8 потоків)
- Підтримка WEBP, JPEG, PNG, TIFF
- Повна валідація + захист від пошкоджених файлів
- Логування та детальна статистика

### Скріншоти

![Головна сторінка](screenshots/1-main.png)
![Завантаження файлів](screenshots/2-main.png)
![Редактор зображення](screenshots/3-main.png)

### 🚀 Швидкий старт

```bash
git clone https://github.com/MaanAndrii/watermarker-pro.git
cd watermarker-pro
pip install -r requirements.txt
streamlit run web_app.py
