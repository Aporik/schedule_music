"""Register official RIOT MUSIC YouTube channel monitors for one Discord user."""

from __future__ import annotations

import argparse
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.integrations.youtube_channel_monitor import (  # noqa: E402
    create_riot_music_youtube_channel_monitors,
)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("discord_user_id")
    args = parser.parse_args()
    result = asyncio.run(
        create_riot_music_youtube_channel_monitors(
            discord_user_id=args.discord_user_id,
        )
    )
    print(
        {
            "requested": result["requested"],
            "registered": result["registered"],
            "failed": result["failed"],
        }
    )


if __name__ == "__main__":
    main()
