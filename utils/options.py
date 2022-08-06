from datetime import date, timedelta

import pandas as pd
import streamlit as st


def option_rebalance_type(fail_df: pd.DataFrame, succ_df: pd.DataFrame) -> pd.DataFrame:
    option = st.selectbox(
        'What do you want to see?',
        ['Successes', 'Failures'])
    if option == 'Successes':
        df = succ_df
    elif option == 'Failures':
        df = fail_df
    return df


def option_source_with_all(df: pd.DataFrame) -> pd.DataFrame:
    source_option = st.selectbox(
        'Select source',
        ['All'] + df['source_alias'].unique().tolist())
    if source_option != 'All':
        df = df[df['source_alias'] == source_option]
    return df


def option_destination_with_all(df: pd.DataFrame) -> pd.DataFrame:
    destination_option = st.selectbox(
        'Select destination',
        ['All'] + df['destination_alias'].unique().tolist())
    if destination_option != 'All':
        df = df[df['destination_alias'] == destination_option]
    return df


def option_source(df: pd.DataFrame) -> pd.DataFrame:
    source_option = st.selectbox(
        'Select source',
        df['source_alias'].unique().tolist())
    return df[df['source_alias'] == source_option]


def option_destination(df: pd.DataFrame) -> pd.DataFrame:
    destination_option = st.selectbox(
        'Select destination',
        df['destination_alias'].unique().tolist())
    return df[df['destination_alias'] == destination_option]


def option_timeframe(df: pd.DataFrame) -> pd.DataFrame:
    initial_date = st.date_input('Initial date', date.today() - timedelta(days=7))
    final_date = st.date_input('Final date')

    if initial_date is not None and final_date is not None:
        df = df[(df['created_at'] >= initial_date) & (df['created_at'] <= final_date)]

    return df
