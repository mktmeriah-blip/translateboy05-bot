"""
Bot Penerjemah Pro — Telegram Bot
Engine  : Google Translate (via deep-translator)
Bahasa  : 134 bahasa
Fitur   : auto-detect, reverse, gaya formal/santai, histori, stats
"""
import html
import logging
import math
from datetime import datetime

from telegram import Update, BotCommand
from telegram.constants import ChatAction, ParseMode
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

from config import BOT_TOKEN, DEFAULT_LANG, MAX_TEXT_LENGTH
from database import (
    clear_history,
    get_history,
    get_or_create_user,
    get_translation_by_id,
    get_user_stats,
    init_db,
    save_translation,
    update_user_settings,
)
from keyboards import (
    confirm_clear_keyboard,
    history_keyboard,
    language_list_keyboard,
    popular_langs_keyboard,
    search_result_keyboard,
    style_keyboard,
    translation_keyboard,
)
from languages import (
    LANG_ALIASES,
    get_lang_flag,
    get_lang_name,
    is_valid_lang,
    search_langs,
    LANGUAGES,
)
from translator import (
    get_confidence_label,
    get_style_label,
    translate_text,
)

logging.basicConfig(
    format="%(asctime)s [%(levelname)s] %(name)s — %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


# ─── HELPER ──────────────────────────────────────────────────────────────────

def fmt_lang(code: str) -> str:
    """Format bahasa jadi 'flag Nama'."""
    return f"{get_lang_flag(code)} {get_lang_name(code)}"


def escape(text: str) -> str:
    return html.escape(str(text))


def format_result(result: dict) -> str:
    """Format hasil terjemahan jadi pesan Telegram (MarkdownV2 via HTML)."""
    detected   = result.get("detected_lang", "auto")
    conf       = result.get("confidence", 0.0)
    target     = result.get("target_lang", DEFAULT_LANG)
    original   = result.get("original", "")
    translated = result.get("translated", "")
    style      = result.get("style", "auto")

    # Baris header bahasa
    if detected and detected != "auto":
        src_str = fmt_lang(detected)
        conf_str = f" <i>({get_confidence_label(conf)})</i>"
    else:
        src_str = "🌐 Auto-detect"
        conf_str = ""

    tgt_str    = fmt_lang(target)
    style_lbl  = get_style_label(style)

    # Potong teks asli kalau terlalu panjang di preview
    orig_preview = escape(original[:300]) + ("..." if len(original) > 300 else "")

    lines = [
        f"🔍 <b>{escape(src_str)}</b>{conf_str} → <b>{escape(tgt_str)}</b>",
        "",
        f"📝 <b>Teks Asli:</b>",
        f"<i>{orig_preview}</i>",
        "",
        f"✅ <b>Terjemahan:</b>",
        escape(translated),
        "",
        f"🎨 Gaya: {escape(style_lbl)}",
    ]
    return "\n".join(lines)


# ─── COMMANDS ────────────────────────────────────────────────────────────────

async def cmd_start(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    u = update.effective_user
    await get_or_create_user(u.id, u.username, u.first_name)

    name = escape(u.first_name or "Bro")
    total_langs = len(LANGUAGES)

    msg = (
        f"👋 <b>Halo, {name}!</b>\n\n"
        f"Aku adalah <b>Bot Penerjemah Pro</b> 🌐\n"
        f"Mendukung <b>{total_langs}+ bahasa</b> dari seluruh dunia!\n\n"
        f"<b>━━━━━━━━━━━━━━━━━━━</b>\n"
        f"💡 <b>Cara pakai:</b>\n"
        f"Ketik/kirim teks apa saja → langsung diterjemahkan ke 🇮🇩 Indonesia\n\n"
        f"<b>Perintah:</b>\n"
        f"🌐 /lang — Ganti bahasa tujuan\n"
        f"📋 /langs — Browse semua {total_langs}+ bahasa\n"
        f"🎨 /style — Pilih gaya bahasa\n"
        f"📜 /history — Riwayat terjemahan\n"
        f"📊 /stats — Statistik kamu\n"
        f"🗑️ /clearhist — Hapus riwayat\n"
        f"❓ /help — Panduan lengkap\n"
        f"<b>━━━━━━━━━━━━━━━━━━━</b>\n\n"
        f"Coba kirim kalimat atau kata dalam bahasa apa saja sekarang! 🚀"
    )
    await update.message.reply_html(msg)


async def cmd_help(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    msg = (
        f"❓ <b>Panduan Bot Penerjemah Pro</b>\n\n"
        f"<b>📖 Terjemahkan teks:</b>\n"
        f"Langsung kirim teks → bot otomatis menerjemahkan ke bahasa tujuan\n\n"
        f"<b>🌐 Kelola bahasa:</b>\n"
        f"• <code>/lang id</code> — Set tujuan ke Indonesia\n"
        f"• <code>/lang en</code> — Set tujuan ke Inggris\n"
        f"• <code>/lang [kode]</code> — Set ke bahasa apapun\n"
        f"• <code>/lang jepang</code> — Cari & set bahasa\n"
        f"• <code>/langs</code> — Browse semua 134+ bahasa\n\n"
        f"<b>🎨 Gaya bahasa:</b>\n"
        f"• <code>/style</code> — Pilih formal / santai / auto\n"
        f"• Efek paling terasa untuk Bahasa Indonesia\n\n"
        f"<b>📜 Histori:</b>\n"
        f"• <code>/history</code> — 5 terjemahan terakhir per halaman\n"
        f"• <code>/clearhist</code> — Hapus semua riwayat\n\n"
        f"<b>📊 Statistik:</b>\n"
        f"• <code>/stats</code> — Total terjemahan, bahasa favorit, dll.\n\n"
        f"<b>🔘 Tombol setelah terjemahan:</b>\n"
        f"• 🔄 <b>Balik</b> — Terjemahkan balik ke bahasa asal\n"
        f"• 🌐 <b>Ganti Bahasa</b> — Pilih bahasa lain untuk teks yang sama\n"
        f"• 🎨 <b>Gaya Bahasa</b> — Ubah gaya & terjemahkan ulang\n\n"
        f"<b>💡 Tips akurasi:</b>\n"
        f"• Teks lebih panjang → deteksi bahasa lebih akurat\n"
        f"• Kalau bahasa terdeteksi salah, gunakan <code>/lang</code> untuk paksa sumber\n"
        f"• Maks <b>{MAX_TEXT_LENGTH:,} karakter</b> per terjemahan\n"
        f"• Gaya formal/santai hanya berpengaruh ke terjemahan Indonesia"
    )
    await update.message.reply_html(msg)


async def cmd_lang(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    u = update.effective_user
    db_user = await get_or_create_user(u.id, u.username, u.first_name)
    current = db_user.get("target_lang", DEFAULT_LANG)

    # Kalau ada argumen
    if ctx.args:
        query = " ".join(ctx.args).strip()
        code = LANG_ALIASES.get(query.lower(), query.lower())

        # Cek langsung sebagai kode bahasa
        if is_valid_lang(code):
            await update_user_settings(u.id, target_lang=code)
            await update.message.reply_html(
                f"✅ Bahasa tujuan diubah ke <b>{fmt_lang(code)}</b>\n"
                f"Sekarang kirim teks untuk diterjemahkan!"
            )
            return

        # Cari berdasarkan nama
        results = search_langs(query)
        if results:
            if len(results) == 1:
                # Langsung set kalau cuma 1 hasil
                found_code = results[0][0]
                await update_user_settings(u.id, target_lang=found_code)
                await update.message.reply_html(
                    f"✅ Bahasa tujuan diubah ke <b>{fmt_lang(found_code)}</b>"
                )
            else:
                await update.message.reply_html(
                    f"🔍 Hasil pencarian untuk <b>{escape(query)}</b>:\nPilih salah satu:",
                    reply_markup=search_result_keyboard(results, mode="set"),
                )
        else:
            await update.message.reply_html(
                f"❌ Bahasa <b>{escape(query)}</b> tidak ditemukan.\n\n"
                f"Gunakan kode bahasa (contoh: <code>en</code>, <code>ja</code>, <code>ar</code>) "
                f"atau nama bahasa (contoh: <code>jepang</code>, <code>arab</code>).\n\n"
                f"Lihat semua: /langs"
            )
        return

    # Tanpa argumen: tampilkan bahasa populer
    await update.message.reply_html(
        f"🌐 <b>Pilih Bahasa Tujuan</b>\n"
        f"Saat ini: <b>{fmt_lang(current)}</b>\n\n"
        f"Pilih bahasa populer atau browse semua:",
        reply_markup=popular_langs_keyboard(mode="set"),
    )


async def cmd_langs(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_html(
        f"📋 <b>Semua Bahasa yang Didukung ({len(LANGUAGES)} bahasa)</b>\n\n"
        f"Pilih bahasa tujuan baru:",
        reply_markup=language_list_keyboard(page=0, mode="set"),
    )


async def cmd_style(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    u = update.effective_user
    db_user = await get_or_create_user(u.id, u.username, u.first_name)
    current = db_user.get("style", "auto")

    await update.message.reply_html(
        f"🎨 <b>Gaya Bahasa</b>\n"
        f"Saat ini: <b>{get_style_label(current)}</b>\n\n"
        f"ℹ️ Gaya <b>formal</b> dan <b>santai</b> paling efektif untuk Bahasa Indonesia & Melayu.\n"
        f"Untuk bahasa lain, Google Translate akan menerjemahkan apa adanya.",
        reply_markup=style_keyboard(trans_id=0),
    )


async def cmd_history(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    await _show_history(update.message, update.effective_user.id, page=0)


async def _show_history(msg_or_query, user_id: int, page: int = 0):
    per_page = 5
    items, total = await get_history(user_id, page=page, per_page=per_page)

    if not items:
        text = (
            "📜 <b>Riwayat kosong.</b>\n\n"
            "Kirim teks apa saja untuk mulai menerjemahkan!"
        )
        if hasattr(msg_or_query, "reply_html"):
            await msg_or_query.reply_html(text)
        else:
            await msg_or_query.edit_message_text(text, parse_mode=ParseMode.HTML)
        return

    total_pages = math.ceil(total / per_page)
    lines = [f"📜 <b>Riwayat Terjemahan</b> (halaman {page+1}/{total_pages})\n"]

    for i, item in enumerate(items, start=page * per_page + 1):
        try:
            dt = datetime.fromisoformat(item["created_at"]).strftime("%d/%m %H:%M")
        except Exception:
            dt = "—"

        src = fmt_lang(item["source_lang"])
        tgt = fmt_lang(item["target_lang"])
        orig  = escape(item["original_text"][:60])  + ("..." if len(item["original_text"])  > 60 else "")
        trans = escape(item["translated_text"][:60]) + ("..." if len(item["translated_text"]) > 60 else "")

        lines.append(
            f"<b>{i}.</b> <code>{dt}</code>  {src} → {tgt}\n"
            f"   📝 {orig}\n"
            f"   ✅ {trans}\n"
        )

    text = "\n".join(lines)
    kb   = history_keyboard(page, total_pages)

    if hasattr(msg_or_query, "reply_html"):
        await msg_or_query.reply_html(text, reply_markup=kb)
    else:
        await msg_or_query.edit_message_text(text, parse_mode=ParseMode.HTML, reply_markup=kb)


async def cmd_stats(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    u = update.effective_user
    stats   = await get_user_stats(u.id)
    db_user = await get_or_create_user(u.id, u.username, u.first_name)

    def lang_lines(items: list[dict], key: str) -> str:
        if not items:
            return "  <i>Belum ada data</i>"
        return "\n".join(
            f"  {fmt_lang(item[key])} — {item['cnt']}x" for item in items
        )

    msg = (
        f"📊 <b>Statistik Kamu</b>\n\n"
        f"🔢 Total terjemahan  : <b>{stats.get('total', 0):,}</b>\n"
        f"📝 Total karakter    : <b>{stats.get('total_chars', 0):,}</b>\n"
        f"🌐 Bahasa sumber unik: <b>{stats.get('unique_source', 0)}</b>\n"
        f"🎯 Bahasa tujuan unik: <b>{stats.get('unique_target', 0)}</b>\n\n"
        f"🏆 <b>Top Bahasa Tujuan:</b>\n{lang_lines(stats.get('top_targets', []), 'target_lang')}\n\n"
        f"🔍 <b>Top Bahasa Sumber Terdeteksi:</b>\n{lang_lines(stats.get('top_sources', []), 'source_lang')}\n\n"
        f"⚙️ <b>Setting Aktif:</b>\n"
        f"  Tujuan : {fmt_lang(db_user.get('target_lang', DEFAULT_LANG))}\n"
        f"  Gaya   : {get_style_label(db_user.get('style', 'auto'))}"
    )
    await update.message.reply_html(msg)


async def cmd_clearhist(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_html(
        "⚠️ <b>Hapus Semua Riwayat?</b>\n\nTindakan ini tidak bisa dibatalkan!",
        reply_markup=confirm_clear_keyboard(),
    )


# ─── MAIN TEXT HANDLER ────────────────────────────────────────────────────────

async def handle_text(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    u    = update.effective_user
    text = update.message.text.strip()

    if not text:
        return

    if len(text) > MAX_TEXT_LENGTH:
        await update.message.reply_html(
            f"⚠️ Teks terlalu panjang (<b>{len(text):,}</b> karakter).\n"
            f"Maksimum: <b>{MAX_TEXT_LENGTH:,}</b> karakter."
        )
        return

    db_user     = await get_or_create_user(u.id, u.username, u.first_name)
    target_lang = db_user.get("target_lang", DEFAULT_LANG)
    style       = db_user.get("style", "auto")

    await update.message.chat.send_action(ChatAction.TYPING)

    result = await translate_text(text, target=target_lang, style=style)

    if result.get("error") == "same_language":
        await update.message.reply_html(
            f"ℹ️ Bahasa input ({fmt_lang(result['detected_lang'])}) sudah sama dengan bahasa tujuan.\n"
            f"Gunakan /lang untuk mengganti bahasa tujuan, atau /langs untuk melihat semua pilihan."
        )
        return

    if result.get("error"):
        await update.message.reply_html(
            f"❌ <b>Gagal menerjemahkan:</b>\n<i>{escape(result['error'])}</i>\n\n"
            f"Coba lagi dalam beberapa detik."
        )
        return

    trans_id = await save_translation(
        user_id    = u.id,
        source_lang= result["detected_lang"],
        target_lang= target_lang,
        original   = text,
        translated = result["translated"],
        style      = style,
    )

    await update.message.reply_html(
        format_result(result),
        reply_markup=translation_keyboard(trans_id, result["detected_lang"], target_lang),
    )


# ─── CALLBACK HANDLER ────────────────────────────────────────────────────────

async def handle_callback(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    q    = update.callback_query
    data = q.data
    u    = q.from_user

    await q.answer()

    # ── Utility ────────────────────────────────────────────────────────────
    if data == "noop":
        return

    if data == "cancel":
        try:
            await q.message.delete()
        except Exception:
            pass
        return

    # ── Set bahasa default ─────────────────────────────────────────────────
    if data.startswith("sl:"):
        code = data[3:]
        await update_user_settings(u.id, target_lang=code)
        await q.message.edit_text(
            f"✅ Bahasa tujuan diubah ke <b>{fmt_lang(code)}</b>\n\n"
            f"Kirim teks apa saja untuk diterjemahkan!",
            parse_mode=ParseMode.HTML,
        )
        return

    # ── Re-translate ke bahasa tertentu ───────────────────────────────────
    if data.startswith("rtl:"):
        _, code, tid_str = data.split(":", 2)
        tid   = int(tid_str)
        trans = await get_translation_by_id(tid)
        if not trans:
            await q.answer("❌ Data tidak ditemukan.", show_alert=True)
            return

        db_user = await get_or_create_user(u.id, u.username, u.first_name)
        style   = db_user.get("style", "auto")

        await q.message.chat.send_action(ChatAction.TYPING)

        result = await translate_text(
            text   = trans["original_text"],
            target = code,
            source = trans["source_lang"],
            style  = style,
        )
        if result.get("error"):
            await q.answer(f"❌ {result['error']}", show_alert=True)
            return

        new_tid = await save_translation(
            user_id     = u.id,
            source_lang = result["detected_lang"],
            target_lang = code,
            original    = trans["original_text"],
            translated  = result["translated"],
            style       = style,
        )

        try:
            await q.message.delete()
        except Exception:
            pass

        await q.message.chat.send_message(
            format_result(result),
            parse_mode  = ParseMode.HTML,
            reply_markup= translation_keyboard(new_tid, result["detected_lang"], code),
        )
        return

    # ── Language list page — mode set ─────────────────────────────────────
    if data.startswith("lps:"):
        page = int(data[4:])
        await q.message.edit_reply_markup(
            reply_markup=language_list_keyboard(page=page, mode="set")
        )
        return

    # ── Language list page — mode re-translate ────────────────────────────
    if data.startswith("lpt:"):
        _, tid_str, page_str = data.split(":", 2)
        await q.message.edit_reply_markup(
            reply_markup=language_list_keyboard(
                page=int(page_str),
                trans_id=int(tid_str),
                mode="trans",
            )
        )
        return

    # ── Reverse translation ────────────────────────────────────────────────
    if data.startswith("rev:"):
        tid   = int(data[4:])
        trans = await get_translation_by_id(tid)
        if not trans:
            await q.answer("❌ Data tidak ditemukan.", show_alert=True)
            return

        db_user = await get_or_create_user(u.id, u.username, u.first_name)
        style   = db_user.get("style", "auto")

        # Target balik = bahasa sumber asli (fallback ke 'en')
        reverse_target = trans["source_lang"]
        if reverse_target in ("auto", "", None):
            reverse_target = "en"

        await q.message.chat.send_action(ChatAction.TYPING)

        result = await translate_text(
            text   = trans["translated_text"],
            target = reverse_target,
            source = trans["target_lang"],
            style  = style,
        )
        if result.get("error"):
            await q.answer(f"❌ {result['error']}", show_alert=True)
            return

        new_tid = await save_translation(
            user_id     = u.id,
            source_lang = trans["target_lang"],
            target_lang = reverse_target,
            original    = trans["translated_text"],
            translated  = result["translated"],
            style       = style,
        )

        await q.message.reply_html(
            format_result(result),
            reply_markup=translation_keyboard(new_tid, trans["target_lang"], reverse_target),
        )
        return

    # ── Change language menu ───────────────────────────────────────────────
    if data.startswith("cl:"):
        tid = int(data[3:])
        await q.message.reply_html(
            f"🌐 <b>Pilih Bahasa Tujuan</b>\n\nTerjemahkan teks yang sama ke bahasa mana?",
            reply_markup=popular_langs_keyboard(trans_id=tid, mode="trans"),
        )
        return

    # ── Style menu ────────────────────────────────────────────────────────
    if data.startswith("sm:"):
        tid     = int(data[3:])
        db_user = await get_or_create_user(u.id, u.username, u.first_name)
        current = db_user.get("style", "auto")
        await q.message.reply_html(
            f"🎨 <b>Gaya Bahasa</b>\n"
            f"Saat ini: <b>{get_style_label(current)}</b>\n\n"
            f"ℹ️ Efek paling jelas untuk Bahasa Indonesia & Melayu.",
            reply_markup=style_keyboard(trans_id=tid),
        )
        return

    # ── Set style (dan re-translate kalau ada tid) ─────────────────────────
    if data.startswith("ss:"):
        _, style, tid_str = data.split(":", 2)
        tid = int(tid_str)

        await update_user_settings(u.id, style=style)

        confirm_msg = (
            f"✅ Gaya bahasa diubah ke <b>{get_style_label(style)}</b>"
        )
        if style in ("formal", "informal"):
            confirm_msg += "\n\n💡 Perubahan paling terasa untuk terjemahan ke Bahasa Indonesia."

        # Re-translate dengan gaya baru kalau ada trans_id
        if tid > 0:
            trans = await get_translation_by_id(tid)
            if trans:
                await q.message.edit_text(
                    confirm_msg + "\n\n⏳ Menerjemahkan ulang dengan gaya baru...",
                    parse_mode=ParseMode.HTML,
                )
                await q.message.chat.send_action(ChatAction.TYPING)

                result = await translate_text(
                    text   = trans["original_text"],
                    target = trans["target_lang"],
                    source = trans["source_lang"],
                    style  = style,
                )

                if not result.get("error"):
                    new_tid = await save_translation(
                        user_id     = u.id,
                        source_lang = result["detected_lang"],
                        target_lang = trans["target_lang"],
                        original    = trans["original_text"],
                        translated  = result["translated"],
                        style       = style,
                    )
                    await q.message.edit_text(
                        format_result(result),
                        parse_mode   = ParseMode.HTML,
                        reply_markup = translation_keyboard(
                            new_tid, result["detected_lang"], trans["target_lang"]
                        ),
                    )
                else:
                    await q.message.edit_text(confirm_msg, parse_mode=ParseMode.HTML)
                return

        await q.message.edit_text(confirm_msg, parse_mode=ParseMode.HTML)
        return

    # ── History page ───────────────────────────────────────────────────────
    if data.startswith("hist:"):
        page = int(data[5:])
        await _show_history(q, u.id, page=page)
        return

    # ── Clear history confirm ──────────────────────────────────────────────
    if data == "clrhist":
        await q.message.edit_reply_markup(reply_markup=confirm_clear_keyboard())
        return

    if data == "clryes":
        count = await clear_history(u.id)
        await q.message.edit_text(
            f"🗑️ <b>{count} riwayat terjemahan</b> telah dihapus.",
            parse_mode=ParseMode.HTML,
        )
        return


# ─── INIT & RUN ──────────────────────────────────────────────────────────────

async def post_init(app: Application) -> None:
    await app.bot.set_my_commands([
        BotCommand("start",      "Mulai bot"),
        BotCommand("lang",       "Ganti bahasa tujuan"),
        BotCommand("langs",      "Browse semua bahasa"),
        BotCommand("style",      "Gaya bahasa (formal/santai)"),
        BotCommand("history",    "Riwayat terjemahan"),
        BotCommand("stats",      "Statistik penggunaan"),
        BotCommand("clearhist",  "Hapus riwayat"),
        BotCommand("help",       "Panduan lengkap"),
    ])
    await init_db()
    logger.info("🤖 Bot Penerjemah Pro — siap!")


def main() -> None:
    if not BOT_TOKEN:
        logger.error("❌ BOT_TOKEN tidak ditemukan! Isi di file .env")
        return

    app = (
        Application.builder()
        .token(BOT_TOKEN)
        .post_init(post_init)
        .build()
    )

    # Command handlers
    app.add_handler(CommandHandler("start",     cmd_start))
    app.add_handler(CommandHandler("help",      cmd_help))
    app.add_handler(CommandHandler("lang",      cmd_lang))
    app.add_handler(CommandHandler("langs",     cmd_langs))
    app.add_handler(CommandHandler("style",     cmd_style))
    app.add_handler(CommandHandler("history",   cmd_history))
    app.add_handler(CommandHandler("stats",     cmd_stats))
    app.add_handler(CommandHandler("clearhist", cmd_clearhist))

    # Text message → translate
    app.add_handler(MessageHandler(
        filters.TEXT & ~filters.COMMAND,
        handle_text,
    ))

    # Inline button callbacks
    app.add_handler(CallbackQueryHandler(handle_callback))

    logger.info("▶️ Starting polling...")
    app.run_polling(allowed_updates=["message", "callback_query"])


if __name__ == "__main__":
    main()
