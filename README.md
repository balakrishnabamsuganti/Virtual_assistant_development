🧠 Virtual Assistant (with GUI, Reminders, and Weather)
A simple Python-based virtual assistant with a graphical user interface (GUI) using Tkinter. It can:

✅ Answer simple questions

✅ Set and notify reminders at scheduled times

✅ Fetch real-time weather updates

✅ Log actions and store data using SQLite

📦 Features
✅ Core Functions
Reminders
Set reminders with specific time (e.g., "set reminder Call mom at 2025-05-17 18:30"), and get popup notifications when the time arrives.

Weather Info
Get weather updates for any city using the OpenWeatherMap API.
Example: weather London

Simple Q&A
Responds to questions like:

"What's your name?"

"What's the time?"

GUI Interface
Interact via a user-friendly window with buttons and a command box.

🖼️ Screenshot
![Assistant Screenshot]("C:\Users\balak\OneDrive\Pictures\Screenshots\Screenshot 2025-05-17 125031.png")
💻 Technologies Used
Python 3.x

Tkinter – GUI framework

SQLite – For persistent reminder storage

threading – For background reminder checking

OpenWeatherMap API – For live weather data

Logging – For tracking assistant actions

🧪 How to Use
1. 🔧 Prerequisites
Python 3.7 or later installed

Install required packages:

bash
Copy
Edit
pip install requests
2. 🔑 Get Weather API Key
Go to OpenWeatherMap

Sign up and generate a free API key


python
Copy
Edit
WEATHER_API_KEY = 'your_openweathermap_api_key_here'
3. 🚀 Run the Application
Navigate to the folder and run:

bash
Copy
Edit
python virtual_assistant.py
✍️ Commands You Can Use
Command Type	Example	Description
Set Reminder	set reminder Pay bills at 2025-05-17 20:00	Sets a popup reminder at the given time
View Reminders	view reminders	Lists all saved reminders
Weather	weather New York	Shows weather info for a city
Ask Time	What's the time?	Tells the current time
Ask Name	What's your name?	Responds with assistant's name

📁 Project Structure
bash
Copy
Edit
virtual_assistant/
├── virtual_assistant.py       # Main script
├── assistant_data.db          # SQLite database (created at runtime)
├── assistant.log              # Logs for actions and errors
└── README.md                  # Documentation
🔔 Reminder Notifications
Every minute, the app checks for due reminders.

If a reminder is due, a popup alert is shown, and the reminder is removed from the database.



🧑‍💻 Author
Balakrishna Bamsuganti
Developed as part of a learning project to build practical Python skills.

