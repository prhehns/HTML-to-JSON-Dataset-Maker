# HTML-to-JSON Dataset Maker

HTML-to-JSON Dataset Maker is a small Flask application and set of utility scripts for building labeled UI-component datasets from HTML. It helps you paste HTML, preview individual DOM elements, assign semantic component labels, and export the labeled result as JSON. The repository also includes scripts for augmenting existing records and generating synthetic Tailwind/DOM-like examples for less common UI labels.

## What this project produces

Dataset records use a simple schema:

```json
{
  "label": "Button",
  "contents": [
    {
      "type": "button",
      "attributes": { "class": "px-4 py-2 bg-blue-600" },
      "name": "px-4 py-2 bg-blue-600",
      "children": []
    }
  ]
}
```

Each record contains:

- `label`: the semantic UI component class.
- `contents`: one or more DOM-like element trees.
- Element nodes may include `type`, `attributes`, `name`, `children`, `styles`, and `text`, depending on the source or generator.

## Repository layout

```text
.
├── app.py                         # Flask app and JSON save endpoint
├── static/main.js                 # Browser-side HTML parsing, labeling, undo/redo, and submission
├── templates/index.html           # Labeling interface
├── dataset_augmenter.py           # Creates augmented JSON/JSONL from labeled_data2.json
├── datasetmakerv2.py              # Generates strict Tailwind-style samples for common UI labels
├── synth_uncommon.py              # Generates synthetic examples for uncommon UI labels
├── data/                          # Generated and augmented dataset files
├── labeled_data*.json             # Manually labeled source datasets
├── synthetic_ui_uncommon.json     # Root-level synthetic export
└── tailwind_labeled_data.json     # Tailwind-style generated export
```

## Requirements

- Python 3.9+
- Flask
- A modern browser
- Internet access in the browser if you want Tailwind CDN styles in the labeling UI and preview iframe

## Installation

Clone the repository, create a virtual environment, and install Flask:

```bash
git clone <repo-url>
cd HTML-to-JSON-Dataset-Maker
python -m venv .venv
source .venv/bin/activate
pip install flask
```

> This project currently does not include a `requirements.txt`; Flask is the only runtime package used by the web app.

## Running the labeling app

Start the Flask server:

```bash
python app.py
```

Then open the local URL shown by Flask, usually:

```text
http://127.0.0.1:5000/
```

### Labeling workflow

1. Paste HTML into the **HTML Input** textarea.
2. Click **Start Labeling**.
3. Review the current component in the preview pane.
4. Click one of the label buttons, such as `Button`, `Card`, `NavigationBar`, or `Modal`.
5. Use **Skip / Next** to move past an element without labeling it.
6. Use **Undo** and **Redo** to adjust recent label actions.
7. Click **Submit** to write the labeled records to `labeled_data.json`.

## Supported labels in the web app

The Flask app exposes these labels to the UI:

```text
Video, Carousel, DropdownMenu, CommentSection, Button, RatingSystem,
SearchBar, RadioButton, RangeSlider, Card, Icon, Slideshow, LogoImage,
Modal, Toast, ToggleSwitch, Sitemap, ImageGallery, InputField, Tab,
Accordion, Checkbox, Link, ChatBubble, NavigationBar, Table, IconButton,
Calendar, Header, FileUpload, Textarea, ProgressBar, Form, Pop-up, Footer,
LoadingSpinner, Sidebar, Badge, Hero
```

## Dataset generation scripts

### Augment an existing dataset

`dataset_augmenter.py` reads `labeled_data2.json`, creates one augmented variant for each original record, and writes:

- `data/labeled_data_augmented2.json`
- `data/labeled_data_augmented2.jsonl`

Run it with:

```bash
python dataset_augmenter.py
```

Augmentations include class shuffling, optional Tailwind utility additions/removals, placeholder image URL changes, link target metadata, button test IDs, and input placeholder/id variations.

### Generate strict Tailwind-style examples

`datasetmakerv2.py` generates many DOM-like Tailwind examples for labels such as `NavigationBar`, `Card`, `Table`, `SearchBar`, `ImageGallery`, `DropdownMenu`, and `Sidebar`.

Run it with:

```bash
python datasetmakerv2.py
```

It writes:

- `tailwind_labeled_data.json`

### Generate uncommon UI examples

`synth_uncommon.py` creates synthetic records for uncommon labels such as `Toast`, `LoadingSpinner`, `Modal`, `Hero`, `ProgressBar`, `ChatBubble`, `Calendar`, `FileUpload`, `RangeSlider`, `Badge`, and `Sitemap`.

Run it with:

```bash
python synth_uncommon.py
```

It writes:

- `data/synthetic_ui_uncommon.json`
- `data/synthetic_ui_uncommon.jsonl`

## JSON vs JSONL

- `.json` files store the complete dataset as one JSON array.
- `.jsonl` files store one JSON record per line, which is convenient for streaming, CLI tools, and many machine-learning data pipelines.

## Development notes

- The web app overwrites `labeled_data.json` when you submit from the UI.
- The browser preview iframe loads Tailwind through the CDN, so previews may look unstyled without network access.
- Generator scripts use fixed random seeds where reproducibility is helpful.
- `datasetmakerv2.py` intentionally keeps each generated node's `name` aligned with its `class` value.

## License

This project is licensed under the terms in [`LICENSE`](LICENSE).
