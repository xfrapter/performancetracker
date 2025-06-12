import sqlite3
import os
from datetime import datetime, timedelta
from contextlib import contextmanager
from .debug import logger

class Database:
    """Handles all SQLite database operations for Performance Tracker."""
    def __init__(self, paths):
        self.db_path = os.path.join(paths.data, 'performance.db')
        self._ensure_db_exists()
        logger.info('Database initialized')

    @contextmanager
    def _get_connection(self):
        """Get a database connection using a context manager."""
        conn = sqlite3.connect(self.db_path)
        try:
            yield conn
        finally:
            conn.close()

    def _ensure_db_exists(self):
        """Ensure the database and its tables exist."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS performance_records (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    task_name TEXT NOT NULL,
                    target_time REAL NOT NULL,
                    actual_time REAL NOT NULL,
                    performance_percentage REAL NOT NULL,
                    start_time TEXT NOT NULL,
                    end_time TEXT NOT NULL,
                    break_time REAL DEFAULT 0,
                    has_break BOOLEAN DEFAULT 0,
                    delays_time REAL DEFAULT 0,
                    has_delays BOOLEAN DEFAULT 0,
                    delay_notes TEXT,
                    skill TEXT,
                    paid_break_time REAL DEFAULT 0,
                    unpaid_break_time REAL DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS shifts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    start_time TEXT NOT NULL,
                    end_time TEXT,
                    skill TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            conn.commit()

    def save_record(self, record_data, record_id=None):
        """Save a performance record."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            if record_id:
                cursor.execute('''
                    UPDATE performance_records
                    SET task_name=?, target_time=?, actual_time=?, performance_percentage=?,
                        start_time=?, end_time=?, break_time=?, has_break=?,
                        delays_time=?, has_delays=?, delay_notes=?, skill=?,
                        paid_break_time=?, unpaid_break_time=?
                    WHERE id=?
                ''', (
                    record_data['task_name'], record_data['target_time'],
                    record_data['actual_time'], record_data['performance_percentage'],
                    record_data['start_time'], record_data['end_time'],
                    record_data['break_time'], record_data['has_break'],
                    record_data['delays_time'], record_data['has_delays'],
                    record_data['delay_notes'], record_data['skill'],
                    record_data['paid_break_time'], record_data['unpaid_break_time'],
                    record_id
                ))
            else:
                cursor.execute('''
                    INSERT INTO performance_records (
                        task_name, target_time, actual_time, performance_percentage,
                        start_time, end_time, break_time, has_break,
                        delays_time, has_delays, delay_notes, skill,
                        paid_break_time, unpaid_break_time
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    record_data['task_name'], record_data['target_time'],
                    record_data['actual_time'], record_data['performance_percentage'],
                    record_data['start_time'], record_data['end_time'],
                    record_data['break_time'], record_data['has_break'],
                    record_data['delays_time'], record_data['has_delays'],
                    record_data['delay_notes'], record_data['skill'],
                    record_data['paid_break_time'], record_data['unpaid_break_time']
                ))
            conn.commit()
            logger.info(f"Record {'updated' if record_id else 'saved'} successfully")

    def get_record_by_id(self, record_id):
        """Get a performance record by ID."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM performance_records WHERE id = ?', (record_id,))
            return cursor.fetchone()

    def delete_record(self, record_id):
        """Delete a performance record."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM performance_records WHERE id = ?', (record_id,))
            conn.commit()
            logger.info(f"Record {record_id} deleted successfully")

    def get_all_records(self):
        """Get all performance records."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM performance_records ORDER BY created_at DESC')
            return cursor.fetchall()

    def start_shift(self, start_time, skill):
        """Start a new shift."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO shifts (start_time, skill) VALUES (?, ?)', (start_time, skill))
            conn.commit()
            logger.info(f"Shift started at {start_time} for {skill}")

    def finish_shift(self, end_time):
        """Finish the current shift."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE shifts 
                SET end_time = ? 
                WHERE id = (SELECT id FROM shifts WHERE end_time IS NULL ORDER BY created_at DESC LIMIT 1)
            ''', (end_time,))
            conn.commit()
            logger.info(f"Shift finished at {end_time}")

    def get_current_shift(self):
        """Get the current shift if any."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM shifts WHERE end_time IS NULL ORDER BY created_at DESC LIMIT 1')
            return cursor.fetchone()

    def get_shift_history(self):
        """Get all completed shifts."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM shifts WHERE end_time IS NOT NULL ORDER BY created_at DESC')
            return cursor.fetchall()

    def _execute(self, query, params=(), fetch=None):
        """Execute a database query and return results."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                cursor.execute(query, params)
                if fetch == 'one':
                    result = cursor.fetchone()
                    return dict(result) if result else None
                if fetch == 'all':
                    return [dict(row) for row in cursor.fetchall()]
                conn.commit()
                return cursor.lastrowid
        except Exception as e:
            print(f"DB Error: {e} on query: {query}")
            return None if fetch else 0

    # --- Task Management ---

    def get_task_by_name(self, name, target_time):
        """Get a task by name and target time."""
        return self._execute(
            "SELECT id FROM tasks WHERE name = ? AND target_time = ?",
            (name, target_time),
            fetch='one'
        )

    def create_task(self, name, target_time):
        """Create a new task."""
        self._execute(
            "INSERT INTO tasks (name, target_time) VALUES (?, ?)",
            (name, target_time)
        )
        return self._execute("SELECT last_insert_rowid() as id", fetch='one')['id']

    def get_or_create_task(self, name, target_time):
        """Get an existing task or create a new one."""
        task = self.get_task_by_name(name, target_time)
        if task:
            return task['id']
        return self.create_task(name, target_time)

    # --- Performance Records ---

    def insert_record(self, data, metrics):
        """Insert a new performance record."""
        task_id = self.get_or_create_task(data['task_name'], data['target_time'])
        
        # Calculate break time based on break type
        break_time = 15 if data.get('break_type') == 'break' else 30 if data.get('break_type') == 'lunch' else 0
        
        self._execute('''
            INSERT INTO performance_records 
            (task_id, actual_time, performance_percentage, start_time, end_time, 
             break_type, break_time, delays_time, has_delays, delay_notes, 
             battery_changes_count, battery_changes_time, paid_break_time, unpaid_break_time)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            task_id, metrics['actual_work_time'], metrics['performance'],
            data['start_time'], data['finish_time'], data.get('break_type'),
            break_time, data['delays_time'], data['has_delays'],
            data['delay_notes'], data['battery_count'], data['battery_count'] * 9,
            data['paid_break_time'], data['unpaid_break_time']
        ))

    def update_record(self, record_id, data, metrics):
        """Update an existing performance record."""
        # Calculate break time based on break type
        break_time = 15 if data.get('break_type') == 'break' else 30 if data.get('break_type') == 'lunch' else 0
        
        self._execute('''
            UPDATE performance_records 
            SET actual_time = ?, performance_percentage = ?, start_time = ?, end_time = ?, 
                break_type = ?, break_time = ?, delays_time = ?, has_delays = ?, 
                delay_notes = ?, battery_changes_count = ?, battery_changes_time = ?,
                paid_break_time = ?, unpaid_break_time = ?
            WHERE id = ?
        ''', (
            metrics['actual_work_time'], metrics['performance'],
            data['start_time'], data['finish_time'], data.get('break_type'),
            break_time, data['delays_time'], data['has_delays'],
            data['delay_notes'], data['battery_count'], data['battery_count'] * 9,
            data['paid_break_time'], data['unpaid_break_time'], record_id
        ))

    def get_recent_records(self, limit=20):
        """Get recent performance records."""
        return self._execute('''
            SELECT pr.*, t.name as task_name, t.target_time
            FROM performance_records pr
            JOIN tasks t ON pr.task_id = t.id
            ORDER BY pr.created_at DESC
            LIMIT ?
        ''', (limit,), fetch='all')

    # --- Shift Management ---

    def get_today_shift_info(self):
        """Get information about today's shift."""
        today = datetime.now().strftime('%Y-%m-%d')
        return self._execute('''
            SELECT *
            FROM shift_records
            WHERE date = ?
        ''', (today,), fetch='one') or {
            "date": today,
            "shift_start_time": None,
            "shift_end_time": None,
            "is_finished": False,
            "total_break_time": 0,
            "paid_break_time": 0,
            "unpaid_break_time": 0
        }

    # --- Statistics ---

    def get_daily_stats(self, date=None):
        """Get statistics for a specific date."""
        if date is None:
            date = datetime.now().strftime('%Y-%m-%d')
        
        query = '''
            SELECT 
                AVG(performance_percentage) as avg_performance,
                COUNT(*) as total_records,
                SUM(actual_time) as total_time,
                SUM(break_time) as total_break_time,
                SUM(delays_time) as total_delay_time,
                MAX(performance_percentage) as best_performance,
                MIN(performance_percentage) as worst_performance
            FROM performance_records
            WHERE date(created_at) = ?
        '''
        result = self._execute(query, (date,), fetch='one')
        
        if not result:
            return {
                'avg_performance': 0,
                'total_records': 0,
                'total_time': 0,
                'total_break_time': 0,
                'total_delay_time': 0,
                'best_performance': 0,
                'worst_performance': 0
            }
        
        # Convert None values to 0
        for key in result:
            if result[key] is None:
                result[key] = 0
        
        return result

    def get_weekly_stats(self, week_start=None):
        """Get statistics for a specific week."""
        if week_start is None:
            week_start = datetime.now()
        
        week_end = week_start + timedelta(days=6)
        
        query = '''
            SELECT 
                AVG(performance_percentage) as avg_performance,
                COUNT(*) as total_records,
                SUM(actual_time) as total_time,
                SUM(break_time) as total_break_time,
                SUM(delays_time) as total_delay_time,
                COUNT(DISTINCT date(created_at)) as active_days,
                MAX(performance_percentage) as best_performance,
                MIN(performance_percentage) as worst_performance
            FROM performance_records
            WHERE date(created_at) BETWEEN ? AND ?
        '''
        result = self._execute(query, (week_start.strftime('%Y-%m-%d'), week_end.strftime('%Y-%m-%d')), fetch='one')
        
        if not result:
            return {
                'avg_performance': 0,
                'total_records': 0,
                'total_time': 0,
                'total_break_time': 0,
                'total_delay_time': 0,
                'active_days': 0,
                'best_performance': 0,
                'worst_performance': 0
            }
        
        # Convert None values to 0
        for key in result:
            if result[key] is None:
                result[key] = 0
        
        return result

    def get_stats_for_date_range(self, start_date, end_date):
        """Get statistics for a date range."""
        query = '''
            SELECT 
                AVG(performance_percentage) as avg_performance,
                COUNT(*) as total_records,
                SUM(actual_time) as total_time,
                SUM(break_time) as total_break_time,
                SUM(delays_time) as total_delay_time,
                COUNT(DISTINCT date(created_at)) as active_days,
                MAX(performance_percentage) as best_performance,
                MIN(performance_percentage) as worst_performance
            FROM performance_records
            WHERE date(created_at) BETWEEN ? AND ?
        '''
        result = self._execute(query, (start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d')), fetch='one')
        
        if not result:
            return {
                'avg_performance': 0,
                'total_records': 0,
                'total_time': 0,
                'total_break_time': 0,
                'total_delay_time': 0,
                'active_days': 0,
                'best_performance': 0,
                'worst_performance': 0
            }
        
        # Convert None values to 0
        for key in result:
            if result[key] is None:
                result[key] = 0
        
        return result

    def get_records_for_date(self, date):
        """Get all records for a specific date."""
        query = '''
            SELECT pr.*, t.name as task_name, t.target_time
            FROM performance_records pr
            JOIN tasks t ON pr.task_id = t.id
            WHERE date(pr.created_at) = ?
            ORDER BY pr.created_at DESC
        '''
        return self._execute(query, (date.strftime('%Y-%m-%d'),), fetch='all') or []

    def calculate_shift_duration(self, shift_info):
        """Calculate the duration of a shift in minutes."""
        if not shift_info or not shift_info.get('shift_start_time') or not shift_info.get('shift_end_time'):
            return 0
        
        try:
            start = datetime.strptime(shift_info['shift_start_time'], '%H:%M')
            end = datetime.strptime(shift_info['shift_end_time'], '%H:%M')
            duration = (end - start).total_seconds() / 60
            return max(0, duration)
        except (ValueError, TypeError):
            return 0

    def calculate_current_shift_duration(self, shift_info):
        """Calculate the duration of the current shift in minutes."""
        if not shift_info or not shift_info.get('shift_start_time'):
            return 0
        
        try:
            start = datetime.strptime(shift_info['shift_start_time'], '%H:%M')
            now = datetime.now()
            current = datetime.strptime(now.strftime('%H:%M'), '%H:%M')
            duration = (current - start).total_seconds() / 60
            return max(0, duration)
        except (ValueError, TypeError):
            return 0

    # Add all other methods as per the user's structure (get_shift_status_today, get_today_shift_info, start_shift, finish_shift, get_daily_stats, get_weekly_stats, get_record_by_id, get_recent_records, delete_record, save_record) 