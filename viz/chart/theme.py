from bokeh.themes import Theme

VIZ_CHART_FOREGROUND = "white"
VIZ_CHART_BACKGROUND = "#1380af"
VIZ_CHART_FOREGROUND_BAD = "white"
VIZ_CHART_BACKGROUND_BAD = "#9b2226"
VIZ_CHART_FOREGROUND_NONE = "white"
VIZ_CHART_BACKGROUND_NONE = "#00000000"

blues = [
    "#2828FF",
    "#2020FF",
    "#1818FF",
    "#1010FF",
    "#0808FF",
    "#0000FF",
    "#0000F8",
    "#0000F0",
    "#0000E8",
    "#0000E0",
    "#0000D8",
    "#0000D0",
    "#0000C8",
    "#0000C0",
    "#0000B8",
    "#0000B0",
    "#0000A8",
    "#0000A0",
    "#000098",
    "#000090",
    "#000088",
    "#000080",
    "#000078",
    "#000070",
    "#000068",
    "#000060",
    "#000058",
    "#000050",
    "#000048",
    "#000040",
    "#000038",
    "#000030",
]

reds = [
    "#FF2828",
    "#FF2020",
    "#FF1818",
    "#FF1010",
    "#FF0808",
    "#FF0000",
    "#F80000",
    "#F00000",
    "#E80000",
    "#E00000",
    "#D80000",
    "#D00000",
    "#C80000",
    "#C00000",
    "#B80000",
    "#B00000",
    "#A80000",
    "#A00000",
    "#980000",
    "#900000",
    "#880000",
    "#800000",
    "#780000",
    "#700000",
    "#680000",
    "#600000",
    "#580000",
    "#500000",
    "#480000",
    "#400000",
    "#380000",
    "#300000",
]


import random
from typing import List


def generate_color(theme: str) -> str:
    if theme == "pastel":
        r = float(random.randint(150, 255))
        g = float(random.randint(150, 255))
        b = float(random.randint(150, 255))
    elif theme == "dark":
        r = float(random.randint(0, 105))
        g = float(random.randint(0, 105))
        b = float(random.randint(0, 105))
    elif theme == "bright":
        r = float(random.randint(0, 255))
        g = float(random.randint(0, 255))
        b = float(random.randint(0, 255))
        max_val = max(r, g, b)
        if max_val < 150:
            r *= 1.5
            g *= 1.5
            b *= 1.5
    else:
        # Default to random colors if theme is not specified
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)

    hex_color = "#{:02x}{:02x}{:02x}".format(int(r), int(g), int(b))
    return hex_color


def generate_colors(count: int, theme: str = "default") -> List[str]:
    to_return: List[str] = []
    for _ in range(count):
        to_return.append(generate_color(theme))
    return to_return


THEME_RED = {
    "attrs": {
        "Plot": {
            "border_fill_color": VIZ_CHART_BACKGROUND_BAD,
            "outline_line_color": VIZ_CHART_BACKGROUND_BAD,
            "background_fill_color": VIZ_CHART_BACKGROUND_BAD,
        },
        "Axis": {
            #
            "axis_line_color": None,
            "major_tick_line_color": VIZ_CHART_FOREGROUND_BAD,
            "minor_tick_line_color": VIZ_CHART_FOREGROUND_BAD,
            "axis_label_text_color": VIZ_CHART_FOREGROUND_BAD,
            "major_label_text_color": VIZ_CHART_FOREGROUND_BAD,
        },
        "Grid": {"grid_line_dash": [6, 4], "grid_line_alpha": 0.9},
        "Title": {"text_color": VIZ_CHART_FOREGROUND_BAD},
    }
}

THEME_BLUE = {
    "attrs": {
        "Plot": {
            "border_fill_color": VIZ_CHART_BACKGROUND,
            "outline_line_color": VIZ_CHART_BACKGROUND,
            "background_fill_color": VIZ_CHART_BACKGROUND,
        },
        "Axis": {
            #
            "axis_line_color": None,
            "major_tick_line_color": VIZ_CHART_FOREGROUND,
            "minor_tick_line_color": VIZ_CHART_FOREGROUND,
            "axis_label_text_color": VIZ_CHART_FOREGROUND,
            "major_label_text_color": VIZ_CHART_FOREGROUND,
        },
        "Grid": {"grid_line_dash": [6, 4], "grid_line_alpha": 0.9},
        "Title": {"text_color": VIZ_CHART_FOREGROUND},
    }
}

THEME_NONE = {
    "attrs": {
        "Plot": {
            "border_fill_color": VIZ_CHART_BACKGROUND_NONE,
            "outline_line_color": VIZ_CHART_BACKGROUND_NONE,
            "background_fill_color": VIZ_CHART_BACKGROUND_NONE,
        },
        "Axis": {
            #
            "axis_line_color": None,
            "major_tick_line_color": VIZ_CHART_FOREGROUND_NONE,
            "minor_tick_line_color": VIZ_CHART_FOREGROUND_NONE,
            "axis_label_text_color": VIZ_CHART_FOREGROUND_NONE,
            "major_label_text_color": VIZ_CHART_FOREGROUND_NONE,
        },
        "Grid": {"grid_line_dash": [6, 4], "grid_line_alpha": 0.9},
        "Title": {"text_color": VIZ_CHART_FOREGROUND_NONE},
    }
}

theme_red = Theme(json=THEME_RED)
theme_blue = Theme(json=THEME_BLUE)
theme_none = Theme(json=THEME_NONE)


def find_theme(**kwargs) -> Theme:
    if kwargs.get("theme_none", False):
        return theme_none

    elif kwargs.get("theme_bad", False):
        return theme_red

    return theme_blue


def find_color_bg(**kwargs) -> str:
    if kwargs.get("theme_none", False):
        return VIZ_CHART_BACKGROUND_NONE

    elif kwargs.get("theme_bad", False):
        return VIZ_CHART_BACKGROUND_BAD

    return VIZ_CHART_BACKGROUND


def find_color_fg(**kwargs) -> str:
    if kwargs.get("theme_none", False):
        return VIZ_CHART_FOREGROUND_NONE

    elif kwargs.get("theme_bad", False):
        return VIZ_CHART_FOREGROUND_BAD

    return VIZ_CHART_FOREGROUND


def cleanup(to_clean: str, **kwargs) -> str:
    color: str = VIZ_CHART_BACKGROUND
    if kwargs.get("theme_bad", False):
        color = VIZ_CHART_BACKGROUND_BAD

    return to_clean.replace("body {", "body {\n\t\t" + f" background-color: {color};")


def add_autoreload(to_clean: str, **kwargs) -> str:
    if not kwargs.get("reload"):
        return to_clean

    meta_tag = '<meta http-equiv="refresh" content="60">'
    return to_clean.replace("<head>", "<head>" + meta_tag, 1)
