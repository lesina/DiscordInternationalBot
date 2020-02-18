RU = "ru"
EN = "en"
DE = "de"

RU_ID = 653652629515272195
EN_ID = 658221821119954945
DE_ID = 658224926318264321

allowed_languages = [
    RU,
    EN,
    DE,
]

language_to_channel_id = {
    RU: RU_ID,
    EN: EN_ID,
    DE: DE_ID,
}

channel_id_to_language = dict([(value, key) for key, value in language_to_channel_id.items()]) 