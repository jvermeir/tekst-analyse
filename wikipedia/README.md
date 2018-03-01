# Analyze Dutch Wikipedia text 

## install

```
./setup.sh
```

## run

```
# Read a number of pages from Wikipedia and store results in json files in data folder
python wiki_text_collector.py -c number of pages to read from Wikipedia>
```

```
# rebuild the file that logs url's that have been visited before
python history.py
```

```
# split large json documents in smaller parts
python document_splitter.py
```

```
# Collect all sentences that contain a conjunction
python text_analyzer.py

```


## TODO

- **done:** read more text from Wikipedia, avoid reading duplicates
- **done:**  extract sentences
- **done:** store sentences in database
- **done:** extract only sentences that contain specific words like 'maar', 'want', 'daardoor' ...
- fix errors like: Mus%C3%A9e_Goupil

## stuff

history file after rebuild is not equal to number of items in json files
```
wc -l history.txt
   58412 history.txt

find data -type f -exec grep -o "\[" {} \; | wc -l
   62376
```
