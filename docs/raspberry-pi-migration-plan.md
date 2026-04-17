# План міграції Watermarker Pro у локальну мережу на Raspberry Pi

## 1) Що вже добре для Raspberry Pi

- Додаток статлес з точки зору бекенду: головна логіка в Python-модулях, UI через Streamlit (`web_app.py`).
- Важкі операції винесені в окремий engine (`watermarker_engine.py`).
- Тимчасові файли ізольовані у temp-директорії сесії (`session.py`, `file_manager.py`).

## 2) Що потрібно переробити обовʼязково (MVP для LAN)

### 2.1. Продакшн-старт для локальної мережі

Зараз README пропонує тільки базовий запуск `streamlit run web_app.py`.
Для Raspberry Pi в LAN треба стандартизувати запуск:

- bind на всі інтерфейси: `--server.address 0.0.0.0`
- фіксований порт: `--server.port 8501`
- вимкнути CORS/XSRF тільки якщо є reverse proxy і окрема ізоляція (інакше залишити дефолт).

**Що змінити в репо:**
- додати `.streamlit/config.toml` з серверними параметрами;
- додати `systemd` unit (`deploy/watermarker.service`) для автозапуску після reboot;
- оновити `README.md` секцією "Raspberry Pi / LAN deployment".

### 2.2. Залежності, сумісні з ARM (Raspberry Pi)

У `requirements.txt` є пакети, які можуть вимагати перевірки wheel на ARM:
- `pillow-heif`
- `resvg-py`
- `streamlit-cropper-fix`

**Що змінити в репо:**
- зафіксувати версії залежностей (pinning), щоб уникати випадкових breakage на ARM;
- додати скрипт smoke-check (`scripts/check_runtime.py`), який імпортує ключові модулі і перевіряє `engine.is_heic_available()` та `engine.is_svg_available()`;
- у README додати fallback-режим: якщо немає HEIC/SVG — працюємо тільки з PNG/JPEG/WebP.

### 2.3. Безпека в LAN

Зараз застосунок не має auth-шару, а Streamlit сам по собі не є повноцінним security-gateway.

**Що змінити в репо:**
- перед Streamlit поставити reverse proxy (Nginx/Caddy) + базова автентифікація;
- обмежити доступ до підмережі (наприклад 192.168.0.0/16) через firewall (ufw/nftables);
- винести секрети/параметри в env змінні (порт, log-level, ліміти).

### 2.4. Керування ресурсами Pi (RAM/CPU/disk)

На Pi вузьке місце — RAM і I/O. У коді вже є треди (`config.MAX_THREADS=8`), що може бути забагато для слабших моделей.

**Що змінити в репо:**
- зробити `DEFAULT_THREADS` залежним від `os.cpu_count()` (з верхньою межею 4 для Pi);
- додати env-overrides для `MAX_FILE_SIZE`, `MAX_IMAGE_DIMENSION`, `MAX_THREADS`;
- додати періодичне очищення temp-директорій, що залишилися після аварійного завершення.

## 3) Що бажано доробити після MVP

### 3.1. Черга задач замість thread burst

Зараз batch виконується через `ThreadPoolExecutor` з паралельною обробкою. Для Pi більш стабільно:
- обмежити concurrent jobs (2-3);
- додати просту чергу та прогрес по задачах;
- (опційно) винести обробку в окремий worker process.

### 3.2. Сховище

Якщо користувачів декілька, `/tmp` і локальний диск Pi швидко фрагментуються.

Рекомендації:
- тримати `temp_dir` на окремому SSD/USB;
- додати configurable `WORK_DIR` (env) замість завжди `tempfile.mkdtemp`;
- лог-rotation для `watermarker.log`.

### 3.3. Спостережуваність

- healthcheck endpoint (через reverse proxy або sidecar);
- базові метрики: час обробки, середній розмір файлу, число помилок;
- системні ліміти в `systemd` (`MemoryMax`, `CPUQuota`, `Restart=always`).

## 4) Рекомендований порядок робіт

1. **Deployment baseline**: `.streamlit/config.toml` + `systemd` + README.
2. **ARM hardening**: pinning requirements + smoke-check скрипт.
3. **Resource controls**: env-конфіг + авто-тюнінг потоків.
4. **Security layer**: reverse proxy + LAN ACL.
5. **Cleanup/ops**: temp retention + log rotation + monitoring.

## 5) Мінімальний Definition of Done для переносу в LAN

- Pi стартує сервіс автоматично після reboot.
- UI доступний по `http://<pi-ip>:8501` в локальній мережі.
- Обробка 20 фото 12MP завершується без OOM.
- Після 24 годин роботи нема неконтрольованого росту temp/log.
- При недоступності HEIC/SVG є зрозумілий fallback без крашу.
