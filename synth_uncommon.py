# Full synthetic UI dataset generation for uncommon labels
# This generates realistic DOM-like trees for uncommon UI components
# and saves them as JSON and JSONL for training use.

import json
import random
from pathlib import Path

random.seed(1337)

OUT_JSON = Path("data/synthetic_ui_uncommon.json")
OUT_JSONL = Path("data/synthetic_ui_uncommon.jsonl")

UNCOMMON_LABELS = {
    "Toast": 400,
    "LoadingSpinner": 300,
    "Modal": 400,
    "Hero": 300,
    "ProgressBar": 300,
    "ChatBubble": 300,
    "Calendar": 200,
    "FileUpload": 200,
    "RangeSlider": 200,
    "Badge": 200,
    "Sitemap": 150
}

def cls(*names):
    return " ".join(names)

def text(options):
    return random.choice(options)

def synthetic(label):
    if label == "Toast":
        return {
            "label": "Toast",
            "contents": [{
                "type": "div",
                "attributes": {
                    "role": "status",
                    "aria-live": "polite",
                    "class": cls("toast", f"toast-{random.choice(['success','error','info','warning'])}", "fixed bottom-4 right-4")
                },
                "children": [
                    {"type":"span","text":text(["Saved successfully","Upload failed","Action completed"])},
                    {"type":"button","attributes":{"aria-label":"Close","class":"toast-close"}}
                ]
            }]
        }

    if label == "LoadingSpinner":
        return {
            "label": "LoadingSpinner",
            "contents": [{
                "type":"div",
                "attributes":{
                    "role":"status",
                    "aria-busy":"true",
                    "class":cls("spinner",random.choice(["sm","md","lg"]))
                },
                "children":[{"type":"span","text":"Loading..."}]
            }]
        }

    if label == "Modal":
        return {
            "label":"Modal",
            "contents":[{
                "type":"div",
                "attributes":{"class":"modal-backdrop"},
                "children":[{
                    "type":"section",
                    "attributes":{"role":"dialog","aria-modal":"true","class":"modal"},
                    "children":[
                        {"type":"header","children":[{"type":"h2","text":"Confirm action"}]},
                        {"type":"p","text":"Are you sure you want to continue?"},
                        {"type":"footer","children":[
                            {"type":"button","text":"Cancel"},
                            {"type":"button","text":"Confirm"}
                        ]}
                    ]
                }]
            }]
        }

    if label == "Hero":
        return {
            "label":"Hero",
            "contents":[{
                "type":"section",
                "attributes":{"class":"hero bg-cover"},
                "children":[
                    {"type":"h1","text":text(["Welcome","Discover More","Build Faster"])},
                    {"type":"p","text":"A short supporting tagline goes here."},
                    {"type":"button","text":"Get Started"}
                ]
            }]
        }

    if label == "ProgressBar":
        value = random.randint(10,90)
        return {
            "label":"ProgressBar",
            "contents":[{
                "type":"div",
                "attributes":{
                    "role":"progressbar",
                    "aria-valuemin":"0",
                    "aria-valuemax":"100",
                    "aria-valuenow":str(value),
                    "class":"progress"
                },
                "children":[{
                    "type":"div",
                    "attributes":{"class":"progress-fill","style":f"width:{value}%"}
                }]
            }]
        }

    if label == "ChatBubble":
        return {
            "label":"ChatBubble",
            "contents":[{
                "type":"div",
                "attributes":{"class":cls("chat-bubble",random.choice(["left","right"]))},
                "children":[
                    {"type":"span","text":text(["Hello!","Can you help me?","Sure, no problem."])},
                    {"type":"time","text":"10:42 AM"}
                ]
            }]
        }

    if label == "Calendar":
        return {
            "label":"Calendar",
            "contents":[{
                "type":"table",
                "attributes":{"class":"calendar"},
                "children":[{"type":"caption","text":"June 2025"}]
            }]
        }

    if label == "FileUpload":
        return {
            "label":"FileUpload",
            "contents":[{
                "type":"input",
                "attributes":{
                    "type":"file",
                    "accept":random.choice([".png,.jpg","application/pdf"]),
                    "class":"file-input"
                }
            }]
        }

    if label == "RangeSlider":
        return {
            "label":"RangeSlider",
            "contents":[{
                "type":"input",
                "attributes":{
                    "type":"range",
                    "min":"0",
                    "max":"100",
                    "value":str(random.randint(20,80)),
                    "class":"slider"
                }
            }]
        }

    if label == "Badge":
        return {
            "label":"Badge",
            "contents":[{
                "type":"span",
                "attributes":{"class":cls("badge",random.choice(["primary","secondary","success"]))},
                "text":random.choice(["New","Beta","99+"])
            }]
        }

    if label == "Sitemap":
        return {
            "label":"Sitemap",
            "contents":[{
                "type":"ul",
                "children":[
                    {"type":"li","text":"Home"},
                    {"type":"li","text":"Products"},
                    {"type":"li","text":"Contact"}
                ]
            }]
        }

records = []

for label, count in UNCOMMON_LABELS.items():
    for _ in range(count):
        records.append(synthetic(label))

with OUT_JSON.open("w",encoding="utf-8") as f:
    json.dump(records,f,indent=2)

with OUT_JSONL.open("w",encoding="utf-8") as f:
    for r in records:
        f.write(json.dumps(r)+"\n")

(len(records), OUT_JSON.resolve(), OUT_JSONL.resolve())
