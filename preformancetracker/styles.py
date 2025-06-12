from toga.style import Pack
from toga.style.pack import COLUMN, ROW

# Colors
PRIMARY_COLOR = '#6200EE'
SECONDARY_COLOR = '#03DAC6'
SUCCESS_COLOR = '#4CAF50'
ERROR_COLOR = '#F44336'
WARNING_COLOR = '#FFC107'
TEXT_COLOR = '#333333'
BACKGROUND_COLOR = '#FFFFFF'
CARD_BACKGROUND = '#F5F5F5'

# Main container style
MAIN_CONTAINER_STYLE = Pack(
    direction=COLUMN,
    flex=1,
    margin=20,
    background_color=BACKGROUND_COLOR
)

# Content container style
CONTENT_STYLE = Pack(
    direction=COLUMN,
    flex=1,
    margin=10
)

# Scroll container style
SCROLL_CONTAINER_STYLE = Pack(
    direction=COLUMN,
    flex=1
)

# Header styles
H1_STYLE = Pack(
    font_size=24,
    font_weight='bold',
    color=PRIMARY_COLOR,
    margin_bottom=10
)

H2_STYLE = Pack(
    font_size=20,
    font_weight='bold',
    color=PRIMARY_COLOR,
    margin_bottom=8
)

# Form styles
LABEL_STYLE = Pack(
    color=TEXT_COLOR,
    margin_bottom=5,
    font_size=14
)

FORM_STYLE = Pack(
    margin_bottom=15,
    padding=10,
    background_color=CARD_BACKGROUND
)

# Card style
CARD_STYLE = Pack(
    background_color=CARD_BACKGROUND,
    margin=10,
    padding=15
)

# Button styles
ACTION_BUTTON_STYLE = Pack(
    margin=5,
    padding=10,
    width=200
)

SUCCESS_BUTTON_STYLE = Pack(
    background_color=SUCCESS_COLOR,
    color='white',
    margin=5,
    padding=10,
    width=200
)

# Table styles
TABLE_STYLE = Pack(
    flex=1,
    margin=10
)

TABLE_HEADER_STYLE = Pack(
    background_color=PRIMARY_COLOR,
    color='white',
    font_weight='bold'
)

# Chart styles
CHART_STYLE = Pack(
    flex=1,
    margin=10,
    background_color=CARD_BACKGROUND,
    padding=15
)

# Debug panel styles
DEBUG_PANEL_STYLE = Pack(
    background_color='#2D2D2D',
    color='#FFFFFF',
    margin=10,
    padding=15
)

DEBUG_TEXT_STYLE = Pack(
    color='#00FF00',
    font_family='monospace',
    font_size=12,
    margin_bottom=5
) 