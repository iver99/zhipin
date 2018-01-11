from bs4 import BeautifulSoup as bs
import logging.config
from os import path
from urllib import request
import json
from job_details_model import JobItem
# location 北京(c101010100)，搜索关键字java
url = "https://www.zhipin.com/c101010100/h_101010100/?query=java&page="
base_url = "https://www.zhipin.com"

log_file_path = path.join(path.dirname(path.abspath(__file__)), 'logging.conf')
logging.config.fileConfig(log_file_path)
logger = logging.getLogger('main')

def obj_dict(obj):
    return obj.__dict__

def fetch_job_details():
    max_page = 5
    index = 0
    with open('output.txt', 'w',encoding = 'utf-8') as f:
        for x in range(max_page):
            specific_page = url + str(x+1)
            logger.info("请求url为: "+ specific_page)
            resp = request.urlopen(specific_page)
            html_data = resp.read().decode('utf8')
            soup = bs(html_data, 'html.parser')
            # 每一页有默认15个job
            jobs_in_page = soup.find_all("div", class_="job-primary")
            # print(jobs_in_page)
            for job_items in jobs_in_page:
                job_item = JobItem()
                job_item.job_title = job_items.a.text
                job_item.url = base_url + job_items.a["href"]
                logger.info(job_items.a["href"])
                logger.info(job_items.a.text)
                print(json.dumps(job_item, default=obj_dict))
                # f.write(json.dumps(job_item, default=obj_dict))
                # f.write('\n')

    # print(demjson.encode(output))
    # 保存到文件


if __name__ == '__main__':
    fetch_job_details()

