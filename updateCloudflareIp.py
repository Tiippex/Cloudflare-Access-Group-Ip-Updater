#!/usr/bin/env python3
import requests
import os
import sys
import time
from datetime import datetime

def log(message):
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{current_time}] {message}")

def get_public_ip():
    response = requests.get("https://ip.tiippex.de")
    if response.status_code == 200:
        return response.text.strip()
    else:
        raise Exception("Could not get public IP")

def get_access_group(api_key, account_id, group_id):
    url = f"https://api.cloudflare.com/client/v4/accounts/{account_id}/access/groups/{group_id}"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()['result']
    else:
        raise Exception(f"Failed to fetch Access Group. Response: {response.text}")

def update_cloudflare_access_group(api_key, account_id, group_id, ip_range):
    url = f"https://api.cloudflare.com/client/v4/accounts/{account_id}/access/groups/{group_id}"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    public_ip = get_public_ip()

    if not ip_range:
        ip_range = []

    ip_range.append(public_ip)

    group_data = get_access_group(api_key, account_id, group_id)

    ip_includes = [{"ip": {"ip": ip}} for ip in ip_range]

    group_data['include'] = ip_includes

    log(f"Trying to update {account_id}'s' Access Group with IPs: {', '.join(ip_range)}")

    response = requests.put(url, json=group_data, headers=headers)

    if response.status_code == 200:
        log(f"Successfully updated Access Group with IPs: {', '.join(ip_range)}")
    else:
        log(f"Failed to update Access Group. Response: {response.text}")

if __name__ == "__main__":
    CLOUDFLARE_API_KEY = os.getenv("CLOUDFLARE_API_KEY")
    CLOUDFLARE_ACCOUNT_ID = os.getenv("CLOUDFLARE_ACCOUNT_ID")
    CLOUDFLARE_GROUP_ID = os.getenv("CLOUDFLARE_GROUP_ID")
    IP_RANGE = os.getenv("IP_RANGE", "").split(",") if os.getenv("IP_RANGE") else []
    UPDATE_INTERVAL_MINUTES = os.getenv("UPDATE_INTERVAL_MINUTES")

    if not CLOUDFLARE_API_KEY or not CLOUDFLARE_ACCOUNT_ID or not CLOUDFLARE_GROUP_ID:
        log("Required environment variables: CLOUDFLARE_API_KEY, CLOUDFLARE_ACCOUNT_ID, CLOUDFLARE_GROUP_ID")
        sys.exit(1)

    try:
        if not UPDATE_INTERVAL_MINUTES:
            log("No UPDATE_INTERVAL_MINUTES set, running once...")
            update_cloudflare_access_group(CLOUDFLARE_API_KEY, CLOUDFLARE_ACCOUNT_ID, CLOUDFLARE_GROUP_ID, IP_RANGE)
            log("Execution complete. Exiting.")
            sys.exit(0)

        else:
            UPDATE_INTERVAL_MINUTES = int(UPDATE_INTERVAL_MINUTES)
            while True:
                try:
                    update_cloudflare_access_group(CLOUDFLARE_API_KEY, CLOUDFLARE_ACCOUNT_ID, CLOUDFLARE_GROUP_ID, IP_RANGE)
                except Exception as e:
                    log(f"Error updating Cloudflare: {e}")

                time.sleep(UPDATE_INTERVAL_MINUTES * 60)

    except KeyboardInterrupt:
        log("\nGracefully shutting down. Exiting...")
        sys.exit(0)
