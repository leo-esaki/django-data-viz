import pandas as pd
from bokeh.plotting import figure

from loguru import logger

from viz.chart.chart_bar import chart_bar
from viz.chart.chart_line import chart_line
from viz.chart.chart_lines import chart_lines
from viz.threads.stats_worker import get_worker, MetricType


def check_empty(key: str, df: pd.DataFrame) -> None:
    if df.empty:
        logger.warning(f"Dataframe is empty, {key} not found in dataset")


def get_data(key: MetricType, **kwargs) -> pd.DataFrame:
    df: pd.DataFrame = get_worker().get_metric_df(key, **kwargs)

    # Filtering by user_id
    if "user_id" in kwargs and "user_id" in df.columns:
        df = df[df["user_id"] == kwargs.get("user_id")]
        check_empty("user_id", df)

    # Filtering by miner
    if "miner_hotkey" in kwargs and "miner_hotkey" in df.columns:
        df = df[df["miner_hotkey"] == kwargs.get("miner_hotkey")]
        check_empty("miner_hotkey", df)

    if "miner" in kwargs and "miner" in df.columns:
        df = df[df["miner"] == kwargs.get("miner")]
        check_empty("miner", df)

    if "validator" in kwargs and "validator" in df.columns:
        df = df[df["validator"] == kwargs.get("validator")]
        check_empty("validator", df)

    # Cleanup user latency unless we're looking at a user chart
    # i.e. cheaters will not be shown on the main charts
    if "user_id" not in kwargs:
        if "is_valid" in df.columns:
            # Filter out users with any invalid items
            valid_users = df.groupby("user_id")["is_valid"].all()
            valid_user_ids = valid_users[valid_users].index
            df = df[df["user_id"].isin(valid_user_ids)]

    return df


def show_votes(**kwargs) -> figure:
    data: pd.DataFrame = get_data(MetricType.VOTES, **kwargs)

    return chart_line(
        title="Vote Count Over Time",
        data=data,
        **kwargs,
    )


def show_votes_by_user(**kwargs) -> figure:
    data: pd.DataFrame = get_data(MetricType.VOTES, **kwargs)

    return chart_bar(
        group_by="user_id",
        title="Vote Count By User",
        # Open the following url on click
        url_column="user_id",
        url_prefix=lambda x: f"/viz/users/{x}/comp",
        data=data,
        **kwargs,
    )


def show_votes_by_compute(**kwargs) -> figure:
    data: pd.DataFrame = get_data(MetricType.VOTES, **kwargs)

    return chart_bar(
        group_by="compute_id",
        title="Votes By Compute",
        data=data,
        **kwargs,
    )


def show_averages_by_hotkey(**kwargs) -> figure:
    data: pd.DataFrame = get_data(MetricType.AVERAGES, **kwargs)

    return chart_lines(
        group_by="miner",
        key_sum="weight",
        title="Miner Averages",
        data=data,
        **kwargs,
    )


def show_weights_by_hotkey(**kwargs) -> figure:
    data: pd.DataFrame = get_data(MetricType.WEIGHTS, **kwargs)

    return chart_lines(
        group_by="miner",
        key_sum="weight",
        key_mean=True,
        title="Miner Weights",
        data=data,
        **kwargs,
    )


def show_votes_by_hotkey(**kwargs) -> figure:
    data: pd.DataFrame = get_data(MetricType.VOTES, **kwargs)

    return chart_bar(
        group_by="miner_hotkey",
        title="Votes By Miner",
        # Open the following url on click
        url_column="miner_hotkey",
        url_prefix=lambda x: f"/viz/hotkeys/{x}",
        data=data,
        **kwargs,
    )


def show_votes_by_round(**kwargs) -> figure:
    data: pd.DataFrame = get_data(MetricType.VOTES, **kwargs)

    return chart_bar(
        group_by="round_id",
        title="Votes By Round",
        data=data,
        **kwargs,
    )


def show_computes(**kwargs) -> figure:
    data: pd.DataFrame = get_data(MetricType.COMPUTES, **kwargs)

    return chart_line(
        title="Computes Over Time",
        data=data,
        **kwargs,
    )


def show_batches(**kwargs) -> figure:
    data: pd.DataFrame = get_data(MetricType.BATCHES, **kwargs)

    return chart_line(
        title="Batches Over Time",
        data=data,
        **kwargs,
    )


def show_user_latency(**kwargs) -> figure:
    data: pd.DataFrame = get_data(MetricType.VOTES, **kwargs)

    return chart_line(
        key_mean=True,
        key_sum="user_latency",
        title="User latency Over Time (ms)",
        data=data,
        **kwargs,
    )


def show_user_latency_by_user(**kwargs) -> figure:
    data = get_data(MetricType.VOTES, **kwargs)

    return chart_bar(
        lowest=True,
        greater_than=0,
        group_by="user_id",
        key_sum="user_latency",
        value_avg=True,
        value_col="user_latency",
        title="Lowest Latencies By User (ms)",
        # Open the following url on click
        url_column="user_id",
        url_prefix=lambda x: f"/viz/users/{x}/comp",
        data=data,
        **kwargs,
    )


def show_total_payouts(**kwargs) -> figure:
    data: pd.DataFrame = get_data(MetricType.PAYOUTS, **kwargs)

    return chart_line(
        cumsum=True,
        key_sum="amount",
        title="Total Payouts Over Time",
        data=data,
        **kwargs,
    )


def show_payouts(**kwargs) -> figure:
    data: pd.DataFrame = get_data(MetricType.PAYOUTS, **kwargs)

    return chart_line(
        key_sum="amount",
        title="Payouts Over Time",
        data=data,
        **kwargs,
    )


def show_payouts_by_user(**kwargs) -> figure:
    data: pd.DataFrame = get_data(MetricType.PAYOUTS, **kwargs)

    return chart_bar(
        decimal_places=6,
        key_sum="amount",
        value_col="amount",
        group_by="user_id",
        title="Payout By User",
        # Open the following url on click
        url_column="user_id",
        url_prefix=lambda x: f"/viz/users/{x}/comp",
        data=data,
        **kwargs,
    )


def show_rounds(**kwargs) -> figure:
    data: pd.DataFrame = get_data(MetricType.ROUNDS, **kwargs)

    return chart_line(
        title="Rounds Over Time",
        data=data,
        **kwargs,
    )
