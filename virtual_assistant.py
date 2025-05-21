import tkinter as tk
from tkinter import messagebox
import sqlite3
import requests
import datetime
import logging
import threading
import time

# ----------- Logging Setup ----------- #
logging.basicConfig(filename='assistant.log', level=logging.INFO,
                    format='%(asctime)s:%(levelname)s:%(message)s')

# ----------- Database Setup ----------- #
conn = sqlite3.connect('assistant_data.db', check_same_thread=False)
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS reminders (
                    id INTEGER PRIMARY KEY,
                    content TEXT NOT NULL,
                    remind_at DATETIME,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                 )''')
conn.commit()

# ----------- Weather API Setup ----------- #
WEATHER_API_KEY = 'e2bfa8d1ec60bc2501cd3d8e3cc7f4ba'
WEATHER_URL = 'http://api.openweathermap.org/data/2.5/weather'

# ----------- Virtual Assistant Functions ----------- #
def add_reminder(content, remind_at=None):
    if content.strip():
        cursor.execute("INSERT INTO reminders (content, remind_at) VALUES (?, ?)", (content, remind_at))
        conn.commit()
        logging.info(f"Reminder added: {content} at {remind_at}")
        return "Reminder added successfully."
    return "Reminder cannot be empty."

def get_reminders():
    cursor.execute("SELECT id, content, remind_at, timestamp FROM reminders ORDER BY timestamp DESC")
    rows = cursor.fetchall()
    if not rows:
        return "No reminders found."
    return "\n".join([f"{row[0]}. {row[1]} (Due: {row[2]})" for row in rows])

def get_weather(city):
    try:
        params = {'q': city, 'appid': WEATHER_API_KEY, 'units': 'metric'}
        response = requests.get(WEATHER_URL, params=params)
        data = response.json()
        if response.status_code == 200:
            temp = data['main']['temp']
            desc = data['weather'][0]['description']
            result = f"Weather in {city}: {temp}°C, {desc}"
            logging.info(f"Weather fetched for {city}")
            return result
        return f"Error: {data.get('message', 'Unable to fetch weather')}"
    except Exception as e:
        logging.error(f"Weather fetch error: {e}")
        return "Error fetching weather data."

def simple_qna(question):
    question = question.lower().strip()
    if 'your name' in question:
        return "I am your virtual assistant."
    elif 'time' in question:
        return f"Current time is: {datetime.datetime.now().strftime('%H:%M:%S')}"
    return "Sorry, I don't understand that question."

# ----------- Notification Checker ----------- #
def check_reminders(app):
    while True:
        now = datetime.datetime.now()
        cursor.execute("SELECT id, content FROM reminders WHERE remind_at IS NOT NULL AND remind_at <= ?", (now,))
        due_reminders = cursor.fetchall()
        for reminder in due_reminders:
            messagebox.showinfo("Reminder", reminder[1])
            cursor.execute("DELETE FROM reminders WHERE id = ?", (reminder[0],))
            conn.commit()
        time.sleep(60)  # Check every 60 seconds

# ----------- GUI Setup ----------- #
class AssistantApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Virtual Assistant")

        self.label = tk.Label(root, text="Enter command:")
        self.label.pack(pady=5)

        self.entry = tk.Entry(root, width=50)
        self.entry.pack(pady=5)

        self.submit_btn = tk.Button(root, text="Submit", command=self.handle_command)
        self.submit_btn.pack(pady=5)

        self.view_btn = tk.Button(root, text="View Reminders", command=self.show_reminders)
        self.view_btn.pack(pady=5)

        self.output = tk.Text(root, height=15, width=60)
        self.output.pack(pady=10)

        # Start reminder checker thread
        threading.Thread(target=check_reminders, args=(self,), daemon=True).start()

    def handle_command(self):
        user_input = self.entry.get()
        response = self.process_input(user_input)
        self.output.insert(tk.END, f"> {user_input}\n{response}\n\n")
        self.entry.delete(0, tk.END)

    def process_input(self, input_text):
        if input_text.startswith("set reminder"):
            try:
                parts = input_text.replace("set reminder", "", 1).strip().rsplit(" at ", 1)
                content = parts[0].strip()
                remind_at = datetime.datetime.strptime(parts[1], "%Y-%m-%d %H:%M") if len(parts) > 1 else None
                return add_reminder(content, remind_at)
            except Exception as e:
                return f"Invalid format. Use: set reminder <message> at YYYY-MM-DD HH:MM"
        elif input_text.startswith("weather"):
            city = input_text.replace("weather", "", 1).strip()
            return get_weather(city)
        elif input_text == "view reminders":
            return get_reminders()
        else:
            return simple_qna(input_text)

    def show_reminders(self):
        reminders = get_reminders()
        self.output.insert(tk.END, f"\n-- Reminders --\n{reminders}\n\n")

# ----------- Run Application ----------- #
if __name__ == '__main__':
    root = tk.Tk()
    app = AssistantApp(root)
    root.mainloop()
    conn.close()
