import requests
import pprint
from numpy import mean
from itertools import chain
from collections import Counter

SPEED_TEST_IDENTIFIER = 'speedTestIdentifier'

SPEED_TEST_WEB_SITE = 'speedTestWebSite'

GET_TESTS_URL = "http://ec2-35-156-136-73.eu-central-1.compute.amazonaws.com:8080/central/all-test"


def get_tests():
    return requests.get(GET_TESTS_URL).json()


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


def main():
    website = raw_input("choose website... (atnt, hot, etc.)\n")
    ratios =  get_website_average_ratio(website, get_tests())
    print "{} ratio:".format(website), ratios


if __name__ == "__main__":
    print "public ip count:"
    count_ips()
    print
    while True:
        try:
            print
            main()
            print
        except Exception:
            print "something went wrong... is Dango typing?"
