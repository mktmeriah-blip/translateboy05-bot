"""
Semua InlineKeyboard builder ada di sini.

Format callback_data yang dipakai:
  sl:{code}          → Set default target lang
  rtl:{code}:{tid}   → Re-translate ke bahasa ini (dari histori ID)
  lps:{page}         → Language list page (mode set default)
  lpt:{tid}:{page}   → Language list page (mode re-translate)
  rev:{tid}          → Reverse translation
  cl:{tid}           → Change language menu
  sm:{tid}           → Style menu
  ss:{style}:{tid}   → Set style (dan re-translate kalau tid > 0)
  hist:{page}        → Halaman histori
  clrhist            → Konfirmasi hapus histori
  clryes             → Hapus histori (confirmed)
  cancel             → Tutup pesan
  noop               → Tidak melakukan apa-apa (tombol display)
"""
import math
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from languages import LANGUAGES, POPULAR_LANGS, get_lang_name, get_lang_flag


# ─── POST-TRANSLATION ─────────────────────────────────────────────────────────

def translation_keyboard(
    trans_id: int,
    source_lang: str,
    target_lang: str,
) -> InlineKeyboardMarkup:
    """Keyboard yang muncul setelah hasil terjemahan."""
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("🔄 Balik",         callback_data=f"rev:{trans_id}"),
            InlineKeyboardButton("🌐 Ganti Bahasa",   callback_data=f"cl:{trans_id}"),
        ],
        [
            InlineKeyboardButton("🎨 Gaya Bahasa",    callback_data=f"sm:{trans_id}"),
            InlineKeyboardButton("📜 Histori",         callback_data="hist:0"),
        ],
    ])


# ─── LANGUAGE SELECTION ───────────────────────────────────────────────────────

def popular_langs_keyboard(
    trans_id: int = 0,
    mode: str = "set",  # "set" atau "trans"
) -> InlineKeyboardMarkup:
    """Quick-select bahasa populer + tombol browse semua."""
    buttons = []
    row: list[InlineKeyboardButton] = []

    for code in POPULAR_LANGS:
        flag = get_lang_flag(code)
        name = get_lang_name(code)
        label = f"{flag} {name}"

        cb = f"sl:{code}" if mode == "set" else f"rtl:{code}:{trans_id}"
        row.append(InlineKeyboardButton(label, callback_data=cb))

        if len(row) == 2:
            buttons.append(row)
            row = []

    if row:
        buttons.append(row)

    # Tombol browse semua bahasa
    if mode == "set":
        browse_cb = "lps:0"
    else:
        browse_cb = f"lpt:{trans_id}:0"

    buttons.append([InlineKeyboardButton("📋 Browse Semua (134 Bahasa)...", callback_data=browse_cb)])
    buttons.append([InlineKeyboardButton("❌ Batal", callback_data="cancel")])

    return InlineKeyboardMarkup(buttons)


def language_list_keyboard(
    page: int = 0,
    trans_id: int = 0,
    mode: str = "set",
    per_page: int = 10,
) -> InlineKeyboardMarkup:
    """Daftar semua bahasa dengan pagination."""
    lang_codes = list(LANGUAGES.keys())
    total_pages = math.ceil(len(lang_codes) / per_page)
    page = max(0, min(page, total_pages - 1))

    start = page * per_page
    end = min(start + per_page, len(lang_codes))
    page_langs = lang_codes[start:end]

    buttons = []
    row: list[InlineKeyboardButton] = []

    for code in page_langs:
        info = LANGUAGES[code]
        label = f"{info['flag']} {info['name']}"
        cb = f"sl:{code}" if mode == "set" else f"rtl:{code}:{trans_id}"
        row.append(InlineKeyboardButton(label, callback_data=cb))
        if len(row) == 2:
            buttons.append(row)
            row = []

    if row:
        buttons.append(row)

    # Navigasi
    nav: list[InlineKeyboardButton] = []
    if page > 0:
        nav_cb = f"lps:{page-1}" if mode == "set" else f"lpt:{trans_id}:{page-1}"
        nav.append(InlineKeyboardButton("◀️", callback_data=nav_cb))

    nav.append(InlineKeyboardButton(
        f"📄 {page+1}/{total_pages}", callback_data="noop"
    ))

    if page < total_pages - 1:
        nav_cb = f"lps:{page+1}" if mode == "set" else f"lpt:{trans_id}:{page+1}"
        nav.append(InlineKeyboardButton("▶️", callback_data=nav_cb))

    buttons.append(nav)
    buttons.append([InlineKeyboardButton("❌ Batal", callback_data="cancel")])

    return InlineKeyboardMarkup(buttons)


def search_result_keyboard(
    results: list[tuple[str, dict]],
    trans_id: int = 0,
    mode: str = "set",
) -> InlineKeyboardMarkup:
    """Hasil pencarian bahasa."""
    buttons = []
    for code, info in results:
        label = f"{info['flag']} {info['name']} ({info['native']})"
        cb = f"sl:{code}" if mode == "set" else f"rtl:{code}:{trans_id}"
        buttons.append([InlineKeyboardButton(label, callback_data=cb)])
    buttons.append([InlineKeyboardButton("❌ Batal", callback_data="cancel")])
    return InlineKeyboardMarkup(buttons)


# ─── STYLE ────────────────────────────────────────────────────────────────────

STYLE_OPTIONS = [
    ("auto",      "🔄 Auto (Bawaan Google)"),
    ("formal",    "👔 Formal (Baku / Resmi)"),
    ("informal",  "😎 Santai / Informal"),
    ("technical", "⚙️ Teknis (Istilah Preserved)"),
]


def style_keyboard(trans_id: int = 0) -> InlineKeyboardMarkup:
    buttons = []
    for style_id, label in STYLE_OPTIONS:
        cb = f"ss:{style_id}:{trans_id}"
        buttons.append([InlineKeyboardButton(label, callback_data=cb)])
    buttons.append([InlineKeyboardButton("❌ Batal", callback_data="cancel")])
    return InlineKeyboardMarkup(buttons)


# ─── HISTORY ─────────────────────────────────────────────────────────────────

def history_keyboard(page: int, total_pages: int) -> InlineKeyboardMarkup:
    buttons: list[list[InlineKeyboardButton]] = []

    nav: list[InlineKeyboardButton] = []
    if page > 0:
        nav.append(InlineKeyboardButton("◀️ Prev", callback_data=f"hist:{page-1}"))
    nav.append(InlineKeyboardButton(f"{page+1}/{total_pages}", callback_data="noop"))
    if page < total_pages - 1:
        nav.append(InlineKeyboardButton("Next ▶️", callback_data=f"hist:{page+1}"))

    if nav:
        buttons.append(nav)

    buttons.append([
        InlineKeyboardButton("🗑️ Hapus Semua", callback_data="clrhist"),
        InlineKeyboardButton("❌ Tutup", callback_data="cancel"),
    ])
    return InlineKeyboardMarkup(buttons)


def confirm_clear_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("✅ Ya, Hapus!", callback_data="clryes"),
            InlineKeyboardButton("❌ Batal",       callback_data="cancel"),
        ]
    ])
