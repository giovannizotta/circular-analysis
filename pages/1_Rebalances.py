import pandas as pd
import streamlit as st

from model.data import get_data
from utils.options import option_rebalance_type, option_source_with_all, option_destination_with_all, option_timeframe
from utils.data_utils import aggregate_on_ppm, convert_to_million_sats, get_hist, get_relevant_columns


def data_after_options(succ_df: pd.DataFrame, fail_df: pd.DataFrame) -> pd.DataFrame:
    df = option_rebalance_type(fail_df, succ_df)

    df = option_destination_with_all(df)

    df = option_source_with_all(df)

    df = option_timeframe(df)

    return df


def main():
    st.markdown("Rebalances")
    st.sidebar.markdown("Rebalance stats")

    succ_df, fail_df = get_data('model/devzor.json')
    succ_df = get_relevant_columns(succ_df)
    fail_df = get_relevant_columns(fail_df)

    df = data_after_options(succ_df, fail_df)
    st.markdown("Hits: " + str(len(df)))

    df = convert_to_million_sats(df)
    st.markdown(f"Total amount of rebalances: {df['msatoshi'].sum():.2f} million sats")

    df = aggregate_on_ppm(df)
    p = get_hist(df)
    st.bokeh_chart(p, use_container_width=True)


main()
