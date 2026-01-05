import json
import random


class UIStrictAugmenter:
    def __init__(self):
        self.labels = [
            'DropdownMenu', 'SearchBar', 'RangeSlider', 'Card',
            'ImageGallery', 'Link', 'NavigationBar', 'Table',
            'IconButton', 'Header', 'Footer', 'Sidebar'
        ]
        self.colors = ["white", "gray-50", "slate-800", "blue-600", "red-500"]
        self.shadows = ["shadow-sm", "shadow", "shadow-lg", "shadow-xl", ""]
        self.rounding = ["rounded-none", "rounded", "rounded-md", "rounded-lg", "rounded-full"]

    def _create_node(self, tag, class_list, children=None):
        """Helper to ensure 'name' always matches 'class' exactly."""
        class_str = " ".join(filter(None, class_list))
        node = {
            "type": tag,
            "attributes": {"class": class_str},
            "name": class_str
        }
        if children:
            node["children"] = children
        return node

    def generate_component(self, label):
        """Generates dynamic variety for specific labels using Tailwind conventions."""

        if label == 'NavigationBar':
            links = [self._create_node('a', [f"text-{random.choice(['blue-500', 'gray-600'])}", "hover:underline"]) for
                     _ in range(random.randint(2, 5))]
            nav = self._create_node('nav', ["flex space-x-6"], links)
            return self._create_node('header',
                                     ["w-full flex items-center justify-between p-4", random.choice(self.colors),
                                      random.choice(self.shadows)], [
                                         self._create_node('h1', ["text-xl font-bold"], []),
                                         nav
                                     ])

        elif label == 'Card':
            # Variety: Some cards have images, different padding/shadows
            children = []
            if random.random() > 0.3:
                children.append(self._create_node('img', ["w-full", "h-40", "object-cover"]))

            body_children = [self._create_node('p', ["text-sm text-gray-500"])]
            if random.random() > 0.5:
                body_children.append(self._create_node('button', ["mt-4", "px-4", "py-2", "bg-black", "text-white"]))

            children.append(self._create_node('div', ["p-4"], body_children))
            return self._create_node('div', ["max-w-sm", "overflow-hidden", random.choice(self.shadows),
                                             random.choice(self.rounding)], children)

        elif label == 'Table':
            rows = []
            for _ in range(random.randint(2, 4)):
                cols = [self._create_node('td', ["p-3", "border-b", "border-gray-200"]) for _ in range(3)]
                rows.append(self._create_node('tr', [], cols))
            return self._create_node('table', ["min-w-full", "border-collapse"], rows)

        elif label == 'SearchBar':
            return self._create_node('div', ["flex", "border", "items-center", "px-2", random.choice(self.rounding)], [
                self._create_node('input', ["flex-1", "p-2", "outline-none"]),
                self._create_node('button', ["p-1", "bg-gray-200"], [])
            ])

        elif label == 'ImageGallery':
            cols = random.choice(["grid-cols-2", "grid-cols-3", "grid-cols-4"])
            imgs = [self._create_node('img', ["w-full", "aspect-square", "object-cover"]) for _ in
                    range(random.randint(3, 6))]
            return self._create_node('div', ["grid", cols, "gap-4"], imgs)

        elif label == 'DropdownMenu':
            items = [self._create_node('div', ["p-2", "hover:bg-gray-100"]) for _ in range(3)]
            return self._create_node('div', ["relative"], [
                self._create_node('button', ["px-4 py-2 bg-white border shadow-sm"]),
                self._create_node('div', ["absolute top-full mt-2 w-48 bg-white border shadow-xl"], items)
            ])

        elif label == 'Sidebar':
            links = [self._create_node('a', ["block py-2 px-4 hover:bg-slate-700"]) for _ in range(6)]
            return self._create_node('aside', ["w-64 h-screen bg-slate-800 text-white flex flex-col"], links)

        # Fallback for simple elements
        tag_map = {'Link': 'a', 'IconButton': 'button', 'RangeSlider': 'input', 'Header': 'header', 'Footer': 'footer'}
        return self._create_node(tag_map.get(label, 'div'), [f"ui-{label.lower()}", random.choice(self.colors)])

    def generate_batch(self, count=20):
        dataset = []
        for label in self.labels:
            for _ in range(count):
                dataset.append({
                    "label": label,
                    "contents": [self.generate_component(label)]
                })
        return dataset


# --- Output ---
augmenter = UIStrictAugmenter()
final_data = augmenter.generate_batch(500)  # 120 total samples

with open('tailwind_labeled_data.json', 'w') as f:
    json.dump(final_data, f, indent=2)