import operator
import sys
import urllib.request
import json
import os

URL = 'https://ncfnodes.acrylminer.com/addresses/data/{receiver_address}'
DATA_KEY = ""


def main():
    if len(sys.argv) > 2 or len(sys.argv) <= 1:
        print(f"Usage: {os.path.basename(sys.argv[0])} receiver_address sender_address")
        sys.exit(1)

    receiver_address = sys.argv[1]
    api_request = urllib.request.urlopen(URL.format(receiver_address=receiver_address, headers={"Accept": "application/json"}))
    json_result = api_request.read()
    data_list = json.loads(json_result, encoding='utf-8')
    if not data_list:
        print(f"No data transactions found")
        sys.exit(1)

    for transaction_data in data_list:
        if transaction_data["key"] == "latest_update_data":
            latest_update_string = transaction_data["value"]
            break
    else:
        sys.exit(1)

    print(latest_update_string)
    return 0


if __name__ == '__main__':
    main()

