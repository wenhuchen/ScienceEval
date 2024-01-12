import json
import sys
from datasets import Dataset
import random
from PIL import Image

data = []
with open(sys.argv[1]) as f:
    for line in f:
        data.append(json.loads(line))

new_data = []
short_answer = 0
image_question = 0
for entry in data:
    if entry['image_answer']:
        continue
    
    if len(entry['images']) > 1:
        continue

    if entry['image_question']:
        image_question += 1
        if entry['images']:
            entry['images'] = Image.open(entry['images'][0])
        else:
            entry['images'] = None #Image.open('images/empty.png')
    else:
        entry['images'] = None

    if entry['short_answer']:
        short_answer += 1

    del entry['image_answer']
    entry['subject'] = entry['html_file'].split('/')[-2]
    del entry['html_file']
    new_data.append(entry)

# print(subject, 'short answer percent:', short_answer / len(new_data), 'image question percent:', image_question / len(new_data))
# total_data.extend(new_data)

print('before:', len(data), 'after:', len(new_data))

# random.shuffle(total_data)

dataset = Dataset.from_list(new_data)
dataset.push_to_hub('TIGER-Lab/ScienceEval', split='test')

#with open('output_filtered.json', 'w') as f:
#    json.dump(total_data, f, indent=2)