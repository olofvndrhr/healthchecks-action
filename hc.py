import os
import re

import httpx


def create_check(
    baseurl: str, api_key: str, check_name: str, check_schedule: str, grace: int
) -> None:
    check_slug = re.sub(r"[^0-9a-zA-Z\-]", "", check_name)

    headers = {
        "Content-Type": "application/json",
        "X-Api-Key": api_key,
    }
    payload = {
        "name": check_name,
        "slug": check_slug,
        "unique": ["name", "slug"],
        "channels": "*",
        "tz": "Europe/Zurich",
        "schedule": check_schedule,
        "grace": grace,
    }

    print(f"creating/updating check: {check_name} ({check_slug})")
    r = httpx.post(
        f"{baseurl}/api/v3/checks/",
        headers=headers,
        json=payload,
        follow_redirects=True,
        timeout=10,
    )

    match r.status_code:
        case 200:
            print("check already exists/was updated")
        case 201:
            print("check was created")
        case _:
            print(f"error in request. {r.text}")
            raise ValueError


def ping_check(baseurl: str, ping_path: str, method: str) -> None:
    match method:
        case "start":
            ping_method = "/start"
        case "fail":
            ping_method = "/fail"
        case _:
            ping_method = ""

    pingurl = f"{baseurl}/ping/{ping_path}{ping_method}"

    print(f"pinging: {pingurl}")
    for tries, _ in enumerate(range(3), 1):
        try:
            r = httpx.get(
                pingurl,
                follow_redirects=True,
                timeout=10,
            )
            r.raise_for_status()
        except Exception as exc:
            print(f"error in request ({tries}). {exc=}")
            if tries >= 3:
                raise exc


def main() -> None:
    baseurl = os.environ["HC_BASE_URL"]

    # check creating specific
    api_key = os.getenv("HC_API_KEY", "")
    check_name = os.getenv("HC_CHECK_NAME", "")
    check_schedule = os.getenv("HC_CHECK_SCHEDULE", "")
    grace = os.getenv("HC_GRACE", "")

    # check ping specific
    ping_path = os.getenv("HC_PING_PATH", "")
    method = os.getenv("HC_METHOD", "")

    # create check
    if all([api_key, check_name, check_schedule, grace]):
        try:
            grace_int = int(grace)
        except Exception as exc:
            print(f"cant convert grace to integer={grace}")
            raise exc

        create_check(baseurl, api_key, check_name, check_schedule, grace_int)

    # ping check
    if all([ping_path, method]):
        ping_check(baseurl, ping_path, method)


if __name__ == "__main__":
    main()
