import asyncio
import csv
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, ttk

import pandas as pd
from telethon import TelegramClient

# Replace with your own credentials
api_id = 'your-api-id'
api_hash = 'you-key'

client = TelegramClient('session_name', api_id, api_hash)

# Function to handle rate limiting dntch limited to 15/sec
async def rate_limited_get_entity(number):
    try:
        user = await client.get_entity(number)
        return user
    except Exception as e:
        return None

async def validate_numbers(numbers):
    valid_numbers = []
    invalid_numbers = []
    
    await client.start()
    
    for number in numbers:
        user = await rate_limited_get_entity(number)
        if user:
            valid_numbers.append((number, user.username if user.username else user.first_name))
        else:
            invalid_numbers.append((number, "Failed to get entity"))
        # Sleep to respect rate limits
        await asyncio.sleep(1 / 15)  # 15 req/sec

    await client.disconnect()
    return valid_numbers, invalid_numbers

def process_file():
    show_processing_animation()
    threading.Thread(target=process_file_in_background).start()

def process_file_in_background():
    file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if file_path:
        try:
            with open(file_path, mode='r', encoding='utf-8-sig') as file:
                reader = csv.reader(file)
                header = next(reader, None)  
                numbers = [row[0] for row in reader if row]  # Handle empty rows

            
            number_text_box.delete('1.0', tk.END)
            number_text_box.insert(tk.END, '\n'.join(numbers))

            # Validate numbers
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            valid_numbers, invalid_numbers = loop.run_until_complete(validate_numbers(numbers))

            
            if valid_numbers:
                valid_df = pd.DataFrame(valid_numbers, columns=["Phone Number", "Name"])
                valid_df.to_csv("valid_numbers.csv", index=False)
            
            
            valid_numbers_text_box.delete('1.0', tk.END)
            for number, name in valid_numbers:
                valid_numbers_text_box.insert(tk.END, f"{number} - {name}\n")

            if invalid_numbers:
                with open("invalid_numbers.txt", "w") as file:
                    for number, reason in invalid_numbers:
                        file.write(f"{number}: {reason}\n")

            messagebox.showinfo("Success", "Processing complete. Check valid_numbers.csv and invalid_numbers.txt.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
    
    hide_processing_animation()

def refresh_results():
    show_processing_animation()
    threading.Thread(target=refresh_results_in_background).start()

def refresh_results_in_background():
   
    number_text_box.delete('1.0', tk.END)
    valid_numbers_text_box.delete('1.0', tk.END)

    
    try:
        with open("last_uploaded_file.csv", mode='r', encoding='utf-8-sig') as file:
            reader = csv.reader(file)
            header = next(reader, None)  
            numbers = [row[0] for row in reader if row]  

        
        number_text_box.insert(tk.END, '\n'.join(numbers))

       
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        valid_numbers, invalid_numbers = loop.run_until_complete(validate_numbers(numbers))

      
        for number, name in valid_numbers:
            valid_numbers_text_box.insert(tk.END, f"{number} - {name}\n")

    except FileNotFoundError:
        messagebox.showwarning("No File", "No file found to refresh.")

    hide_processing_animation()

def show_processing_animation():
    global processing_animation
    processing_animation = True
    valid_numbers_text_box.config(state=tk.NORMAL)
    valid_numbers_text_box.delete('1.0', tk.END)
    valid_numbers_text_box.insert(tk.END, "Processing")
    animate_processing_text()

def animate_processing_text():
    if processing_animation:
        current_text = valid_numbers_text_box.get('1.0', tk.END)
        if "Processing" in current_text:
            valid_numbers_text_box.delete('1.0', tk.END)
            valid_numbers_text_box.insert(tk.END, "Processing" + "." * (len(current_text) % 4))
        valid_numbers_text_box.after(300, animate_processing_text)

def hide_processing_animation():
    global processing_animation
    processing_animation = False
    valid_numbers_text_box.config(state=tk.NORMAL)

def download_csv():
    try:
        with open("valid_numbers.csv", "r") as file:
            content = file.read()
        with filedialog.asksaveasfile(defaultextension=".csv", filetypes=[("CSV files", "*.csv")]) as file:
            if file:
                file.write(content)
        messagebox.showinfo("Success", "CSV file downloaded successfully.")
    except FileNotFoundError:
        messagebox.showwarning("File Not Found", "No valid_numbers.csv file found.")

def create_ui():
    global number_text_box, valid_numbers_text_box, processing_animation

    root = tk.Tk()
    root.title("Telegram Number Validator")
    root.geometry("1200x700") 
    root.configure(bg="#f0f0f0")


    title_label = tk.Label(root, text="Telegram Number Validator", font=("Helvetica", 20, "bold"), bg="#4a90e2", fg="white")
    title_label.pack(pady=20, fill=tk.X)

   
    main_frame = tk.Frame(root, bg="#ffffff", bd=2, relief=tk.RAISED)
    main_frame.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)

 
    tk.Button(main_frame, text="Upload CSV File", command=process_file, font=("Helvetica", 12), bg="#4a90e2", fg="white", relief=tk.RAISED).grid(row=0, column=0, padx=10, pady=10, sticky="w")

  
    tk.Button(main_frame, text="Refresh", command=refresh_results, font=("Helvetica", 12), bg="#4a90e2", fg="white", relief=tk.RAISED).grid(row=0, column=1, padx=10, pady=10, sticky="w")

    # Download CSV Button
    tk.Button(main_frame, text="Download CSV", command=download_csv, font=("Helvetica", 12), bg="#4a90e2", fg="white", relief=tk.RAISED).grid(row=3, column=1, padx=10, pady=10, sticky="e")

   
    tk.Label(main_frame, text="Numbers from CSV:", font=("Helvetica", 14, "bold"), bg="#ffffff").grid(row=1, column=0, pady=5, padx=10, sticky="w")
    tk.Label(main_frame, text="Valid Numbers:", font=("Helvetica", 14, "bold"), bg="#ffffff").grid(row=1, column=1, pady=5, padx=10, sticky="w")

    number_text_box = scrolledtext.ScrolledText(main_frame, width=40, height=20, wrap=tk.WORD, font=("Helvetica", 12))
    number_text_box.grid(row=2, column=0, pady=10, padx=10, sticky="nsew")

    valid_numbers_text_box = scrolledtext.ScrolledText(main_frame, width=40, height=20, wrap=tk.WORD, font=("Helvetica", 12))
    valid_numbers_text_box.grid(row=2, column=1, pady=10, padx=10, sticky="nsew")

    
    main_frame.grid_columnconfigure(0, weight=1)
    main_frame.grid_columnconfigure(1, weight=1)
    main_frame.grid_rowconfigure(2, weight=1)

    root.mainloop()

if __name__ == "__main__":
    create_ui()
