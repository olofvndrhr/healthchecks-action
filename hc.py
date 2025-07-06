import os
import re

import httpx


def create_check(
    baseurl: str, api_key: str, check_name: str, check_schedule: str, grace: int
) -> None:
    _check_slug = re.sub(r"[^0-9a-zA-Z\-]", "-", check_name)
    check_slug = re.sub(r"-{2,}", "-", _check_slug)

    print(f"creating slug from name={check_name}, slug={check_slug}")
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


def _ping_get(url: str) -> None:
    for tries, _ in enumerate(range(3), 1):
        print(f"GET pinging: {url} ({tries})")
        try:
            r = httpx.get(url, follow_redirects=True, timeout=10)
            r.raise_for_status()
        except Exception as exc:
            print(f"error in request. {exc=}")
            if tries >= 3:
                raise exc
        else:
            break


def _ping_post(url: str, data: str) -> None:
    for tries, _ in enumerate(range(3), 1):
        print(f"POST pinging: {url} ({tries})")
        print(f"POST ping data={data}")
        try:
            r = httpx.post(url, content=data, follow_redirects=True, timeout=10)
            r.raise_for_status()
        except Exception as exc:
            print(f"error in request. {exc=}")
            if tries >= 3:
                raise exc
        else:
            break


def ping_check(baseurl: str, ping_path: str, method: str, data: str) -> None:
    match method:
        case "start":
            print("healthchecks - start")
            pingurl = f"{baseurl}/ping/{ping_path}/start"
        case "fail":
            print("healthchecks - fail")
            pingurl = f"{baseurl}/ping/{ping_path}/fail"
        case "log":
            print("healthchecks - log")
            pingurl = f"{baseurl}/ping/{ping_path}/log"
        case _:
            print("healthchecks - ok")
            pingurl = f"{baseurl}/ping/{ping_path}"

    if data:
        _ping_post(pingurl, data)
    else:
        _ping_get(pingurl)


def main() -> None:
    baseurl = os.getenv("HC_BASE_URL")
    if not baseurl:
        print("no baseurl given")
        raise ValueError

    # check creating specific
    api_key = os.getenv("HC_API_KEY", "")
    check_name = os.getenv("HC_CHECK_NAME", "")
    check_schedule = os.getenv("HC_CHECK_SCHEDULE", "")
    grace = os.getenv("HC_GRACE", "")

    # check ping specific
    ping_path = os.getenv("HC_PING_PATH", "")
    method = os.getenv("HC_METHOD", "")
    succeeded = os.getenv("HC_SUCCEEDED", "")
    ping_body = os.getenv("HC_PING_BODY", "")

    # create check
    if all([api_key, check_name, check_schedule, grace]):
        try:
            grace_int = int(grace)
        except Exception as exc:
            print(f"cant convert grace to integer={grace}")
            raise exc

        create_check(baseurl, api_key, check_name, check_schedule, grace_int)

    # ping check
    if ping_path:
        if succeeded and succeeded.lower() in ["true", "success"]:
            print("succeeded = true")
            ping_method = ""
        elif succeeded and succeeded.lower() in ["false", "failure", "cancelled"]:
            print("succeeded = false")
            ping_method = "fail"
        else:
            ping_method = method

        ping_check(baseurl, ping_path, ping_method, ping_body)


if __name__ == "__main__":
    main()
