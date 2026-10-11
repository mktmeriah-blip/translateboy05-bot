"""
Translation engine wrapper.
Pakai deep-translator (Google Translate informal/web) secara default.
Kalau GOOGLE_API_KEY di-set, pakai Google Cloud Translation API (resmi).
"""
import asyncio
import logging
import re
from config import GOOGLE_API_KEY

logger = logging.getLogger(__name__)


# ─── STYLE REPLACEMENTS ──────────────────────────────────────────────────────
# Pasangan kata: (pola_regex, pengganti)

# Informal → Formal (Indonesia)
_FORMAL_ID: list[tuple[str, str]] = [
    (r"\bgue\b", "saya"), (r"\bgw\b", "saya"),
    (r"\baku\b", "saya"),
    (r"\blo\b", "Anda"), (r"\blu\b", "Anda"),
    (r"\belo\b", "Anda"), (r"\belu\b", "Anda"),
    (r"\bkamu\b", "Anda"),
    (r"\bnggak\b", "tidak"), (r"\bngga\b", "tidak"),
    (r"\bgak\b", "tidak"), (r"\bga\b", "tidak"),
    (r"\benggak\b", "tidak"),
    (r"\baja\b", "saja"), (r"\bdoang\b", "saja"),
    (r"\bemang\b", "memang"),
    (r"\bgimana\b", "bagaimana"), (r"\bgmn\b", "bagaimana"),
    (r"\bkayak\b", "seperti"), (r"\bkaya\b", "seperti"),
    (r"\bbanget\b", "sekali"), (r"\bbgt\b", "sekali"),
    (r"\budah\b", "sudah"), (r"\budh\b", "sudah"),
    (r"\bbelom\b", "belum"), (r"\bblm\b", "belum"),
    (r"\bmau\b", "ingin"), (r"\bmo\b", "ingin"),
    (r"\bcuma\b", "hanya"),
    (r"\btapi\b", "tetapi"), (r"\btp\b", "tetapi"),
    (r"\bbuat\b", "untuk"),
    (r"\bterus\b", "kemudian"), (r"\btrus\b", "kemudian"),
    (r"\bpake\b", "menggunakan"),
    (r"\bbilang\b", "mengatakan"),
    (r"\bnulis\b", "menulis"),
]

# Formal → Informal (Indonesia)
_INFORMAL_ID: list[tuple[str, str]] = [
    (r"\bsaya\b", "gue"),
    (r"\bAnda\b", "lo"), (r"\bkamu\b", "lo"),
    (r"\btidak\b", "nggak"), (r"\bbukan\b", "bukan"),
    (r"\bsangat\b", "banget"), (r"\bsekali\b", "banget"),
    (r"\bsudah\b", "udah"), (r"\btelah\b", "udah"),
    (r"\bbelum\b", "belom"),
    (r"\bbagaimana\b", "gimana"),
    (r"\bingin\b", "mau"), (r"\bhendak\b", "mau"),
    (r"\buntuk\b", "buat"),
    (r"\bhanya\b", "cuma"),
    (r"\btetapi\b", "tapi"), (r"\bnamun\b", "tapi"),
    (r"\bmenggunakan\b", "pake"),
]


def _apply_style(text: str, patterns: list[tuple[str, str]]) -> str:
    for pattern, replacement in patterns:
        text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
    return text


def _apply_style_for_lang(text: str, target_lang: str, style: str) -> str:
    """Terapkan penyesuaian gaya bahasa (paling efektif untuk id/ms)."""
    if target_lang not in ("id", "ms"):
        return text
    if style == "formal":
        return _apply_style(text, _FORMAL_ID)
    if style == "informal":
        return _apply_style(text, _INFORMAL_ID)
    return text


# ─── DETEKSI BAHASA ───────────────────────────────────────────────────────────

async def detect_language(text: str) -> tuple[str, float]:
    """
    Deteksi bahasa teks via Google Translate (deep-translator).
    Return (lang_code, confidence) — confidence selalu 0.95 karena GT reliable.
    """
    if not text or len(text.strip()) < 3:
        return "auto", 0.0

    try:
        from deep_translator import GoogleTranslator

        def _detect():
            # Terjemahkan ke English dulu untuk tahu source language
            t = GoogleTranslator(source="auto", target="en")
            t.translate(text[:200])  # Cukup 200 char untuk deteksi
            return t.source

        loop = asyncio.get_event_loop()
        detected = await loop.run_in_executor(None, _detect)

        if detected and detected not in ("auto", ""):
            # Normalisasi kode
            if detected in ("zh-cn",):
                detected = "zh-CN"
            elif detected in ("zh-tw",):
                detected = "zh-TW"
            return detected, 0.95

    except Exception as e:
        logger.warning(f"detect_language gagal: {e}")

    return "auto", 0.0


# ─── TERJEMAHAN ──────────────────────────────────────────────────────────────

async def translate_text(
    text: str,
    target: str,
    source: str = "auto",
    style: str = "auto",
) -> dict:
    """
    Terjemahkan teks.

    Return dict:
        translated    : hasil terjemahan
        detected_lang : bahasa yang terdeteksi
        confidence    : kepercayaan deteksi (0–1)
        target_lang   : bahasa tujuan yang dipakai
        style         : gaya yang diterapkan
        original      : teks asli
        error         : pesan error (None jika sukses)
    """
    result = {
        "translated": "",
        "detected_lang": source if source != "auto" else "auto",
        "confidence": 1.0 if source != "auto" else 0.0,
        "target_lang": target,
        "style": style,
        "original": text,
        "error": None,
    }

    if not text or not text.strip():
        result["error"] = "Teks kosong."
        return result

    # Deteksi bahasa sumber jika auto
    if source == "auto":
        detected, conf = await detect_language(text)
        result["detected_lang"] = detected
        result["confidence"] = conf

    # Jangan terjemahkan kalau bahasa sama
    src_known = result["detected_lang"] not in ("auto", "")
    if src_known and result["detected_lang"] == target:
        result["translated"] = text
        result["error"] = "same_language"
        return result

    # Pilih engine
    if GOOGLE_API_KEY:
        translated = await _translate_official(text, target, source)
    else:
        translated = await _translate_deep(text, target, source)

    if translated is None:
        result["error"] = "Gagal menerjemahkan. Coba lagi dalam beberapa detik."
        return result

    # Terapkan gaya bahasa (post-processing)
    translated = _apply_style_for_lang(translated, target, style)

    result["translated"] = translated
    return result


async def _translate_deep(text: str, target: str, source: str = "auto") -> str | None:
    """Terjemahkan via deep-translator (Google Translate tidak resmi)."""
    try:
        from deep_translator import GoogleTranslator

        def _do():
            translator = GoogleTranslator(source=source, target=target)
            return translator.translate(text)

        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(None, _do)
        return result if result else None

    except Exception as e:
        logger.error(f"deep-translator error: {e}")
        return None


async def _translate_official(text: str, target: str, source: str = "auto") -> str | None:
    """Terjemahkan via Google Cloud Translation API (resmi, butuh API key)."""
    try:
        from google.cloud import translate_v2 as translate

        def _do():
            client = translate.Client(client_options={"api_key": GOOGLE_API_KEY})
            src = None if source == "auto" else source
            resp = client.translate(text, target_language=target, source_language=src)
            return resp.get("translatedText")

        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, _do)

    except ImportError:
        logger.warning("google-cloud-translate tidak terinstall. Fallback ke deep-translator.")
        return await _translate_deep(text, target, source)
    except Exception as e:
        logger.error(f"Google Cloud Translate error: {e}")
        return None


# ─── HELPER ──────────────────────────────────────────────────────────────────

STYLE_LABELS: dict[str, str] = {
    "auto":      "🔄 Auto",
    "formal":    "👔 Formal",
    "informal":  "😎 Santai / Informal",
    "technical": "⚙️ Teknis",
    "casual":    "💬 Kasual",
}


def get_style_label(style: str) -> str:
    return STYLE_LABELS.get(style, f"❓ {style}")


CONFIDENCE_LABELS: list[tuple[float, str]] = [
    (0.90, "🟢 Tinggi"),
    (0.65, "🟡 Sedang"),
    (0.00, "🔴 Rendah"),
]


def get_confidence_label(conf: float) -> str:
    for threshold, label in CONFIDENCE_LABELS:
        if conf >= threshold:
            return label
    return "❓"
