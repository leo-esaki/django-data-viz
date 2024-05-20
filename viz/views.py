from django.http import HttpResponse

from viz.chart.chart_builder import render_html_chart
from viz.chart.charts import show_user_latency, show_user_latency_by_user


def show_viz(param):
    return HttpResponse(
        render_html_chart(show_user_latency(), show_user_latency_by_user())
    )
