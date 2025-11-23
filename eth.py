import os
import sys
import time
import platform
import requests
import logging
from dotenv import load_dotenv

from bip_utils import (
    Bip39MnemonicGenerator,
    Bip39SeedGenerator,
    Bip44,
    Bip44Coins,
    Bip44Changes,
    Bip39WordsNum,
)

# ----------------------------------------------------
# CONFIG + LOGGING
# ----------------------------------------------------
LOG_FILE_NAME = "breadcracker.log"
ENV_FILE_NAME = "breadcracker.env"
WALLETS_FILE_NAME = "wallets_with_balance.txt"

wallets_scanned = 0

directory = os.path.dirname(os.path.abspath(__file__))
log_file_path = os.path.join(directory, LOG_FILE_NAME)
env_file_path = os.path.join(directory, ENV_FILE_NAME)
wallets_file_path = os.path.join(directory, WALLETS_FILE_NAME)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(log_file_path),
        logging.StreamHandler(sys.stdout),
    ],
)

# ----------------------------------------------------
# CREATE .env IF MISSING
# ----------------------------------------------------
if not os.path.exists(env_file_path):
    print("The breadcracker.env file does not exist. Let's create it.")
    etherscan_api_key = input("Enter your Etherscan API key: ").strip()

    with open(env_file_path, "w") as env_file:
        env_file.write(f"ETHERSCAN_API_KEY={etherscan_api_key}\n")

load_dotenv(env_file_path)

required_env_vars = ["ETHERSCAN_API_KEY"]
missing = [v for v in required_env_vars if not os.getenv(v)]

if missing:
    raise EnvironmentError(f"Missing environment variables: {', '.join(missing)}")

ETHERSCAN_KEY = os.getenv("ETHERSCAN_API_KEY")

# ----------------------------------------------------
# FUNCTIONS
# ----------------------------------------------------
def bip_phrase():
    return Bip39MnemonicGenerator().FromWordsNumber(Bip39WordsNum.WORDS_NUM_12)

def eth_address_from_seed(seed):
    seed_bytes = Bip39SeedGenerator(seed).Generate()
    wallet = (Bip44.FromSeed(seed_bytes, Bip44Coins.ETHEREUM)
              .Purpose().Coin().Account(0)
              .Change(Bip44Changes.CHAIN_EXT)
              .AddressIndex(0))
    return wallet.PublicKey().ToAddress()

def btc_address_from_seed(seed):
    seed_bytes = Bip39SeedGenerator(seed).Generate()
    wallet = (Bip44.FromSeed(seed_bytes, Bip44Coins.BITCOIN)
              .Purpose().Coin().Account(0)
              .Change(Bip44Changes.CHAIN_EXT)
              .AddressIndex(0))
    return wallet.PublicKey().ToAddress()

def check_eth_balance(address):
    url = (
        f"https://api.etherscan.io/api"
        f"?module=account&action=balance"
        f"&address={address}&tag=latest&apikey={ETHERSCAN_KEY}"
    )
    try:
        r = requests.get(url, timeout=10).json()
        if r.get("status") == "1":
            return int(r["result"]) / 1e18
    except:
        return 0
    return 0

def check_btc_balance(address):
    try:
        r = requests.get(
            f"https://blockchain.info/balance?active={address}",
            timeout=10
        ).json()
        sat = r[address]["final_balance"]
        return sat / 100_000_000
    except:
        return 0

def save_wallet(seed, btc_addr, btc_bal, eth_addr, eth_bal):
    with open(wallets_file_path, "a") as f:
        f.write(
            f"Seed: {seed}\n"
            f"BTC: {btc_addr} | Balance: {btc_bal} BTC\n"
            f"ETH: {eth_addr} | Balance: {eth_bal} ETH\n"
            f"{'-'*40}\n\n"
        )

# ----------------------------------------------------
# MAIN LOOP (NO CURSES)
# ----------------------------------------------------
print("\n\n=== BreadCracker (Linux / Console Edition) ===\n")

while True:
    wallets_scanned += 1

    seed = bip_phrase()
    btc_addr = btc_address_from_seed(seed)
    eth_addr = eth_address_from_seed(seed)

    btc_bal = check_btc_balance(btc_addr)
    eth_bal = check_eth_balance(eth_addr)

    print(f"\n[{wallets_scanned}] Seed: {seed}")
    print(f"BTC: {btc_addr} | Balance: {btc_bal}")
    print(f"ETH: {eth_addr} | Balance: {eth_bal}")

    if btc_bal > 0 or eth_bal > 0:
        print(">>> FOUND WALLET WITH BALANCE!!! Saving...")
        save_wallet(seed, btc_addr, btc_bal, eth_addr, eth_bal)

    time.sleep(0.05)
