#!/usr/bin/env bash
# =============================================================================
# Watermarker Pro v8.0 — Installation Wizard for Raspberry Pi
# =============================================================================
set -euo pipefail

# ── Кольори ──────────────────────────────────────────────────────────────────
RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'
BLUE='\033[0;34m'; CYAN='\033[0;36m'; BOLD='\033[1m'; NC='\033[0m'

ok()   { echo -e "${GREEN}  ✓${NC} $*"; }
info() { echo -e "${CYAN}  →${NC} $*"; }
warn() { echo -e "${YELLOW}  !${NC} $*"; }
err()  { echo -e "${RED}  ✗ ПОМИЛКА:${NC} $*" >&2; }
die()  { err "$*"; exit 1; }

# ── Глобальні змінні (будуть заповнені під час візарду) ──────────────────────
INSTALL_DIR=""
VENV_DIR=""
APP_PORT=8501
APP_HOST="0.0.0.0"
AUTOSTART=false
SERVICE_USER=""
THREADS=2
GIT_CLONED=false
REPO_URL="https://github.com/MaanAndrii/watermarker-pro.git"

# =============================================================================
# КРОК 0 — Банер
# =============================================================================
show_banner() {
    clear
    echo -e "${BOLD}${BLUE}"
    echo "  ╔══════════════════════════════════════════════════════╗"
    echo "  ║       Watermarker Pro v8.0  —  Майстер встановлення  ║"
    echo "  ║            Raspberry Pi  |  Debian/Ubuntu             ║"
    echo "  ╚══════════════════════════════════════════════════════╝"
    echo -e "${NC}"
    echo -e "  Цей майстер проведе вас через усі кроки встановлення."
    echo -e "  Натисніть ${BOLD}Enter${NC} для підтвердження або введіть значення."
    echo -e "  Кроки: перевірка → git clone → директорія → пакети → Python → потоки → автозапуск\n"
}

# =============================================================================
# КРОК 1 — Перевірка системи
# =============================================================================
check_system() {
    echo -e "\n${BOLD}══ Крок 1/7: Перевірка системи ══${NC}\n"

    # ОС
    if [[ -f /etc/os-release ]]; then
        . /etc/os-release
        info "Операційна система: ${PRETTY_NAME:-unknown}"
    fi

    # Архітектура
    ARCH=$(uname -m)
    info "Архітектура: ${ARCH}"
    if [[ "$ARCH" != "aarch64" && "$ARCH" != "armv7l" && "$ARCH" != "x86_64" ]]; then
        warn "Непідтримувана архітектура: ${ARCH}. Продовжуємо на свій ризик."
    fi

    # Python
    if command -v python3 &>/dev/null; then
        PY_VER=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
        PY_MAJOR=$(echo "$PY_VER" | cut -d. -f1)
        PY_MINOR=$(echo "$PY_VER" | cut -d. -f2)
        if (( PY_MAJOR < 3 || (PY_MAJOR == 3 && PY_MINOR < 8) )); then
            die "Потрібен Python 3.8+. Знайдено: ${PY_VER}"
        fi
        ok "Python ${PY_VER}"
    else
        die "Python 3 не знайдено. Встановіть: sudo apt install python3"
    fi

    # pip
    if python3 -m pip --version &>/dev/null; then
        ok "pip $(python3 -m pip --version | awk '{print $2}')"
    else
        warn "pip не знайдено. Буде встановлено автоматично."
    fi

    # Вільна пам'ять
    FREE_MB=$(free -m | awk '/^Mem:/{print $7}')
    if (( FREE_MB < 256 )); then
        warn "Мало вільної RAM: ${FREE_MB} МБ. Рекомендовано 512+ МБ."
    else
        ok "Вільна RAM: ${FREE_MB} МБ"
    fi

    # Вільне місце
    FREE_DISK=$(df -BM . | awk 'NR==2{gsub("M","",$4); print $4}')
    if (( FREE_DISK < 500 )); then
        warn "Мало місця на диску: ${FREE_DISK} МБ. Рекомендовано 1+ ГБ."
    else
        ok "Вільне місце: ${FREE_DISK} МБ"
    fi

    echo ""
    read -rp "  Продовжити встановлення? [Y/n]: " CONTINUE
    CONTINUE="${CONTINUE:-Y}"
    [[ "$CONTINUE" =~ ^[Yy]$ ]] || { info "Встановлення скасовано."; exit 0; }
}

# =============================================================================
# КРОК 2 — Клонування з GitHub
# =============================================================================
clone_from_git() {
    echo -e "\n${BOLD}══ Крок 2/7: Отримання проєкту з GitHub ══${NC}\n"

    # Перевірка / встановлення git
    if ! command -v git &>/dev/null; then
        warn "git не знайдено."
        if command -v apt-get &>/dev/null; then
            read -rp "  Встановити git зараз? [Y/n]: " DO_GIT_INSTALL
            DO_GIT_INSTALL="${DO_GIT_INSTALL:-Y}"
            if [[ "$DO_GIT_INSTALL" =~ ^[Yy]$ ]]; then
                info "Встановлення git..."
                sudo apt-get install -y git -qq
                ok "git встановлено: $(git --version)"
            else
                warn "Клонування пропущено — git не доступний."
                return
            fi
        else
            warn "Встановіть git вручну та перезапустіть скрипт."
            return
        fi
    else
        ok "git $(git --version | awk '{print $3}')"
    fi

    echo ""
    echo -e "  Звідки взяти файли Watermarker Pro?"
    echo -e "    1) Клонувати з GitHub  ${BOLD}← рекомендовано${NC}"
    echo -e "    2) Файли вже є на цьому пристрої"
    read -rp "  Ваш вибір [1]: " GIT_CHOICE
    GIT_CHOICE="${GIT_CHOICE:-1}"

    if [[ "$GIT_CHOICE" != "1" ]]; then
        info "Клонування пропущено. Файли будуть знайдені на кроці 3."
        return
    fi

    # URL репозиторію
    echo ""
    read -rp "  URL репозиторію [${REPO_URL}]: " INPUT_URL
    REPO_URL="${INPUT_URL:-$REPO_URL}"

    # Гілка
    read -rp "  Гілка [main]: " INPUT_BRANCH
    GIT_BRANCH="${INPUT_BRANCH:-main}"

    # Куди клонувати
    DEFAULT_DEST="${HOME}/watermarker-pro"
    read -rp "  Куди зберегти проєкт [${DEFAULT_DEST}]: " INPUT_DEST
    CLONE_DEST="${INPUT_DEST:-$DEFAULT_DEST}"
    CLONE_DEST="${CLONE_DEST%/}"

    if [[ -d "${CLONE_DEST}/.git" ]]; then
        warn "Репозиторій вже існує в '${CLONE_DEST}'."
        read -rp "  Оновити (git pull)? [Y/n]: " DO_PULL
        DO_PULL="${DO_PULL:-Y}"
        if [[ "$DO_PULL" =~ ^[Yy]$ ]]; then
            info "Оновлення репозиторію..."
            git -C "$CLONE_DEST" fetch origin "$GIT_BRANCH" 2>&1 | tail -3
            git -C "$CLONE_DEST" checkout "$GIT_BRANCH" 2>/dev/null || true
            git -C "$CLONE_DEST" pull origin "$GIT_BRANCH"
            ok "Репозиторій оновлено."
        else
            info "Використовуємо наявний репозиторій без оновлення."
        fi
    else
        info "Клонування ${REPO_URL} (гілка: ${GIT_BRANCH})..."
        git clone --branch "$GIT_BRANCH" --depth 1 "$REPO_URL" "$CLONE_DEST"
        ok "Клоновано до: ${CLONE_DEST}"
    fi

    [[ -f "${CLONE_DEST}/web_app.py" ]] || die "Клонування завершено, але web_app.py не знайдено в '${CLONE_DEST}'"

    INSTALL_DIR="$CLONE_DEST"
    GIT_CLONED=true
    ok "Директорія проєкту: ${INSTALL_DIR}"
}

# =============================================================================
# КРОК 3 — Вибір директорії (якщо не клоновано)
# =============================================================================
choose_directory() {
    echo -e "\n${BOLD}══ Крок 3/7: Директорія та мережеві налаштування ══${NC}\n"

    # Якщо проєкт вже клоновано — тільки підтвердити директорію
    if $GIT_CLONED; then
        ok "Директорія вже визначена: ${INSTALL_DIR}"
    else
        SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
        DEFAULT_DIR="$SCRIPT_DIR"

        echo -e "  Де знаходяться файли Watermarker Pro?"
        read -rp "  Директорія [${DEFAULT_DIR}]: " INSTALL_DIR
        INSTALL_DIR="${INSTALL_DIR:-$DEFAULT_DIR}"
        INSTALL_DIR="${INSTALL_DIR%/}"

        [[ -f "${INSTALL_DIR}/web_app.py" ]] || die "Файл web_app.py не знайдено в '${INSTALL_DIR}'"
        ok "Директорія проєкту: ${INSTALL_DIR}"
    fi

    VENV_DIR="${INSTALL_DIR}/venv"
    ok "Віртуальне середовище: ${VENV_DIR}"

    # Порт
    echo ""
    read -rp "  Порт для веб-інтерфейсу [${APP_PORT}]: " INPUT_PORT
    APP_PORT="${INPUT_PORT:-$APP_PORT}"
    if ! [[ "$APP_PORT" =~ ^[0-9]+$ ]] || (( APP_PORT < 1024 || APP_PORT > 65535 )); then
        warn "Некоректний порт. Буде використано 8501."
        APP_PORT=8501
    fi
    ok "Порт: ${APP_PORT}"

    # Хост
    echo ""
    echo -e "  Доступ до інтерфейсу:"
    echo -e "    1) Тільки з цього пристрою (localhost)"
    echo -e "    2) З локальної мережі (0.0.0.0)  ${BOLD}← рекомендовано для Pi${NC}"
    read -rp "  Ваш вибір [2]: " HOST_CHOICE
    HOST_CHOICE="${HOST_CHOICE:-2}"
    [[ "$HOST_CHOICE" == "1" ]] && APP_HOST="127.0.0.1" || APP_HOST="0.0.0.0"
    ok "Хост: ${APP_HOST}"
}

# =============================================================================
# КРОК 4 — Системні пакети
# =============================================================================
install_system_packages() {
    echo -e "\n${BOLD}══ Крок 4/7: Системні пакети ══${NC}\n"

    if ! command -v apt-get &>/dev/null; then
        warn "apt-get не знайдено. Пропускаємо встановлення системних пакетів."
        return
    fi

    echo -e "  Буде встановлено системні залежності через apt."
    read -rp "  Продовжити? [Y/n]: " DO_APT
    DO_APT="${DO_APT:-Y}"
    [[ "$DO_APT" =~ ^[Yy]$ ]] || { info "Пропущено."; return; }

    info "Оновлення списку пакетів..."
    sudo apt-get update -qq

    PKGS=(
        python3-pip
        python3-venv
        python3-dev
        build-essential
        libjpeg-dev
        zlib1g-dev
        libpng-dev
        libwebp-dev
        libfreetype6-dev
        libffi-dev
        # для pillow-heif (HEIC/HEIF підтримка)
        libheif-dev
        libde265-dev
        # загальне
        git
        curl
    )

    info "Встановлення пакетів: ${PKGS[*]}"
    sudo apt-get install -y "${PKGS[@]}" 2>&1 | grep -E "(Installed|already)" | head -20 || true
    ok "Системні пакети встановлено."
}

# =============================================================================
# КРОК 5 — Python-середовище та залежності
# =============================================================================
install_python_deps() {
    echo -e "\n${BOLD}══ Крок 5/7: Python-залежності ══${NC}\n"

    # Створення venv
    if [[ -d "$VENV_DIR" ]]; then
        warn "Директорія venv вже існує: ${VENV_DIR}"
        read -rp "  Перестворити? [y/N]: " RECREATE
        if [[ "${RECREATE:-N}" =~ ^[Yy]$ ]]; then
            rm -rf "$VENV_DIR"
        fi
    fi

    if [[ ! -d "$VENV_DIR" ]]; then
        info "Створення віртуального середовища..."
        python3 -m venv "$VENV_DIR"
        ok "Створено: ${VENV_DIR}"
    fi

    PIP="${VENV_DIR}/bin/pip"
    PYTHON="${VENV_DIR}/bin/python"

    info "Оновлення pip/setuptools/wheel..."
    "$PIP" install --upgrade pip setuptools wheel -q
    ok "pip оновлено."

    # Встановлення пакетів
    info "Встановлення залежностей з requirements.txt..."
    echo ""

    REQS_FILE="${INSTALL_DIR}/requirements.txt"

    # Окремо встановлюємо resvg-py, бо може не мати колеса для arm
    PACKAGES=(
        streamlit
        "Pillow>=10.0.0"
        translitua
        pandas
        streamlit-cropper-fix
        pillow-heif
        cachetools
        streamlit-sortables
    )

    for PKG in "${PACKAGES[@]}"; do
        info "  Встановлення ${PKG}..."
        if "$PIP" install "$PKG" -q 2>/dev/null; then
            ok "  ${PKG}"
        else
            warn "  Не вдалося встановити ${PKG} — спробуйте вручну: pip install ${PKG}"
        fi
    done

    # resvg-py — Rust-бінарна залежність, може потребувати cargo
    info "  Встановлення resvg-py (SVG-підтримка)..."
    if "$PIP" install resvg-py -q 2>/dev/null; then
        ok "  resvg-py"
    else
        warn "  resvg-py не вдалося встановити. SVG-водяні знаки будуть недоступні."
        warn "  Для встановлення вручну: sudo apt install cargo && pip install resvg-py"
    fi

    ok "Python-залежності встановлено."
}

# =============================================================================
# КРОК 6 — Кількість потоків
# =============================================================================
configure_threads() {
    echo -e "\n${BOLD}══ Крок 6/7: Налаштування продуктивності ══${NC}\n"

    CPU_CORES=$(nproc 2>/dev/null || echo 4)
    RECOMMENDED=$(( CPU_CORES > 4 ? 4 : CPU_CORES ))

    echo -e "  Кількість ядер CPU: ${CPU_CORES}"
    echo -e "  Рекомендована кількість потоків для обробки: ${RECOMMENDED}"
    echo -e "  (Raspberry Pi 4/5: 4 ядра; Pi 3: 4 ядра; Pi Zero: 1 ядро)"
    echo ""
    read -rp "  Кількість потоків [${RECOMMENDED}]: " INPUT_THREADS
    THREADS="${INPUT_THREADS:-$RECOMMENDED}"

    if ! [[ "$THREADS" =~ ^[0-9]+$ ]] || (( THREADS < 1 || THREADS > 8 )); then
        warn "Некоректне значення. Буде використано ${RECOMMENDED}."
        THREADS="$RECOMMENDED"
    fi
    ok "Потоків для обробки: ${THREADS}"
}

# =============================================================================
# КРОК 7 — Автозапуск (systemd)
# =============================================================================
setup_autostart() {
    echo -e "\n${BOLD}══ Крок 7/7: Автозапуск при старті системи ══${NC}\n"

    if ! command -v systemctl &>/dev/null; then
        warn "systemd не знайдено. Пропускаємо налаштування автозапуску."
        return
    fi

    read -rp "  Налаштувати автозапуск через systemd? [Y/n]: " DO_SERVICE
    DO_SERVICE="${DO_SERVICE:-Y}"
    if ! [[ "$DO_SERVICE" =~ ^[Yy]$ ]]; then
        info "Автозапуск пропущено."
        return
    fi

    SERVICE_USER="${SERVICE_USER:-$(whoami)}"
    read -rp "  Від якого користувача запускати [${SERVICE_USER}]: " INPUT_USER
    SERVICE_USER="${INPUT_USER:-$SERVICE_USER}"

    SERVICE_FILE="/etc/systemd/system/watermarker-pro.service"

    info "Створення systemd-сервісу..."
    sudo tee "$SERVICE_FILE" > /dev/null <<EOF
[Unit]
Description=Watermarker Pro v8.0
After=network.target
Wants=network-online.target

[Service]
Type=simple
User=${SERVICE_USER}
WorkingDirectory=${INSTALL_DIR}
ExecStart=${VENV_DIR}/bin/streamlit run web_app.py \\
    --server.port ${APP_PORT} \\
    --server.address ${APP_HOST} \\
    --server.enableCORS false \\
    --server.enableXsrfProtection false \\
    --server.maxUploadSize 200
Restart=on-failure
RestartSec=5
StandardOutput=journal
StandardError=journal
Environment=PYTHONUNBUFFERED=1

[Install]
WantedBy=multi-user.target
EOF

    sudo systemctl daemon-reload
    sudo systemctl enable watermarker-pro.service
    sudo systemctl start watermarker-pro.service

    if systemctl is-active --quiet watermarker-pro.service; then
        ok "Сервіс запущено та додано до автозапуску."
    else
        warn "Сервіс не запустився. Перевірте: sudo journalctl -u watermarker-pro -n 50"
    fi
    AUTOSTART=true
}

# =============================================================================
# Тест запуску
# =============================================================================
test_installation() {
    echo -e "\n${BOLD}── Перевірка встановлення ──${NC}\n"

    PYTHON="${VENV_DIR}/bin/python"

    local ALL_OK=true
    for MOD in streamlit PIL pandas cachetools; do
        if "$PYTHON" -c "import $MOD" 2>/dev/null; then
            ok "import ${MOD}"
        else
            warn "Модуль '${MOD}' не знайдено"
            ALL_OK=false
        fi
    done

    if $ALL_OK; then
        ok "Всі ключові модулі доступні."
    else
        warn "Деякі модулі відсутні. Запустіть: ${VENV_DIR}/bin/pip install -r ${INSTALL_DIR}/requirements.txt"
    fi
}

# =============================================================================
# Підсумок
# =============================================================================
show_summary() {
    # Визначаємо IP-адресу
    LOCAL_IP=$(hostname -I 2>/dev/null | awk '{print $1}' || echo "YOUR_PI_IP")

    echo ""
    echo -e "${BOLD}${GREEN}"
    echo "  ╔══════════════════════════════════════════════════════╗"
    echo "  ║          ✓  Встановлення завершено!                  ║"
    echo "  ╚══════════════════════════════════════════════════════╝"
    echo -e "${NC}"
    echo -e "  ${BOLD}Як запустити:${NC}"
    echo ""
    echo -e "    ${CYAN}# Активувати середовище та запустити вручну:${NC}"
    echo -e "    cd ${INSTALL_DIR}"
    echo -e "    source venv/bin/activate"
    echo -e "    streamlit run web_app.py --server.port ${APP_PORT} --server.address ${APP_HOST}"
    echo ""

    if $AUTOSTART; then
        echo -e "    ${CYAN}# Управління systemd-сервісом:${NC}"
        echo -e "    sudo systemctl status watermarker-pro"
        echo -e "    sudo systemctl restart watermarker-pro"
        echo -e "    sudo systemctl stop watermarker-pro"
        echo -e "    sudo journalctl -u watermarker-pro -f"
        echo ""
    fi

    echo -e "  ${BOLD}Відкрийте у браузері:${NC}"
    echo -e "    http://localhost:${APP_PORT}       ← з цього пристрою"
    echo -e "    http://${LOCAL_IP}:${APP_PORT}   ← з іншого пристрою в мережі"
    echo ""
    echo -e "  ${BOLD}Налаштування:${NC}"
    echo -e "    Потоків обробки: ${THREADS}"
    echo -e "    Директорія: ${INSTALL_DIR}"
    echo -e "    Логи: ${INSTALL_DIR}/watermarker.log"
    echo ""
}

# =============================================================================
# ГОЛОВНА ФУНКЦІЯ
# =============================================================================
main() {
    # Перенаправляємо stdin з терміналу — критично при запуску через curl | bash
    exec < /dev/tty

    show_banner
    check_system
    clone_from_git
    choose_directory
    install_system_packages
    install_python_deps
    configure_threads
    setup_autostart
    test_installation
    show_summary
}

main "$@"
