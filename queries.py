__author__ = 'orenko'


TABLE_SYSTEM_INFO = "system_info"
TABLE_DOWNLOAD_INFO = "file_download_info"
TABLE_ISP = "ISP_speed_test_website_download_info"
ALL_TABLES = (TABLE_ISP, TABLE_SYSTEM_INFO, TABLE_DOWNLOAD_INFO)

CREATE_TABLE_SYSTEM_INFO =\
    """
    CREATE TABLE system_info (
     ID SERIAL PRIMARY KEY,
     test_id VARCHAR(100) NOT NULL,
     operating_system VARCHAR(45) NOT NULL,
     browser VARCHAR(20) NOT NULL,
     public_IP VARCHAR(45) NOT NULL,
     connection VARCHAR(20) NOT NULL);
    """

CREATE_TABLE_DOWNLOAD_INFO =\
    """
    CREATE TABLE file_download_info (
     ID SERIAL PRIMARY KEY,
     test_id VARCHAR(100) NOT NULL,
     file_url VARCHAR(100) NOT NULL,
     file_name VARCHAR(100) NOT NULL,
     file_size_in_bytes FLOAT NOT NULL,
     file_downloaded_time_in_ms BIGINT NOT NULL,
     file_download_rate_KBs FLOAT NOT NULL,
     startDownloadingTime VARCHAR(45) NOT NULL);
    """

CREATE_TABLE_ISP =\
    """
    CREATE TABLE ISP_speed_test_website_download_info (
     ID SERIAL PRIMARY KEY,
     test_id VARCHAR(100) NOT NULL,
     name VARCHAR(45) NOT NULL,
     download_speed_rate_mbs FLOAT NOT NULL,
     start_measuring_time VARCHAR(40) NOT NULL);
    """

MOCK_INSERT_SYSTEM_INFO =\
    """
    INSERT INTO system_info
    (
     test_id,
     operating_system,
     browser,
     public_IP,
     connection)

    VALUES ('0', 'IOS', 'dango0', '127.0.0.1', 'fastAsFuck');
    """


MOCK_INSERT_SYSTEM_INFO_PARTIAL =\
    """
    INSERT INTO system_info
    (
     test_id,
     operating_system,
     browser,
     public_IP,
     connection) VALUES ('0', 'IOS', 'dango0', '127.0.0.1', 'fastAsFuck');
    """

MOCK_INSERT_DOWNLOAD_INFO =\
    """
    INSERT INTO file_download_info
    (test_id,
    file_url,
    file_name,
    file_size_in_bytes,
    file_downloaded_time_in_ms,
    file_download_rate_KBs,
    startDownloadingTime)
    VALUES ('0', 'aws.dango.efes', 'dango0', '512', 1200, 1000, '1922-12-12');
    """

MOCK_INSERT_ISP =\
    """
    INSERT INTO ISP_speed_test_website_download_info
    (
    test_id,
    name,
    download_speed_rate_mbs,
    start_measuring_time)
    VALUES ('0', 'dango0', 99.5, '1970-01-01');
    """

SELECT_ALL = "SELECT * FROM system_info;"

DROP_TABLE = "DROP TABLE {};"

SELECT_SCHEMA = """SELECT column_name, data_type, character_maximum_length
                from INFORMATION_SCHEMA.COLUMNS WHERE table_name = '{}';"""


NATURAL_VIEW =\
"""
SELECT file_name, download_speed_rate_mbs/8*2^10,
  file_download_rate_kbs, connection, public_ip, test_id
FROM system_info
  NATURAL JOIN file_download_info
  NATURAL JOIN isp_speed_test_website_download_info
"""