import json
from typing import Dict, Tuple, List

import numpy as np
import pandas as pd
import streamlit as st
from bokeh.plotting import figure

from model.failure import Failure, FailureData
from model.route import Route
from model.success import Success


def groupby_ppm_aggregate_on_amount(df: pd.DataFrame) -> pd.DataFrame:
    # aggregate ppm and sum amounts
    return df.groupby('ppm').agg({'msatoshi': 'sum'}).reset_index()


def convert_to_million_sats(df: pd.DataFrame) -> pd.DataFrame:
    df['msatoshi'] = df['msatoshi'].div(1000)  # convert to satoshi
    df['msatoshi'] = df['msatoshi'].div(1000000)  # convert to Million sat
    return df


def get_hist(df: pd.DataFrame):
    p = figure(x_axis_label='ppm', y_axis_label='amount (Million sats)', title='Histogram')
    p.left[0].formatter.use_scientific = False

    # create histogram
    hist, bins_count = np.histogram(df['ppm'], bins=20, weights=df['msatoshi'])
    p.quad(top=hist, bottom=0, left=bins_count[:-1], right=bins_count[1:], fill_color='#FF4B4B', line_color='white',
           alpha=0.8)
    return p


@st.experimental_memo
def get_relevant_columns(df: pd.DataFrame) -> pd.DataFrame:
    df = df[['source_alias', 'destination_alias', 'msatoshi', 'ppm', 'created_at']]
    return df


def group_by_column_and_aggregate_on_amount_and_weighted_ppm(df: pd.DataFrame, column: str, column_name: str) -> pd.DataFrame:
    # this weighted mean is needed to weight the amount by the ppm
    wm = lambda x: np.average(x, weights=df.loc[x.index, "msatoshi"])

    df = df.groupby(column).agg({'msatoshi': 'sum', 'ppm': wm}).reset_index()
    sorted_df = df.sort_values(by='msatoshi', ascending=False)
    sorted_df.rename(columns={column: column_name}, inplace=True)
    sorted_df.rename(columns={'msatoshi': 'Amount (Million sats)'}, inplace=True)
    sorted_df.rename(columns={'ppm': 'Average weighted PPM'}, inplace=True)
    return sorted_df


def get_dict_from_file(filename) -> Dict[str, any]:
    with open(filename) as f:
        return json.load(f)


@st.experimental_memo
def parse_data(filename) -> Tuple[List[Success], List[Failure], List[Route]]:
    data = get_dict_from_file(filename)
    successes: List[Success] = []
    for s in data['successes']:
        success = Success.from_dict(s)
        successes.append(success)

    failures: List[Failure] = []
    for s in data['failures']:
        failure = Failure.from_dict(s)
        failures.append(failure)

    routes: List[Route] = []
    for s in data['routes']:
        route = Route.from_dict(s)
        routes.append(route)

    return successes, failures, routes


@st.experimental_memo
def get_data(filename) -> Tuple[pd.DataFrame, pd.DataFrame]:
    successes, failures, routes = parse_data(filename)

    successes_df = pd.DataFrame(successes)
    successes_df.dropna(subset=['payment_hash'], inplace=True)
    routes_df = pd.DataFrame(routes)
    routes_df.dropna(subset=['payment_hash'], inplace=True)

    # Explode the FailureData column into multiple columns
    failures_df = pd.DataFrame(failures)
    failure_data_fields = list(FailureData.__dict__['__annotations__'])
    fdf = pd.DataFrame(failures_df["data"].to_list(), columns=failure_data_fields)
    fdf["code"] = failures_df["code"]
    fdf["message"] = failures_df["message"]
    fdf.dropna(subset=['payment_hash'], inplace=True)

    successes_with_routes_df = pd.merge(successes_df, routes_df, on="payment_hash")
    failures_with_routes_df = pd.merge(fdf, routes_df, on="payment_hash")

    successes_with_routes_df["created_at"] = pd.to_datetime(successes_with_routes_df["created_at"], unit='s').dt.date
    failures_with_routes_df["created_at"] = pd.to_datetime(failures_with_routes_df["created_at"], unit='s').dt.date

    return successes_with_routes_df, failures_with_routes_df
