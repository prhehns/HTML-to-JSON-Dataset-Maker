"""Create schema-pure augmented UI component datasets.

The script reads manually labeled records from ``labeled_data2.json`` and writes
both JSON and JSONL outputs under ``data/``. For every original record it keeps a
copy of the original and creates one lightly mutated variant. Mutations preserve
the high-level ``{label, contents}`` schema while adding variety to classes,
URLs, form metadata, and selected attributes.
"""

import copy
import json
import random
from pathlib import Path


random.seed(42)

IN = Path("labeled_data2.json")
OUT_JSON = Path("data/labeled_data_augmented2.json")
OUT_JSONL = Path("data/labeled_data_augmented2.jsonl")

TAILWIND_ADDITIONS = [
    "mt-1", "mt-2", "mb-2", "p-1", "p-2", "px-2", "py-1", "rounded", "shadow",
    "bg-gray-50", "bg-white", "text-sm", "text-lg", "font-semibold", "w-full",
]


def shuffle_classes(class_str):
    """Return the same CSS class tokens in random order."""
    parts = class_str.split()
    random.shuffle(parts)
    return " ".join(parts)


def tweak_class(class_val):
    """Apply small randomized Tailwind-style changes to a class string."""
    if not class_val:
        return class_val
    if random.random() < 0.5:
        class_val = shuffle_classes(class_val)
    if random.random() < 0.3:
        add = random.choice(TAILWIND_ADDITIONS)
        if add not in class_val.split():
            class_val = class_val + " " + add
    tokens = class_val.split()
    if len(tokens) > 1 and random.random() < 0.15:
        tokens.pop(random.randrange(len(tokens)))
        class_val = " ".join(tokens)
    return class_val


def augment_node(node, path=""):
    """Recursively augment a DOM-like node while preserving dataset shape."""
    node = copy.deepcopy(node)

    if "attributes" in node and isinstance(node["attributes"], dict):
        attrs = node["attributes"]

        if "class" in attrs and isinstance(attrs["class"], str):
            attrs["class"] = tweak_class(attrs["class"])

        if node.get("type") == "img" and "src" in attrs and isinstance(attrs["src"], str):
            if "placeholder.com" in attrs["src"]:
                size = random.choice(["120", "150", "200", "300", "400"])
                attrs["src"] = f"https://via.placeholder.com/{size}"
            else:
                attrs["src"] = attrs["src"] + ("?v=2" if "?" not in attrs["src"] else "&v=2")

        if node.get("type") == "a" and random.random() < 0.4:
            attrs["target"] = "_blank"
            attrs["rel"] = "noopener noreferrer"

        if node.get("type") == "button" and random.random() < 0.5:
            attrs["data-test-id"] = f"btn-{abs(hash(path)) % 10000}"

        if node.get("type") in ("input", "textarea"):
            if "placeholder" in attrs and isinstance(attrs["placeholder"], str) and random.random() < 0.6:
                if not attrs["placeholder"].endswith("..."):
                    attrs["placeholder"] += "..."
            if node.get("type") == "input" and random.random() < 0.3:
                attrs["id"] = f"input-{abs(hash(path)) % 10000}"

    if "name" in node and isinstance(node["name"], str) and random.random() < 0.25:
        node["name"] = node["name"] + " " + random.choice(["alt", "v2", "mod"])

    if "children" in node and isinstance(node["children"], list):
        node["children"] = [
            augment_node(ch, path + f"/{node.get('type', '')}-{i}")
            for i, ch in enumerate(node["children"])
        ]

    return node


def main():
    """Load source records, create augmented records, and write both outputs."""
    with IN.open("r", encoding="utf-8") as f:
        data = json.load(f)

    clean_augmented = []

    for rec in data:
        clean_augmented.append(copy.deepcopy(rec))

        aug = copy.deepcopy(rec)
        if isinstance(aug.get("contents"), list):
            aug["contents"] = [
                augment_node(item, path=f"/root-{i}")
                for i, item in enumerate(aug["contents"])
            ]
        clean_augmented.append(aug)

    with OUT_JSON.open("w", encoding="utf-8") as f:
        json.dump(clean_augmented, f, ensure_ascii=False, indent=2)

    with OUT_JSONL.open("w", encoding="utf-8") as f:
        for r in clean_augmented:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

    print(len(data), len(clean_augmented), OUT_JSON.resolve(), OUT_JSONL.resolve())


if __name__ == "__main__":
    main()
