Crawling script from Stem EZ website. The processed dataset is uploaded to https://huggingface.co/datasets/TIGER-Lab/ScienceEval.


Visit https://www.stemez.com/, go the desired website and download the desired subject into a folder.

1. Download Dataset
```
python download_math.py
```

2. Process Dataset
```
python process_math.py
```

3. Extract answer
```
python gpt4_extract.py
```
