from app.core.db import RIOT_MUSIC_X_SOURCES, RIOT_MUSIC_YOUTUBE_CHANNELS, VTUBER_X_SOURCES


def test_requested_vtuber_x_sources_are_seeded() -> None:
    assert VTUBER_X_SOURCES == (
        ("MOCO", "hth_moco"),
        ("BAMBI", "hth_bambi"),
        ("SAKUYA", "NUROJUNK_SAKUYA"),
        ("KAGURA", "NJ_KAGURA"),
        ("Enma_Ruri", "Ruri_Enma"),
        ("Setono_Toto", "setono_toto1010"),
        ("Setono_Toto", "setono_toto_sub"),
        ("Minase_Nagi", "minase_nagi7"),
    )


def test_riot_music_official_artist_sources_are_seeded() -> None:
    assert RIOT_MUSIC_X_SOURCES == (
        ("IORI MATSUNAGA", "iori_m_RIOT"),
        ("ANKO ASAKURA", "anko_a_RIOT"),
        ("MIONA SUMERAGI", "miona_s_RIOT"),
        ("CHISE ITSUKI", "chise_i_BW"),
        ("SHIRASE SHIRAKAWA", "shirase_s_BW"),
        ("RANZE TOKINIWA", "ranze_t_BW"),
        ("MINAMI IZUMI", "minami_i_MGS"),
        ("SHUNA", "shuna_MGS"),
        ("MEMENTOVANITAS", "memento_v_MGS"),
        ("DENSHINBASHIRA-CHAN", "denchan_MGS"),
        ("LECIEL MIYAJIMA", "leciel_m_MGS"),
        ("KUGURU KASAYA", "kuguru_k_MGS"),
    )


def test_riot_music_youtube_channels_are_available_for_bulk_monitoring() -> None:
    assert len(RIOT_MUSIC_YOUTUBE_CHANNELS) == len(RIOT_MUSIC_X_SOURCES)
    assert RIOT_MUSIC_YOUTUBE_CHANNELS[0] == (
        "IORI MATSUNAGA",
        "https://www.youtube.com/channel/UC--zuEfONeFXPvLqX0Kvbuw",
    )
    assert RIOT_MUSIC_YOUTUBE_CHANNELS[-1] == (
        "KUGURU KASAYA",
        "https://www.youtube.com/@KUGURUKASAYA",
    )
