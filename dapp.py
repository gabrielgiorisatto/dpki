from os import environ
import logging
import requests
import json
from urllib.parse import urlparse

logging.basicConfig(level="INFO")
logger = logging.getLogger(__name__)

rollup_server = environ["ROLLUP_HTTP_SERVER_URL"]
logger.info(f"HTTP rollup_server url is {rollup_server}")

def hex2str(hex):
    """
    Decodes a hex string into a regular string
    """
    return bytes.fromhex(hex[2:]).decode("utf-8")

def str2hex(str):
    """
    Encodes a string as a hex string
    """
    return "0x" + str.encode("utf-8").hex()

# Simulate a simple in-memory storage for keys (in production, consider using a database)
public_keys = {}

def handle_advance(data):
    logger.info(f"Received advance request data {data}")
    payload = json.loads(hex2str(data["payload"]))

    # Parse the payload (this could be in JSON format or another suitable format)
    action = payload["action"]
    key = payload["key"]
    signature = payload["signature"]

    if action == "register":
        # Logic to register the public key
        public_keys[key] = {"status": "active", "signature": signature}
        notice = {"payload": str2hex(f"Key {key} registered successfully.")}
    elif action == "revoke":
        # Logic to revoke the public key
        if key in public_keys and public_keys[key]["status"] == "active":
            public_keys[key]["status"] = "revoked"
            notice = {"payload": str2hex(f"Key {key} revoked successfully.")}
        else:
            notice = {"payload": str2hex(f"Key {key} not found or already revoked.")}
    else:
        notice = {"payload": str2hex("Invalid action.")}

    response = requests.post(rollup_server + "/notice", json=notice)
    logger.info(f"Received notice status {response.status_code} body {response.content}")
    return "accept"

def handle_inspect(data):
    logger.info(f"Received inspect request data {data}")
    url = urlparse(hex2str(data["payload"]))
    # key = hex2str(data["key"])
    key = url.path.replace("key/", "").split("/")[0]
    logger.info(f"URL {url} KEY {key}")
    if key in public_keys:
        report = {"payload": str2hex(json.dumps(public_keys[key]))}
    else:
        report = {"payload": str2hex(f"Key {key} not found.")}
    response = requests.post(rollup_server + "/report", json=report)
    logger.info(f"Received report status {response.status_code}")
    return "accept"

handlers = {
    "advance_state": handle_advance,
    "inspect_state": handle_inspect
}

finish = {"status": "accept"}

while True:
    logger.info("Sending finish")
    response = requests.post(rollup_server + "/finish", json=finish)
    logger.info(f"Received finish status {response.status_code}")
    if response.status_code == 202:
        logger.info("No pending rollup request, trying again")
    else:
        rollup_request = response.json()
        handler = handlers[rollup_request["request_type"]]
        finish["status"] = handler(rollup_request["data"])
