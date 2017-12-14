# Chinese authors' Writing Style Recognition

### Requirements
- Python 3.6
- JRE 1.8.0_131-b11
- FudanNLP 2.1
- NLTK 3.2.5
- jieba 0.39
- matplotlib 2.1.0
- numpy 1.13.3
- sklearn

### Setup
1. Put the `.txt` files, each of which contains all the text from one author, under the `./input/` folder.
2. If you are working on Windows, run `run.bat` in the cmd or just double click it. 
This script extracts author's writing features from their texts and generates several files in `./output/` folder. 
`python run.py <a_author.txt>` will load the processing script only for this author.
Files generated are
- `cleaned_<author>.txt` 
	the text after preprocessing
- `cleaned_<author><number>.txt`
	split pieces of the preprocessed file
- `all_feat_<author>.txt` 
	features extracted from the whole cleaned text of the author
- `feat_<author><number>.txt`
	features extracted from the number-th piece of cleaned file
- `depen_<author><number>.txt`
	sentence dependency features
- `depen_text_<author>.txt`
	the encoded text file

3. After that, run `plot.bat` will launch the script for plotting related infomation in the `./output/` folder.

If you are working on other OS, sorry, no batch processing is available yet.



