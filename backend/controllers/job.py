from sqlalchemy.orm import Session
from utils.source_data_fetcher import SourceDataFetcher
from utils.json_converter import JSONConverter
from utils.job_data_cleaner import JobDataCleaner, SaveS3
from bd.job import JobPosting
from fastapi import HTTPException
import pandas as pd
import s3fs
import os


def update_job_postings(db: Session, url: str):
    data_fetcher = SourceDataFetcher(url)
    data = data_fetcher.fetch_data()
    if not data:
        return None

    converter = JSONConverter(data)
    json_result = converter.convert_to_json()
    cleaner = JobDataCleaner(json_result)
    cleaned_data = cleaner.clean_data()

    s3_saver = SaveS3(cleaned_data)
    file_parquet_path = s3_saver.write_to_minio_parquet()

    # Carga los datos desde el archivo .parquet
    fs = s3fs.S3FileSystem(
        client_kwargs={"endpoint_url": os.getenv("MINIO_ENDPOINT")},
        key=os.getenv("MINIO_ACCESS_KEY"),
        secret=os.getenv("MINIO_SECRET_KEY"),
        use_ssl=False,
    )

    try:
        with fs.open(file_parquet_path, "rb") as f:
            df = pd.read_parquet(f)
    except Exception as e:
        print(f"Failed to load parquet file: {e}")
        raise HTTPException(
            status_code=500, detail="Failed to load job data from the datalake"
        )

    # Guardar en base de datos usando el DataFrame
    for index, row in df.iterrows():
        job_posting = JobPosting(
            job_slug=row["jobSlug"],
            job_title=row["jobTitle"],
            company_name=row["companyName"],
            job_geo=row["jobGeo"],
            job_level=row["jobLevel"],
            pub_date=row["pubDate"],
            annual_salary=row.get("annualSalaryMin", None),
            salary_currency=row["salaryCurrency"],
            responsibilities_1=row.get("responsibilities_1", ""),
            responsibilities_2=row.get("responsibilities_2", ""),
            responsibilities_3=row.get("responsibilities_3", ""),
            file_json=file_parquet_path,  # Ruta del archivo parquet
        )
        db.add(job_posting)
    db.commit()
    return True
