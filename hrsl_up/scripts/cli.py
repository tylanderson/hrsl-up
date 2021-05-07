import click
from typing import List

from hrsl_up import download_aws, upload_gcp, FACTOR_FOLDER


@click.group()
def cli():
    """A small tool for download HRSL data"""
    pass


@cli.command()
@click.option(
    # fmt: off
    "--factor", "-f",
    # fmt: on
    multiple=True,
    type=click.Choice(FACTOR_FOLDER.keys(), case_sensitive=False),
    default=["general"],
    show_default=True,
    help="HRSL factor to download.",
)
@click.argument("save_folder", required=True)
def download(factor: List, save_folder: str):
    """Download HRSL data from AWS bucket"""
    allowed_factors = FACTOR_FOLDER.keys()
    if any(f not in allowed_factors for f in factor):
        raise ValueError(f"Only one of {allowed_factors} valid input for --factor")
    if "all" in factor:
        factor = allowed_factors
    download_aws(factor, save_folder)


@cli.command()
@click.argument("local")
@click.argument("remote")
@click.option(
    # fmt: off
    "--key", "-k",
    # fmt: on
    help="Service Account JSON for uploading to GCP",
)
def upload(local, remote, key):
    """Upload to GCP"""
    upload_gcp(local, remote, key)
