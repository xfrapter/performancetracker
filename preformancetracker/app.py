import toga
from toga.style import Pack
from toga.style.pack import COLUMN
from datetime import datetime, timedelta
import os
from .database import Database
from .views import home_view_new as home_view, add_record_view, records_view, stats_view, start_shift_view, finish_shift_view
from .styles import MAIN_CONTAINER_STYLE, H1_STYLE
from .debug import logger, get_recent_logs

class PerformanceTrackerApp(toga.App):
    def __init__(self, app_name, app_id):
        super().__init__(app_name, app_id)
        self.db = Database(self.paths)
        self.editing_record_id = None
        self.main_container = None
        self.form_widgets = {}
        logger.info('App initialized')

    def _create_header(self, title, back_handler=None):
        """Create a header with a title and optional back button."""
        header_box = toga.Box(style=Pack(direction='row', padding=10, alignment='center'))
        
        if back_handler:
            back_button = toga.Button('← Back', on_press=back_handler, style=Pack(padding_right=20))
            header_box.add(back_button)
        
        title_label = toga.Label(title, style=H1_STYLE)
        header_box.add(title_label)
        
        return header_box

    def startup(self):
        """Initialize the application."""
        logger.info('App startup')
        # Initialize views
        self.views = {
            'home': home_view.create_home_view(self),
            'add_record': add_record_view.create(self),
            'records': records_view.create(self),
            'stats': stats_view.create(self),
            'start_shift': start_shift_view.create(self),
            'finish_shift': finish_shift_view.create(self),
            'debug': self.create_debug_view()
        }
        
        # Set initial view
        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_container = toga.Box(style=MAIN_CONTAINER_STYLE)
        self.set_view("home")
        self.main_window.content = self.main_container
        self.main_window.show()

    def set_view(self, view_name, **kwargs):
        """Switch to a different view."""
        logger.info(f'Switching to view: {view_name}')
        self.main_container.clear()
        view_creators = {
            "home": home_view.create_home_view,
            "add_record": add_record_view.create,
            "edit_record": add_record_view.create,
            "view_records": records_view.create,
            "statistics": stats_view.create,
            "start_shift": start_shift_view.create,
            "finish_shift": finish_shift_view.create,
            "debug": self.create_debug_view,
        }
        creator = view_creators.get(view_name, home_view.create_home_view)
        view_content = creator(self, **kwargs) if view_name != 'debug' else creator()
        self.main_container.add(view_content)

    def create_debug_view(self):
        box = toga.Box(style=Pack(direction=COLUMN, padding=20))
        box.add(toga.Label('Debug Panel', style=Pack(font_size=20, font_weight='bold', padding_bottom=10)))
        logs = get_recent_logs(50)
        for ts, msg in logs:
            box.add(toga.Label(f"{ts.strftime('%H:%M:%S')} {msg}", style=Pack(font_size=12)))
        back_button = toga.Button('Back to Home', on_press=lambda w: self.set_view('home'))
        box.add(back_button)
        return box

    async def save_record_async(self):
        """Save a performance record asynchronously."""
        try:
            logger.info('Saving record...')
            fw = self.form_widgets
            start_dt = datetime.strptime(fw['start_input'].value, '%H:%M')
            finish_dt = datetime.strptime(fw['finish_input'].value, '%H:%M')
            if finish_dt < start_dt: finish_dt += timedelta(days=1)
            total_elapsed = (finish_dt - start_dt).total_seconds() / 60
            total_break = float(fw['paid_break_input'].value) + float(fw['unpaid_break_input'].value) if fw['break_checkbox'].value else 0
            delays = float(fw['delays_input'].value) if fw['delays_checkbox'].value else 0
            actual_work = max(0, total_elapsed - total_break)
            effective_time = max(1, actual_work - delays)
            performance = (float(fw['target_input'].value) / effective_time) * 100
            record_data = {
                'task_name': fw['task_display'].text, 'target_time': float(fw['target_input'].value),
                'actual_time': actual_work, 'performance_percentage': performance, 'start_time': fw['start_input'].value, 
                'end_time': fw['finish_input'].value, 'break_time': total_break, 'has_break': fw['break_checkbox'].value,
                'delays_time': delays, 'has_delays': fw['delays_checkbox'].value, 'delay_notes': fw['delays_notes_input'].value,
                'skill': "Picker", 'paid_break_time': float(fw['paid_break_input'].value), 'unpaid_break_time': float(fw['unpaid_break_input'].value)
            }
            self.db.save_record(record_data, self.editing_record_id)
            await self.main_window.info_dialog("Success", f"Record {'updated' if self.editing_record_id else 'saved'}!")
            self.set_view('view_records')
        except Exception as e:
            logger.exception('Error saving record: %s', e)
            await self.main_window.error_dialog("Save Error", f"Could not save record: {e}")

    async def delete_record_async(self, record_id):
        """Delete a performance record asynchronously."""
        if await self.main_window.confirm_dialog("Delete Record?", "This cannot be undone."):
            self.db.delete_record(record_id)
            self.set_view('view_records')

    async def start_shift_async(self):
        """Start a new shift asynchronously."""
        try:
            start_time = self.form_widgets['shift_start_input'].value.strip()
            datetime.strptime(start_time, '%H:%M')
            self.db.start_shift(start_time, "Picker")
            await self.main_window.info_dialog("Shift Started", f"Your shift has officially started at {start_time}.")
            self.set_view("home")
        except Exception as e: await self.main_window.error_dialog("Error", f"Could not start shift: {e}")

    async def finish_shift_async(self):
        """Finish the current shift asynchronously."""
        try:
            finish_time = self.form_widgets['finish_time_input'].value.strip()
            datetime.strptime(finish_time, '%H:%M')
            if await self.main_window.confirm_dialog("Finish Shift?", "You cannot add more records today after finishing."):
                self.db.finish_shift(finish_time)
                await self.main_window.info_dialog("Shift Ended", "Your shift has been recorded. Great work!")
                self.set_view("home")
        except Exception as e: await self.main_window.error_dialog("Error", f"Could not finish shift: {e}")

    def show_error_dialog(self, title, message):
        """Show an error dialog."""
        self.main_window.error_dialog(title, message)

    def show_info_dialog(self, title, message):
        """Show an information dialog."""
        self.main_window.info_dialog(title, message)

def main():
    return PerformanceTrackerApp('Performance Tracker', 'com.example.performancetracker') 