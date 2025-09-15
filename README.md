# Block-Chain-Analysis
A short project for crypto forensics.
Includes the 2 tasks required with 
1) GET data from Etherscan website to plot a graph
2) Conduct Crypto Analysis based on transaction history 
## Quickstart (Windows PowerShell)
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env   # put your ETHERSCAN_API_KEY inside .env
mkdir data\outputs
python -m src.task1_wallet_graph --wallet 0xde0b295669a9fd93d5f28d9ec85e40f4cb697bae --limit 15
