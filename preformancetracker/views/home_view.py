import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW
from datetime import datetime
from ..styles import H1_STYLE, CONTENT_STYLE, SCROLL_CONTAINER_STYLE, ACTION_BUTTON_STYLE, SUCCESS_COLOR, TEXT_COLOR, PRIMARY_COLOR

from . import daily_view, weekly_view, calendar_view

def create(app):
    container = toga.ScrollContainer(style=SCROLL_CONTAINER_STYLE)
    content = toga.Box(style=CONTENT_STYLE)

    title_box = toga.Box(style=Pack(direction=COLUMN, margin_bottom=20, align_items='center'))
    title_box.add(toga.Label("Performance Tracker", style=H1_STYLE))
    now = datetime.now()
    title_box.add(toga.Label(f"{now.strftime('%A, %B %d, %Y')}", style=Pack(color=TEXT_COLOR)))
    content.add(title_box)

    app.current_view_content = toga.Box(style=Pack(direction=COLUMN, flex=1))
    content.add(app.current_view_content)
    app.current_view_content.add(toga.Label("Welcome! Add a record to get started.", style=Pack(text_align='center', color=TEXT_COLOR, font_size=16)))

    actions_box = toga.Box(style=Pack(direction=COLUMN, margin_top=20, align_items='center'))
    actions = [
        ("➕ Add Record", lambda w: app.set_view('add_record'), PRIMARY_COLOR),
        ("📋 View Records", lambda w: app.set_view('view_records'), '#2196F3'),
        ("📊 Statistics", lambda w: app.set_view('statistics'), '#9C27B0'),
        ("🐞 Debug", lambda w: app.set_view('debug'), '#FF5722'),
    ]
    for label, handler, color in actions:
        style = ACTION_BUTTON_STYLE.copy()
        style.background_color = color
        style.color = 'white' if color != PRIMARY_COLOR else 'black'
        actions_box.add(toga.Button(label, on_press=handler, style=style))
    content.add(actions_box)

    container.content = content
    return container 