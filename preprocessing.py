import pandas as pd


def preprocess(df):
    return df.pipe(convert_types).pipe(convert_timestamp).pipe(split_request)


def convert_types(df):
    return df.astype({"status": int, "body_bytes_sent": int})


def convert_timestamp(df):
    timestamp_format = "%d/%b/%Y:%H:%M:%S %z"
    df["timestamp"] = pd.to_datetime(
        df["time_local"], format=timestamp_format, utc=True
    )
    return df.drop(columns="time_local")


def split_request(df):
    pattern = r"^(?P<request_type>\S+) (?P<request_uri>\S+) (?P<request_protocol>\S+)$"
    df_split_request = df["request"].str.extract(pattern)
    return df.join(df_split_request).drop(columns="request")
