"""
Watermarker Pro v8.0 - Translations Module
===========================================
UI text strings in multiple languages
"""

TRANSLATIONS = {
    "ua": {
        "title": "📸 Watermarker Pro v8.0",
        "subtitle": "Професійна обробка фото з вотермаркою",

        # Sidebar
        "sb_config": "🛠 Налаштування",
        "btn_defaults": "↺ Скинути налаштування",

        # Presets
        "sec_presets": "💾 Менеджер пресетів",
        "lbl_load_preset": "Завантажити пресет (.json)",
        "btn_save_preset": "⬇️ Зберегти повний пресет",
        "msg_preset_loaded": "✅ Пресет завантажено!",
        "error_preset": "❌ Помилка пресету: {}",

        # File Settings
        "sec_file": "1️⃣ Файл та Експорт",
        "lbl_format": "Формат виводу",
        "lbl_quality": "Якість (%)",
        "lbl_naming": "Іменування файлів",
        "lbl_prefix": "Префікс файлу",

        # Geometry
        "sec_geo": "2️⃣ Геометрія (Ресайз)",
        "chk_resize": "Змінювати розмір",
        "lbl_mode": "Режим ресайзу",
        "lbl_px": "Розмір (px)",
        "btn_preset_hd": "HD",
        "btn_preset_fhd": "FHD",
        "btn_preset_4k": "4K",

        # Watermark
        "sec_wm": "3️⃣ Вотермарка",
        "tab_logo": "🖼️ Логотип",
        "tab_text": "🔤 Текст",
        "lbl_logo_up": "Завантажити (PNG або SVG)",
        "lbl_text_input": "Текст вотермарки",
        "lbl_font": "Шрифт",
        "lbl_color": "Колір",
        "msg_preset_logo_active": "ℹ️ Використовується логотип з пресету",
        "msg_no_fonts": "⚠️ Шрифти не знайдено в assets/fonts",
        "msg_svg_no_cairosvg": "⚠️ SVG вотермарки потребують: pip install cairosvg",

        # Watermark Settings
        "lbl_pos": "Позиція",
        "opt_pos_tile": "Замощення (Паттерн)",
        "lbl_scale": "Розмір / Масштаб (%)",
        "lbl_opacity": "Прозорість",
        "lbl_gap": "Проміжок (px)",
        "lbl_margin": "Відступ (px)",
        "lbl_angle": "Кут нахилу (°)",

        # Performance
        "sec_perf": "⚙️ Продуктивність",
        "lbl_threads": "Потоки (Threads)",
        "help_threads": "Зменшіть якщо додаток вилітає",

        # HEIC indicator
        "heic_available": "✅ HEIC/HEIF підтримується",
        "heic_unavailable": "⚠️ HEIC не підтримується — встановіть: pip install pillow-heif",

        # Workspace
        "files_header": "📂 Робоча область",
        "uploader_label": "Завантажити фото",
        "btn_process": "🚀 Обробити",
        "btn_cancel": "⛔ Скасувати",
        "msg_processing": "⏳ Обробка...",
        "msg_cancelled": "⛔ Обробку скасовано",
        "msg_done": "✅ Готово!",
        "error_wm_load": "❌ Помилка завантаження вотермарки: {}",
        "btn_dl_zip": "📦 Скачати ZIP",
        "exp_dl_separate": "⬇️ Скачати окремо",

        # File Grid
        "grid_select_all": "✅ Вибрати всі",
        "grid_deselect_all": "⬜ Зняти всі",
        "grid_delete": "🗑️ Видалити",
        "btn_selected": "✅ Обрано",
        "btn_select": "⬜ Обрати",
        "warn_no_files": "⚠️ Спочатку оберіть файли!",
        "btn_clear_workspace": "♻️ Очистити все",
        "expander_add_files": "📤 Додати файли",
        "stat_files_selected": "Файлів: {} | Обрано: {}",

        # Drag-and-drop order
        "sec_order": "🔀 Порядок обробки",
        "order_hint": "Перетягніть файли для зміни порядку (впливає на нумерацію в режимі 'Prefix + Sequence')",

        # Batch rename preview
        "sec_rename_preview": "📋 Попередній перегляд імен",
        "rename_col_original": "Оригінал",
        "rename_col_output": "Результат",

        # Preview
        "prev_header": "👁️ Живий перегляд",
        "prev_placeholder": "Оберіть файл (✅) для перегляду",
        "stat_res": "Роздільна здатність",
        "stat_size": "Розмір файлу",
        "btn_generate_preview": "🔄 Оновити перегляд",
        "msg_preview_error": "❌ Помилка генерації перегляду",

        # Before/After comparison
        "sec_compare": "🔍 Порівняння до/після",
        "compare_before": "До",
        "compare_after": "Після",

        # Processing stats
        "sec_stats": "📊 Статистика обробки",
        "stats_total_files": "Файлів оброблено",
        "stats_total_before": "Загальний розмір (до)",
        "stats_total_after": "Загальний розмір (після)",
        "stats_avg_compression": "Середня компресія",
        "stats_resolution_change": "Зміна роздільної здатності",

        # Editor
        "btn_open_editor": "🛠 Редагувати (Crop/Rotate)",
        "lbl_aspect": "Пропорції",
        "btn_save_edit": "💾 Зберегти зміни",
        "msg_edit_saved": "✅ Зміни збережено!",

        # Language
        "lang_select": "Мова інтерфейсу / Interface Language",

        # About
        "about_expander": "ℹ️ Про програму",
        "about_prod": "**Продукт:** Watermarker Pro v8.0",
        "about_auth": "**Автор:** Marynyuk Andriy",
        "about_lic": "**Ліцензія:** Proprietary",
        "about_repo": "[GitHub Repository](https://github.com/MaanAndrii)",
        "about_copy": "© 2025 Всі права захищено",
        "about_changelog_title": "📝 Історія змін",
        "about_changelog": """**v8.0:**
- 📋 Batch rename preview (таблиця до обробки)
- 🔍 Порівняння до/після зі слайдером
- 🔀 Drag-and-drop порядок файлів
- 🖼️ SVG як вотермарка (cairosvg)
- 🧹 Розподіл utils.py на session/preset/file_manager
- 🔒 LRU-кеш шрифтів з обмеженням
- 📊 Зведена статистика після batch
- ⛔ Кнопка скасування обробки
- ✅ Індикатор підтримки HEIC

**v7.0 Complete Rewrite:**
- 🔒 Повна обробка помилок
- 🎯 Валідація всіх даних
- 📊 Професійне логування
- 🚀 Оптимізація пам'яті
"""
    },

    "en": {
        "title": "📸 Watermarker Pro v8.0",
        "subtitle": "Professional photo watermarking",

        # Sidebar
        "sb_config": "🛠 Configuration",
        "btn_defaults": "↺ Reset Settings",

        # Presets
        "sec_presets": "💾 Presets Manager",
        "lbl_load_preset": "Load Preset (.json)",
        "btn_save_preset": "⬇️ Save Full Preset",
        "msg_preset_loaded": "✅ Preset loaded!",
        "error_preset": "❌ Preset error: {}",

        # File Settings
        "sec_file": "1️⃣ File & Export",
        "lbl_format": "Output Format",
        "lbl_quality": "Quality (%)",
        "lbl_naming": "File Naming",
        "lbl_prefix": "File Prefix",

        # Geometry
        "sec_geo": "2️⃣ Geometry (Resize)",
        "chk_resize": "Enable Resize",
        "lbl_mode": "Resize Mode",
        "lbl_px": "Size (px)",
        "btn_preset_hd": "HD",
        "btn_preset_fhd": "FHD",
        "btn_preset_4k": "4K",

        # Watermark
        "sec_wm": "3️⃣ Watermark",
        "tab_logo": "🖼️ Logo",
        "tab_text": "🔤 Text",
        "lbl_logo_up": "Upload Logo (PNG or SVG)",
        "lbl_text_input": "Watermark Text",
        "lbl_font": "Font",
        "lbl_color": "Color",
        "msg_preset_logo_active": "ℹ️ Using logo from preset",
        "msg_no_fonts": "⚠️ No fonts found in assets/fonts",
        "msg_svg_no_cairosvg": "⚠️ SVG watermarks require: pip install cairosvg",

        # Watermark Settings
        "lbl_pos": "Position",
        "opt_pos_tile": "Tiled (Pattern)",
        "lbl_scale": "Size / Scale (%)",
        "lbl_opacity": "Opacity",
        "lbl_gap": "Gap (px)",
        "lbl_margin": "Margin (px)",
        "lbl_angle": "Angle (°)",

        # Performance
        "sec_perf": "⚙️ Performance",
        "lbl_threads": "Max Threads",
        "help_threads": "Reduce if app crashes",

        # HEIC indicator
        "heic_available": "✅ HEIC/HEIF supported",
        "heic_unavailable": "⚠️ HEIC not supported — install: pip install pillow-heif",

        # Workspace
        "files_header": "📂 Workspace",
        "uploader_label": "Upload Photos",
        "btn_process": "🚀 Process",
        "btn_cancel": "⛔ Cancel",
        "msg_processing": "⏳ Processing...",
        "msg_cancelled": "⛔ Processing cancelled",
        "msg_done": "✅ Done!",
        "error_wm_load": "❌ Watermark load error: {}",
        "btn_dl_zip": "📦 Download ZIP",
        "exp_dl_separate": "⬇️ Download Separate",

        # File Grid
        "grid_select_all": "✅ Select All",
        "grid_deselect_all": "⬜ Deselect All",
        "grid_delete": "🗑️ Delete",
        "btn_selected": "✅ Selected",
        "btn_select": "⬜ Select",
        "warn_no_files": "⚠️ Select files first!",
        "btn_clear_workspace": "♻️ Clear Workspace",
        "expander_add_files": "📤 Add Files",
        "stat_files_selected": "Files: {} | Selected: {}",

        # Drag-and-drop order
        "sec_order": "🔀 Processing Order",
        "order_hint": "Drag to reorder (affects numbering in 'Prefix + Sequence' mode)",

        # Batch rename preview
        "sec_rename_preview": "📋 Rename Preview",
        "rename_col_original": "Original",
        "rename_col_output": "Output",

        # Preview
        "prev_header": "👁️ Live Preview",
        "prev_placeholder": "Select a file (✅) to preview",
        "stat_res": "Resolution",
        "stat_size": "File Size",
        "btn_generate_preview": "🔄 Refresh Preview",
        "msg_preview_error": "❌ Preview generation error",

        # Before/After comparison
        "sec_compare": "🔍 Before / After",
        "compare_before": "Before",
        "compare_after": "After",

        # Processing stats
        "sec_stats": "📊 Processing Stats",
        "stats_total_files": "Files processed",
        "stats_total_before": "Total size (before)",
        "stats_total_after": "Total size (after)",
        "stats_avg_compression": "Avg compression",
        "stats_resolution_change": "Resolution change",

        # Editor
        "btn_open_editor": "🛠 Edit (Crop/Rotate)",
        "lbl_aspect": "Aspect Ratio",
        "btn_save_edit": "💾 Save Changes",
        "msg_edit_saved": "✅ Changes saved!",

        # Language
        "lang_select": "Interface Language / Мова інтерфейсу",

        # About
        "about_expander": "ℹ️ About",
        "about_prod": "**Product:** Watermarker Pro v8.0",
        "about_auth": "**Author:** Marynyuk Andriy",
        "about_lic": "**License:** Proprietary",
        "about_repo": "[GitHub Repository](https://github.com/MaanAndrii)",
        "about_copy": "© 2025 All rights reserved",
        "about_changelog_title": "📝 Changelog",
        "about_changelog": """**v8.0:**
- 📋 Batch rename preview table
- 🔍 Before/After slider comparison
- 🔀 Drag-and-drop file ordering
- 🖼️ SVG watermark support (cairosvg)
- 🧹 utils.py split into session/preset/file_manager
- 🔒 LRU font cache with size limit
- 📊 Batch processing summary stats
- ⛔ Cancel button for batch processing
- ✅ HEIC support indicator

**v7.0 Complete Rewrite:**
- 🔒 Complete error handling
- 🎯 Full data validation
- 📊 Professional logging
- 🚀 Memory optimization
"""
    }
}
