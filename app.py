from flask import Flask, render_template, request, jsonify
import json

app = Flask(__name__)
LABELS = ['Video', 'Carousel', 'DropdownMenu', 'CommentSection', 'Button', 'RatingSystem',
          'SearchBar', 'RadioButton', 'RangeSlider', 'Card', 'Icon', 'Slideshow', 'LogoImage',
          'Modal', 'Toast', 'ToggleSwitch', 'Sitemap', 'ImageGallery', 'InputField', 'Tab',
          'Accordion', 'Checkbox', 'Link', 'ChatBubble', 'NavigationBar', 'Table', 'IconButton',
          'Calendar', 'Header', 'FileUpload', 'Textarea', 'ProgressBar', 'Form', 'Pop-up', 'Footer',
          'LoadingSpinner', 'Sidebar', 'Badge', 'Hero']

@app.route('/')
def index():
    return render_template('index.html', labels=LABELS)

@app.route('/submit', methods=['POST'])
def submit():
    data = request.json
    with open('labeled_data.json', 'w') as f:
        json.dump(data, f, indent=2)
    return jsonify({"status": "success", "message": "Data saved."})

if __name__ == '__main__':
    app.run(debug=True)
