import json
from typing import Dict, Tuple, List

import streamlit as st
import pandas as pd

from model.failure import Failure, FailureData
from model.route import Route
from model.success import Success


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
