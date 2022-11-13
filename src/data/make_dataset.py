# -*- coding: utf-8 -*-
import click
import logging
from pathlib import Path
from dotenv import find_dotenv, load_dotenv
import dotenv
import os
import dask.dataframe as dd


@click.command()
@click.argument("input_filepath", type=click.Path(exists=True))
@click.argument("output_filepath", type=click.Path())
def main(input_filepath, output_filepath):
    """Runs data processing scripts to turn raw data from (../raw) into
    cleaned data ready to be analyzed (saved in ../processed).
    """
    input_filepath = Path(input_filepath)
    output_filepath = Path(output_filepath)
    logger = logging.getLogger(__name__)
    logger.info("making final data set from raw data")
    accs = read_data(input_filepath / os.getenv("RAW_NAME"))
    accs = transform_data(accs)
    write_data(accs, output_filepath)


def read_data(path):
    return dd.read_csv(path, dtype={"Zipcode": "object"})


def transform_data(accs):
    accs["Start_Time"] = accs["Start_Time"].astype("datetime64[s]")
    accs["End_Time"] = accs["End_Time"].astype("datetime64[s]")
    accs["Start_DOW"] = accs["Start_Time"].dt.dayofweek
    accs["Start_Bucket"] = assign_bucket(accs["Start_Time"])
    return accs.set_index("Start_Time")


def assign_bucket(times):
    return times.dt.hour


def write_data(accs, path):
    logger = logging.getLogger(__name__)
    accs.to_parquet(path / os.getenv("PROC_NAME"))
    logger.info("wrote processed dataset to " + str(path / os.getenv("PROC_NAME")))


if __name__ == "__main__":
    log_fmt = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    # not used in this stub but often useful for finding various files
    project_dir = Path(__file__).resolve().parents[2]

    # find .env automagically by walking up directories until it's found, then
    # load up the .env entries as environment variables
    load_dotenv(find_dotenv())

    main()
