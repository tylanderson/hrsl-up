import click
from typing import List

from hrsl_up.download import download_aws


@click.command()
@click.option(
    # fmt: off
    "--factor", "-f",
    # fmt: on
    multiple=True,
    default=["general"],
    show_default=True,
    help='HRSL factor to download. One of: "all", "general", "men", "women", "women-reproductive", "elderly", "youth", "children"',
)
@click.argument("save_folder", required=True)
def download(factor: List, save_folder: str):
    """Download HRSL"""
    allowed_factors = [
        "general",
        "men",
        "women",
        "women-reproductive",
        "elderly",
        "youth",
        "children",
    ]
    if any(f not in allowed_factors for f in factor):
        raise ValueError(f"Only one of {allowed_factors} valid input for --factor")
    if "all" in factor:
        factor = allowed_factors
    download_aws(factor, save_folder)


if __name__ == "__main__":
    download()
