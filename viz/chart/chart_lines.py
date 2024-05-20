import random
from typing import Dict, List, Optional

import pandas as pd
from bokeh.models import (
    ColumnDataSource,
    InlineStyleSheet,
)
from bokeh.plotting import figure

from viz.config import (
    VIZ_CHART_INTERVAL,
    VIZ_CHART_SMOOTH,
)
from viz.chart.chart_base import (
    apply_smoothing,
    build_data_boundaries,
    create_plot,
)
from viz.chart.chart_line import chart_line
from viz.chart.theme import generate_colors
from viz.utils import build_empty

random.seed(100)
COLORS: List[str] = generate_colors(256)


def prepare_and_aggregate_data(
    data: pd.DataFrame,
    period: str,
    group_by: str,
    key_sum: Optional[str],
    key_mean: bool,
) -> pd.DataFrame:
    """
    Prepares and aggregates the data by resampling based on a specified period and grouping.

    Args:
        data (pd.DataFrame): The DataFrame to process.
        period (str): The resampling period.
        group_by (str): The column name to group by.
        key_sum (Optional[str]): The column to perform sum/mean on.
        key_mean (bool): If True, computes the mean; otherwise, sums the values.

    Returns:
        pd.DataFrame: The processed DataFrame ready for plotting.
    """
    data["created"] = pd.to_datetime(data["created"], unit="s")

    aggregation = {"_id": "size"}  # Default aggregation
    if key_sum:
        aggregation[key_sum] = "mean" if key_mean else "sum"

    # Resample data with grouping
    resampled_data = (
        data.set_index("created")
        .groupby([pd.Grouper(freq=period), group_by])
        .agg(aggregation)
        .reset_index()
    )

    return resampled_data


def create_chart(
    title: str,
    stylesheets: List[InlineStyleSheet],
    resampled: pd.DataFrame,
    group_by: str,
    **kwargs,
) -> figure:
    """
    Creates and renders a line plot from the aggregated data.

    Args:
        data (pd.DataFrame): The aggregated data for plotting.
        title (str): The title of the chart.
        group_by (str): The column used for grouping the data.
        stylesheets (List[InlineStyleSheet]): A list of custom stylesheets.

    Returns:
        bokeh.plotting.figure: The configured and populated plot.
    """
    plot = create_plot(title, stylesheets, use_tool=False, **kwargs)

    grouped_data = resampled.groupby(group_by)
    color_cycle = iter(COLORS)

    for _group, sub_df in grouped_data:
        source = ColumnDataSource(sub_df)
        color = next(color_cycle)

        plot.line(
            "period",
            "count_smoothed",
            source=source,
            color=color,
            line_width=3,
            line_alpha=0.4,
        )
    return plot


def chart_lines(
    data: pd.DataFrame,
    title: str,
    group_by: str,
    key_sum: Optional[str] = None,
    key_mean: Optional[bool] = False,
    **kwargs,
) -> figure:
    """
    Creates a line chart with separate lines for each group
    based on the provided DataFrame.

    Args:
        data (pd.DataFrame): The input DataFrame containing the data.
        title (str): The title of the chart.
        key_sum (str): The column name to sum values for.
        theme_bad (bool): If True, uses the 'reds' color palette; otherwise,
            uses the 'blues' color palette.
        key_mean (bool): If True, calculates the mean of the values; otherwise,
            sums the values.
        group_by (str): The column name to group the data by.
        **kwargs: Additional keyword arguments.

    Returns:
        bokeh.plotting.figure: The line chart figure with separate
            lines for each group.
    """
    if len(data) < 1:
        return chart_line(build_empty(key_sum), title=title)

    period: str = kwargs.get("period", VIZ_CHART_INTERVAL)

    stylesheets: List[InlineStyleSheet] = []
    if kwargs.get("custom_css", False):
        stylesheets.append(InlineStyleSheet(css=kwargs["custom_css"]))

    resampled = prepare_and_aggregate_data(data, period, group_by, key_sum, key_mean)
    resampled = resampled.rename(columns={"created": "period"})

    if key_sum is not None:
        resampled = resampled.rename(columns={key_sum: "count"})
    else:
        resampled = resampled.rename(columns={"_id": "count"})

    resampled = apply_smoothing(resampled, VIZ_CHART_SMOOTH, **kwargs)
    resampled = build_data_boundaries(resampled, period, **kwargs)

    plot = create_chart(title, stylesheets, resampled, group_by, **kwargs)

    return plot
