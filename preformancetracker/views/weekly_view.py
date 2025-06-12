import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW
from datetime import datetime, timedelta
from ..styles import (
    CONTENT_STYLE, SCROLL_CONTAINER_STYLE, H2_STYLE, LABEL_STYLE,
    CARD_STYLE, TEXT_COLOR, SUCCESS_COLOR, ERROR_COLOR
)

def create(app):
    """Create the weekly view."""
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
        "Weekly Overview",
        style=H2_STYLE
    ))
    container.add(header)

    # Week Navigation
    nav_box = toga.Box(style=Pack(direction=ROW, padding_bottom=10))
    
    prev_week_btn = toga.Button(
        "◀ Previous",
        on_press=lambda w: update_week(app, container, -1),
        style=Pack(padding=5, color=TEXT_COLOR)
    )
    nav_box.add(prev_week_btn)
    
    week_label = toga.Label(
        get_week_range(0),
        style=LABEL_STYLE
    )
    nav_box.add(week_label)
    
    next_week_btn = toga.Button(
        "Next ▶",
        on_press=lambda w: update_week(app, container, 1),
        style=Pack(padding=5, color=TEXT_COLOR)
    )
    nav_box.add(next_week_btn)
    
    container.add(nav_box)

    # Content Area
    content_box = toga.Box(style=Pack(direction=COLUMN))
    container.add(content_box)

    # Initial week display
    update_week(app, content_box, 0)

    scroll_container.content = container
    return scroll_container

def get_week_range(week_offset):
    """Get the date range for the specified week offset."""
    today = datetime.now()
    start_of_week = today - timedelta(days=today.weekday() + (7 * week_offset))
    end_of_week = start_of_week + timedelta(days=6)
    return f"{start_of_week.strftime('%b %d')} - {end_of_week.strftime('%b %d, %Y')}"

def update_week(app, container, week_offset):
    """Update the weekly view based on the selected week."""
    # Clear existing content
    container.clear()

    # Calculate week dates
    today = datetime.now()
    start_of_week = today - timedelta(days=today.weekday() + (7 * week_offset))
    
    # Get weekly stats
    stats = app.db.get_weekly_stats(start_of_week)
    
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
        f"Weekly Average: {stats['avg_performance']:.1f}%",
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

    # Daily Breakdown
    for day_offset in range(7):
        date = start_of_week + timedelta(days=day_offset)
        day_stats = app.db.get_daily_stats(date)
        
        if day_stats:
            day_box = toga.Box(style=Pack(
                direction=COLUMN,
                padding=10,
                background_color='#ffffff',
                border_radius=5,
                margin_bottom=5
            ))
            
            # Day Header
            day_box.add(toga.Label(
                date.strftime("%A, %B %d"),
                style=Pack(font_size=14, font_weight='bold', padding_bottom=5, color=TEXT_COLOR)
            ))
            
            # Performance
            perf_color = SUCCESS_COLOR if day_stats['avg_performance'] >= 100 else ERROR_COLOR
            day_box.add(toga.Label(
                f"Performance: {day_stats['avg_performance']:.1f}%",
                style=Pack(font_size=12, color=perf_color, padding_bottom=5)
            ))
            
            # Records and Time
            day_box.add(toga.Label(
                f"Records: {day_stats['total_records']} | Time: {day_stats['total_time']:.1f} min",
                style=Pack(font_size=12, color=TEXT_COLOR)
            ))
            
            container.add(day_box) 