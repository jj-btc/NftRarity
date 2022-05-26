import json
import requests

# Borrowed from some stackoverflow answer, but i couldn't find the source
# fetch abi from etherscan
ABI_ENDPOINT = 'https://api.etherscan.io/api?module=contract&action=getabi&address='

def fetch_abi(contract_address):
    response = requests.get('%s%s' % (ABI_ENDPOINT, contract_address))
    response_json = response.json()
    abi_json = json.loads(response_json['result'])

    return json.dumps(abi_json, indent=4, sort_keys=True)


