import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW
from datetime import datetime
from ..styles import (
    CONTENT_STYLE, SCROLL_CONTAINER_STYLE, H2_STYLE, 
    LABEL_STYLE, CARD_STYLE, TEXT_COLOR, SUCCESS_COLOR, ERROR_COLOR
)

def create(app):
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
    title = toga.Label('Records', style=H2_STYLE)
    header.add(title)
    content.add(header)

    # Records Table
    table = toga.Table(
        headings=['Task', 'Time', 'Performance', 'Actions'],
        style=Pack(flex=1, background_color=CARD_STYLE.background_color)
    )

    # Load records
    records = app.db.get_recent_records()
    for record in records:
        row = [
            record['task_name'],
            f"{record['start_time']} - {record['end_time']}",
            f"{record['performance_percentage']:.1f}%",
            toga.Box(style=Pack(direction=ROW))
        ]
        
        # Add action buttons
        actions_box = toga.Box(style=Pack(direction=ROW))
        
        edit_button = toga.Button(
            '✏️ Edit',
            on_press=lambda w, r=record['id']: app.set_view('add_record', record_id=r),
            style=Pack(padding=5, margin=2, background_color=SUCCESS_COLOR, color='white')
        )
        actions_box.add(edit_button)
        
        delete_button = toga.Button(
            '🗑️ Delete',
            on_press=lambda w, r=record['id']: app.delete_record_async(r),
            style=Pack(padding=5, margin=2, background_color=ERROR_COLOR, color='white')
        )
        actions_box.add(delete_button)
        
        row[3] = actions_box
        table.data.append(row)

    content.add(table)
    container.content = content
    return container 