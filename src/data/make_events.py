# -*- coding: utf-8 -*-
import click
import logging
from pathlib import Path
from dotenv import find_dotenv, load_dotenv
import os
import dask.dataframe as dd
import dask
import pandas as pd
import numpy as np


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
    accs = read_data(input_filepath / os.getenv("PROC_NAME"))
    accs = transform_data_np(accs)
    write_data(accs, output_filepath)


def read_data(path):
    return dd.read_parquet(path)


def transform_data_dask(accs):
    lngs = dask.array.linspace(
        accs.Start_Lng.max().compute(), accs.Start_Lng.min().compute(), num=10
    )
    lats = dask.array.linspace(
        accs.Start_Lat.max().compute(), accs.Start_Lat.min().compute(), num=10
    )
    times = dask.array.from_array(
        pd.date_range(
            start=accs.index.min().compute(),
            end=accs.index.max().compute(),
            freq="15min",
        ).values
    )
    ts, lngs, lats = dask.array.meshgrid(times, lngs, lats)


def transform_data_np(accs):
    lngs = np.linspace(
        accs.Start_Lng.max().compute(), accs.Start_Lng.min().compute(), num=10
    )
    lats = np.linspace(
        accs.Start_Lat.max().compute(), accs.Start_Lat.min().compute(), num=10
    )
    times = pd.date_range(
        start=accs.index.min().compute(), end=accs.index.max().compute(), freq="15min"
    ).values
    times, lngs, lats = np.meshgrid(times, lngs, lats)
    events = pd.DataFrame(
        {"time": times.reshape(-1), "lng": lngs.reshape(-1), "lat": lats.reshape(-1)}
    )
    events["accident"] = np.random.randint(0, 2, size=len(events))  # ! Placeholder
    return events


def write_data(accs, path):
    logger = logging.getLogger(__name__)
    accs.to_parquet(path / os.getenv("EV_NAME"))
    logger.info("wrote processed dataset to " + str(path / os.getenv("EV_NAME")))


if __name__ == "__main__":
    log_fmt = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    # not used in this stub but often useful for finding various files
    project_dir = Path(__file__).resolve().parents[2]

    # find .env automagically by walking up directories until it's found, then
    # load up the .env entries as environment variables
    load_dotenv(find_dotenv())

    main()
