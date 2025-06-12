import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW
from datetime import datetime, timedelta
from ..styles import (
    CONTENT_STYLE, SCROLL_CONTAINER_STYLE, H2_STYLE, 
    LABEL_STYLE, CARD_STYLE, TEXT_COLOR
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
    title = toga.Label('Statistics', style=H2_STYLE)
    header.add(title)
    content.add(header)

    # Daily Stats Card
    daily_box = toga.Box(style=CARD_STYLE)
    daily_box.add(toga.Label('Today\'s Performance', style=H2_STYLE))
    
    daily_stats = app.db.get_daily_stats()
    stats = [
        f"Average Performance: {daily_stats['avg_performance']:.1f}%",
        f"Total Records: {daily_stats['total_records']}",
        f"Total Time: {daily_stats['total_time']:.1f} minutes",
        f"Break Time: {daily_stats['total_break_time']:.1f} minutes",
        f"Delay Time: {daily_stats['total_delay_time']:.1f} minutes",
        f"Best Performance: {daily_stats['best_performance']:.1f}%",
        f"Worst Performance: {daily_stats['worst_performance']:.1f}%"
    ]
    for stat in stats:
        daily_box.add(toga.Label(stat, style=LABEL_STYLE))
    content.add(daily_box)

    # Weekly Stats Card
    weekly_box = toga.Box(style=CARD_STYLE)
    weekly_box.add(toga.Label('This Week\'s Performance', style=H2_STYLE))
    
    weekly_stats = app.db.get_weekly_stats()
    stats = [
        f"Average Performance: {weekly_stats['avg_performance']:.1f}%",
        f"Total Records: {weekly_stats['total_records']}",
        f"Total Time: {weekly_stats['total_time']:.1f} minutes",
        f"Break Time: {weekly_stats['total_break_time']:.1f} minutes",
        f"Delay Time: {weekly_stats['total_delay_time']:.1f} minutes",
        f"Active Days: {weekly_stats['active_days']}",
        f"Best Performance: {weekly_stats['best_performance']:.1f}%",
        f"Worst Performance: {weekly_stats['worst_performance']:.1f}%"
    ]
    for stat in stats:
        weekly_box.add(toga.Label(stat, style=LABEL_STYLE))
    content.add(weekly_box)

    # Navigation Buttons
    nav_box = toga.Box(style=Pack(direction=ROW, padding_top=20))
    
    views = [
        ('📅 Calendar', 'calendar'),
        ('📊 Weekly', 'weekly'),
        ('📈 Daily', 'daily')
    ]
    
    for label, view in views:
        button = toga.Button(
            label,
            on_press=lambda w, v=view: app.set_view(v),
            style=Pack(flex=1, padding=10, margin=5, background_color='#2196F3', color='white')
        )
        nav_box.add(button)
    
    content.add(nav_box)
    container.content = content
    return container 