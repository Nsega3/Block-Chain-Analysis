import os
from dotenv import load_dotenv
load_dotenv()

ETHERSCAN_API_KEY = os.getenv("ETHERSCAN_API_KEY", "")
BASE_URL = "https://api.etherscan.io/v2/api"
CHAIN_ID = "1"
ETHER_VALUE = 10 ** 18

