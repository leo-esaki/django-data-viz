from typing import Callable, List, Optional

import pandas as pd
from bokeh.models import (
    ColumnDataSource,
    FactorRange,
    HoverTool,
    InlineStyleSheet,
    TapTool,
    CustomJS,
)
from bokeh.plotting import figure
from bokeh.transform import factor_cmap

from viz.config import (
    VIZ_CHART_WIDTH,
    VIZ_CHART_HEIGHT,
)
from viz.chart.theme import blues, reds
from viz.utils import build_empty


def make_human_readable(key: str) -> str:
    if key is None:
        return "Unknown"

    return " ".join(word.capitalize() for word in key.split("_"))


def preprocess_data(
    data: pd.DataFrame,
    group_by: str,
    lowest: bool = False,
    lower_than: Optional[float] = None,
    greater_than: Optional[float] = None,
    value_col: Optional[str] = None,
    value_avg: Optional[bool] = False,
) -> pd.DataFrame:
    if value_col:
        agg_func = "mean" if value_avg else "sum"
        grouped = (
            data.groupby(group_by)[value_col]
            .agg(agg_func)
            .reset_index(name="total_value")
        )
        value_column = "total_value"
    else:
        grouped = data.groupby(group_by).size().reset_index(name="count")
        value_column = "count"

    if lower_than is not None:
        grouped = grouped[grouped[value_column] < lower_than]

    if greater_than is not None:
        grouped = grouped[grouped[value_column] > greater_than]

    # Sort the grouped data by the value column in descending order
    grouped = grouped.sort_values(by=value_column, ascending=lowest)

    # Limit the number of items to display if top_n is provided
    grouped = grouped.head(len(blues))

    return grouped


def create_chart(
    grouped: pd.DataFrame,
    group_by: str,
    value_column: str,
    title: str,
    decimal_places: Optional[int] = 2,
    theme_bad: Optional[bool] = False,
    url_column: Optional[str] = None,
    url_prefix: Optional[str | Callable] = None,
    **kwargs,
) -> figure:
    stylesheets: List[InlineStyleSheet] = []
    if kwargs.get("custom_css", False):
        stylesheets.append(InlineStyleSheet(css=kwargs["custom_css"]))

    # Create a ColumnDataSource from the grouped data
    source = ColumnDataSource(grouped)

    # Create the bar chart figure
    plot = figure(
        tools="",
        width=VIZ_CHART_WIDTH,
        height=VIZ_CHART_HEIGHT,
        toolbar_location=None,
        sizing_mode="stretch_both",
        x_range=FactorRange(*grouped[group_by]),
        stylesheets=stylesheets,
    )

    plot.title.text = title if not kwargs.get("notitle", False) else None

    # Make the chart mousehoverable
    plot.add_tools(
        HoverTool(
            tooltips=[
                (make_human_readable(group_by), f"@{group_by}"),
                (
                    make_human_readable(value_column),
                    f"@{value_column}" + f"{{0,0.{str('0' * decimal_places)}}}",
                ),
            ],
            formatters={
                f"@{value_column}": "numeral",
            },
            mode="vline",
        )
    )

    color_palette = reds if theme_bad else blues

    # Add a bar renderer to the plot
    plot.vbar(
        x=group_by,
        top=value_column,
        source=source,
        width=0.9,
        line_color="white",
        fill_color=factor_cmap(
            group_by, palette=color_palette, factors=grouped[group_by].unique()
        ),
        nonselection_fill_alpha=0.8,
        nonselection_fill_color=blues[0],
    )

    # Adjust the layout and styling
    if not kwargs.get("nolabel", False):
        plot.yaxis.axis_label = title

    plot.y_range.start = 0
    plot.grid.grid_line_alpha = 0.3
    plot.xaxis.major_label_orientation = 0.0
    plot.axis.axis_label_text_font_style = "bold"
    plot.xaxis.major_label_text_font_size = "0pt"

    # Add the OpenURL interaction if url_column is provided
    if url_column:
        if not url_prefix:
            raise ValueError("No url_prefix defined for url_column")

        if url_column not in grouped.columns:
            return plot

        if callable(url_prefix):
            urls: List[str] = [
                f"{url_prefix(url_item)}" for url_item in grouped[url_column]
            ]

        else:
            urls: List[str] = [
                f"{url_prefix}{url_item}" for url_item in grouped[url_column]
            ]

        callback = CustomJS(
            args=dict(data=urls),
            code="""
                var selected_index = cb_data.source.selected.indices[0];
                var url = data[selected_index];
                window.open(url, '_blank');
                // Clear the selection after opening the URL
                cb_data.source.selected.indices = [];
                cb_data.source.change.emit();""",
        )
        plot.add_tools(TapTool(callback=callback))

    return plot


def chart_bar(
    data: pd.DataFrame,
    title: str,
    group_by: str,
    lowest: bool = False,
    theme_bad: Optional[bool] = False,
    lower_than: Optional[float] = None,
    greater_than: Optional[float] = None,
    value_col: Optional[str] = None,
    value_avg: Optional[bool] = False,
    decimal_places: Optional[int] = 2,
    url_column: Optional[str] = None,
    url_prefix: Optional[str | Callable] = None,
    **kwargs,
) -> figure:
    """
    Creates a bar chart based on the provided DataFrame.

    Args:
        data (pd.DataFrame): The input DataFrame containing the data.
        title (str): The title of the chart.
        group_by (str): The column name to group the data by.
        lowest (bool): Whether to sort in ascending order.
        theme_bad (bool): Indicates if a theme indicating bad performance is used.
        lower_than (Optional[float]): Filter for values lower than this.
        greater_than (Optional[float]): Filter for values greater than this.
        value_col (Optional[str]): The column name to sum or average values.
        value_avg (bool): Whether to compute mean instead of sum.
        decimal_places (int): Number of decimal places in the output.
        url_column (Optional[str]): Column containing URLs for linking.
        url_prefix (Optional[Union[str, Callable]]): Prefix or function for URL manipulation.
        **kwargs: Additional keyword arguments passed to the chart creation function.

    Returns:
        bokeh.plotting.figure: The bar chart figure.
    """
    if len(data) < 1:
        return chart_bar(build_empty(), title, "_id")

    if group_by not in data.columns:
        return chart_bar(build_empty(), title, "_id")

    grouped = preprocess_data(
        data, group_by, lowest, lower_than, greater_than, value_col, value_avg
    )

    value_column = "total_value" if value_col else "count"

    return create_chart(
        grouped,
        group_by,
        value_column,
        title,
        decimal_places,
        theme_bad,
        url_column,
        url_prefix,
        **kwargs,
    )
