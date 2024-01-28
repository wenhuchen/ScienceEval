from datasets import load_dataset
from datasets import Dataset
from PIL import Image

dataset = load_dataset('wenhu/TheoremQA')

entries = []
for entry in dataset['test']:
    path = entry['Picture']

    if path != 'NONE':
        path = path.replace('images/', 'theoremqa_images/')
        path = Image.open(path)
    else:
        path = None

    entries.append({
        'Question': entry['Question'], 
        'Answer': entry['Answer'],
        'Answer_type': entry['Answer_type'],
        'Picture': path
        })

new_dataset = Dataset.from_list(entries)
new_dataset.push_to_hub('TIGER-Lab/TheoremQA', split='test')