from mnemonic import Mnemonic
from hdwallet import HDWallet
from hdwallet.symbols import BTC as BTC_SYMBOL
import requests

def check_btc(addr):
    try:
        r = requests.get(f"https://blockchain.info/rawaddr/{addr}", timeout=5)
        if r.status_code == 200:
            j = r.json()
            return j.get("final_balance", 0)
        return 0
    except:
        return 0

mnemo = Mnemonic("english")

print("Crypto Hunter - fixed, không cà chớn")

while True:
    # tạo 12 từ khóa
    seed_words = mnemo.generate(strength=128)

    # tạo ví từ mnemonic
    wallet = HDWallet(symbol=BTC_SYMBOL)
    wallet.from_mnemonic(seed_words)

    address = wallet.p2pkh_address()
    bal = check_btc(address)

    print(f"[{address}] | balance = {bal}")

    if bal > 0:
        print("FOUND WALLET WITH BALANCE!")
        with open("found.txt", "a") as f:
            f.write(f"{seed_words} | {address} | {bal}\n")
