import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW
from datetime import datetime
from ..styles import (
    CONTENT_STYLE, SCROLL_CONTAINER_STYLE, H2_STYLE, 
    LABEL_STYLE, CARD_STYLE, TEXT_COLOR, SUCCESS_BUTTON_STYLE
)

def create(app):
    """Create the finish shift view."""
    container = toga.ScrollContainer(style=SCROLL_CONTAINER_STYLE)
    content = toga.Box(style=CONTENT_STYLE)

    # Header
    header = toga.Box(style=Pack(direction=ROW, padding_bottom=20))
    back_button = toga.Button(
        '← Back',
        on_press=lambda w: app.set_view('home'),
        style=Pack(padding_right=10, color=TEXT_COLOR)
    )
    header.add(back_button)
    title = toga.Label('Finish Shift', style=H2_STYLE)
    header.add(title)
    content.add(header)

    # Content Card
    card = toga.Box(style=CARD_STYLE)

    # Current Time
    current_time = datetime.now().strftime('%H:%M')
    time_label = toga.Label(
        f'Current Time: {current_time}',
        style=LABEL_STYLE
    )
    card.add(time_label)

    # Finish Button
    finish_button = toga.Button(
        '⏹️ Finish Shift',
        on_press=app.finish_shift_async,
        style=SUCCESS_BUTTON_STYLE
    )
    card.add(finish_button)

    content.add(card)
    container.content = content
    return container 