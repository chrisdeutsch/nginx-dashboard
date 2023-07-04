import gzip
import re

import pandas as pd


def parse_log(filename):
    """Docstring"""

    # Default 'combined' log format
    pattern = re.compile(
        r"^(?P<remote_addr>.*) - (?P<remote_user>.*) \[(?P<time_local>.*)\] "
        r"\"(?P<request>.*?)\" (?P<status>\d+) (?P<body_bytes_sent>\d+) "
        r"\"(?P<http_referer>.*?)\" \"(?P<http_user_agent>.*?)\"$"
    )

    log = None

    with open_wrapper(filename) as fin:
        for line in fin:
            m = pattern.match(line)
            assert m is not None

            group_dict = m.groupdict()
            if log is None:
                log = {key: [val] for key, val in group_dict.items()}
            else:
                for key, val in group_dict.items():
                    log[key].append(val)

    return pd.DataFrame(log)


def open_wrapper(filename):
    """Wrapper to open gzipped and non-gzipped log files for reading."""

    if filename.endswith(".gz"):
        return gzip.open(filename, "rt")
    else:
        return open(filename, "r")
