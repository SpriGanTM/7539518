import tkinter as tk
from tkinter import messagebox
import json
import os
from datetime import datetime

FILE = "weather.json"

def load_data():
    if os.path.exists(FILE):
        with open(FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_data():
    with open(FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def update_list(items=None):
    listbox.delete(0, tk.END)
    arr = items if items else data
    for i in arr:
        line = f"{i['date']} | {i['temp']}°C | {i['desc']} | Осадки: {i['rain']}"
        listbox.insert(tk.END, line)

def add_entry():
    date = entry_date.get()
    temp = entry_temp.get()
    desc = entry_desc.get()
    rain = rain_var.get()

    if date == "" or temp == "" or desc == "":
        messagebox.showerror("Ошибка", "Заполните все поля")
        return

    try:
        datetime.strptime(date, "%d.%m.%Y")
    except:
        messagebox.showerror("Ошибка", "Дата должна быть в формате ДД.ММ.ГГГГ")
        return

    try:
        temp = float(temp)
    except:
        messagebox.showerror("Ошибка", "Температура должна быть числом")
        return

    item = {
        "date": date,
        "temp": temp,
        "desc": desc,
        "rain": rain
    }

    data.append(item)
    save_data()
    update_list()

    entry_date.delete(0, tk.END)
    entry_temp.delete(0, tk.END)
    entry_desc.delete(0, tk.END)

def filter_date():
    d = filter_date_entry.get()
    res = [i for i in data if i["date"] == d]
    update_list(res)

def filter_temp():
    t = filter_temp_entry.get()
    try:
        t = float(t)
    except:
        messagebox.showerror("Ошибка", "Введите число")
        return

    res = [i for i in data if i["temp"] > t]
    update_list(res)

def reset_filter():
    update_list()

root = tk.Tk()
root.title("Weather Diary")

data = load_data()

entry_date = tk.Entry(root)
entry_date.pack()

entry_temp = tk.Entry(root)
entry_temp.pack()

entry_desc = tk.Entry(root)
entry_desc.pack()

rain_var = tk.StringVar(value="нет")
tk.OptionMenu(root, rain_var, "да", "нет").pack()

tk.Button(root, text="Добавить запись", command=add_entry).pack()

filter_date_entry = tk.Entry(root)
filter_date_entry.pack()

tk.Button(root, text="Фильтр по дате", command=filter_date).pack()

filter_temp_entry = tk.Entry(root)
filter_temp_entry.pack()

tk.Button(root, text="Температура >", command=filter_temp).pack()

tk.Button(root, text="Сбросить фильтр", command=reset_filter).pack()

listbox = tk.Listbox(root, width=70)
listbox.pack()

update_list()

root.mainloop()
