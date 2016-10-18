__author__ = 'orenko'

import requests

jdk_url = "http://download.oracle.com/otn-pub/java/jdk/8u60-b27/jre-8u60-linux-x64.rpm"

def get_jdk(jdk_url):
    cookies = dict(gpw_e24="http%3A%2F%2Fwww.oracle.com%2F", oraclelicense="accept-securebackup-cookie")
    payload = {'User-Agent': 'Mozilla/5.0'}
    return requests.get(jdk_url, headers=payload, cookies=cookies)

with open("jdk.rpm", "wb") as f:
    f.write(get_jdk(jdk_url).content)