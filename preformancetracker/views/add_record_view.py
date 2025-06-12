import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW
from datetime import datetime, timedelta
from ..styles import (
    CONTENT_STYLE, SCROLL_CONTAINER_STYLE, H2_STYLE, 
    LABEL_STYLE, FORM_STYLE, CARD_STYLE, SUCCESS_BUTTON_STYLE, TEXT_COLOR, PRIMARY_COLOR
)

def _update_task_name(app):
    fw = app.form_widgets
    try:
        start_str, finish_str = fw['start_input'].value, fw['finish_input'].value
        datetime.strptime(start_str, '%H:%M'); datetime.strptime(finish_str, '%H:%M')
        fw['task_display'].text = f"{datetime.now().strftime('%a')} {start_str}-{finish_str}"
    except (ValueError, TypeError, KeyError):
        fw['task_display'].text = "Invalid time format..."

def _toggle_details(app):
    """Toggle visibility of break details."""
    fw = app.form_widgets
    fw['break_details'].style.visibility = 'visible' if fw['break_checkbox'].value else 'hidden'

def _toggle_delays(app):
    """Toggle visibility of delays details."""
    fw = app.form_widgets
    fw['delay_details'].style.visibility = 'visible' if fw['delays_checkbox'].value else 'hidden'

def _validate_number(value, min_value=0):
    try:
        num = float(value)
        return num >= min_value
    except (ValueError, TypeError):
        return False

def create(app, edit_mode=False, record_id=None):
    app.editing_record_id = record_id if edit_mode else None
    record = app.db.get_record_by_id(record_id) if edit_mode else {}

    container = toga.ScrollContainer(style=SCROLL_CONTAINER_STYLE)
    content = toga.Box(style=CONTENT_STYLE)
    content.add(app._create_header("Edit Record" if edit_mode else "Add Record", lambda w: app.set_view('view_records' if edit_mode else 'home')))

    now = datetime.now()
    app.form_widgets = {
        'task_display': toga.Label("...", style=Pack(padding=10, background_color=CARD_STYLE.background_color, color='#BB86FC', margin_bottom=15, font_weight='bold', text_align='center')),
        'target_input': toga.TextInput(
            value=str(record.get('target_time', 30.0)),
            placeholder="Enter target time in minutes",
            style=FORM_STYLE
        ),
        'start_input': toga.TextInput(
            value=record.get('start_time', now.strftime('%H:%M')),
            placeholder="HH:MM",
            on_change=lambda w: _update_task_name(app),
            style=FORM_STYLE
        ),
        'finish_input': toga.TextInput(
            value=record.get('end_time', (now + timedelta(minutes=30)).strftime('%H:%M')),
            placeholder="HH:MM",
            on_change=lambda w: _update_task_name(app),
            style=FORM_STYLE
        ),
        'break_checkbox': toga.Switch(
            "Include Break",
            value=bool(record.get('has_break')),
            on_change=lambda w: _toggle_details(app),
            style=Pack(color=TEXT_COLOR, margin_top=10)
        ),
        'paid_break_input': toga.TextInput(
            value=str(record.get('paid_break_time', 0)),
            placeholder="Enter paid break time in minutes",
            style=FORM_STYLE
        ),
        'unpaid_break_input': toga.TextInput(
            value=str(record.get('unpaid_break_time', 0)),
            placeholder="Enter unpaid break time in minutes",
            style=FORM_STYLE
        ),
        'delays_checkbox': toga.Switch(
            "Include Delays",
            value=bool(record.get('has_delays')),
            on_change=lambda w: _toggle_delays(app),
            style=Pack(color=TEXT_COLOR, margin_top=10)
        ),
        'delays_input': toga.TextInput(
            value=str(record.get('delays_time', 0)),
            placeholder="Enter delays time in minutes",
            style=FORM_STYLE
        ),
        'delays_notes_input': toga.TextInput(
            value=record.get('delay_notes', ''),
            placeholder="Enter delay notes",
            style=FORM_STYLE
        )
    }
    fw = app.form_widgets

    content.add(toga.Label("Task Name:", style=LABEL_STYLE))
    content.add(fw['task_display'])
    
    content.add(toga.Label("Target Time (minutes):", style=LABEL_STYLE))
    content.add(fw['target_input'])
    
    time_box = toga.Box(style=Pack(direction=ROW))
    time_box.add(toga.Box(
        style=Pack(flex=1, direction=COLUMN, margin_right=5),
        children=[
            toga.Label("Start Time:", style=LABEL_STYLE),
            fw['start_input']
        ]
    ))
    time_box.add(toga.Box(
        style=Pack(flex=1, direction=COLUMN, margin_left=5),
        children=[
            toga.Label("Finish Time:", style=LABEL_STYLE),
            fw['finish_input']
        ]
    ))
    content.add(time_box)
    
    break_details = toga.Box(
        style=Pack(direction=COLUMN, margin_top=5),
        children=[
            toga.Label("Paid Break (min):", style=LABEL_STYLE),
            fw['paid_break_input'],
            toga.Label("Unpaid Break (min):", style=LABEL_STYLE),
            fw['unpaid_break_input']
        ]
    )
    delay_details = toga.Box(
        style=Pack(direction=COLUMN, margin_top=5),
        children=[
            toga.Label("Delays Time (min):", style=LABEL_STYLE),
            fw['delays_input'],
            toga.Label("Delay Notes:", style=LABEL_STYLE),
            fw['delays_notes_input']
        ]
    )
    fw.update({'break_details': break_details, 'delay_details': delay_details})

    content.add(fw['break_checkbox'])
    content.add(break_details)
    content.add(fw['delays_checkbox'])
    content.add(delay_details)

    content.add(toga.Button(
        "💾 Save Record",
        on_press=lambda w: app.add_background_task(app.save_record_async),
        style=SUCCESS_BUTTON_STYLE
    ))

    container.content = content
    _update_task_name(app)
    _toggle_details(app)
    _toggle_delays(app)
    return container 