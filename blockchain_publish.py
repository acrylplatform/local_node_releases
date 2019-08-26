import hashlib
import json
import os
import sys
import urllib

import pyacryl

GITHUB_RELEASES_URL = "https://api.github.com/repos/acrylplatform/local_node_releases/releases/latest"

pyacryl.setNode(node="https://nodes.acrylplatform.com", chain="mainnet", chain_id="A")
pyacryl.setChain(chain="mainnet", chain_id="A")


def get_package_sha265(hashing_file_path):
    hash_ = hashlib.sha256()
    with open(hashing_file_path, 'rb') as hashing_file:
        while True:
            data = hashing_file.read(65536)
            if not data:
                break

            hash_.update(data)

    hash_digest = hash_.hexdigest()
    return hash_digest


def main():
    if len(sys.argv) > 2 or len(sys.argv) <= 1:
        print(f"Usage: {os.path.basename(sys.argv[0])} package_file_name")
        sys.exit(1)

    package_file_name = sys.argv[1]

    sender_private_key = os.getenv("ACRYL_SENDER_ADDRESS_PRIVATE_KEY")
    if not sender_private_key:
        print("Sender private key is not set. Set ACRYL_SENDER_ADDRESS_PRIVATE_KEY env variable", file=sys.stderr)
        sys.exit(1)

    sender_address = pyacryl.Address(privateKey=sender_private_key)
    api_request = urllib.request.urlopen(GITHUB_RELEASES_URL)
    json_result = api_request.read()
    release_data = json.loads(json_result, encoding='utf-8')
    for asset in release_data["assets"]:
        if asset["name"] == os.path.basename(package_file_name):
            package_url = asset["browser_download_url"]
            break

    else:
        print("No package file found", file=sys.stderr)
        sys.exit(1)

    sha256_checksum = get_package_sha265(package_file_name)
    update_data = {
        "rpm_package_url": package_url,
        "sha256_checksum": sha256_checksum
    }
    result = sender_address.dataTransaction(
        [{'key': 'latest_update_data', 'value': json.dumps(update_data), 'type': 'string'}]
    )

    if "error" in result and result["error"] is not None:
        if "message" in result:
            print(f"Transaction error: {result['message']}", file=sys.stderr)
        else:
            print(f"Transaction error: {result['error']}", file=sys.stderr)

        sys.exit(1)

    print(f"Blockchain data update successful! Txid: {result['id']}")

    return


if __name__ == "__main__":
    main()