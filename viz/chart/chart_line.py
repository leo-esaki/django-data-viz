from typing import List, Optional

import pandas as pd
from bokeh.models import (
    ColumnDataSource,
    HoverTool,
    InlineStyleSheet,
)

from viz.config import (
    VIZ_CHART_SMOOTH,
    VIZ_CHART_INTERVAL,
)
from viz.chart.chart_base import (
    apply_smoothing,
    build_data_boundaries,
    create_plot,
    resample_data,
)
from viz.utils import build_empty


def chart_line(
    data: pd.DataFrame,
    title: str,
    key_sum: Optional[str] = None,
    theme_bad: Optional[bool] = False,
    key_mean: Optional[bool] = False,
    cumsum: Optional[bool] = False,
    decimal_places: Optional[int] = 2,
    **kwargs,
):
    """
    Creates a line chart based on the provided DataFrame.

    Args:
        df (pd.DataFrame): The input DataFrame containing the data.
        title (str): The title of the chart.
        **kwargs: Additional keyword arguments.
            period (str): The resampling period (e.g., '5min', '1h').
            key_sum (str): The column name to sum values for.
            key_mean (bool): If we should average the values

    Returns:
        bokeh.plotting.figure: The line chart figure.
    """
    if len(data) < 1:
        return chart_line(build_empty(key_sum), title=title)

    data["created"] = pd.to_datetime(data["created"], unit="s")
    period: str = kwargs.get("period", VIZ_CHART_INTERVAL)

    resampled = resample_data(data, period, key_sum, key_mean, **kwargs)
    resampled = apply_smoothing(resampled, VIZ_CHART_SMOOTH, **kwargs)
    resampled = build_data_boundaries(resampled, period, **kwargs)

    source = ColumnDataSource(resampled)

    stylesheets: List[InlineStyleSheet] = []
    if kwargs.get("custom_css", False):
        stylesheets.append(InlineStyleSheet(css=kwargs["custom_css"]))

    plot = create_plot(title, stylesheets, **kwargs)

    plot.line(
        "period",
        "count_smoothed",
        source=source,
        color="white",
        line_width=2,
        line_alpha=0.5,
    )

    plot.add_tools(
        HoverTool(
            tooltips=[
                ("Date", "@period{%F}"),
                ("Time", "@period{%T}"),
                ("Amount", "@count_smoothed"),
            ],
            formatters={
                "@period": "datetime",
                "@count_smoothed": "numeral",
            },
            mode="vline",
        )
    )

    return plot
