#!/usr/bin/env python3
import requests
import random
import os
import datetime

TOKEN = os.environ.get("CHASTER_TOKEN")
WEARER_ID = os.environ.get("WEARER_ID")
HEADERS = {"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"}

def log(message):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}")

def get_locks():
    r = requests.get("https://api.chaster.app/api/locks", headers=HEADERS, params={"userId": WEARER_ID, "status": "locked"})
    return r.json() if r.status_code == 200 else None

def add_time(lock_id, seconds):
    r = requests.post(f"https://api.chaster.app/api/locks/{lock_id}/update-time", headers=HEADERS, json={"duration": seconds})
    return r.status_code == 200

def random_event(lock_id):
    roll = random.random()
    if roll < 0.10:
        minutes = random.randint(15, 60)
        if add_time(lock_id, minutes * 60):
            log(f"MISCHIEF: Added {minutes} minutes. Just because.")
    elif roll < 0.15:
        minutes = random.randint(5, 15)
        if add_time(lock_id, -(minutes * 60)):
            log(f"REWARD: Removed {minutes} minutes. She has been good.")
    else:
        log(f"WATCH: Checked lock {lock_id}. All quiet. She stays locked.")

def main():
    log("Warden running...")
    locks = get_locks()
    if not locks:
        log("No active locks found. Nothing to do.")
        return
    for lock in locks:
        lock_id = lock.get("_id")
        if lock_id:
            log(f"Found active lock: {lock_id}")
            random_event(lock_id)

if __name__ == "__main__":
    main()