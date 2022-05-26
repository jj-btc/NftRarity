import concurrent
import json
from concurrent.futures import ThreadPoolExecutor

from unamed_utils.abi import fetch_abi
from web3 import Web3

from nft_metadata.download import chunks

DEFAULT_THREAD_NUM = 20

def do_get_uri(w3_contract, token_ids):
    res = {}
    for each_id in token_ids:
        md_uri = w3_contract.functions.tokenURI(each_id).call()
        res[each_id] = md_uri
    return res

class NftMetadataUri:

    def __init__(self, token_ids, contract_addr, ws_node_url, abi_path=None):
        self.contract_addr = Web3.toChecksumAddress(contract_addr)
        if abi_path:
            with open(abi_path, 'r') as abi_f:
                self.contract_abi = json.load(abi_f)
        else:
            self.contract_abi = json.loads(fetch_abi(contract_addr))

        self.w3 = Web3(Web3.HTTPProvider(ws_node_url))
        self.contract = self.w3.eth.contract(address=self.contract_addr, abi=self.contract_abi)
        self.token_uris = {}
        self.token_ids = token_ids
        self.tpool = ThreadPoolExecutor(DEFAULT_THREAD_NUM)

    def get_all_md_uri(self):
        job_id = 0
        futures = []
        for sub_token_ids in chunks(self.token_ids, DEFAULT_THREAD_NUM):
            print("Task %s got %d tokens to fetch" % (job_id, len(sub_token_ids)))
            # sub_res = do_get_uri(self.contract, sub_token_ids)
            futures.append(self.tpool.submit(do_get_uri, self.contract, sub_token_ids))
            job_id += 1

        for each_f in concurrent.futures.as_completed(futures):
            self.token_uris.update(each_f.result())

        return self.token_uris