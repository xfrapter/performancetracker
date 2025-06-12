import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW
from datetime import datetime, timedelta
from ..styles import (
    CONTENT_STYLE, SCROLL_CONTAINER_STYLE, H2_STYLE, LABEL_STYLE,
    CARD_STYLE, TEXT_COLOR, SUCCESS_COLOR, ERROR_COLOR
)

def create(app):
    """Create the daily view."""
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
        "Daily Overview",
        style=H2_STYLE
    ))
    container.add(header)

    # Date Navigation
    nav_box = toga.Box(style=Pack(direction=ROW, padding_bottom=10))
    
    prev_day_btn = toga.Button(
        "◀ Previous",
        on_press=lambda w: update_day(app, container, -1),
        style=Pack(padding=5, color=TEXT_COLOR)
    )
    nav_box.add(prev_day_btn)
    
    date_label = toga.Label(
        datetime.now().strftime("%B %d, %Y"),
        style=LABEL_STYLE
    )
    nav_box.add(date_label)
    
    next_day_btn = toga.Button(
        "Next ▶",
        on_press=lambda w: update_day(app, container, 1),
        style=Pack(padding=5, color=TEXT_COLOR)
    )
    nav_box.add(next_day_btn)
    
    container.add(nav_box)

    # Content Area
    content_box = toga.Box(style=Pack(direction=COLUMN))
    container.add(content_box)

    # Initial day display
    update_day(app, content_box, 0)

    scroll_container.content = container
    return scroll_container

def update_day(app, container, day_offset):
    """Update the daily view based on the selected day."""
    # Clear existing content
    container.clear()

    # Calculate target date
    today = datetime.now()
    target_date = today + timedelta(days=day_offset)
    
    # Get daily stats
    stats = app.db.get_daily_stats(target_date)
    
    if not stats or not stats.get('total_records'):
        container.add(toga.Label(
            "No records for this day.",
            style=Pack(
                padding=10,
                font_style='italic',
                text_align='center',
                color=TEXT_COLOR
            )
        ))
        return

    # Summary Box
    summary_box = toga.Box(style=Pack(
        direction=COLUMN,
        padding=10,
        background_color=CARD_STYLE['background_color'],
        border_radius=5,
        margin_bottom=10
    ))
    
    # Average Performance
    perf_color = SUCCESS_COLOR if stats['avg_performance'] >= 100 else ERROR_COLOR
    summary_box.add(toga.Label(
        f"Daily Average: {stats['avg_performance']:.1f}%",
        style=Pack(font_size=16, color=perf_color, padding_bottom=5)
    ))
    
    # Total Records
    summary_box.add(toga.Label(
        f"Total Records: {stats['total_records']}",
        style=Pack(font_size=14, padding_bottom=5, color=TEXT_COLOR)
    ))
    
    # Total Time
    summary_box.add(toga.Label(
        f"Total Work Time: {stats['total_time']:.1f} minutes",
        style=Pack(font_size=14, color=TEXT_COLOR)
    ))
    
    container.add(summary_box)

    # Records List
    records = app.db.get_records_for_date(target_date)
    
    for record in records:
        record_box = toga.Box(style=Pack(
            direction=COLUMN,
            padding=10,
            background_color='#ffffff',
            border_radius=5,
            margin_bottom=5
        ))
        
        # Task Name and Performance
        task_box = toga.Box(style=Pack(direction=ROW, padding_bottom=5))
        task_box.add(toga.Label(
            record['task_name'],
            style=Pack(font_weight='bold', color=TEXT_COLOR)
        ))
        task_box.add(toga.Label(
            f"Performance: {record['performance_percentage']:.1f}%",
            style=Pack(
                margin_left=10,
                color=SUCCESS_COLOR if record['performance_percentage'] >= 100 else ERROR_COLOR
            )
        ))
        record_box.add(task_box)
        
        # Time Info
        time_info = (
            f"Start: {record['start_time']} | "
            f"Finish: {record['end_time']} | "
            f"Duration: {record['actual_time']:.1f} min"
        )
        record_box.add(toga.Label(time_info, style=Pack(font_size=12, color=TEXT_COLOR)))
        
        # Break and Delay Info
        details = []
        if record['has_break']:
            details.append(f"Break: {record['break_time']:.1f} min")
        if record['has_delays']:
            details.append(f"Delays: {record['delays_time']:.1f} min")
        if record['battery_changes_count'] > 0:
            details.append(f"Battery Changes: {record['battery_changes_count']}")
        
        if details:
            record_box.add(toga.Label(
                " | ".join(details),
                style=Pack(font_size=12, color='#666666')
            ))
        
        container.add(record_box) 