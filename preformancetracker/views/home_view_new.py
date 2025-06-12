import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW
from datetime import datetime
from ..styles import H1_STYLE, CONTENT_STYLE, SCROLL_CONTAINER_STYLE, ACTION_BUTTON_STYLE, SUCCESS_COLOR, TEXT_COLOR, PRIMARY_COLOR
from ..debug import logger

from . import daily_view, weekly_view, calendar_view

def create_home_view(app):
    """Create the home view with modern styling."""
    logger.info("Creating home view")
    
    # Main container
    main_box = toga.Box(style=CONTENT_STYLE)
    
    # Header
    header = toga.Box(style=Pack(direction=ROW, margin_bottom=20))
    title = toga.Label('Performance Tracker', style=H1_STYLE)
    header.add(title)
    
    # Content container with scroll
    content = toga.ScrollContainer(style=SCROLL_CONTAINER_STYLE)
    content_box = toga.Box(style=Pack(direction=COLUMN, margin=10))
    
    # Quick actions section
    quick_actions = toga.Box(style=Pack(direction=COLUMN, margin_bottom=20))
    quick_actions.add(toga.Label('Quick Actions', style=Pack(font_size=18, font_weight='bold', margin_bottom=10)))
    
    # Action buttons
    add_record_btn = toga.Button('Add Record', style=ACTION_BUTTON_STYLE, on_press=lambda w: app.show_view('add_record'))
    view_records_btn = toga.Button('View Records', style=ACTION_BUTTON_STYLE, on_press=lambda w: app.show_view('view_records'))
    stats_btn = toga.Button('Statistics', style=ACTION_BUTTON_STYLE, on_press=lambda w: app.show_view('statistics'))
    
    quick_actions.add(add_record_btn)
    quick_actions.add(view_records_btn)
    quick_actions.add(stats_btn)
    
    # Shift management section
    shift_management = toga.Box(style=Pack(direction=COLUMN, margin_bottom=20))
    shift_management.add(toga.Label('Shift Management', style=Pack(font_size=18, font_weight='bold', margin_bottom=10)))
    
    start_shift_btn = toga.Button('Start Shift', style=ACTION_BUTTON_STYLE, on_press=lambda w: app.show_view('start_shift'))
    finish_shift_btn = toga.Button('Finish Shift', style=ACTION_BUTTON_STYLE, on_press=lambda w: app.show_view('finish_shift'))
    
    shift_management.add(start_shift_btn)
    shift_management.add(finish_shift_btn)
    
    # Debug section
    debug_section = toga.Box(style=Pack(direction=COLUMN))
    debug_section.add(toga.Label('Debug', style=Pack(font_size=18, font_weight='bold', margin_bottom=10)))
    
    debug_btn = toga.Button('View Debug Info', style=ACTION_BUTTON_STYLE, on_press=lambda w: app.show_view('debug'))
    debug_section.add(debug_btn)
    
    # Add all sections to content box
    content_box.add(quick_actions)
    content_box.add(shift_management)
    content_box.add(debug_section)
    
    # Add content box to scroll container
    content.content = content_box
    
    # Add header and content to main box
    main_box.add(header)
    main_box.add(content)
    
    return main_box 