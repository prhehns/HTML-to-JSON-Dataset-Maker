// Parsed DOM elements awaiting review in the labeling workflow.
let elementList = [];
let currentIndex = 0;
let labelHistory = [];
let redoStack = [];

// Wire UI controls after the labeling page has loaded.
document.addEventListener('DOMContentLoaded', () => {
  document.getElementById('htmlInput').addEventListener('input', resetState);
  document.getElementById('nextBtn').addEventListener('click', showNextElement);
  document.getElementById('undoBtn').addEventListener('click', undo);
  document.getElementById('redoBtn').addEventListener('click', redo);
  document.getElementById('submitBtn').addEventListener('click', submitLabels);
});

/** Reset in-memory labeling progress whenever the source HTML changes. */
function resetState() {
  elementList = [];
  currentIndex = 0;
  labelHistory = [];
  redoStack = [];
  document.getElementById('previewFrame').srcdoc = '';
}

/** Parse textarea HTML and begin reviewing each element in document order. */
function parseHTMLAndStart() {
  const html = document.getElementById('htmlInput').value;
  const doc = new DOMParser().parseFromString(html, 'text/html');
  elementList = Array.from(doc.body.querySelectorAll('*'));
  currentIndex = 0;
  showCurrentElement();
}

/** Render the current element in an isolated iframe preview. */
function showCurrentElement() {
  if (currentIndex >= elementList.length) {
    alert("All components labeled.");
    return;
  }

  const el = elementList[currentIndex];
  const wrapper = document.createElement('div');
  wrapper.appendChild(el.cloneNode(true));

  const previewFrame = document.getElementById('previewFrame');
  previewFrame.srcdoc = `
    <html>
      <head>
        <script src="https://cdn.tailwindcss.com"></script>
        <style>body { padding: 1rem; }</style>
      </head>
      <body class="bg-white">
        ${wrapper.innerHTML}
      </body>
    </html>
  `;
}


/** Save the selected label for the current element and advance the cursor. */
function assignLabel(label) {
  if (!label || currentIndex >= elementList.length) return;

  const el = elementList[currentIndex];
  const data = {
    label: label,
    contents: [extractElementData(el.cloneNode(true))]
  };

  labelHistory.push(data);
  redoStack = [];
  currentIndex++;
  showCurrentElement();
}

/** Convert a live DOM element into the dataset's serializable node shape. */
function extractElementData(el) {
  const attributes = Object.fromEntries(
    [...el.attributes].filter(attr => attr.value && attr.value !== 'null' && attr.value !== 'undefined')
                     .map(attr => [attr.name, attr.value])
  );

  const styles = getComputedStyleAsArray(el).filter(
    style => style && !style.includes('N/A') && !style.includes('undefined') && !style.includes('null')
  );

  const children = [...el.children].map(c => extractElementData(c)).filter(Boolean);

  return {
    type: el.tagName.toLowerCase(),
    ...(Object.keys(attributes).length && { attributes }),
    name: el.getAttribute('class') || el.tagName.toLowerCase(),
    ...(children.length && { children }),
    ...(styles.length && { styles })
  };
}


/** Capture a compact subset of computed styles that may help model training. */
function getComputedStyleAsArray(el) {
  const styles = [];

  const style = window.getComputedStyle(el);
  const props = ['color', 'background-color', 'font-size', 'padding', 'margin', 'border'];

  props.forEach(prop => {
    const val = style.getPropertyValue(prop);
    if (val && val.trim() && val !== 'N/A' && val !== 'none') {
      styles.push(`${prop}: ${val.trim()}`);
    }
  });

  return styles;
}


/** Skip the current element without adding a labeled record. */
function showNextElement() {
  currentIndex++;
  showCurrentElement();
}

/** Remove the most recent label assignment and revisit that element. */
function undo() {
  if (labelHistory.length === 0) return;
  const last = labelHistory.pop();
  redoStack.push(last);
  currentIndex--;
  showCurrentElement();
}

/** Reapply the most recently undone label assignment. */
function redo() {
  if (redoStack.length === 0) return;
  const redoItem = redoStack.pop();
  labelHistory.push(redoItem);
  currentIndex++;
  showCurrentElement();
}

/** Send all labeled records to Flask for persistence as JSON. */
function submitLabels() {
  fetch('/submit', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(labelHistory)
  })
    .then(res => res.json())
    .then(data => alert("Submitted: " + data.message));
}
