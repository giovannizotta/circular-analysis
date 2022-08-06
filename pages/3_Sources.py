import pandas as pd
import streamlit as st

from model.data import get_data

from utils.options import option_rebalance_type, option_source, option_timeframe
from utils.data_utils import aggregate_on_ppm, convert_to_million_sats, get_hist, get_relevant_columns, \
    aggregate_by_destination


def data_after_options(succ_df: pd.DataFrame, fail_df: pd.DataFrame) -> pd.DataFrame:
    df = option_rebalance_type(fail_df, succ_df)

    df = option_source(df)

    df = option_timeframe(df)

    return df


def main():
    st.markdown("Rebalances from the perspective of a source")

    succ_df, fail_df = get_data('model/devzor.json')
    succ_df = get_relevant_columns(succ_df)
    fail_df = get_relevant_columns(fail_df)

    df = data_after_options(succ_df, fail_df)
    df = convert_to_million_sats(df)

    df_aggdest = aggregate_by_destination(df.copy())

    df = aggregate_on_ppm(df)
    p = get_hist(df)
    st.bokeh_chart(p, use_container_width=True)

    st.markdown("Hits: " + str(len(df)))
    st.markdown(f"Total amount rebalanced from this source: {df['msatoshi'].sum():.2f} million sats")

    st.dataframe(df_aggdest)


main()
