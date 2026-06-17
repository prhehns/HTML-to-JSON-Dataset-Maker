"""Flask entry point for the HTML component labeling application.

The app serves a single-page labeling interface. Users paste HTML in the
browser, label each parsed DOM element with a UI-component category, and submit
those labels back to the server as JSON.
"""

import json

from flask import Flask, jsonify, render_template, request


app = Flask(__name__)

# Labels exposed as buttons in the browser UI. Keep this list aligned with the
# component taxonomy expected by downstream dataset consumers.
LABELS = [
    'Video', 'Carousel', 'DropdownMenu', 'CommentSection', 'Button', 'RatingSystem',
    'SearchBar', 'RadioButton', 'RangeSlider', 'Card', 'Icon', 'Slideshow', 'LogoImage',
    'Modal', 'Toast', 'ToggleSwitch', 'Sitemap', 'ImageGallery', 'InputField', 'Tab',
    'Accordion', 'Checkbox', 'Link', 'ChatBubble', 'NavigationBar', 'Table', 'IconButton',
    'Calendar', 'Header', 'FileUpload', 'Textarea', 'ProgressBar', 'Form', 'Pop-up', 'Footer',
    'LoadingSpinner', 'Sidebar', 'Badge', 'Hero'
]


@app.route('/')
def index():
    """Render the labeling page with all supported component labels."""
    return render_template('index.html', labels=LABELS)


@app.route('/submit', methods=['POST'])
def submit():
    """Persist submitted label records to ``labeled_data.json``.

    The browser posts an array of records in the shape ``{label, contents}``.
    This endpoint writes the payload exactly as submitted so the UI can be used
    for quick local dataset creation.
    """
    data = request.json
    with open('labeled_data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)
    return jsonify({"status": "success", "message": "Data saved."})


if __name__ == '__main__':
    app.run(debug=True)
