from bs4 import BeautifulSoup
import boto3
import json
import os
import pandas as pd
import re
import requests

from botocore import UNSIGNED
from botocore.config import Config

from build_files_from_ncbi import (
    build_ncbi_data,
    GENOMES_OUTPUT_PATH,
)

import pandas as pd
import logging

# Configure logging
logging.basicConfig(
    filemode='a',
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)

BUCKET_FILELIST_OUTPUT_PATH = "catalog/build/intermediate/s3_bucketlist.json"
RDEVAL_DATA_OUTPUT_PATH = "catalog/build/intermediate/primary-rdeval.tsv"


def extract_rdeval_statistics_from_html(html_source, html_path_prefix="https://genomeark.s3.amazonaws.com/"):
    file_path = html_path_prefix + html_source
    if file_path.startswith("http"):
        response = requests.get(file_path, headers={"User-Agent": "Mozilla/5.0"})
        response.raise_for_status()
        html_content = response.text
    else:
        with open(file_path, "r", encoding="utf-8") as f:
            html_content = f.read()

    soup = BeautifulSoup(html_content, "html.parser")  # Use built-in parser

    data = []
    # Find all divs with id ending in .fastq
    for div in soup.find_all("div", id=re.compile(r".*-all\.rd$")):
        sample_id = re.split('[/_.]', html_source)[-3]
        info = {
            'html_source': file_path,
            'sample_ids': sample_id,
            "srr_ids": None,
            "number_of_reads": None,
            "total_read_length": None,
            "average_read_length": None,
            "read_N50": None,
            "smallest_read_length": None,
            "largest_read_length": None,
            "gc_content": None,
            "base_composition": None,
            "average_read_quality": None,
        }

        info['srr_ids'] = ",".join([li.text.split('.')[0] for li in div.find_all("li")])

        for p in div.find_all("p"):
            text = p.get_text()

            if "Number of reads:" in text:
                info["number_of_reads"] = int(text.split(": ")[-1])
            elif "Total read length:" in text:
                info["total_read_length"] = int(text.split(": ")[-1])
            elif "Average read length:" in text:
                info["average_read_length"] = float(text.split(": ")[-1])
            elif "Read N50:" in text:
                info["read_N50"] = int(text.split(": ")[-1])
            elif "Smallest read length:" in text:
                info["smallest_read_length"] = int(text.split(": ")[-1])
            elif "Largest read length:" in text:
                info["largest_read_length"] = int(text.split(": ")[-1])
            elif "GC content %:" in text:
                info["gc_content"] = float(text.split(": ")[-1])
            elif "Base composition (A:C:T:G):" in text:
                info["base_composition"] = list(zip(['A', 'C', 'G', 'T'], map(int, text.split(": ")[-1].split(":"))))
            elif "Average read quality:" in text:
                info["average_read_quality"] = float(text.split(": ")[-1])

        data.append(info)

    if len(data) > 1:
        raise ValueError("More than one sample found in rdeval html report")
    return data[0]


def read_rdeval_html_report(file_name):
    with open(file_name, "r") as f:
        html = f.read()


def generate_bucket_file_list():
    # Create an S3 client with unsigned requests (no authentication)
    s3 = boto3.client('s3', config=Config(signature_version=UNSIGNED))

    bucket_name = "genomeark"

    file_list = []

    num_pages = 0
    num_files = 0
    # Paginator to handle more than 1000 objects
    if not os.path.exists(BUCKET_FILELIST_OUTPUT_PATH):
        print('Fetching bucket file list, pages: ')
        logger.info("generating new bucket file list")
        paginator = s3.get_paginator("list_objects_v2")
        pages = paginator.paginate(Bucket=bucket_name)

        for page in pages:
            if num_files % 1000 == 0:
                print(f"\rProcessed pages: {num_pages}, files: {num_files}", end="")
            num_pages += 1
            if "Contents" in page:
                for obj in page["Contents"]:
                    file_parts = obj["Key"].split("/")[-1].split(".")
                    suffix = file_parts[-1]
                    if suffix == "gz" and len(file_parts) > 2:
                        suffix = ".".join(file_parts[-2:])

                    file_list.append((obj["Key"], obj["LastModified"].strftime("%Y-%m-%d"), suffix))
                    num_files += 1

        print(f"\rProcessed pages: {num_pages}, files: {num_files}", end="\n")

        with open(BUCKET_FILELIST_OUTPUT_PATH, "w") as f:
            f.write(json.dumps(file_list))
    else:
        logger.info("reading existing bucket file list")
        with open(BUCKET_FILELIST_OUTPUT_PATH, "r") as f:
            file_list = json.loads(f.read())
    return file_list


if __name__ == "__main__":
    logger.info("Creating input data")
    if not os.path.exists(GENOMES_OUTPUT_PATH):
        logger.info("Fetching basic ncbi data")
        build_ncbi_data()

    file_list = generate_bucket_file_list()

    # df_genomes = pd.read_csv(GENOMES_OUTPUT_PATH, sep="\t")
    # df_primary = pd.read_csv(RDEVAL_DATA_OUTPUT_PATH, sep="\t")

    if not os.path.exists(RDEVAL_DATA_OUTPUT_PATH):
        # df_primary = df_primary.assign(sample_ids = df_primary["sample_ids"].str.split(",")).explode("sample_ids")
        # df_primary = df_primary[~df_primary["sample_ids"].isnull() & df_primary["sample_ids"].str.startswith('SRA')]
        # df_primary["sample_ids"] = df_primary["sample_ids"].str.replace("SRA:", "")
        # print(df_primary.head())
        num_rdeval_processed = 0
        rdeval_data = []
        print(f"\rProcessed rdeval files: {num_rdeval_processed}", end="")
        for (file_name, last_modified, suffix) in file_list:
            if "rdeval" in file_name:
                num_rdeval_processed += 1
                rdeval_data.append(extract_rdeval_statistics_from_html(file_name))
                print(f"\rProcessed rdeval files: {num_rdeval_processed}", end="")
        print(f"\rProcessed rdeval files: {num_rdeval_processed}", end="\n")
        pd.DataFrame(data=rdeval_data).to_csv(RDEVAL_DATA_OUTPUT_PATH, index=False)
        # print(rdeval_data.head())
        # merged_df = df_primary.join(rdeval_data.set_index("sample_ids"), on="sample_ids", how="left")
        # merged_df.to_csv(PRIMARYDATA_WITH_OUTPUT_PATH, sep="\t", index=False)
        # # #df = read_assemblies(ASSEMBLIES_PATH)

    # # df_primary

    # rdeval_data.to_csv("rdeval_data.csv", index=False)
    rdeval_data = pd.read_csv("rdeval_data.csv")

    # print(merged_df.shape)
    # print(df_primary.head())
    # print(rdeval_data.head())
