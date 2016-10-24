from queries import *
import psycopg2


__author__ = 'orenko'


class AWSWorker:
    def __init__(self):
        self.con = psycopg2.connect("dbname='speed_test' user='DangOren'\
                                         host='speed-test.c6bjskxymj4x.us-west-2.rds.amazonaws.com'\
                                        password='{}'".format("".join([chr(x) for x in PASS])))
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


def pretty_print(rows):
    for row in rows:
        print ", ".join([str(x) for x in row])


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


def print_all():
    for table in TABLE_ISP, TABLE_SYSTEM_INFO, TABLE_DOWNLOAD_INFO:
        pretty_print(AWSWorker.select_all(table))


if __name__=="__main__" :

    print_all()
    quit()

    worker = AWSWorker()
    for i in range(0):
        for table in ALL_TABLES:
            worker.delete_row_safe(table, i)
    print_all()
    quit()

    grouped = get_grouped()
    for i in grouped:
        print i
    quit()

    for t in ALL_TABLES:
        print t
    quit()
    # create_table()
    worker = AWSWorker()



    # worker.delete_row_safe(TABLE_ISP, 3)
    # worker.send_command(MOCK_INSERT_ISP)
    # create_table(CREATE_TABLE_ISP)
    # worker.create_table(CREATE_TABLE_DOWNLOAD_INFO)

    # pretty_print(AWSWorker.select_all(TABLE_ISP))
    # for i in get_speed_test("c441e895-03d2-4875-a4a6-73041266eea2"):
    #     print i

    # print AWSWorker.get_schema(TABLE_DOWNLOAD_INFO)
    print_all()


    worker = AWSWorker()
    for i in range(50, 80):
        for table in ALL_TABLES:
            worker.delete_row_safe(table, i)


    # worker = AWSWorker()
    # worker.drop_table(TABLE_ISP)
    # worker.drop_table(TABLE_DOWNLOAD_INFO)
    # worker.drop_table(TABLE_SYSTEM_INFO)
    # worker.create_table(CREATE_TABLE_ISP)
    # worker.create_table(CREATE_TABLE_DOWNLOAD_INFO)
    # worker.create_table(CREATE_TABLE_SYSTEM_INFO)
    # print_all()
    # print "done"
    # quit()