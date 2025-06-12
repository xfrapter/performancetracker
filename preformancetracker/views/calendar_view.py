import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW
from datetime import datetime, timedelta
from ..styles import (
    CONTENT_STYLE, SCROLL_CONTAINER_STYLE, H2_STYLE, LABEL_STYLE,
    CARD_STYLE, TEXT_COLOR, SUCCESS_COLOR, ERROR_COLOR
)

def create(app):
    """Create the calendar view."""
    # Create scroll container for better responsiveness
    scroll_container = toga.ScrollContainer(style=SCROLL_CONTAINER_STYLE)
    container = toga.Box(direction=COLUMN, style=CONTENT_STYLE)

    # Header
    header = toga.Box(style=Pack(direction=ROW, padding_bottom=10))
    header.add(toga.Button(
        "← Back",
        on_press=lambda w: app.set_view('home'),
        style=Pack(padding=5, color=TEXT_COLOR)
    ))
    header.add(toga.Label(
        "Calendar View",
        style=H2_STYLE
    ))
    container.add(header)

    # Month Navigation
    nav_box = toga.Box(style=Pack(direction=ROW, padding_bottom=10))
    
    prev_month_btn = toga.Button(
        "◀ Previous",
        on_press=lambda w: update_calendar(app, calendar_box, -1),
        style=Pack(padding=5, color=TEXT_COLOR)
    )
    nav_box.add(prev_month_btn)
    
    month_label = toga.Label(
        datetime.now().strftime("%B %Y"),
        style=LABEL_STYLE
    )
    nav_box.add(month_label)
    
    next_month_btn = toga.Button(
        "Next ▶",
        on_press=lambda w: update_calendar(app, calendar_box, 1),
        style=Pack(padding=5, color=TEXT_COLOR)
    )
    nav_box.add(next_month_btn)
    
    container.add(nav_box)

    # Calendar Grid
    calendar_box = toga.Box(style=Pack(direction=COLUMN))
    container.add(calendar_box)

    # Initial calendar display
    update_calendar(app, calendar_box, 0)

    scroll_container.content = container
    return scroll_container

def update_calendar(app, container, month_offset):
    """Update the calendar display based on the selected month."""
    # Clear existing calendar
    container.clear()

    # Calculate the target month
    today = datetime.now()
    target_month = today.replace(day=1) + timedelta(days=32 * month_offset)
    target_month = target_month.replace(day=1)

    # Create calendar grid
    grid = toga.Box(style=Pack(direction=COLUMN))
    
    # Add weekday headers
    weekdays = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']
    header_row = toga.Box(style=Pack(direction=ROW))
    for day in weekdays:
        header_row.add(toga.Label(
            day,
            style=Pack(
                flex=1,
                text_align='center',
                font_weight='bold',
                padding=5,
                color=TEXT_COLOR
            )
        ))
    grid.add(header_row)

    # Add calendar days
    first_day = target_month.weekday()
    days_in_month = (target_month.replace(month=target_month.month % 12 + 1, day=1) - timedelta(days=1)).day
    
    current_row = toga.Box(style=Pack(direction=ROW))
    
    # Add empty cells for days before the first of the month
    for _ in range(first_day):
        current_row.add(toga.Box(style=Pack(flex=1, padding=5)))
    
    # Add days of the month
    for day in range(1, days_in_month + 1):
        if len(current_row.children) == 7:
            grid.add(current_row)
            current_row = toga.Box(style=Pack(direction=ROW))
        
        # Get performance data for this day
        date = target_month.replace(day=day)
        stats = app.db.get_daily_stats(date)
        
        # Create day cell
        day_box = toga.Box(style=Pack(
            flex=1,
            padding=5,
            background_color=CARD_STYLE['background_color'] if stats else '#ffffff',
            border_radius=5
        ))
        
        # Add day number
        day_box.add(toga.Label(
            str(day),
            style=Pack(
                text_align='center',
                font_weight='bold',
                color=TEXT_COLOR
            )
        ))
        
        # Add performance indicator if available
        if stats and stats.get('avg_performance'):
            perf_color = SUCCESS_COLOR if stats['avg_performance'] >= 100 else ERROR_COLOR
            day_box.add(toga.Label(
                f"{stats['avg_performance']:.0f}%",
                style=Pack(
                    text_align='center',
                    color=perf_color,
                    font_size=12
                )
            ))
        
        current_row.add(day_box)
    
    # Add remaining empty cells
    while len(current_row.children) < 7:
        current_row.add(toga.Box(style=Pack(flex=1, padding=5)))
    
    grid.add(current_row)
    container.add(grid) 