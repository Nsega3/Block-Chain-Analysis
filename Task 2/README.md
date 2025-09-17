This is a simple program that will run data on the SHIB INU.csv and print out a simple graph

Shiba Inu Analysis is a written style analysis using essay-style writing to perform analysis.

To Run:

1) Activate a virtual environment

cd shib-analysis
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt

2) download data from Coingecko "shib-usd-max.csv"
3) Run using
   python .\src\analyze.py --csv shib_oct2021.csv --out chart.png

