from datetime import datetime
from typing import List, Optional

import pandas as pd
from bokeh.models import (
    DataRange1d,
    InlineStyleSheet,
    NumeralTickFormatter,
)
from bokeh.models.formatters import DatetimeTickFormatter
from bokeh.plotting import figure

from viz.config import (
    VIZ_CHART_WIDTH,
    VIZ_CHART_HEIGHT,
)
from viz.utils import build_insert, last_cycle


def resample_data(
    data: pd.DataFrame,
    period: str,
    key_mean: bool = False,
    key_sum: Optional[str] = None,
    **kwargs
) -> pd.DataFrame:
    # Resample data to the specified period and sum or count values
    if key_sum is None or key_sum not in data.columns:
        resampled = (
            data.set_index("created")
            .resample(period)[["_id"]]
            .size()
            .fillna(0)
            .reset_index()
        )
    else:
        if key_mean:
            resampled = (
                data.set_index("created")
                .resample(period)
                .agg({key_sum: "mean"})
                .reset_index()
            )
        else:
            # Check the data type of the key_sum column
            is_numeric: bool = pd.api.types.is_numeric_dtype(
                data.iloc[0][key_sum],
            )

            if is_numeric:
                # If numeric, sum the values
                resampled = (
                    data.set_index("created")
                    .resample(period)
                    .agg({key_sum: "sum"})
                    .reset_index()
                )
            else:
                # If numeric, sum the values
                resampled = (
                    data.set_index("created")
                    .resample(period)
                    .agg({key_sum: "nunique"})
                    .reset_index()
                )

    resampled.columns = ["period", "count"]
    return resampled


def apply_smoothing(
    resampled: pd.DataFrame, window_size: int, **kwargs
) -> pd.DataFrame:
    # Ensure the 'count' column exists to prevent errors
    if "count" not in resampled.columns:
        raise ValueError("DataFrame must contain a 'count' column")

    # Calculate the rolling mean on the 'count' column
    resampled["count_smoothed"] = (
        resampled["count"].rolling(window=window_size, min_periods=1).mean()
    )

    return resampled


def build_data_boundaries(
    resampled: pd.DataFrame, period: str, **kwargs
) -> pd.DataFrame:
    rows: List[pd.DataFrame] = []
    tdelta = pd.Timedelta(period)

    should_trail: bool = kwargs.get("trail_values", False)

    rows.append(build_insert(last_cycle(), period))
    if len(resampled) > 0:
        rows.append(build_insert(resampled.iloc[0]["period"] - tdelta, period))
    rows.append(resampled)

    # Trail the last value to the right side of the chart
    # Makes some charts look less buggy (weights & averages)
    if len(resampled) > 0 and should_trail:
        rows.append(
            build_insert(
                #
                datetime.now(),
                period,
                last_count=resampled.iloc[-1]["count"],
            )
        )

    else:
        rows.append(build_insert(resampled.iloc[-1]["period"] + tdelta, period))
        rows.append(build_insert(datetime.now(), period))

    return pd.concat(rows, ignore_index=True)


def create_plot(title: str, stylesheets: List[InlineStyleSheet], **kwargs) -> figure:
    plot = figure(
        tools="",
        width=VIZ_CHART_WIDTH,
        height=VIZ_CHART_HEIGHT,
        toolbar_location=None,
        x_axis_type="datetime",
        sizing_mode="stretch_both",
        stylesheets=stylesheets,
    )

    if not kwargs.get("notitle", False):
        plot.title.text = title

    plot.yaxis.formatter = NumeralTickFormatter(format="0,0")
    plot.xaxis.formatter = DatetimeTickFormatter(
        days="%Y-%m-%d", hours="%H", minutes="%M"
    )

    if not kwargs.get("nolabel", False):
        plot.xaxis.axis_label = "Time"
        plot.yaxis.axis_label = title
        plot.axis.axis_label_text_font_style = "bold"
    else:
        plot.axis.major_label_text_font_size = "0pt"

    plot.grid.grid_line_alpha = 0.3
    plot.x_range = DataRange1d(range_padding=0.0)

    return plot
