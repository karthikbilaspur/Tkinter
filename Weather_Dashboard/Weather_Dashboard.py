import tkinter as tk
from tkinter import messagebox
import requests

def get_weather():
    city = city_entry.get()
    api_key = "YOUR_API_KEY_HERE"  # Replace with your actual API key
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    
    try:
        response = requests.get(url)
        data = response.json()
        
        if data["cod"] != "404":
            # Update Large Display
            temp_val.config(text=f"{round(data['main']['temp'])}°")
            city_display.config(text=f"{data['name']}, {data['sys']['country']}")
            condition_val.config(text=data['weather'][0]['description'].upper())
            
            # Update Stats Grid
            hum_val.config(text=f"{data['main']['humidity']}%")
            wind_val.config(text=f"{data['wind']['speed']} m/s")
            press_val.config(text=f"{data['main']['pressure']} hPa")
            feels_val.config(text=f"{data['main']['feels_like']}°C")
        else:
            messagebox.showerror("Error", "City not found!")
    except:
        messagebox.showerror("Error", "Connection Issue")

# --- UI Setup ---
root = tk.Tk()
root.title("Advanced Weather Dashboard")
root.geometry("600x500")
root.configure(bg="#1e2124")

# Styling Variables
font_large = ("Segoe UI", 48, "bold")
font_medium = ("Segoe UI", 14)
font_small = ("Segoe UI", 10)
bg_color = "#1e2124"
accent_color = "#7289da"
text_color = "white"

# --- Top Search Bar ---
header_frame = tk.Frame(root, bg=bg_color, pady=20)
header_frame.pack(fill="x")

city_entry = tk.Entry(header_frame, font=font_medium, width=30, bg="#2f3136", fg="white", borderwidth=0)
city_entry.pack(side="left", padx=(50, 10), ipady=5)
city_entry.insert(0, "New York")

search_btn = tk.Button(header_frame, text="Update", command=get_weather, bg=accent_color, fg="white", font=font_small, relief="flat", padx=20)
search_btn.pack(side="left", ipady=4)

# --- Main Display Section ---
main_frame = tk.Frame(root, bg=bg_color)
main_frame.pack(pady=10)

temp_val = tk.Label(main_frame, text="--°", font=font_large, fg=text_color, bg=bg_color)
temp_val.pack()

city_display = tk.Label(main_frame, text="Search for a city", font=font_medium, fg=accent_color, bg=bg_color)
city_display.pack()

condition_val = tk.Label(main_frame, text="CONDITION", font=font_small, fg="#99aab5", bg=bg_color)
condition_val.pack(pady=(0, 20))

# --- Bottom Stats Grid ---
stats_frame = tk.Frame(root, bg="#2f3136", padx=20, pady=20)
stats_frame.pack(fill="x", padx=50)

# Grid Layout for details
labels = ["Humidity", "Wind Speed", "Pressure", "Feels Like"]
for i, label_text in enumerate(labels):
    tk.Label(stats_frame, text=label_text, font=font_small, fg="#99aab5", bg="#2f3136").grid(row=0, column=i, padx=15, pady=5)

hum_val = tk.Label(stats_frame, text="--", font=font_medium, fg=text_color, bg="#2f3136")
hum_val.grid(row=1, column=0)

wind_val = tk.Label(stats_frame, text="--", font=font_medium, fg=text_color, bg="#2f3136")
wind_val.grid(row=1, column=1)

press_val = tk.Label(stats_frame, text="--", font=font_medium, fg=text_color, bg="#2f3136")
press_val.grid(row=1, column=2)

feels_val = tk.Label(stats_frame, text="--", font=font_medium, fg=text_color, bg="#2f3136")
feels_val.grid(row=1, column=3)

root.mainloop()