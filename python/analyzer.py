import json
import zipfile
import os
import datetime
import requests
import shutil

from numpy import mean
from itertools import chain
from collections import Counter

BACKUP = "backup"

USERS = ["admin", "oren", "eli"]

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


def KBps_to_mbps(KBps):
    return KBps * 0.008


def get_average_speed(tests):
    comparisons = get_comparisons(tests)
    comparisons = list(chain(*[subtest for subtest in comparisons]))
    return KBps_to_mbps(mean([comparison.get('fileDownloadInfo').get('fileDownloadRateKBPerSec')
                 for comparison in comparisons]))


def get_website_average_result(website, tests):
    comparisons = get_comparisons(tests)
    filtered_comparisons = [sieve_comparisons_by_websites(website, comparison) for comparison in comparisons]
    subtests = list(chain(*[subtest for subtest in [comparison for comparison in filtered_comparisons if comparison]]))
    return KBps_to_mbps(mean([subtest.get(SPEED_TEST_WEB_SITE).get('downloadRateInKBps')
                 for subtest in subtests]))



def sieve_comparisons_by_websites(speedtest_website, test):
    return [comparison for comparison in test
            if comparison.get(SPEED_TEST_WEB_SITE)
            .get(SPEED_TEST_IDENTIFIER) == speedtest_website]


def sieve_tests_by_website(tests, website):
    return [test for test in tests if test.get('speedTestWebsiteIdentifier') == website]


def get_website_average_ratio(website, tests):
    comparisons = get_comparisons(tests)
    filtered_comparisons = [sieve_comparisons_by_websites(website, comparison) for comparison in comparisons]
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


def get_weekday_from_test(test):
    start_time = test['startTime'] / 1000
    stamp = datetime.datetime.fromtimestamp(start_time)
    return stamp.weekday()


def sieve_weekday(tests, weekday):
    return [test for test in tests if get_weekday_from_test(test) == weekday]


def main():
    website = raw_input("choose website... (atnt, hot, etc.)\n")
    ratios =  get_website_average_ratio(website, get_tests())
    print "{} ratio:".format(website), ratios


def get_latest_test_time(tests):
    last_test = max([test['endTime'] / 1000 for test in tests if test.get('endTime')])
    return datetime.datetime.fromtimestamp(last_test)


def backup_tests():
    stamp = "".join(str(datetime.datetime.now()).split(".")[:-1]).replace(" ", "_")
    backup_file_path = os.path.join(BACKUP, TESTS_CACHE + "_" + stamp)
    shutil.copy(TESTS_CACHE, backup_file_path)
    print "copied tests backup to: {}".format(backup_file_path)


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
    user_count = dict(c)
    print "\nuser count:"
    for k, v in user_count.items():
        print k, ":", v
    print
    users = user_count.keys()
    websites = set([test.get("speedTestWebsiteIdentifier")
                    for test in tests
                    if test.get("speedTestWebsiteIdentifier")])

    for user in users:
        print "stas for user:", user.upper()
        for website in websites:
            print "stats for website:", website
            try:
                user_tests = sieve_users(tests, [user])
                print get_website_average_ratio(website, user_tests)
            except Exception as e:
                print "something went wrong... is Dango typing? ({})".format(e.message or e)
                print
        try:
            print "user average speed (mbps):", get_average_speed(user_tests)
            print "user average speedtest result HOT (mbps):", \
                get_website_average_result("hot", user_tests)
            print "user average speedtest result BEZEQ (mbps):", \
                get_website_average_result("bezeq", user_tests)
            print "user average speedtest result NETFLIX (mbps):", \
                get_website_average_result("fast", user_tests)
            user_sys_info = user_tests[-1].get("systemInfo")
            print "user Infra:", user_sys_info.get("infrastructure")
            print "user ISP:", user_sys_info.get("isp")
            print "user last test:", get_latest_test_time(user_tests)
            print

        except Exception as e:
            print "something went wrong... is Dango typing? ({})".format(e.message or e)
            print

    timestamped_tests = [test for test in tests if test.get("startTime")]
    print

    for website in websites:
        print "global average for website:", website
        print get_website_average_ratio(website, tests)
        print "last test:", get_latest_test_time(sieve_tests_by_website(tests, website))
        print

    print "sunday tests", len(sieve_weekday(timestamped_tests, 6))
    print "saturday tests", len(sieve_weekday(timestamped_tests, 5))
    print "friday tests", len(sieve_weekday(timestamped_tests, 4))
    print "thursday tests", len(sieve_weekday(timestamped_tests, 3))
    print "wednesday tests", len(sieve_weekday(timestamped_tests, 2))
    print "tuesday tests", len(sieve_weekday(timestamped_tests, 1))
    print "monday tests", len(sieve_weekday(timestamped_tests, 0))

    # print get_latest_test_time(sieve_tests_by_website(tests, "speedof"))
    quit()
