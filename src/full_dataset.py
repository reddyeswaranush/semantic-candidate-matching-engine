import json

from rec.src.config import CANDIDATES_FILE


def load_candidates(limit=None):

    candidates = []

    with open(
        CANDIDATES_FILE,
        "r",
        encoding="utf-8"
    ) as f:

        for line_num, line in enumerate(f):

            candidates.append(
                json.loads(line)
            )

            if (
                limit is not None
                and len(candidates) >= limit
            ):
                break

    return candidates


if __name__ == "__main__":

    candidates = load_candidates(
        limit=None
    )

    print(
        f"Total Candidates: {len(candidates)}"
    )