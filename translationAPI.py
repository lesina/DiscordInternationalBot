DEFAULT = "default"
EN = "en"
DE = "de"
RU = "ru"

DEFAULT_ID = 653652629515272195
EN_ID = 658221821119954945
DE_ID = 658224926318264321
RU_ID = 747738427662925865

allowed_languages = [
    DEFAULT,
    RU,
    EN,
    DE,
]

language_to_channel_id = {
    RU: RU_ID,
    EN: EN_ID,
    DE: DE_ID,
    DEFAULT: DEFAULT_ID,
}

channel_id_to_language = dict([(value, key) for key, value in language_to_channel_id.items()]) 