import requests
import pprint

GET_TESTS_URL = "http://ec2-35-156-136-73.eu-central-1.compute.amazonaws.com:8080/central/all-test"


def get_tests():
    return requests.get(GET_TESTS_URL).json()


def get_comparisons(tests):
    return [t.get("comparisonInfoTests") for t in tests]



def compare(filedownload_info, debug=True):
    download_rate_KBs = filedownload_info.get('fileDownloadInfo').get('fileDownloadRateKBPerSec')
    speedtest_rate_KBs =  filedownload_info.get('speedTestWebSite').get('downloadRateInKBps')
    ratio = float(download_rate_KBs) / speedtest_rate_KBs
    if debug:
        print "website:", filedownload_info.get('speedTestWebSite').get('speedTestIdentifier')
        print "download rate:", download_rate_KBs
        print "speedtest rate", speedtest_rate_KBs
        print "ratio:", ratio
    return ratio


if __name__ == "__main__":
    pp = pprint.PrettyPrinter(indent=1)
    for comparison in get_comparisons(get_tests()[-3:]):
        for test in comparison:
            pp.pprint(test)
            compare(test)
            print
        print "-------------------\n"*3
