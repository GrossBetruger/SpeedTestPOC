import json
import zipfile
import os
import requests
import pprint
from numpy import mean
from itertools import chain
from collections import Counter

TESTS_CACHE = "tests_cache"

TOKEN_PATH = "/home/shanip/.token"

EXCTRACTED_TOKEN_PATH = "token.aws"

SPEED_TEST_IDENTIFIER = 'speedTestIdentifier'

SPEED_TEST_WEB_SITE = 'speedTestWebSite'

GET_TESTS_URL = "http://ec2-52-28-182-127.eu-central-1.compute.amazonaws.com:8008/central/all-tests"

try:
    from local_settings import *
except ImportError:
    print "local settings not found"


def decrypt_token(token_path):
    zipfile.ZipFile(token_path).extractall(path=".", pwd=raw_input("password?\n"))
    with open(EXCTRACTED_TOKEN_PATH) as f:
        token = f.read().strip()
    os.unlink(EXCTRACTED_TOKEN_PATH)
    return token


def get_tests(token):
    return requests.get(GET_TESTS_URL, 
            headers={"Authorization": token,
                    "Case-Yellow-User": "oren"}).json()


def get_comparisons(tests):
    return [t.get("comparisonInfoTests") for t in tests]


def compare(test, debug=True):
    download_rate_KBs = test.get('fileDownloadInfo').get('fileDownloadRateKBPerSec')
    speedtest_rate_KBs = test.get(SPEED_TEST_WEB_SITE).get('downloadRateInKBps')
    ratio = float(download_rate_KBs) / speedtest_rate_KBs
    if debug:
        print "website:", test.get(SPEED_TEST_WEB_SITE).get(SPEED_TEST_IDENTIFIER)
        print "download rate:", download_rate_KBs
        print "speedtest rate", speedtest_rate_KBs
        print "ratio:", ratio
    return ratio


def sieve_websites(speedtest_website, test):
    return [comparison for comparison in test
            if comparison.get(SPEED_TEST_WEB_SITE)
            .get(SPEED_TEST_IDENTIFIER) == speedtest_website]


def get_website_average_ratio(website, tests):
    comparisons = get_comparisons(tests)
    filtered_comparisons = [sieve_websites(website, comparison) for comparison in comparisons]
    subtests = list(chain(*[subtest for subtest in [comparison for comparison in filtered_comparisons if comparison]]))
    if len(subtests) == 0:
        raise Exception("no subtests found!")
    print "number of subtests:", len(subtests)
    ratios = [compare(subtest, debug=False) for subtest in subtests]
    return mean(ratios)


def count_ips():
    counter = Counter()
    ips = [test.get("systemInfo").get("publicIP") for test in get_tests()]
    for ip in ips:
        counter.update([ip])
    for k, v in dict(counter).iteritems():
        print k, v


def readtoken(token_path):
    with open(token_path) as f:
        return f.read().strip()


def cache_tests(tests, cache_path):
    with open(cache_path, "w") as f:
        json.dump(tests, f)


def read_tests_from_cache(cache_path):
    with open(cache_path) as f:
        return json.load(f)


def sieve_users(tests, users):
    return [test for test in tests if test.get("user") and test.get("user") in users]



def main():
    website = raw_input("choose website... (atnt, hot, etc.)\n")
    ratios =  get_website_average_ratio(website, get_tests())
    print "{} ratio:".format(website), ratios




if __name__ == "__main__":
    TOKEN = readtoken(TOKEN_PATH)

    from_cache = raw_input("read from cache?\n")
    from_cache = True if from_cache.lower() == "yes" else False
    if from_cache:
        tests = read_tests_from_cache(TESTS_CACHE)
    else:
        tests = get_tests(TOKEN)
        cache_tests(tests, TESTS_CACHE)

    c = Counter()
    c.update([x.get('user') for x in tests if x.get('user')])
    print c
    for user in ["admin", "oren"]:
        print "stas for user:", user.upper()
        for website in ["hot", "bezeq", "ookla", "atnt", "speedof", "fast"]:
            print "stats for website:", website
            try:
                print get_website_average_ratio(website, sieve_users(tests, [user]))
                print
            except Exception as e:
                print "something went wrong... is Dango typing? ({})".format(e.message or e)
                print
    quit()
