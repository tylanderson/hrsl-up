import s3fs
import gcsfs
from pathlib import Path
import os
from tqdm import tqdm


BUCKET = "dataforgood-fb-data"
PREFIX = "hrsl-cogs"

FACTOR_FOLDER = {
    "general": "hrsl_general",
    "men": "hrsl_men",
    "women": "hrsl_women",
    "women-reproductive": "hrsl_women_of_reproductive_age_15_49",
    "elderly": "hrsl_elderly_60_plus",
    "youth": "hrsl_youth_15_24",
    "children": "hrsl_children_under_five",
}

VERSION = "v1"


def download_aws(factors, save_dir):
    folders = [FACTOR_FOLDER[factor] for factor in factors]
    remote_path = f"{BUCKET}/{PREFIX}"
    fs = s3fs.S3FileSystem(anon=True)

    files = []
    for folder in folders:
        pattern = f"*{folder}**{VERSION}**/*.tif"
        folder_files = match_files(remote_path, pattern)
        files += folder_files

    for f in tqdm(files):
        local_file = Path(os.path.join(save_dir, f.split(f"{remote_path}/")[-1]))
        if not local_file.exists():
            local_file.parent.mkdir(parents=True, exist_ok=True)
            download_file(fs, f, str(local_file))


def upload_gcp(local, remote, key=None):
    files = list(Path(local).rglob("*.tif"))
    fs = gcsfs.GCSFileSystem(token=key)
    for f in tqdm(files):
        stem = f.relative_to(local)
        remote_path = os.path.join(remote, stem)
        upload_file(fs, str(f), remote_path)


def match_files(path, pattern):
    fs = s3fs.S3FileSystem(anon=True)
    files = [f"s3://{f}" for f in fs.glob(f"s3://{path}/{pattern}")]
    return files


def download_file(filesystem, remote, local):
    filesystem.get(remote, local)


def upload_file(filesystem, local, remote):
    filesystem.put(local, remote)
