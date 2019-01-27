import requests
from requests.exceptions import ConnectionError
import random
import os
import time
from bs4 import BeautifulSoup
from pyquery import PyQuery as pq

reuseProxy = False
successFulProxy ={}
maxRetriesCount = 0
class RequestProxy:
    agent_file = 'useragents.txt'

    def __init__(self, web_proxy_list=[]):
        self.useragents = self.load_user_agents(RequestProxy.agent_file)
        #####
        # Proxy format:
        # http://<USERNAME>:<PASSWORD>@<IP-ADDR>:<PORT>
        #####
        self.proxy_list = web_proxy_list
        self.proxy_list += self.freeProxy_url_parser('http://free-proxy-list.net')

        self.proxy_list += self.freeProxy_url_parser('http://www.sslproxies.org/')

    def get_proxy_list(self):
        return self.proxy_list

    def load_user_agents(self, useragentsfile):
        useragents = []
        with open(useragentsfile, 'rb') as uaf:
            for ua in uaf.readlines():
                if ua:
                    useragents.append(ua.strip()[1:-1-1])
        random.shuffle(useragents)
        return useragents

    def get_random_user_agent(self):
        user_agent = random.choice(self.useragents)
        return user_agent

    def generate_random_request_headers(self):
        headers = {
            "Connection": "close",  # another way to cover tracks
            "User-Agent": self.get_random_user_agent()
        }
        return headers

    def freeProxy_url_parser(self, web_url):
        curr_proxy_list = []
        content = requests.get(web_url).content
        soup = BeautifulSoup(content, "html.parser")
        table = soup.find("table", attrs={"id": "proxylisttable"})

        # The first tr contains the field names.
        headings = [th.get_text() for th in table.find("tr").find_all("th")]

        datasets = []
        for row in table.find_all("tr")[1:]:
            dataset = zip(headings, (td.get_text() for td in row.find_all("td")))
            datasets.append(dataset)

        for dataset in datasets:
            # Check Field[0] for tags and field[1] for values!
            proxy = "https://"
            IsHttps = False
            for field in dataset:
                if field[0] == 'IP Address':
                    proxy = proxy+field[1]+':'
                elif field[0] == 'Port':
                    proxy = proxy+field[1]

                if field[0] == 'Https':
                    if field[1] == "yes":
                        IsHttps = True

            if IsHttps:
                curr_proxy_list.append(proxy.__str__())
        return curr_proxy_list

    def generate_proxied_request(self, url, params={}, req_timeout=5):
        global successFulProxy
        global maxRetriesCount
        try:
                request = None
                if self.proxy_list.__len__() <=5:
                    req_proxy = RequestProxy()

                random.shuffle(self.proxy_list)
                req_headers = dict(params.items() + self.generate_random_request_headers().items())

                if successFulProxy != None and successFulProxy != {}:
                    rand_proxy = successFulProxy
                else:
                    rand_proxy = random.choice(self.proxy_list)

                    request = None
                    USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36'
                    req_headers = {'User-Agent': USER_AGENT,}
                    request = requests.get(test_url, proxies={"https": rand_proxy},headers=req_headers, timeout=req_timeout)
        except ConnectionError:
            self.proxy_list.remove(rand_proxy)
            print "Proxy unreachable :", rand_proxy, " PL Size = ",len(self.proxy_list)
            successFulProxy = None
            return self.generate_proxied_request(url)
            #pass
        except Exception as e:
            self.proxy_list.remove(rand_proxy)
            print "Read timed out - :", rand_proxy, " PL Size = ", len(self.proxy_list)
            successFulProxy = None
            return self.generate_proxied_request(url)

        if (not type(request) == type(None)) or successFulProxy != None:
                try:
                    if not type(request) == type(None):
                        ipAdd = request.text
                    else:
                        ipAdd = successFulProxy

                    USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36'
                    req_headers = {'User-Agent': USER_AGENT,}
                    data = requests.get(url, proxies={"https": rand_proxy},headers=req_headers, timeout=10)

                    print(str(data.status_code) + " :: "+ ipAdd)

                    if data.status_code!=999:
                        successFulProxy = rand_proxy
                        time.sleep(3)
                        maxRetriesCount = 0
                        return data
                    else:
                        self.proxy_list.remove(rand_proxy)
                        maxRetriesCount = 0
                        successFulProxy = None
                        return self.generate_proxied_request(url)

                except Exception as e:
                    print("inkedin error" + str(e))
                    maxRetriesCount = maxRetriesCount+1
                    if maxRetriesCount == 5:
                        successFulProxy = None
                    return self.generate_proxied_request(url)
            #pass
        return ""
test_url = 'https://icanhazip.com'

if __name__ == '__main__':

    start = time.time()
    req_proxy = RequestProxy()
    print "Initialization took: ", (time.time()-start)
    print "Size : ", len(req_proxy.get_proxy_list())
    print " ALL = ", req_proxy.get_proxy_list()

    test_url = 'https://icanhazip.com'

    while True:
        start = time.time()
        request = req_proxy.generate_proxied_request(test_url)
