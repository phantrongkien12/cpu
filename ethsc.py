import os
import time
import requests
import ecdsa
from Crypto.Hash import keccak
from colorama import Fore

def generate_eth_keypair():
    # private key 32 bytes đúng chuẩn Ethereum
    private_key = os.urandom(32)

    # tạo public key bằng secp256k1
    sk = ecdsa.SigningKey.from_string(private_key, curve=ecdsa.SECP256k1)
    vk = sk.verifying_key
    public_key_bytes = b"\x04" + vk.to_string()

    # keccak256(public_key)[-20 bytes]
    keccak_hash = keccak.new(digest_bits=256)
    keccak_hash.update(public_key_bytes)
    address = "0x" + keccak_hash.hexdigest()[-40:]

    return private_key.hex(), address


api_key = "UYX6E5N1I84X7JGE5A48RU1DP5B51Q9KQH"

while True:
    private_key, address = generate_eth_keypair()

    print(Fore.GREEN + f"Private Key: {private_key}")
    print(Fore.WHITE + f"Address: {address}")

    url = f"https://api.etherscan.io/api?module=account&action=balance&address={address}&tag=latest&apikey={api_key}"
    response = requests.get(url)

    if response.status_code != 200:
        print("API lỗi, thử lại...")
        continue

    data = response.json()

    if data.get("status") == "0":
        print(Fore.RED + "Balance: 0 ETH")
    else:
        balance = int(data["result"]) / 10**18
        print(Fore.RED + f"Balance: {balance} ETH")

        if balance > 0:
            with open("data.txt", "w") as f:
                f.write(address + "\n")
                f.write(private_key + "\n")
                f.write(str(balance))
            print(Fore.YELLOW + "Tìm thấy ví có tiền! Đã lưu vào data.txt")
            break

    time.sleep(0.5)
