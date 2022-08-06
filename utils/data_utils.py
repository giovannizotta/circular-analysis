import numpy as np
import pandas as pd
import streamlit as st
from bokeh.plotting import figure


def aggregate_on_ppm(df: pd.DataFrame) -> pd.DataFrame:
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


def aggregate_by_source(df: pd.DataFrame) -> pd.DataFrame:
    # aggregate ppm and sum amounts
    df = df.groupby('source_alias').agg({'msatoshi': 'sum', 'ppm': 'mean'}).reset_index()
    sorted_df = df.sort_values(by='msatoshi', ascending=False)
    sorted_df.rename(columns={'source_alias': 'Source'}, inplace=True)
    sorted_df.rename(columns={'msatoshi': 'Amount (Million sats)'}, inplace=True)
    sorted_df.rename(columns={'ppm': 'Average PPM'}, inplace=True)
    return sorted_df


def aggregate_by_destination(df: pd.DataFrame) -> pd.DataFrame:
    # aggregate ppm and sum amounts
    df = df.groupby('destination_alias').agg({'msatoshi': 'sum', 'ppm': 'mean'}).reset_index()
    sorted_df = df.sort_values(by='msatoshi', ascending=False)
    sorted_df.rename(columns={'destination_alias': 'Destination'}, inplace=True)
    sorted_df.rename(columns={'msatoshi': 'Amount (Million sats)'}, inplace=True)
    sorted_df.rename(columns={'ppm': 'Average PPM'}, inplace=True)
    return sorted_df
