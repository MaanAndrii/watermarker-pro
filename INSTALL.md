# Watermarker Pro v8.0 — Встановлення на Raspberry Pi

## Вимоги

| Компонент | Мінімум | Рекомендовано |
|---|---|---|
| Модель | Raspberry Pi 3B | Raspberry Pi 4/5 |
| RAM | 1 ГБ | 4 ГБ |
| Місце на диску | 1 ГБ | 4 ГБ |
| Python | 3.8 | 3.11 |
| ОС | Raspberry Pi OS Bullseye | Raspberry Pi OS Bookworm (64-bit) |

---

## Варіант A — Автоматичне встановлення через візард

Найпростіший спосіб:

```bash
cd /шлях/до/watermarker-pro
bash install.sh
```

Візард крок за кроком запитає:
- директорію встановлення
- порт (за замовчуванням 8501)
- доступ з мережі або тільки локально
- кількість потоків обробки
- чи потрібен автозапуск при старті системи

---

## Варіант B — Ручне встановлення

### Крок 1. Оновлення системи

```bash
sudo apt update && sudo apt upgrade -y
```

### Крок 2. Встановлення системних залежностей

```bash
sudo apt install -y \
    python3 python3-pip python3-venv python3-dev \
    build-essential git curl \
    libjpeg-dev zlib1g-dev libpng-dev libwebp-dev \
    libfreetype6-dev libffi-dev \
    libheif-dev libde265-dev
```

> **Примітка про HEIC (iPhone-фото):** `libheif-dev` потрібен для підтримки формату `.heic/.heif`.
> Якщо пакет недоступний у вашій версії ОС, можна пропустити — HEIC просто не буде підтримуватися.

### Крок 3. Копіювання файлів проєкту

Якщо ще не зроблено — скопіюйте папку `watermarker-pro` на Raspberry Pi.

Через SSH + scp (виконується на вашому комп'ютері):
```bash
scp -r ./watermarker-pro pi@192.168.1.100:/home/pi/
```

Або через git:
```bash
git clone https://github.com/MaanAndrii/watermarker-pro.git
cd watermarker-pro
```

### Крок 4. Віртуальне середовище Python

```bash
cd /home/pi/watermarker-pro
python3 -m venv venv
source venv/bin/activate
```

### Крок 5. Оновлення pip та встановлення залежностей

```bash
pip install --upgrade pip setuptools wheel

pip install \
    streamlit \
    "Pillow>=10.0.0" \
    translitua \
    pandas \
    streamlit-cropper-fix \
    pillow-heif \
    cachetools \
    streamlit-sortables
```

#### Встановлення resvg-py (підтримка SVG-водяних знаків)

Пакет `resvg-py` містить Rust-бінарний код та може зайняти кілька хвилин на Pi:

```bash
pip install resvg-py
```

Якщо встановлення не вдалося — потрібен компілятор Rust:

```bash
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
source "$HOME/.cargo/env"
pip install resvg-py
```

> Без `resvg-py` SVG-водяні знаки будуть недоступні, решта функцій працює нормально.

### Крок 6. Перевірка встановлення

```bash
python -c "import streamlit, PIL, pandas, cachetools; print('OK')"
```

### Крок 7. Перший запуск

```bash
# Переконайтеся, що venv активовано:
source /home/pi/watermarker-pro/venv/bin/activate

streamlit run web_app.py \
    --server.port 8501 \
    --server.address 0.0.0.0 \
    --server.enableCORS false \
    --server.enableXsrfProtection false \
    --server.maxUploadSize 200
```

Відкрийте у браузері:
- З Raspberry Pi: `http://localhost:8501`
- З іншого пристрою в мережі: `http://<IP-адреса-Pi>:8501`

Дізнатися IP-адресу Pi:
```bash
hostname -I
```

---

## Автозапуск через systemd

Щоб застосунок запускався автоматично при увімкненні Pi:

### 1. Створіть файл сервісу

```bash
sudo nano /etc/systemd/system/watermarker-pro.service
```

Вміст файлу:

```ini
[Unit]
Description=Watermarker Pro v8.0
After=network.target

[Service]
Type=simple
User=pi
WorkingDirectory=/home/pi/watermarker-pro
ExecStart=/home/pi/watermarker-pro/venv/bin/streamlit run web_app.py \
    --server.port 8501 \
    --server.address 0.0.0.0 \
    --server.enableCORS false \
    --server.enableXsrfProtection false \
    --server.maxUploadSize 200
Restart=on-failure
RestartSec=5
StandardOutput=journal
StandardError=journal
Environment=PYTHONUNBUFFERED=1

[Install]
WantedBy=multi-user.target
```

> Замініть `User=pi` та шлях `/home/pi/` на фактичне ім'я вашого користувача.

### 2. Увімкніть та запустіть сервіс

```bash
sudo systemctl daemon-reload
sudo systemctl enable watermarker-pro
sudo systemctl start watermarker-pro
```

### 3. Перевірка статусу

```bash
sudo systemctl status watermarker-pro

# Перегляд логів у реальному часі:
sudo journalctl -u watermarker-pro -f
```

### Корисні команди управління сервісом

```bash
sudo systemctl stop watermarker-pro      # зупинити
sudo systemctl restart watermarker-pro   # перезапустити
sudo systemctl disable watermarker-pro   # вимкнути автозапуск
```

---

## Налаштування firewall (за потреби)

Якщо порт 8501 заблоковано:

```bash
# ufw (якщо встановлено):
sudo ufw allow 8501/tcp
sudo ufw reload

# iptables:
sudo iptables -A INPUT -p tcp --dport 8501 -j ACCEPT
```

---

## Усунення проблем

### Помилка: "No module named 'streamlit'"
```bash
source /home/pi/watermarker-pro/venv/bin/activate
pip install streamlit
```

### Помилка з Pillow / JPEG
```bash
sudo apt install libjpeg-dev zlib1g-dev
pip install --force-reinstall Pillow
```

### HEIC не підтримується
```bash
sudo apt install libheif-dev libde265-dev
pip install --force-reinstall pillow-heif
```

### resvg-py не встановлюється
SVG-водяні знаки недоступні, але застосунок працює без них. Щоб все ж встановити:
```bash
sudo apt install cargo
pip install resvg-py
```

### Застосунок повільно працює на Pi 3
- Зменшіть кількість потоків до 1–2 у налаштуваннях
- Зменшіть максимальний розмір зображень (параметр `resize_val`)
- Використовуйте формат JPEG (швидше, ніж PNG)

### Перевірка логів застосунку
```bash
cat /home/pi/watermarker-pro/watermarker.log
```

---

## Оновлення

```bash
cd /home/pi/watermarker-pro
git pull origin main
source venv/bin/activate
pip install --upgrade -r requirements.txt
sudo systemctl restart watermarker-pro
```

---

## Видалення

```bash
sudo systemctl stop watermarker-pro
sudo systemctl disable watermarker-pro
sudo rm /etc/systemd/system/watermarker-pro.service
sudo systemctl daemon-reload
rm -rf /home/pi/watermarker-pro
```
