# ─── 134 BAHASA YANG DIDUKUNG GOOGLE TRANSLATE ───────────────────────────────
# Format: code → {name (dalam Bahasa Indonesia), native (nama asli), flag}

LANGUAGES: dict[str, dict] = {
    "af":       {"name": "Afrikaans",              "native": "Afrikaans",             "flag": "🇿🇦"},
    "sq":       {"name": "Albania",                "native": "Shqip",                 "flag": "🇦🇱"},
    "am":       {"name": "Amharik",                "native": "አማርኛ",                  "flag": "🇪🇹"},
    "ar":       {"name": "Arab",                   "native": "العربية",               "flag": "🇸🇦"},
    "hy":       {"name": "Armenia",                "native": "Հայerեն",               "flag": "🇦🇲"},
    "as":       {"name": "Assam",                  "native": "অসমীয়া",               "flag": "🇮🇳"},
    "ay":       {"name": "Aymara",                 "native": "Aymar aru",             "flag": "🇧🇴"},
    "az":       {"name": "Azerbaijan",             "native": "Azərbaycan",            "flag": "🇦🇿"},
    "bm":       {"name": "Bambara",                "native": "Bamanankan",            "flag": "🇲🇱"},
    "eu":       {"name": "Basque",                 "native": "Euskara",               "flag": "🏴"},
    "be":       {"name": "Belarusia",              "native": "Беларуская",            "flag": "🇧🇾"},
    "bn":       {"name": "Bengali",                "native": "বাংলা",                 "flag": "🇧🇩"},
    "bho":      {"name": "Bhojpuri",               "native": "भोजपुरी",              "flag": "🇮🇳"},
    "bs":       {"name": "Bosnia",                 "native": "Bosanski",              "flag": "🇧🇦"},
    "bg":       {"name": "Bulgaria",               "native": "Български",             "flag": "🇧🇬"},
    "ca":       {"name": "Katalan",                "native": "Català",                "flag": "🏴"},
    "ceb":      {"name": "Cebuano",                "native": "Cebuano",               "flag": "🇵🇭"},
    "zh-CN":    {"name": "Cina (Sederhana)",        "native": "中文(简体)",            "flag": "🇨🇳"},
    "zh-TW":    {"name": "Cina (Tradisional)",      "native": "中文(繁體)",            "flag": "🇹🇼"},
    "co":       {"name": "Korsika",                "native": "Corsu",                 "flag": "🇫🇷"},
    "hr":       {"name": "Kroasia",                "native": "Hrvatski",              "flag": "🇭🇷"},
    "cs":       {"name": "Ceko",                   "native": "Čeština",              "flag": "🇨🇿"},
    "da":       {"name": "Denmark",                "native": "Dansk",                 "flag": "🇩🇰"},
    "dv":       {"name": "Divehi",                 "native": "ދިވެހި",                "flag": "🇲🇻"},
    "doi":      {"name": "Dogri",                  "native": "डोगरी",                 "flag": "🇮🇳"},
    "nl":       {"name": "Belanda",                "native": "Nederlands",            "flag": "🇳🇱"},
    "en":       {"name": "Inggris",                "native": "English",               "flag": "🇬🇧"},
    "eo":       {"name": "Esperanto",              "native": "Esperanto",             "flag": "🌐"},
    "et":       {"name": "Estonia",                "native": "Eesti",                 "flag": "🇪🇪"},
    "ee":       {"name": "Ewe",                    "native": "Eʋegbe",               "flag": "🇬🇭"},
    "fil":      {"name": "Filipino",               "native": "Filipino",              "flag": "🇵🇭"},
    "fi":       {"name": "Finlandia",              "native": "Suomi",                 "flag": "🇫🇮"},
    "fr":       {"name": "Prancis",                "native": "Français",             "flag": "🇫🇷"},
    "fy":       {"name": "Frisian Barat",          "native": "Frysk",                "flag": "🇳🇱"},
    "gl":       {"name": "Galisia",                "native": "Galego",                "flag": "🇪🇸"},
    "ka":       {"name": "Georgia",                "native": "ქართული",               "flag": "🇬🇪"},
    "de":       {"name": "Jerman",                 "native": "Deutsch",               "flag": "🇩🇪"},
    "el":       {"name": "Yunani",                 "native": "Ελληνικά",             "flag": "🇬🇷"},
    "gn":       {"name": "Guarani",                "native": "Guaraní",              "flag": "🇵🇾"},
    "gu":       {"name": "Gujarati",               "native": "ગુજરાતી",               "flag": "🇮🇳"},
    "ht":       {"name": "Kreol Haiti",            "native": "Kreyòl Ayisyen",       "flag": "🇭🇹"},
    "ha":       {"name": "Hausa",                  "native": "Hausa",                 "flag": "🇳🇬"},
    "haw":      {"name": "Hawaii",                 "native": "ʻŌlelo Hawaiʻi",       "flag": "🌺"},
    "iw":       {"name": "Ibrani",                 "native": "עברית",                "flag": "🇮🇱"},
    "hi":       {"name": "Hindi",                  "native": "हिन्दी",                "flag": "🇮🇳"},
    "hmn":      {"name": "Hmong",                  "native": "Hmong",                 "flag": "🏔️"},
    "hu":       {"name": "Hungaria",               "native": "Magyar",                "flag": "🇭🇺"},
    "is":       {"name": "Islandia",               "native": "Íslenska",             "flag": "🇮🇸"},
    "ig":       {"name": "Igbo",                   "native": "Igbo",                  "flag": "🇳🇬"},
    "ilo":      {"name": "Ilocano",                "native": "Ilocano",               "flag": "🇵🇭"},
    "id":       {"name": "Indonesia",              "native": "Bahasa Indonesia",      "flag": "🇮🇩"},
    "ga":       {"name": "Irlandia",               "native": "Gaeilge",               "flag": "🇮🇪"},
    "it":       {"name": "Italia",                 "native": "Italiano",              "flag": "🇮🇹"},
    "ja":       {"name": "Jepang",                 "native": "日本語",                "flag": "🇯🇵"},
    "jv":       {"name": "Jawa",                   "native": "Basa Jawa",             "flag": "🇮🇩"},
    "kn":       {"name": "Kannada",                "native": "ಕನ್ನಡ",                "flag": "🇮🇳"},
    "kk":       {"name": "Kazakh",                 "native": "Қазақ",                 "flag": "🇰🇿"},
    "km":       {"name": "Khmer",                  "native": "ភាសាខ្មែរ",             "flag": "🇰🇭"},
    "rw":       {"name": "Kinyarwanda",            "native": "Kinyarwanda",           "flag": "🇷🇼"},
    "gom":      {"name": "Konkani",                "native": "कोंकणी",                "flag": "🇮🇳"},
    "ko":       {"name": "Korea",                  "native": "한국어",                 "flag": "🇰🇷"},
    "kri":      {"name": "Krio",                   "native": "Krio",                  "flag": "🇸🇱"},
    "ku":       {"name": "Kurdi (Kurmanji)",        "native": "Kurdî",                "flag": "🏳️"},
    "ckb":      {"name": "Kurdi (Sorani)",          "native": "کوردی",                "flag": "🏳️"},
    "ky":       {"name": "Kirgiz",                 "native": "Кыргызча",             "flag": "🇰🇬"},
    "lo":       {"name": "Laos",                   "native": "ລາວ",                   "flag": "🇱🇦"},
    "la":       {"name": "Latin",                  "native": "Latina",                "flag": "🏛️"},
    "lv":       {"name": "Latvia",                 "native": "Latviešu",             "flag": "🇱🇻"},
    "ln":       {"name": "Lingala",                "native": "Lingála",              "flag": "🇨🇩"},
    "lt":       {"name": "Lituania",               "native": "Lietuvių",             "flag": "🇱🇹"},
    "lg":       {"name": "Luganda",                "native": "Luganda",               "flag": "🇺🇬"},
    "lb":       {"name": "Luksemburg",             "native": "Lëtzebuergesch",       "flag": "🇱🇺"},
    "mk":       {"name": "Makedonia",              "native": "Македонски",           "flag": "🇲🇰"},
    "mai":      {"name": "Maithili",               "native": "मैथिली",                "flag": "🇮🇳"},
    "mg":       {"name": "Malagasi",               "native": "Malagasy",              "flag": "🇲🇬"},
    "ms":       {"name": "Melayu",                 "native": "Bahasa Melayu",         "flag": "🇲🇾"},
    "ml":       {"name": "Malayalam",              "native": "മലയാളം",                "flag": "🇮🇳"},
    "mt":       {"name": "Malta",                  "native": "Malti",                 "flag": "🇲🇹"},
    "mi":       {"name": "Maori",                  "native": "Māori",                "flag": "🇳🇿"},
    "mr":       {"name": "Marathi",                "native": "मराठी",                 "flag": "🇮🇳"},
    "mni-Mtei": {"name": "Meitei (Manipuri)",      "native": "ꯃꯤꯇꯩ",                "flag": "🇮🇳"},
    "lus":      {"name": "Mizo",                   "native": "Mizo tawng",            "flag": "🇮🇳"},
    "mn":       {"name": "Mongolia",               "native": "Монгол",                "flag": "🇲🇳"},
    "my":       {"name": "Myanmar",                "native": "မြန်မာဘာသာ",            "flag": "🇲🇲"},
    "ne":       {"name": "Nepal",                  "native": "नेपाली",                "flag": "🇳🇵"},
    "nso":      {"name": "Sepedi",                 "native": "Sesotho sa Leboa",      "flag": "🇿🇦"},
    "no":       {"name": "Norwegia",               "native": "Norsk",                 "flag": "🇳🇴"},
    "ny":       {"name": "Nyanja (Chichewa)",       "native": "Nyanja",               "flag": "🇲🇼"},
    "or":       {"name": "Odia (Oriya)",           "native": "ଓଡ଼ିଆ",                "flag": "🇮🇳"},
    "om":       {"name": "Oromo",                  "native": "Afaan Oromo",           "flag": "🇪🇹"},
    "ps":       {"name": "Pashto",                 "native": "پښتو",                  "flag": "🇦🇫"},
    "fa":       {"name": "Persia",                 "native": "فارسی",                "flag": "🇮🇷"},
    "pl":       {"name": "Polandia",               "native": "Polski",                "flag": "🇵🇱"},
    "pt":       {"name": "Portugis",               "native": "Português",            "flag": "🇵🇹"},
    "pa":       {"name": "Punjabi",                "native": "ਪੰਜਾਬੀ",               "flag": "🇮🇳"},
    "qu":       {"name": "Quechua",                "native": "Quechua",               "flag": "🇵🇪"},
    "ro":       {"name": "Rumania",                "native": "Română",               "flag": "🇷🇴"},
    "ru":       {"name": "Rusia",                  "native": "Русский",              "flag": "🇷🇺"},
    "sm":       {"name": "Samoa",                  "native": "Gagana Sāmoa",         "flag": "🇼🇸"},
    "sa":       {"name": "Sansekerta",             "native": "संस्कृत",               "flag": "📜"},
    "gd":       {"name": "Gaelik Skotlandia",      "native": "Gàidhlig",             "flag": "🏴󠁧󠁢󠁳󠁣󠁴󠁿"},
    "sr":       {"name": "Serbia",                 "native": "Српски",               "flag": "🇷🇸"},
    "st":       {"name": "Sesotho",                "native": "Sesotho",               "flag": "🇱🇸"},
    "sn":       {"name": "Shona",                  "native": "chiShona",              "flag": "🇿🇼"},
    "sd":       {"name": "Sindhi",                 "native": "سنڌي",                  "flag": "🇵🇰"},
    "si":       {"name": "Sinhala",                "native": "සිංහල",                 "flag": "🇱🇰"},
    "sk":       {"name": "Slowakia",               "native": "Slovenčina",           "flag": "🇸🇰"},
    "sl":       {"name": "Slovenia",               "native": "Slovenščina",          "flag": "🇸🇮"},
    "so":       {"name": "Somalia",                "native": "Soomaali",              "flag": "🇸🇴"},
    "es":       {"name": "Spanyol",                "native": "Español",              "flag": "🇪🇸"},
    "su":       {"name": "Sunda",                  "native": "Basa Sunda",            "flag": "🇮🇩"},
    "sw":       {"name": "Swahili",                "native": "Kiswahili",             "flag": "🇹🇿"},
    "sv":       {"name": "Swedia",                 "native": "Svenska",               "flag": "🇸🇪"},
    "tg":       {"name": "Tajik",                  "native": "Тоҷикӣ",               "flag": "🇹🇯"},
    "ta":       {"name": "Tamil",                  "native": "தமிழ்",                 "flag": "🇮🇳"},
    "tt":       {"name": "Tatar",                  "native": "Татар",                 "flag": "🇷🇺"},
    "te":       {"name": "Telugu",                 "native": "తెలుగు",                "flag": "🇮🇳"},
    "th":       {"name": "Thailand",               "native": "ภาษาไทย",               "flag": "🇹🇭"},
    "ti":       {"name": "Tigrinya",               "native": "ትግርኛ",                  "flag": "🇪🇷"},
    "ts":       {"name": "Tsonga",                 "native": "Xitsonga",              "flag": "🇿🇦"},
    "tr":       {"name": "Turki",                  "native": "Türkçe",               "flag": "🇹🇷"},
    "tk":       {"name": "Turkmen",                "native": "Türkmen",              "flag": "🇹🇲"},
    "ak":       {"name": "Twi (Akan)",             "native": "Twi",                   "flag": "🇬🇭"},
    "uk":       {"name": "Ukraina",                "native": "Українська",           "flag": "🇺🇦"},
    "ur":       {"name": "Urdu",                   "native": "اردو",                  "flag": "🇵🇰"},
    "ug":       {"name": "Uyghur",                 "native": "ئۇيغۇرچە",             "flag": "🇨🇳"},
    "uz":       {"name": "Uzbek",                  "native": "O'zbek",               "flag": "🇺🇿"},
    "vi":       {"name": "Vietnam",                "native": "Tiếng Việt",           "flag": "🇻🇳"},
    "cy":       {"name": "Wales",                  "native": "Cymraeg",               "flag": "🏴󠁧󠁢󠁷󠁬󠁳󠁿"},
    "xh":       {"name": "Xhosa",                  "native": "isiXhosa",              "flag": "🇿🇦"},
    "yi":       {"name": "Yiddish",                "native": "ייִדיש",               "flag": "✡️"},
    "yo":       {"name": "Yoruba",                 "native": "Yorùbá",               "flag": "🇳🇬"},
    "zu":       {"name": "Zulu",                   "native": "isiZulu",               "flag": "🇿🇦"},
}

# Alias untuk kode lama / alternatif → kode yang dipakai
LANG_ALIASES: dict[str, str] = {
    "he": "iw",     # Hebrew (kode lama)
    "zh": "zh-CN",  # Chinese default ke Simplified
    "jw": "jv",     # Javanese (kode lama)
    "tl": "fil",    # Tagalog → Filipino
    "nb": "no",     # Norwegian Bokmål
    "in": "id",     # Indonesian (kode lama)
}

# Bahasa populer untuk quick-select
POPULAR_LANGS = [
    "id", "en", "ar", "ja", "ko",
    "zh-CN", "zh-TW", "de", "fr", "es",
    "ru", "pt", "hi", "tr", "vi",
    "th", "ms", "it", "nl", "sv",
]

# Bahasa yang punya script non-Latin (untuk info transliterasi)
NON_LATIN_LANGS = {
    "ar", "he", "iw", "hi", "bn", "ta", "te", "ml", "kn", "gu", "pa",
    "ja", "ko", "zh-CN", "zh-TW", "th", "my", "km", "lo", "si",
    "ka", "am", "ti", "mk", "sr", "bg", "ru", "uk", "be",
    "mn", "ne", "mr", "ur", "fa", "ps", "ug",
}


def get_lang_name(code: str) -> str:
    code = LANG_ALIASES.get(code, code)
    lang = LANGUAGES.get(code)
    return lang["name"] if lang else code.upper()


def get_lang_native(code: str) -> str:
    code = LANG_ALIASES.get(code, code)
    lang = LANGUAGES.get(code)
    return lang.get("native", "") if lang else ""


def get_lang_flag(code: str) -> str:
    code = LANG_ALIASES.get(code, code)
    lang = LANGUAGES.get(code)
    return lang["flag"] if lang else "🌐"


def is_valid_lang(code: str) -> bool:
    code = LANG_ALIASES.get(code, code)
    return code in LANGUAGES


def normalize_lang(code: str) -> str:
    """Normalize/resolve alias ke canonical code."""
    return LANG_ALIASES.get(code.lower(), code.lower())


def search_langs(query: str) -> list[tuple[str, dict]]:
    """Cari bahasa berdasarkan nama (Indo atau native). Return list (code, info)."""
    q = query.lower().strip()
    results = []
    for code, info in LANGUAGES.items():
        if (q in info["name"].lower() or
                q in info.get("native", "").lower() or
                q == code.lower()):
            results.append((code, info))
    return results[:15]  # Maks 15 hasil
