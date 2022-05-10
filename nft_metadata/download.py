import json
from concurrent.futures import ThreadPoolExecutor, wait, ALL_COMPLETED

import requests

DEFAULT_THREAD_NUM = 10


def chunks(lst, n):
    """Yield successive n-split chunks from lst."""
    each_sized = max(1, len(lst) // n)
    for i in range(0, len(lst), each_sized):
        end = min(i + each_sized, len(lst))
        yield lst[i:end]

def do_fetch(output_dir, job_id, token_urls):
    res = []
    with open(output_dir + "/" + job_id, 'w') as f_w:
        for (each_id, each_url) in token_urls:
            try:
                resp = requests.get(each_url)
                resp_j = resp.json()
                resp_j['id'] = each_id
                res.append(resp_j)
                f_w.write(json.dumps(resp_j))
                f_w.write('\n')
            except Exception as e:
                # print("id: %s, error: %s", (each_id, e))
                pass
    return res

class NftMetadataFetcher:
    def __init__(self, token_urls, output_dir, thread_num=DEFAULT_THREAD_NUM):
        self.token_urls = token_urls
        self.output_dir = output_dir
        self.thread_num = thread_num
        self.tpool = ThreadPoolExecutor(thread_num)

    def start_download(self):
        job_id = 0
        tasks = []
        for sub_token_ids in chunks(self.token_urls, self.thread_num):
            print("Task %s got %d tokens to fetch" % (job_id, len(sub_token_ids)))
            tasks.append(self.tpool.submit(do_fetch, self.output_dir, str(job_id), sub_token_ids))
            job_id += 1
        wait(tasks, return_when=ALL_COMPLETED)

