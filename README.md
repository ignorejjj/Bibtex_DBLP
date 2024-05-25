# Bibtex_DBLP
A simple script designed to convert BibTeX (.bib) file into neatly formatted entries as found on DBLP. 

For each article item in the input BibTeX file, a search will be performed on DBLP using its title. If a corresponding entry is found, it will be replaced; otherwise, a message will be displayed in the console, and the original item will be retained.

## Requirements

pip install -r requirements.txt

## Usage

python bibparser.py --input_path custom.bib --output_path new.bib 
