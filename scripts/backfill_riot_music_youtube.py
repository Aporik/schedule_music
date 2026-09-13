"""Run an idempotent historical RIOT MUSIC utawaku archive backfill."""

from __future__ import annotations

import argparse
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.core.db import RIOT_MUSIC_YOUTUBE_CHANNELS  # noqa: E402
from app.integrations.youtube_channel_monitor import backfill_youtube_channel  # noqa: E402


async def backfill_all(*, max_videos_per_channel: int | None, concurrency: int) -> dict:
    totals = {
        "channels_checked": 0,
        "videos_found": 0,
        "archives_saved": 0,
        "setlists_found": 0,
        "failed": 0,
    }
    channels = []
    for artist_name, channel_url in RIOT_MUSIC_YOUTUBE_CHANNELS:
        print(f"Starting {artist_name}...", flush=True)
        try:
            result = await backfill_youtube_channel(
                channel_url=channel_url,
                artist_name=artist_name,
                max_videos=max_videos_per_channel,
                concurrency=concurrency,
            )
            totals["channels_checked"] += 1
            for key in ("videos_found", "archives_saved", "setlists_found", "failed"):
                totals[key] += int(result[key])
            row = {"artist_name": artist_name, **result}
        except Exception as exc:
            totals["failed"] += 1
            row = {"artist_name": artist_name, "error": str(exc)}
        channels.append(row)
        print(row, flush=True)
    return {**totals, "channels": channels}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-videos-per-channel", type=int)
    parser.add_argument("--concurrency", type=int, default=3)
    args = parser.parse_args()
    result = asyncio.run(
        backfill_all(
            max_videos_per_channel=args.max_videos_per_channel,
            concurrency=args.concurrency,
        )
    )
    print(result)


if __name__ == "__main__":
    main()
