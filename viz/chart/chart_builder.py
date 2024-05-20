from typing import List

from bokeh.embed import file_html
from bokeh.layouts import column
from bokeh.plotting import figure
from bokeh.resources import CDN

from viz.chart.theme import (
    cleanup,
    add_autoreload,
    find_theme,
)


def build_chart(chart_funcs: List[figure]) -> figure:
    to_return = column(
        *chart_funcs,
        sizing_mode="stretch_both",
    )

    to_return.margin = [20, 20, 20, 20]

    return to_return


def show_chart_types(*chart_funcs: List[figure], **kwargs) -> None:
    from bokeh.io import curdoc
    from bokeh.plotting import show

    doc = curdoc()

    doc.theme = find_theme(**kwargs)

    show(build_chart(chart_funcs), title="Human Validator Bot")

    import sys

    sys.exit(0)


def render_html_chart(*chart_funcs: List[figure], **kwargs) -> str:
    theme = find_theme(**kwargs)
    return add_autoreload(
        cleanup(
            file_html(
                build_chart(chart_funcs),
                CDN,
                theme=theme,
                title="Human Validator Bot",
            ),
            **kwargs,
        ),
        **kwargs,
    )
