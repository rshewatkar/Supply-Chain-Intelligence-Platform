from app.utils.file_utils import (
    file_exists,
    load_json,
    save_json,
)

sample = {
    "company": "AMD",
    "country": "USA",
}

save_json(sample, "temp/test.json")

loaded = load_json("temp/test.json")

assert loaded["company"] == "AMD"

assert file_exists("temp/test.json")

print("All file utility tests passed.")