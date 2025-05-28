let elementList = [];
let currentIndex = 0;
let labelHistory = [];
let redoStack = [];

document.addEventListener('DOMContentLoaded', () => {
  document.getElementById('htmlInput').addEventListener('input', resetState);
  document.getElementById('nextBtn').addEventListener('click', showNextElement);
  document.getElementById('undoBtn').addEventListener('click', undo);
  document.getElementById('redoBtn').addEventListener('click', redo);
  document.getElementById('submitBtn').addEventListener('click', submitLabels);
});

function resetState() {
  elementList = [];
  currentIndex = 0;
  labelHistory = [];
  redoStack = [];
  document.getElementById('previewFrame').srcdoc = '';
}

function parseHTMLAndStart() {
  const html = document.getElementById('htmlInput').value;
  const doc = new DOMParser().parseFromString(html, 'text/html');
  elementList = Array.from(doc.body.querySelectorAll('*'));
  currentIndex = 0;
  showCurrentElement();
}

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
        <link href="https://cdn.tailwindcss.com" rel="stylesheet">
        <style> body { padding: 1rem; } </style>
      </head>
      <body>${wrapper.innerHTML}</body>
    </html>
  `;
}

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

function extractElementData(el) {
  return {
    type: el.tagName.toLowerCase(),
    attributes: Object.fromEntries([...el.attributes].map(attr => [attr.name, attr.value])),
    name: el.getAttribute('class') || el.tagName.toLowerCase(),
    children: [...el.children].map(c => extractElementData(c)),
    styles: getComputedStyleAsArray(el)
  };
}

function getComputedStyleAsArray(el) {
  return [
    `color: ${el.style.color || 'N/A'}`,
    `background-color: ${el.style.backgroundColor || 'N/A'}`,
    `font-size: ${el.style.fontSize || 'N/A'}`,
    `padding: ${el.style.padding || 'N/A'}`,
    `margin: ${el.style.margin || 'N/A'}`,
    `border: ${el.style.border || 'N/A'}`
  ];
}

function showNextElement() {
  currentIndex++;
  showCurrentElement();
}

function undo() {
  if (labelHistory.length === 0) return;
  const last = labelHistory.pop();
  redoStack.push(last);
  currentIndex--;
  showCurrentElement();
}

function redo() {
  if (redoStack.length === 0) return;
  const redoItem = redoStack.pop();
  labelHistory.push(redoItem);
  currentIndex++;
  showCurrentElement();
}

function submitLabels() {
  fetch('/submit', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(labelHistory)
  })
    .then(res => res.json())
    .then(data => alert("Submitted: " + data.message));
}
