#!/usr/bin/python3

import datetime
import requests
import subprocess
import time

HOSTS = ["p1", "p2", "p3", "p4"]
PORT = 8080

HTTP_TIMEOUT = 1
SLEEP_SECS = 90

BRIGHTNESS = 1


def check_health(host: str) -> bool:
    try:
        res = requests.get(f"http://{host}:{PORT}/health", timeout=HTTP_TIMEOUT)
        ok = res.text == "OK"
    except requests.exceptions.ConnectionError:
        ok = False

    return ok


def write_message(message: str, log=True) -> None:
    set_brightness(BRIGHTNESS)
    try:
        requests.post(
            f"http://p4:{PORT}/message", data=message.encode(), timeout=HTTP_TIMEOUT
        )
        print(datetime.datetime.now().isoformat(), message)
    except requests.exceptions.ConnectionError:
        print(
            datetime.datetime.now().isoformat(),
            "Failed to write message to scroll phat:",
            message,
        )


def set_brightness(brightness: int) -> bool:
    try:
        requests.post(
            f"http://p4:{PORT}/brightness", json=brightness, timeout=HTTP_TIMEOUT
        )
    except requests.exceptions.ConnectionError:
        return False

    return True


def hard_reset(host: str) -> None:
    # Effectively power-cycles the host
    write_message(f"Resetting {host}")
    subprocess.run(["/sbin/clusterctrl", "off", host])
    subprocess.run(["/sbin/clusterctrl", "on", host])


def main():
    # Switch them all on
    subprocess.run(["/sbin/clusterctrl", "on"])

    ok_last = {host: True for host in HOSTS}

    while True:
        
        ok_now = {}
        for host in HOSTS:
            ok_now[host] = check_health(host)

            if ok_now[host] or ok_last[host]:
                continue

            # Status was bad on both the last checks :(
            hard_reset(host)
        
        if all(ok for ok in ok_now.values()):
            write_message(f"ALL OK!")
        else:
            ok = ", ".join(host for host, ok in ok_now.items() if ok)
            not_ok = ", ".join(host for host, ok in ok_now.items() if not ok)
            if ok:
                write_message(f"OK: {ok}")
            write_message(f"BAD: {not_ok}")

        write_message( subprocess.run(["hostname", "-I"], capture_output=True).stdout.decode().strip().upper())
        time.sleep(SLEEP_SECS)
        ok_last = ok_now


if __name__ == "__main__":
    main()
