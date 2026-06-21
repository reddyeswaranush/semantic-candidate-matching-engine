import json
import os


STORAGE_FILE = (
    "storage/uploaded_candidates.json"
)


def create_storage():

    if not os.path.exists(
        STORAGE_FILE
    ):

        with open(
            STORAGE_FILE,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                [],
                f,
                indent=4
            )


def load_candidates():

    create_storage()

    with open(
        STORAGE_FILE,
        "r",
        encoding="utf-8"
    ) as f:

        return json.load(f)


def save_candidates(
    candidates
):

    with open(
        STORAGE_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            candidates,
            f,
            indent=4
        )


def add_candidates(
    new_candidates
):

    candidates = (
        load_candidates()
    )

    candidates.extend(
        new_candidates
    )

    save_candidates(
        candidates
    )

    return len(
        candidates
    )


def total_candidates():

    return len(
        load_candidates()
    )

def replace_candidates(candidates):

    save_candidates(
        candidates
    )