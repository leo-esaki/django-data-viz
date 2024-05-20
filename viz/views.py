from django.shortcuts import render
from django.http import HttpResponse

from viz.chart.chart_builder import render_html_chart
from viz.chart.charts import show_user_latency, show_user_latency_by_user

# Create your views here.
def index():
	# return HttpResponse("Hello, word. You're at the viz index.")
	return render_html_chart(show_user_latency(), show_user_latency_by_user())
