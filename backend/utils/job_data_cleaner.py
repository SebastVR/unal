class JobDataCleaner:
    def __init__(self, data):
        self.data = json.loads(data)

    def clean_data(self):
        for job in self.data["jobs"]:
            job["annualSalaryMin"] = int(job["annualSalaryMin"])
        return self.data


import json
from dotenv import load_dotenv
import os
import s3fs
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq

load_dotenv()


class SaveS3:
    def __init__(self, json_data):
        if isinstance(json_data, dict):
            self.json = json_data  # Asumimos que es un diccionario
        else:
            self.json = json.loads(json_data)

    def write_to_minio(self):

        fs = s3fs.S3FileSystem(
            client_kwargs={"endpoint_url": os.getenv("MINIO_ENDPOINT")},
            key=os.getenv("MINIO_ACCESS_KEY"),
            secret=os.getenv("MINIO_SECRET_KEY"),
            use_ssl=False,
        )

        with fs.open("testbucket/jobs.json", "w") as f:
            json.dump(self.json, f)

        return "Successfully uploaded as object..."

    def write_to_minio_parquet(self):

        fs = s3fs.S3FileSystem(
            client_kwargs={"endpoint_url": os.getenv("MINIO_ENDPOINT")},
            key=os.getenv("MINIO_ACCESS_KEY"),
            secret=os.getenv("MINIO_SECRET_KEY"),
            use_ssl=False,
        )
        dic = json.loads(str(self.json))
        df = pd.DataFrame.from_dict(dic)
        print(df)
        tb = pa.Table.from_pandas(df)
        pq.write_to_dataset(
            tb,
            "testbucket/jobs.parquet",
            filesystem=fs,
            use_dictionary=True,
            compression="snappy",
            version="2.4",
        )

        return "Successfully uploaded as parquet file"
