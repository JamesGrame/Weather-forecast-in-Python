import tkinter as tk
from tkinter import messagebox
import requests


def get_weather():
    api_key = '312d4b7547fcb8b5caa08026163c01c1'
    city = city_entry.get()
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&units=imperial&APPID={api_key}"
    response = requests.get(url)
    data = response.json()

    if data.get('cod') == 200:
        weather = data['weather'][0]['main']
        temp_f = round(data['main']['temp'])
        # Store temperature in Fahrenheit for conversion
        convert_button.temp_f = temp_f
        result_label.config(text=f"The weather in {city} is: {weather}\nThe temperature is: {temp_f}ºF")
        update_background(temp_f)
        # Show convert button
        convert_button.pack(padx=10, pady=5, fill='x')
    else:
        messagebox.showerror("Error", "City not found")


def convert_to_celsius():
    temp_f = convert_button.temp_f
    temp_c = (temp_f - 32) * 5.0/9.0
    temp_c = round(temp_c, 2)
    conversion_result_label.config(text=f"Temperature in Celsius: {temp_c}ºC")


def update_background(temp):
    if temp <= 32:
        result_label.config(bg="#a3d0ff")
    elif temp <= 70:
        result_label.config(bg="#fff4c3")
    else:
        result_label.config(bg="#ff9c8a")


def create_gradient(event):
    canvas.delete("gradient")
    width = event.width
    height = event.height
    (r1, g1, b1) = canvas.winfo_rgb(bg_color_start)  # Starting color
    (r2, g2, b2) = canvas.winfo_rgb(bg_color_end)  # Ending color
    for i in range(256):
        nr = int(r1 + (r2 - r1) * i / 255)
        ng = int(g1 + (g2 - g1) * i / 255)
        nb = int(b1 + (b2 - b1) * i / 255)
        color = "#%4.4x%4.4x%4.4x" % (nr, ng, nb)
        canvas.create_line(0, i*height/255, width, i*height/255, tags=("gradient",), fill=color)
    canvas.lower("gradient")


# Create main window
root = tk.Tk()
root.title("Weather Forecast")
root.geometry("450x350")

# Gradient colors
bg_color_start = '#a3d0ff'  # Lighter color at the top
bg_color_end = '#0056b3'    # Darker color at the bottom

# Gradient background
canvas = tk.Canvas(root)
canvas.pack(fill="both", expand=True)
canvas.bind("<Configure>", create_gradient)

frame = tk.Frame(root, bg="white", bd=2, relief=tk.GROOVE)
frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER, relwidth=0.9, relheight=0.9)

city_label = tk.Label(frame, text="Enter city:", bg="white", fg="black", font=('Helvetica', 14))
city_label.pack(padx=10, pady=5, anchor='nw')

city_entry = tk.Entry(frame, font=('Helvetica', 14), fg="black", bd=0, highlightthickness=2, highlightcolor="#0056b3")
city_entry.pack(padx=10, fill='x', expand=True)
city_entry.focus()

search_button = tk.Button(frame, text="Search", command=get_weather, bg="#0084ff", fg="white",
                          activebackground="#0056b3", activeforeground="white", bd=0, highlightthickness=0,
                          font=('Helvetica', 12))
search_button.pack(padx=10, pady=10, fill='x')

result_label = tk.Label(frame, text="", bg="white", fg="black", font=('Helvetica', 12), justify="left", bd=2,
                        relief=tk.GROOVE)
result_label.pack(padx=10, pady=5, fill='x', expand=True)

convert_button = tk.Button(frame, text="Convert to Celsius", command=convert_to_celsius, bg="#20bebe", fg="white",
                           activebackground="#5adad1", activeforeground="white", bd=0, highlightthickness=0,
                           font=('Helvetica', 12))
# Initially hidden, will be shown after fetching weather
convert_button.pack_forget()

conversion_result_label = tk.Label(frame, text="", bg="white", fg="black", font=('Helvetica', 12), justify="left")
conversion_result_label.pack(padx=10, pady=5, fill='x', expand=True)

root.mainloop()
