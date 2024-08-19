from os import environ
import logging
import requests
import json
from urllib.parse import urlparse
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
import base64

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

def load_public_key_base64(public_key_base64):
    return RSA.import_key(base64.b64decode(public_key_base64))

def verify_signature(message, signature_base64, public_key_base64):
    public_key = load_public_key_base64(public_key_base64)
    h = SHA256.new(message.encode('utf-8'))
    try:
        pkcs1_15.new(public_key).verify(h, base64.b64decode(signature_base64))
        return True
    except (ValueError, TypeError):
        return False

public_keys = {}

def handle_advance(data):
    logger.info(f"Received advance request data {data}")
    payload = json.loads(hex2str(data["payload"]))

    action = payload["action"]
    key = payload["key"]
    signature = payload["signature"]
    message = payload.get("message", "")

    if not verify_signature(message, signature, key):
        notice = {"payload": str2hex(f"Invalid message signature.")}
    elif action == "register":
        if verify_signature(message, signature, key):
            public_keys[key] = {"status": "active", "signature": signature}
            notice = {"payload": str2hex(f"Key {key} registered successfully.")}
        else:
            notice = {"payload": str2hex(f"Invalid message signature.")}
    elif action == "revoke":
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
