import requests
import random
import time
from hdwallet import HDWallet
from hdwallet.symbols import BTC as BTC_SYMBOL
from hdwallet.utils import generate_mnemonic

def check_btc(address):
    try:
        r = requests.get(f"https://blockchain.info/rawaddr/{address}")
        if r.status_code == 200:
            j = r.json()
            balance = j.get("final_balance", 0)
            return balance
        return 0
    except:
        return 0


print("Crypto-hunter fixed edition")

while True:
    mnemonic = generate_mnemonic(strength=128)
    wallet = HDWallet(symbol=BTC_SYMBOL)
    wallet.from_mnemonic(mnemonic=mnemonic)

    btc_address = wallet.p2pkh_address()

    bal = check_btc(btc_address)

    print(f"[+] {btc_address} | BTC: {bal}")

    if bal > 0:
        print("FOUND WALLET WITH FUNDS!")
        with open("found.txt", "a") as f:
            f.write(f"{mnemonic} | {btc_address} | {bal}\n")
