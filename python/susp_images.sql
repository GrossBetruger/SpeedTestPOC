select start_measuring_timestamp, file_download_ratekbper_sec, download_rate_in_mbps,
  (file_download_ratekbper_sec / ((download_rate_in_mbps / 8.0) * 1024)) as ratio,
  s3file_address
from comparison_info join file_download_info on comparison_info.file_download_info_id = file_download_info.id
join speed_test_web_site on speed_test_web_site.id = comparison_info.speed_test_web_site_download_info_id where

((file_download_ratekbper_sec / ((download_rate_in_mbps / 8.0) * 1024))  > {}
or (file_download_ratekbper_sec / ((download_rate_in_mbps / 8.0) * 1024))  < {})
and (current_timestamp - interval '{} hour')::abstime::int::bigint < start_measuring_timestamp / 1000

