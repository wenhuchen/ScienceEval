from bs4 import BeautifulSoup
import re
import glob
import os
import urllib.request
import argparse
import shutil
import json
import tqdm
import re
from multiprocessing import Pool
import unicode_to_latex
import string
import random

parser = argparse.ArgumentParser(
                    prog='stemez',
                    description='What the program does',
                    epilog='Text at the bottom of help')
#parser.add_argument('--subject', type=str)
args = parser.parse_args()

subject_dict = {
    'physics': ('Physics', 'DPhysics'),
    'chemistry': ('Chemistry', 'EChemistry'),
    'biology': ('Biology', 'FBiology'),
    'cs': ('ComputerScience', 'GComputerScience')
}
all_mapping = {}
encoding = 'windows-1252'


def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def clean(sentence: str):
    print(sentence)
    x = unicode_to_latex.unicode_to_latex(sentence)
    # x = x.replace('{\\textasciicircum}', '^')
    x = x.replace('‒', '-')
    x = re.sub(r' +', r' ', x)
    x = re.sub(r'\\ensuremath{([^}]*)}', r'\1', x)
    x = x.replace('{}', '')
    try:
        random_file = id_generator()
        with open(f'/tmp/{random_file}.json', 'w') as f:
            json.dump({'string': x}, f)
        with open(f'/tmp/{random_file}.json', 'r') as f:
            json.load(f)
    except Exception:
        raise ValueError(x)

    return x


def extract_content(html_file):
    filename, images = html_file
    with open(filename, 'r', encoding=encoding) as file:
        string = file.read()
        string = re.sub(r'<sub>([^< ]+)</sub>', r'_\1', string)
        string = re.sub(r'<sup>([^< ]+)</sup>', r'^\1', string)
        string = re.sub('–', '-', string)
        soup = BeautifulSoup(string, 'html.parser')
        paragraphs = soup.find_all('p', class_='MsoNormal')
        content = []
        for p in paragraphs:
            for span_text in p.find_all('span'):
                if span_text and not span_text.has_attr('class'):
                    span_text = span_text.get_text(strip=True)
                    if 'PROBLEM' in span_text:
                        span_text = span_text.split(':')[-1]
                        content = [span_text.replace('\n', ' ').strip()]
                    else:
                        content.append(span_text.replace('\n', ' ').strip())

                if re.search(r'[0-9]+ – [0-9]+:', content[-1]):
                    content.clear()

    result = ' '.join(content)
    result = clean(result)
    if 'Solution:' in result:
        return {
            'question': result.split('Solution:')[0].strip(),
            'solution': result.split('Solution:')[1].strip(),
            'images': images,
            'html_file': filename
            }
    elif 'Solutions:' in result:
        return {
            'question': result.split('Solutions:')[0].strip(),
            'solution': result.split('Solutions:')[1].strip(),
            'images': images,
            'html_file': filename
            }
    else:
        return {}

def download_image(html_file, base):
    all_mapping[html_file] = []
    with open(html_file, 'r', encoding=encoding) as file:
        soup = BeautifulSoup(file, 'html.parser')
        for image in soup.find_all('img'):
            if image:
                image = image['src']
                if '/' in image:
                    #if os.path.exists(f'images/{image.split("/")[0]}'):
                    #    shutil.rmtree(f'images/{image.split("/")[0]}')
                    all_mapping[html_file].append(f'images/{image}')
                    if not os.path.exists(f'images/{image.split("/")[0]}'):
                        os.mkdir(f'images/{image.split("/")[0]}')
                        urllib.request.urlretrieve(base + image, f'images/{image}')

if __name__ == '__main__':

    html_files = []
    for sub in ['physics', 'chemistry', 'biology', 'cs']:
        subject, field = subject_dict[sub]
        base = f'https://stemez.com/subjects/science/{field}/{field}/{field}/'

        # Replace 'example.html' with the path to your HTML file
        for html_file in tqdm.tqdm(glob.glob(f'/Users/wenhuchen/Documents/Crawler/{subject}/*.htm')):
            download_image(html_file, base)
            html_files.append((html_file, all_mapping[html_file]))

    entries = []
    with Pool() as pool:
        print(len(html_files))
        for entry in pool.imap(extract_content, html_files):
            if entry:
                entries.append(entry)

    print(len(entries))
    with open('outputs.jsonl', 'w') as f:
        for line in entries:
            f.write(json.dumps(line) + '\n')
        #json.dump(entries, f, indent=2)

    # extract_content(('/Users/wenhuchen/Documents/Crawler/Chemistry/E27-0906.htm', {}))