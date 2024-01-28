from json import JSONDecodeError
from tkinter import *
from tkinter import messagebox
from random import choice, randint, shuffle
import pyperclip
import json

# ---------------------------- PASSWORD GENERATOR ------------------------------- #


def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    # nr_letters = int(input("How many letters would you like in your password?\n"))
    # nr_symbols = int(input(f"How many symbols would you like?\n"))
    # nr_numbers = int(input(f"How many numbers would you like?\n"))

    password_letters = [choice(letters) for _ in range(randint(8, 10))]
    password_symbols = [choice(symbols) for _ in range(randint(2, 4))]
    password_numbers = [choice(numbers) for _ in range(randint(2, 4))]

    password_list = password_letters + password_symbols + password_numbers
    shuffle(password_list)
    password = "".join(password_list)
    password_entry.insert(0, password)
    pyperclip.copy(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #


def save():
    website = website_entry.get()
    user = user_entry.get()
    password = password_entry.get()
    new_data = {
        website: {"user": user,
                  "password": password}
    }

    if len(website) == 0 or len(user) == 0 or len(password) == 0:
        messagebox.showinfo(title="Oops", message="Don't leave any spaces empty!")
    else:
        is_ok = messagebox.askokcancel(title=website, message=f"These are the details entered: "
                                                              f"\nEmail/Username: {user} "
                                                              f"\nPassword: {password} "
                                                              f"\nIs it ok to save?")
        if is_ok:
            try:
                with open("Password.json", mode="r") as file:
                    data = json.load(file)
            except FileNotFoundError:
                with open("Password.json", mode="w") as file:
                    json.dump(new_data, file, indent=4)
            except JSONDecodeError:
                with open("Password.json", mode="w") as file:
                    json.dump(new_data, file, indent=4)
            else:
                data.update(new_data)
                with open("Password.json", mode="w") as file:
                    json.dump(data, file, indent=4)
            finally:
                website_entry.delete(0, END)
                password_entry.delete(0, END)


# ---------------------------- SEARCH PASSWORD ------------------------------- #


def search_password():
    website = website_entry.get()
    try:
        with open("Password.json", mode="r") as file:
            data = json.load(file)
    except FileNotFoundError:
        messagebox.showinfo(title="Oops", message="No File Found")
    except JSONDecodeError:
        messagebox.showinfo(title="Oops", message="No data in File")
    else:
        if website in data:
            user = data[website]["user"]
            password = data[website]["password"]
            messagebox.showinfo(title=f"{website}", message=f"\nEmail/Username: {user}\nPassword: {password} ")
        else:
            messagebox.showinfo(title="Oops", message="No data for this website")

# ---------------------------- UI SETUP ------------------------------- #


window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

# Logo
canvas = Canvas(width=200, height=200)
lock_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=lock_img)
canvas.grid(column=1, row=0)

# Labels
website_label = Label(text="Website:")
website_label.grid(column=0, row=1)
user_label = Label(text="Email/Username:")
user_label.grid(column=0, row=2)
password_label = Label(text="Password:")
password_label.grid(column=0, row=3)

# Entries
website_entry = Entry(width=34)
website_entry.grid(column=1, row=1)
website_entry.focus()
user_entry = Entry(width=53)
user_entry.grid(column=1, columnspan=2, row=2)
user_entry.insert(0, "dummy@gmail.com")
password_entry = Entry(width=34)
password_entry.grid(column=1, row=3)

# Button
add_button = Button(width=45, text="Add", command=save)
add_button.grid(column=1, columnspan=2, row=4)
generate_password_button = Button(text="Generate Password", command=generate_password)
generate_password_button.grid(column=2, row=3)
search_button = Button(width=14, text="Search", command=search_password)
search_button.grid(column=2, row=1)

window.mainloop()
