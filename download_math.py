from bs4 import BeautifulSoup
import urllib.request
import tqdm
import re
import argparse
import os

parser = argparse.ArgumentParser(
                    prog='stemez',
                    description='What the program does',
                    epilog='Text at the bottom of help')
args = parser.parse_args()

subject_dict = {
    'Algebra': ('Algebra', 'AAlgebra'),
    'Geometry': ('Geometry', 'BGeometry'),
    'PreCalculus': ('PreCalculus', 'CPreCalculus'),
    'Calculus': ('Calculus', 'ICalculus'),
    'AdvCalculus': ('AdvCalculus', 'KAdvCalculus'),
    'Statistics': ('Statistics', 'HStatistics'),
    'LinearAlgebra': ('LinearAlgebra', 'QLinearAlgebra'),
    'FiniteDiscreteMath': ('FiniteDiscreteMath', 'RFiniteDiscreteMath'),
    'DifferentialEquations': ('DifferentialEquations', 'NDifferentialEquations'),
    'ComplexVariables': ('ComplexVariables', 'PComplexVariables'),
    'VectorAnalysis': ('VectorAnalysis', 'TVectorAnalysis'),
    'NumericalAnalysis': ('NumericalAnalysis', 'SNumericalAnalysis'),
    'Topology': ('Topology', '1PTopology')
}

for subject in ['AdvCalculus', 'Statistics', 'LinearAlgebra', 'FiniteDiscreteMath', 'DifferentialEquations',
                'ComplexVariables', 'VectorAnalysis', 'NumericalAnalysis', 'Topology']:
    subject, field = subject_dict[subject]

    # Read the HTML file
    with open(f'{subject}_files/index.html', 'r', encoding = 'windows-1252') as file:
        print(f'{subject}_files/index.html')
        html = file.read()

    base = f'https://stemez.com/subjects/maths/{field}/{field}/{field}/'

    # Create a BeautifulSoup object
    soup = BeautifulSoup(html, 'html.parser')
    a_tags = soup.find_all('a')
    hrefs = [a.get('href') for a in a_tags]

    all_hrefs=  []
    # Print all the href links
    for href in tqdm.tqdm(hrefs):
        if href and '-Ch' in href:
            html = urllib.request.urlopen(href)
            soup = BeautifulSoup(html, 'html.parser')
            a_tags = soup.find_all('a')

            # Extract href attributes
            for a in a_tags:
                if a.get('href') and 'Ch' in a.get('href'):
                    page_url = base + a.get('href')
                    html = urllib.request.urlopen(page_url)

                    # Create a BeautifulSoup object
                    soup = BeautifulSoup(html, 'html.parser')

                    # Find all the <a> tags
                    a_tags_more = soup.find_all('a')
                    for a_more in a_tags_more:
                        if a_more.get('href'):
                            url = a_more.get('href')
                            if re.search('.[0-9]+-[0-9]+.htm', url):
                                all_hrefs.append(base + url)

    for url in tqdm.tqdm(all_hrefs):
        if not os.path.exists(f'{subject}_files/{url.split("/")[-1]}'):
            try:
                urllib.request.urlretrieve(url, f'{subject}_files/{url.split("/")[-1]}')
            except Exception:
                print(url)
