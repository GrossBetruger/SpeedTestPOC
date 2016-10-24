__author__ = 'orenko'

import json

template = {"test_id" :"a19f06fa-abe9-4f63-b151-cb37bb761069",
             "test_kodi" : {"url": "http://mirrors.kodi.tv/releases/osx/x86_64/kodi-16.1-Jarvis-x86_64.dmg",
                            "file_name": "kodi-16.1-Jarvis-x86_64.dmg",
                            "file_size_bytes": 68666613,
                            "speed_test_start_time": "2016-10-24 04:00:48",
                            "download_test_time": "2016-10-24 04:01:28",
                            "speed_test_result": 32.71,
                            "file_download_rate": 1031.65,
                            },
            "test_firefox" : {"url": "https://ftp.mozilla.org/pub/firefox/releases/37.0b1/win32/en-US/Firefox%20Setup%2037.0b1.exe",
                            "file_name": "Firefox Setup 37.0b1.exe",
                            "file_size_bytes": 40797024,
                            "speed_test_start_time": "2016-10-24 04:02:54",
                            "download_test_time": "2016-10-24 04:03:26",
                            "speed_test_result": 33.48,
                            "file_download_rate": 2343.58,
                            },
            "operating_system" : "WINDOWS 10",
            "browser": "FIREFOX",
            "ISP": "HOT",
            "connection": "WIFI",
            "public_ip": "37.142.192.249"}

if __name__=="__main__":
    print json.dumps(template)