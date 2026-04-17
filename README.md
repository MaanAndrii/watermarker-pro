# 📸 Watermarker Pro v7.0

> **Professional Batch Photo Watermarking Application**

Повністю переписаний професійний інструмент для пакетної обробки фото з вотермарками. Версія 7.0 включає повну обробку помилок, валідацію даних, логування та оптимізацію пам'яті.

---

## 🎯 Ключові особливості

### ✨ Основний функціонал
- **Пакетна обробка** - одночасна обробка десятків фото
- **Два типи вотермарок** - текстові та графічні (PNG з прозорістю)
- **Гнучке позиціонування** - 5 позицій + режим замощення
- **Розумний ресайз** - Max Side, Exact Width, Exact Height
- **Множинні формати** - JPEG, PNG, WEBP
- **Редактор зображень** - crop та rotate з live preview

### 🔒 Надійність
- ✅ Повна валідація всіх вхідних даних
- ✅ Обробка corrupted images
- ✅ Memory leak prevention
- ✅ Thread-safe операції
- ✅ Професійне логування
- ✅ EXIF metadata preservation

### 🚀 Продуктивність
- Багатопотокова обробка (1-8 threads)
- Кешування шрифтів та thumbnails
- Оптимізація використання RAM
- Proxy images для редактора

---

## 📦 Встановлення

### Вимоги
- Python 3.8+
- pip

### Швидкий старт

```bash
# 1. Клонування репозиторію
git clone https://github.com/MaanAndrii/watermarker-pro.git
cd watermarker-pro

# 2. Встановлення залежностей
pip install -r requirements.txt

# 3. Запуск додатку
streamlit run web_app.py
```

### 🥧 Деплой у локальній мережі на Raspberry Pi

1. Встановіть залежності та створіть venv:
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. Перевірте runtime-сумісність (HEIC/SVG/imports):
```bash
python scripts/check_runtime.py
```

3. Запуск у LAN (доступ з інших пристроїв):
```bash
streamlit run web_app.py --server.address 0.0.0.0 --server.port 8501
```

4. Для автозапуску через `systemd` використайте:
- `deploy/watermarker.service`
- `deploy/watermarker-pro.env.example`

5. Для Raspberry Pi можна зменшити ліміти через env:
```bash
export WM_MAX_THREADS=4
export WM_DEFAULT_THREADS=2
export WM_MAX_FILE_SIZE_MB=50
export WM_MAX_IMAGE_DIMENSION=8000
export WM_WORK_DIR=/var/lib/watermarker/tmp
```

### Чи можна прибрати обмеження Streamlit повністю?

Коротко: **ні, повністю без лімітів не можна** (через websocket/message модель Streamlit).
Але для LAN можна суттєво підняти межі:

```bash
export WM_STREAMLIT_MAX_UPLOAD_MB=1024
export WM_STREAMLIT_MAX_MESSAGE_MB=1024
bash scripts/run_pi.sh
```

Для `systemd` ці змінні задаються у `deploy/watermarker-pro.env.example`,
а сервіс запускає `scripts/run_pi.sh`.

### Структура проєкту

```
watermarker-pro/
├── web_app.py              # Головний файл додатку
├── config.py               # Централізована конфігурація
├── logger.py               # Система логування
├── validators.py           # Валідація та санітизація
├── watermarker_engine.py   # Ядро обробки зображень
├── editor_module.py        # Модуль редактора
├── utils.py                # Утиліти та допоміжні функції
├── translations.py         # Переклади UI
├── requirements.txt        # Залежності
├── README.md              # Документація
├── assets/
│   └── fonts/             # TTF/OTF шрифти для текстових вотермарок
└── tests/
    └── test_engine.py     # Unit тести
```

---

## 🎨 Використання

### Для чого в проєкті Streamlit?

Streamlit тут виконує роль **швидкого UI-шару** над вашим Python-ядром обробки зображень:

- дає веб-інтерфейс без окремого фронтенд-фреймворку;
- дозволяє швидко зібрати workflow: upload → налаштування → preview → batch processing;
- добре підходить для внутрішнього інструменту в LAN, де важлива швидкість розробки, а не складний продукт-frontend.

Тобто Streamlit у цьому проєкті — це не “ядро обробки”, а **оболонка для взаємодії з користувачем**.
Ядро обробки живе окремо в `watermarker_engine.py`.

### 1. Базовий workflow

1. **Завантажте фото** - перетягніть або оберіть файли
2. **Налаштуйте вотермарку** - текст або логотип
3. **Оберіть позицію** - куток або замощення
4. **Налаштуйте ресайз** (опціонально)
5. **Оберіть файли** для обробки
6. **Натисніть "Обробити"**
7. **Скачайте ZIP** або окремі файли

### 2. Текстова вотермарка

```
1. Перейдіть на вкладку "🔤 Текст"
2. Введіть текст вотермарки
3. Оберіть шрифт (з папки assets/fonts/)
4. Оберіть колір
5. Налаштуйте розмір та прозорість
```

### 3. Графічна вотермарка

```
1. Перейдіть на вкладку "🖼️ Логотип"
2. Завантажте PNG з прозорістю
3. Налаштуйте розмір та прозорість
4. Оберіть позицію
```

### 4. Пресети

**Збереження:**
```
1. Налаштуйте всі параметри
2. "💾 Менеджер пресетів" → "Зберегти повний пресет"
3. Файл .json буде завантажено
```

**Завантаження:**
```
1. "💾 Менеджер пресетів" → "Завантажити пресет"
2. Оберіть .json файл
3. Всі налаштування будуть застосовані
```

### 5. Редактор

```
1. Оберіть файл у робочій області
2. Натисніть "🛠 Редагувати"
3. Поверніть (↺/↻)
4. Обріжте (виберіть область)
5. Натисніть "💾 Зберегти"
```

---

## ⚙️ Конфігурація

### config.py - основні параметри:

```python
# Ліміти файлів
MAX_FILE_SIZE = 100 * 1024 * 1024  # 100 MB
MAX_IMAGE_DIMENSION = 10000        # 10K px

# Підтримувані формати
SUPPORTED_INPUT_FORMATS = ['.jpg', '.jpeg', '.png', '.webp']
SUPPORTED_OUTPUT_FORMATS = ['JPEG', 'WEBP', 'PNG']

# Продуктивність
DEFAULT_THREADS = 2
MAX_THREADS = 8

# Якість
DEFAULT_QUALITY = 80
```

---

## 🧪 Тестування

### Запуск тестів

```bash
# Всі тести
pytest tests/test_engine.py -v

# Конкретний тест
pytest tests/test_engine.py::test_generate_filename_sequence -v

# З покриттям коду
pytest tests/test_engine.py --cov=watermarker_engine --cov-report=html
```

### Категорії тестів

- **Validation Tests** - тестування валідаторів
- **Engine Tests** - тестування основного функціоналу
- **Integration Tests** - тестування повного workflow
- **Performance Tests** - тестування на великих файлах

---

## 📊 Логування

Логи зберігаються у `watermarker.log`:

```python
# Рівні логування
INFO  - загальна інформація про роботу
DEBUG - детальна діагностична інформація
WARNING - попередження (не критичні)
ERROR - помилки з stack trace
```

### Приклад логу:

```
2025-01-15 10:23:45 - watermarker - INFO - App started - Language: ua
2025-01-15 10:23:52 - watermarker.engine - INFO - Processed: output_001.jpg (800x600 → 1920x1440)
2025-01-15 10:23:55 - watermarker - INFO - Batch processing completed: 5 files
```

---

## 🔧 Розширення

### Додавання нового шрифту

```bash
1. Покладіть .ttf або .otf файл у assets/fonts/
2. Перезапустіть додаток
3. Шрифт з'явиться у списку
```

### Додавання нової мови

```python
# translations.py
TRANSLATIONS = {
    "new_lang": {
        "title": "Your Translation",
        "btn_process": "Process",
        # ... всі інші ключі
    }
}
```

---

## 🐛 Відомі обмеження

1. **Розмір файлу**: максимум 100 MB на файл
2. **Розміри зображення**: 10px - 10000px
3. **Формат вотермарки**: тільки PNG з alpha-каналом
4. **Threads**: занадто багато потоків може призвести до OOM

---

## 📈 Changelog

### v7.0 (2025-01-15) - Complete Rewrite

**🔒 Безпека та надійність:**
- Повна валідація всіх вхідних даних
- Обробка corrupted images
- Санітизація імен файлів
- Thread-safe операції з session state

**🚀 Продуктивність:**
- Виправлено memory leaks
- Кешування шрифтів та thumbnails
- Оптимізація роботи з великими зображеннями
- Proxy images для редактора

**📊 Моніторинг:**
- Професійне логування у файл та консоль
- Детальна звітність про помилки
- Статистика обробки

**🔧 Архітектура:**
- Модульна структура (8 окремих файлів)
- Централізована конфігурація
- Розділення responsibilities
- Готовність до unit-тестування

**✨ Нові можливості:**
- EXIF metadata preservation при обертанні
- Покращена валідація кольорів
- Безпечне ділення (division by zero protection)
- Rate-limiting для thumbnails

### v6.0 (попередня версія)
- Базовий функціонал
- Модульна структура
- Підтримка пресетів

---

## 🤝 Контрибуція

Contributions are welcome! 

1. Fork репозиторій
2. Створіть feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit зміни (`git commit -m 'Add AmazingFeature'`)
4. Push до branch (`git push origin feature/AmazingFeature`)
5. Створіть Pull Request

### Вимоги до PR:
- ✅ Код проходить всі тести
- ✅ Додано тести для нового функціоналу
- ✅ Оновлено документацію
- ✅ Код відповідає PEP 8

---

## 📄 Ліцензія

**Proprietary License**

© 2025 Marynyuk Andriy. All rights reserved.

---

## 👤 Автор

**Marynyuk Andriy**
- GitHub: [@MaanAndrii](https://github.com/MaanAndrii)

---

## 🙏 Подяки

- **Streamlit** - за чудовий фреймворк для UI
- **Pillow** - за потужну бібліотеку роботи з зображеннями
- **streamlit-cropper** - за компонент crop

---

## 📞 Підтримка

Виникли проблеми? Створіть [Issue](https://github.com/MaanAndrii/watermarker-pro/issues) на GitHub.

---

**⭐ Якщо проєкт вам сподобався - поставте зірочку на GitHub!**
