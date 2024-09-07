import os
import sys
from typing import NotRequired, TypedDict

import dotenv
import requests

dotenv.load_dotenv(verbose=True)
dotenv.load_dotenv(os.path.join(".", ".env"))

api_endpoint = "https://api.coreserver.jp"
access_request_url = "/v1/tool/ssh_ip_allow"


class ResultJson(TypedDict):
    status_code: int
    message: NotRequired[str]
    error_target: NotRequired[str]
    error_message: NotRequired[str]
    error_code: NotRequired[int]


def date_stamp() -> str:
    import datetime

    t_delta = datetime.timedelta(hours=9)
    JST = datetime.timezone(t_delta, "JST")
    now = datetime.datetime.now(JST)
    return now.strftime("%Y/%m/%d %H:%M:%S")


def main() -> int:
    ip = requests.get("https://api.ipify.org").content.decode("utf8")
    body = {
        "account": os.environ.get("CS_USER"),
        "server_name": os.environ.get("CS_SERVER"),
        "api_secret_key": os.environ.get("API_KEY"),
        "param[addr]": ip,
    }

    response = requests.post(
        api_endpoint + access_request_url,
        data=dict(body),
    )

    # WTF: Coreserver's HTTP status code is always 200,
    #      but the actual status code is within the JSON.
    result: ResultJson = response.json()
    if result["status_code"] != 200:
        print(
            (
                "Unexpected response from server!\n"
                f"Error target: {result.get('error_target', '')}, "
                f"Error message: {result.get('error_message', '')}, "
                f"Error code: {result.get('error_code', '')}"
            ),
            file=sys.stderr,
        )
        with open("err.log", "a") as fp:
            import json

            fp.write(
                (
                    f"[{date_stamp()}] API request failure: "
                    f"{json.dumps(result.__dict__)}\n"
                )
            )
        return 1

    with open("run.log", "a") as fp:
        fp.write(
            (
                f"[{date_stamp()}] "
                "Successfully sent API request for SSH permission\n"
            )
        )

    return 0


if __name__ == "__main__":
    exit(main())
