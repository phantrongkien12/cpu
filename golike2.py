try:
    import cloudscraper, os, json, requests, random, time, sys, re
    from colorama import Fore, init
    from fake_useragent import UserAgent
except:
    os.system("pip install cloudscraper requests colorama fake-useragent")
    import cloudscraper, os, json, requests, random, time, sys, re
    from colorama import Fore, init
    from fake_useragent import UserAgent

init(autoreset=True)
ua = UserAgent()

def delay(sec):
    for i in range(sec, -1, -1):
        sys.stdout.write(f"\r{Fore.YELLOW}[⏳️] ➜ Đang chờ {i}s.. ")
        sys.stdout.flush()
        time.sleep(1)
    print()

def select_parse(inp):
    return [int(i) for i in re.split(r"[+, ]+", inp.strip()) if i.isdigit()]

def require_input(prompt, allow_empty=False):
    """Hàm bắt buộc nhập dữ liệu"""
    while True:
        value = input(prompt).strip()
        if not allow_empty and not value:
            print(Fore.RED + "[❌] ➜ Trường này không được để trống!")
        else:
            return value

def main():
    os.system("cls" if os.name == "nt" else "clear")
    print(Fore.CYAN + "════════════════════════════════════════════════")
    print(Fore.MAGENTA + " ⚜️ TOOL GOLIKE INSTAGRAM - NEWBIE VIẾT CODE ⚜️")
    print(Fore.CYAN + "════════════════════════════════════════════════")

    auth = require_input(Fore.WHITE + "[🐷] ➜ Nhập Authorization: ")
    t = require_input(Fore.WHITE + "[🐷] ➜ Nhập T: ")

    scraper = cloudscraper.create_scraper()
    headers = {"Authorization": auth, "T": t, "Content-Type": "application/json;charset=utf-8"}
    try:
        r = scraper.get("https://gateway.golike.net/api/users/me", headers=headers, timeout=20).json()
    except:
        print(Fore.RED + "[❌] ➜ Đăng nhập thất bại!")
        return

    if r.get("status") != 200:
        print(Fore.RED + "[❌] ➜ Đăng nhập thất bại!")
        return
    print(Fore.GREEN + "[✅] ➜ Đăng nhập thành công!")
    user = r["data"]
    print(Fore.CYAN + f"[🔍] ➜ Tài khoản: {user['username']} | Số dư: {user['coin']}")

    accs = scraper.get("https://gateway.golike.net/api/instagram-account", headers=headers, timeout=20).json()
    if accs.get("status") != 200 or not accs.get("data"):
        print(Fore.RED + "[❌] ➜ Không tìm thấy tài khoản Instagram nào.")
        return

    data = accs["data"]
    print(Fore.MAGENTA + "[👀] ➜ Danh sách tài khoản Instagram hiện có:")
    for i, a in enumerate(data, 1):
        print(Fore.BLUE + f"[⚜️] ➜ {i}. {a['instagram_username']}")

    while True:
        sel = select_parse(require_input(Fore.WHITE + "[🐷] ➜ Vui lòng chọn tài khoản chạy (1 hoặc 1+2+3): "))
        if sel:
            break
        else:
            print(Fore.RED + "[❌] ➜ Vui lòng chọn ít nhất một tài khoản hợp lệ!")

    cookies = []
    for i in sel:
        name = data[i - 1]['instagram_username']
        cookie = require_input(Fore.YELLOW + f"[🐷] ➜ Nhập cookie của tài khoản {name}: ")
        cookies.append(cookie)

    def get_int_input(prompt, default):
        value = input(prompt).strip()
        return int(value) if value.isdigit() else default

    num_task = get_int_input(Fore.YELLOW + "[🐷] ➜ Nhập số nhiệm vụ muốn làm (mặc định 1): ", 50)
    delay_sec = get_int_input(Fore.YELLOW + "[🐷] ➜ Nhập delay giữa mỗi nhiệm vụ (mặc định 3s): ", 30)
    rest_after = get_int_input(Fore.YELLOW + "[🐷] ➜ Nghỉ ngơi sau bao nhiêu nhiệm vụ (0 = bỏ qua): ", 0)
    rest_time = get_int_input(Fore.YELLOW + "[🐷] ➜ Nghỉ ngơi bao nhiêu giây (0 = bỏ qua): ", 0)
    change_after = get_int_input(Fore.YELLOW + "[🐷] ➜ Đổi tài khoản sau bao nhiêu nhiệm vụ (0 = bỏ qua): ", 0)
    auto_change = require_input(Fore.YELLOW + "[🐷] ➜ Tự đổi tài khoản khi hết nhiệm vụ không (y/n): ").lower() == "y"

    total_done = 0
    for n, i in enumerate(sel):
        acc = data[i - 1]
        cookie = cookies[n]
        name = acc['instagram_username']
        id_acc = acc['id']
        print(Fore.CYAN + f"[⚙️] ➜ Đang chạy tài khoản {name}")
        suc = fai = earned = 0

        for task_count in range(1, num_task + 1):
            try:
                job = scraper.get(f"https://gateway.golike.net/api/advertising/publishers/instagram/jobs?instagram_account_id={id_acc}&data=null", headers=headers, timeout=20).json()
                if job.get("status") != 200 or not job.get("data"):
                    if auto_change:
                        print(Fore.MAGENTA + f"[⏭️] ➜ Đang chuyển sang tài khoản tiếp theo..")
                        break
                    else:
                        print(Fore.YELLOW + f"[❌] ➜ Hết nhiệm vụ, dừng tài khoản {name}")
                        return

                j = job["data"]
                jid, oid, jtype = j["id"], j["object_id"], j["type"].lower()

                csrf_token = ""
                if "csrftoken=" in cookie:
                    csrf_token = cookie.split("csrftoken=")[1].split(";")[0]

                insta_headers = {
                    'accept': '*/*',
                    'accept-language': 'vi,en-US;q=0.9,en;q=0.8',
                    'content-type': 'application/x-www-form-urlencoded',
                    'cookie': cookie,
                    'origin': 'https://www.instagram.com',
                    'priority': 'u=1, i',
                    'referer': 'https://www.instagram.com/',
                    'sec-ch-prefers-color-scheme': 'dark',
                    'sec-fetch-dest': 'empty',
                    'sec-fetch-mode': 'cors',
                    'sec-fetch-site': 'same-origin',
                    'user-agent': ua.random,
                    'x-asbd-id': '129477',
                    'x-csrftoken': csrf_token,
                    'x-ig-app-id': '936619743392459',
                    'x-ig-www-claim': '0',
                    'x-instagram-ajax': '1014868636',
                    'x-requested-with': 'XMLHttpRequest'
                }

                ok = False
                if jtype == "follow":
                    r = requests.post(f"https://www.instagram.com/api/v1/friendships/create/{oid}/", headers=insta_headers)
                    ok = r.status_code == 200
                elif jtype == "like":
                    r = requests.post(f"https://www.instagram.com/api/v1/web/likes/{oid}/like/", headers=insta_headers)
                    ok = r.status_code == 200

                time.sleep(1)
                if ok:
                    done = scraper.post("https://gateway.golike.net/api/advertising/publishers/instagram/complete-jobs",
                                        headers=headers,
                                        json={"instagram_account_id": id_acc,
                                              "instagram_users_advertising_id": jid,
                                              "async": True,
                                              "data": "null"}).json()
                    if done.get("success"):
                        money = done["data"]["prices"]
                        suc += 1
                        earned += money
                        print(Fore.GREEN + f"[⚜️] ➜ [{task_count}] Thành công | {jtype.capitalize()} | ID: {oid} | +{money} | Tổng: {earned}")
                    else:
                        fai += 1
                        print(Fore.RED + f"[⚜️] ➜ [{task_count}] Thất bại | {jtype.capitalize()} | ID: {oid} | Tổng: {earned}")
                else:
                    fai += 1
                    print(Fore.RED + f"[⚜️] ➜ [{task_count}] Thất bại | {jtype.capitalize()} | ID: {oid} | Tổng: {earned}")

                total_done += 1
                delay(delay_sec)
                if rest_after > 0 and total_done % rest_after == 0:
                    delay(rest_time)
                if change_after > 0 and total_done % change_after == 0:
                    print(Fore.MAGENTA + f"[⏭️] ➜ Đang chuyển sang tài khoản tiếp theo..")
                    break
            except:
                fai += 1
                delay(3)
                continue

        print(Fore.GREEN + f"[🎉] ➜ Hoàn thành | Nhiệm vụ: {suc + fai} | Thành công: {suc} | Thất bại: {fai} | Kiếm được: {earned} | Tổng: {earned}")

if __name__ == "__main__":
    main()
