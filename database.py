"""
Database module — aiosqlite async SQLite
Tables: users, translations
"""
import aiosqlite
import logging
from datetime import datetime
from config import DB_PATH, MAX_HISTORY

logger = logging.getLogger(__name__)


# ─── INIT ────────────────────────────────────────────────────────────────────

async def init_db():
    async with aiosqlite.connect(DB_PATH) as db:
        # Tabel users
        await db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id     INTEGER PRIMARY KEY,
                username    TEXT,
                first_name  TEXT,
                target_lang TEXT NOT NULL DEFAULT 'id',
                style       TEXT NOT NULL DEFAULT 'auto',
                created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Tabel riwayat terjemahan
        await db.execute("""
            CREATE TABLE IF NOT EXISTS translations (
                id              INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id         INTEGER NOT NULL,
                source_lang     TEXT NOT NULL,
                target_lang     TEXT NOT NULL,
                original_text   TEXT NOT NULL,
                translated_text TEXT NOT NULL,
                style           TEXT NOT NULL DEFAULT 'auto',
                char_count      INTEGER DEFAULT 0,
                created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
            )
        """)

        # Index untuk query cepat
        await db.execute("""
            CREATE INDEX IF NOT EXISTS idx_translations_user_date
            ON translations(user_id, created_at DESC)
        """)

        await db.commit()
    logger.info("✅ Database initialized.")


# ─── USER ────────────────────────────────────────────────────────────────────

async def get_or_create_user(
    user_id: int,
    username: str | None = None,
    first_name: str | None = None,
) -> dict:
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row

        async with db.execute(
            "SELECT * FROM users WHERE user_id = ?", (user_id,)
        ) as cur:
            row = await cur.fetchone()

        if row is None:
            await db.execute(
                """INSERT INTO users (user_id, username, first_name, target_lang, style)
                   VALUES (?, ?, ?, 'id', 'auto')""",
                (user_id, username, first_name),
            )
            await db.commit()
            async with db.execute(
                "SELECT * FROM users WHERE user_id = ?", (user_id,)
            ) as cur:
                row = await cur.fetchone()
        else:
            # Update nama kalau berubah
            if username != row["username"] or first_name != row["first_name"]:
                await db.execute(
                    "UPDATE users SET username=?, first_name=? WHERE user_id=?",
                    (username, first_name, user_id),
                )
                await db.commit()

        return dict(row)


async def update_user_settings(user_id: int, **kwargs) -> None:
    valid = {"target_lang", "style"}
    updates = {k: v for k, v in kwargs.items() if k in valid}
    if not updates:
        return

    set_clause = ", ".join(f"{k} = ?" for k in updates)
    values = list(updates.values()) + [user_id]

    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            f"UPDATE users SET {set_clause}, updated_at = CURRENT_TIMESTAMP WHERE user_id = ?",
            values,
        )
        await db.commit()


# ─── TRANSLATIONS ─────────────────────────────────────────────────────────────

async def save_translation(
    user_id: int,
    source_lang: str,
    target_lang: str,
    original: str,
    translated: str,
    style: str = "auto",
) -> int:
    """Simpan terjemahan ke histori. Return ID-nya."""
    async with aiosqlite.connect(DB_PATH) as db:
        cur = await db.execute(
            """INSERT INTO translations
               (user_id, source_lang, target_lang, original_text, translated_text, style, char_count)
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (user_id, source_lang, target_lang, original, translated, style, len(original)),
        )
        trans_id = cur.lastrowid

        # Batasi histori per user
        await db.execute(
            """DELETE FROM translations
               WHERE user_id = ? AND id NOT IN (
                   SELECT id FROM translations
                   WHERE user_id = ?
                   ORDER BY created_at DESC
                   LIMIT ?
               )""",
            (user_id, user_id, MAX_HISTORY),
        )
        await db.commit()

    return trans_id


async def get_history(
    user_id: int,
    page: int = 0,
    per_page: int = 5,
) -> tuple[list[dict], int]:
    """Ambil histori terjemahan. Return (items, total)."""
    offset = page * per_page
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row

        async with db.execute(
            "SELECT COUNT(*) FROM translations WHERE user_id = ?", (user_id,)
        ) as cur:
            total = (await cur.fetchone())[0]

        async with db.execute(
            """SELECT * FROM translations WHERE user_id = ?
               ORDER BY created_at DESC LIMIT ? OFFSET ?""",
            (user_id, per_page, offset),
        ) as cur:
            items = [dict(r) for r in await cur.fetchall()]

    return items, total


async def get_translation_by_id(trans_id: int) -> dict | None:
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute(
            "SELECT * FROM translations WHERE id = ?", (trans_id,)
        ) as cur:
            row = await cur.fetchone()
            return dict(row) if row else None


async def clear_history(user_id: int) -> int:
    """Hapus semua histori user. Return jumlah yang dihapus."""
    async with aiosqlite.connect(DB_PATH) as db:
        cur = await db.execute(
            "DELETE FROM translations WHERE user_id = ?", (user_id,)
        )
        await db.commit()
        return cur.rowcount


async def get_user_stats(user_id: int) -> dict:
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row

        async with db.execute(
            """SELECT
                COUNT(*) as total,
                COALESCE(SUM(char_count), 0) as total_chars,
                COUNT(DISTINCT source_lang) as unique_source,
                COUNT(DISTINCT target_lang) as unique_target
               FROM translations WHERE user_id = ?""",
            (user_id,),
        ) as cur:
            stats = dict(await cur.fetchone())

        async with db.execute(
            """SELECT target_lang, COUNT(*) as cnt
               FROM translations WHERE user_id = ?
               GROUP BY target_lang ORDER BY cnt DESC LIMIT 5""",
            (user_id,),
        ) as cur:
            stats["top_targets"] = [dict(r) for r in await cur.fetchall()]

        async with db.execute(
            """SELECT source_lang, COUNT(*) as cnt
               FROM translations WHERE user_id = ?
               GROUP BY source_lang ORDER BY cnt DESC LIMIT 5""",
            (user_id,),
        ) as cur:
            stats["top_sources"] = [dict(r) for r in await cur.fetchall()]

    return stats
