from queries import *
import psycopg2
from collections import defaultdict
import json
from datetime import datetime
from numpy import mean
import time

BROWSER = "browser"

SPEED_TEST_WEBSITE = "speed_test_website"

PUBLIC_IP = "public_ip"

CONNECTION = "connection"

COMPARISON_INFO = "comparison_info"

OPERATING_SYSTEM = "operating_system"

TEST_ID = "test_id"

VERSION_1_MAX = 21

FILE_DOWNLOAD_START_TIME = "file_download_start_time"

FILE_NAME = "file_name"

SPEED_TEST_START_TIME = "speed_test_start_time"

TEST_POSTGRESQL = "test_postgresql"

SPEED_TEST_RESULT = "speed_test_result_mbs"
SPEED_TEST_RESULT_OLD = "speed_test_result"

FILE_DOWNLOAD_RATE = "file_download_rate_KBs"
FILE_DOWNLOAD_RATE_OLD = "file_download_rate"

FIELD_OK = "field ok"

FILED_FILE_SIZE_BYTES = "file_size_bytes"

FIELD_URL = "url"

OUTER_KEYS = [TEST_ID,
              OPERATING_SYSTEM,
              COMPARISON_INFO,
              CONNECTION,
              PUBLIC_IP,
              SPEED_TEST_WEBSITE,
              BROWSER]

INNER_KEYS = [FIELD_URL,
             FILE_NAME,
             FILED_FILE_SIZE_BYTES,
             FILE_DOWNLOAD_RATE,
              SPEED_TEST_START_TIME,
             FILE_DOWNLOAD_START_TIME,
             SPEED_TEST_RESULT]

INNER_KEYS_OLD = [FIELD_URL,
             FILE_NAME,
             FILED_FILE_SIZE_BYTES,
             FILE_DOWNLOAD_RATE_OLD,
             SPEED_TEST_START_TIME,
             FILE_DOWNLOAD_START_TIME,
             SPEED_TEST_RESULT_OLD]

MIN_TEST_SIZE = 3

COMPARISON_INFO_KEY = COMPARISON_INFO

__author__ = 'orenko'


class AWSWorker:
    def __init__(self):
        self.con = psycopg2.connect("dbname='speedtestProduction' user='DangOren'\
                                         host='speedtestproduction.c6bjskxymj4x.us-west-2.rds.amazonaws.com'\
                                        password='{}'".format(raw_input("enter password")))
        self.cur = self.con.cursor()

    def send_query(self, query, flat=False):
        self.cur.execute(query)
        raw = self.cur.fetchall()
        if flat:
            return [x[0] for x in raw]
        return raw

    def send_command(self, cmd):
        self.cur.execute(cmd)
        self.con.commit()

    def create_table(self, create_command):
        self.send_command(create_command)

    def drop_table(self, table_name):
        confirm = raw_input("drop table: '{}' ARE YOU SURE?!?!".format(table_name))
        if confirm.lower() == "yes":
            self.send_command(DROP_TABLE.format(table_name))
            self.con.commit()

    def delete_row_safe(self, table_name, row_id):
        self.send_command("DELETE FROM {} WHERE id = {}".format(table_name, row_id))
        self.con.commit()

    @classmethod
    def select_all(cls, table_name):
        all_selector = AWSWorker()
        return all_selector.send_query("SELECT * FROM {};".format(table_name))

    @classmethod
    def get_schema(cls, table_name):
        schema_selector = AWSWorker()
        return schema_selector.send_query(SELECT_SCHEMA.format(table_name))


def pretty_print_download_info(rows):
    for row in rows:
        print row[0]
        jsn_pretty_print(row[1])
        print row[2]


def jsn_pretty_print(dic):
    print json.dumps(dic, sort_keys=True,
                     indent=4, separators=(',', ': '))



def get_speed_test(speed_test_id):
    output = []
    speed_test_worker = AWSWorker()
    for table in ALL_TABLES:
        output.append(speed_test_worker.send_query("SELECT * FROM {} WHERE test_id = '{}'".format(table, speed_test_id)))
    return output


def get_grouped():
    grouper = AWSWorker()
    data = grouper.send_query("""SELECT * FROM ISP_speed_test_website_download_info
                              JOIN file_download_info
                              ON ISP_speed_test_website_download_info.test_id = file_download_info.test_id
                              JOIN system_info
                              ON file_download_info.test_id = system_info.test_id""")
    return data


def restart_db():
    from hashlib import md5
    print "WARNING! you are about to DELETE ALL DATA from a remote DB"
    confirm = raw_input("enter password for restarting DB")
    hasher = md5()
    hasher.update(confirm)
    hashed_password = hasher.hexdigest()
    if hashed_password == HASHED_PASS:
        print "authentication passed"
        restarter = AWSWorker()
        restarter.drop_table(TABLE_ISP)
        restarter.drop_table(TABLE_DOWNLOAD_INFO)
        restarter.drop_table(TABLE_SYSTEM_INFO)
        restarter.create_table(CREATE_TABLE_ISP)
        restarter.create_table(CREATE_TABLE_DOWNLOAD_INFO)
        restarter.create_table(CREATE_TABLE_SYSTEM_INFO)
        print "restarting dbs done"
    else:
        print "authentication failed"


def restart_db_auth_test():
    from hashlib import md5
    print "WARNING! you are about to DELETE ALL DATA from a remote DB"
    confirm = raw_input("enter password for restarting DB")
    hasher = md5()
    hasher.update(confirm)
    hashed_password = hasher.hexdigest()
    if hashed_password == HASHED_PASS:
        print "authentication passed"
    else:
        print "authentication failed"


def aggregate_tables():
    aggregator = AWSWorker()
    global_json = defaultdict(list)
    for table in ALL_TABLES:
        table_dump = list(aggregator.send_query(SELECT_ALL.format(table)))
        for x in table_dump:
            payload = [x[0]] + [x[2:]]
            if payload not in global_json [x[1]]:
                global_json [x[1]] += [x[0]] + [x[2:]]
    return global_json


def test_data_json_sanity(data_json):
    for key in OUTER_KEYS:
        assert key in data_json
        print key, FIELD_OK
    print "outer keys test passed"

    tests = data_json[COMPARISON_INFO_KEY].keys()
    assert len(tests) >= MIN_TEST_SIZE
    print "min test number test passed"

    for test_name in tests:
        print "testing:", test_name
        inner_json = data_json[COMPARISON_INFO_KEY][test_name]
        for key in INNER_KEYS:
            assert key in inner_json
            print key, FIELD_OK
        print "\tinner keys test passed"

        assert type(inner_json[FIELD_URL]) == unicode
        assert type(inner_json[FILED_FILE_SIZE_BYTES]) == float
        assert type(inner_json[FILE_NAME]) == unicode
        assert type(inner_json[FILE_DOWNLOAD_START_TIME]) == unicode
        assert type(inner_json[FILE_DOWNLOAD_RATE]) == float
        assert type(inner_json[SPEED_TEST_START_TIME]) == unicode
        assert type(inner_json[SPEED_TEST_RESULT]) == float
        print "\tleaf data type test passed"
        assert parse_time(inner_json[SPEED_TEST_START_TIME]) < \
               parse_time(inner_json[FILE_DOWNLOAD_START_TIME])
        print "timestamp sanity test past"
    print "json test past"


def test_data_json_sanity_old(data_json):
    for key in OUTER_KEYS:
        assert key in data_json
        print key, FIELD_OK
    print "outer keys test passed"

    tests = data_json[COMPARISON_INFO_KEY].keys()
    assert len(tests) >= MIN_TEST_SIZE
    print "min test number test passed"

    for test_name in tests:
        print "testing:", test_name
        inner_json = data_json[COMPARISON_INFO_KEY][test_name]
        for key in INNER_KEYS_OLD:
            assert key in inner_json
            print key, FIELD_OK
        print "\tinner keys test passed"

        assert type(inner_json[FIELD_URL]) == unicode
        assert type(inner_json[FILED_FILE_SIZE_BYTES]) == float
        assert type(inner_json[FILE_NAME]) == unicode
        assert type(inner_json[FILE_DOWNLOAD_START_TIME]) == unicode
        assert type(inner_json[FILE_DOWNLOAD_RATE_OLD]) == float
        assert type(inner_json[SPEED_TEST_START_TIME]) == unicode
        assert type(inner_json[SPEED_TEST_RESULT_OLD]) == float
        print "\tleaf data type test passed"
        assert parse_time(inner_json[SPEED_TEST_START_TIME]) < \
               parse_time(inner_json[FILE_DOWNLOAD_START_TIME])
        print "timestamp sanity test past"
    print "json test past"


def test_download_info_table_sanity(table_dump, mode='permissive'):
    corruption_counter = int()
    for i, row in enumerate(table_dump):
        row_id = row[0]
        print row_id, FILE_DOWNLOAD_RATE
        try:
            ordinal = i+1
            print "test #: %d" % ordinal
            assert type(row[0]) == int
            assert type(row[1]) == dict
            if row_id <= VERSION_1_MAX:
                test_data_json_sanity_old(row[1])
            else:
                test_data_json_sanity(row[1])
            assert type(row[2]) == datetime
            print "sql fields type test passed\n"
        except AssertionError as e:
            print "assertion error in row id: {}".format(row[0])
            corruption_counter += 1
            if mode != 'permissive':
                raise AssertionError(e)
    print "\ntesting done, number of corrupted rows: %d, out of total: %d" % (corruption_counter, ordinal)


def mBit_toKByte(num):
    return num / 8 * 2**10


def aggregate_speed_diffs(data, rounded=False):
    diffs = []
    for row in data:
        jsn = row[1]
        for test in jsn[COMPARISON_INFO_KEY].keys():
            speed_test_key = SPEED_TEST_RESULT if SPEED_TEST_RESULT in jsn[COMPARISON_INFO_KEY][test] else SPEED_TEST_RESULT_OLD
            download_rate_key = FILE_DOWNLOAD_RATE if FILE_DOWNLOAD_RATE in jsn[COMPARISON_INFO_KEY][test]  else FILE_DOWNLOAD_RATE_OLD
            actual_rate = jsn[COMPARISON_INFO_KEY][test][download_rate_key]
            expected_rate = mBit_toKByte(jsn[COMPARISON_INFO_KEY][test][speed_test_key])
            diffs.append(actual_rate/expected_rate)
    if rounded:
        return [round(x, 2) for x in diffs]
    return diffs


def parse_time(datetime_str):
    datetime_str.replace(":", "-")
    dt = datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:%S')
    return time.mktime(dt.timetuple())

if __name__ == "__main__":
    worker = AWSWorker()
    data = worker.send_query(SELECT_ALL.format(TABLE_NAME_SEMI_STRUCTURED))
    pretty_print_download_info(data)
    test_download_info_table_sanity(data)
    diff = aggregate_speed_diffs(data, rounded=True)
    print diff
    print "percent of speed-test prediction actually used:", str(round(mean(diff)*100, 2))+"%"
    print "number of global tests", len(data)
    print "number of small tests", len(diff)
    quit()
