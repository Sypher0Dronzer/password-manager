import json
from tkinter import *
from tkinter import messagebox
import random
import pyperclip


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']
    n_letter = random.randint(4, 8)
    n_numbers = random.randint(2, 4)
    n_symbols = random.randint(2, 4)
    gen_pass = []
    gen_pass = [random.choice(letters) for i in range(n_letter)]
    gen_pass.extend(random.choice(numbers) for i in range(n_numbers))
    gen_pass.extend(random.choice(symbols) for i in range(n_symbols))
    random.shuffle(gen_pass)
    p = "".join(gen_pass)
    # for i in gen_pass:
    #     p += i
    password_entry.insert(0, p)
    pyperclip.copy(p)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():
    website = website_entry.get()
    user_mail = user_entry.get()
    password = password_entry.get()
    new_data = {website: {
        "email": user_mail,
        "password": password
    }}
    if len(website) == 0 or len(password) == 0:
        messagebox.showinfo(title="Oops!", message="Please do not leave any fields empty!")
    else:
        is_ok = messagebox.askyesno(title=f"{website}",
                                    message=f"These are the details entered:\n Email: {user_mail}\n Password: {password}\n Is that okay?")
        if is_ok:
            # here data is stored in a text file but to improve the user experience we will be storing data in the json file
            # with open(file="data.txt", mode='a') as data:
            #     data.writelines(f"{website} | {user_mail} | {password}\n")

            try:  # if the json file is not present then it will give an error stating FileNotFound
                with open(file="data.json", mode="r") as data_file:
                    # reading the data from file
                    data = json.load(data_file)
            except FileNotFoundError:
                with open(file="data.json", mode="w") as data_file:
                    json.dump(new_data, data_file, indent=4)
            else:
                # updating the data
                data.update(new_data)
                with open(file="data.json", mode="w") as data_file:
                    # and finally writing the updated data into the file
                    json.dump(data, data_file, indent=4)
            finally:
                website_entry.delete(0, END)
                password_entry.delete(0, END)

# ---------------------------SEARCHING THE WEBSITE PASSWORD----------------------#
def find_password():
    website=website_entry.get()
    try:
        with open("data.json",'r') as data_file:
            data=json.load(data_file)
    except FileNotFoundError:
        messagebox.showinfo(title="Error", message="No data file found".title())
    else:
        # note if there is an issue that can be solved using if-else then do not use exception handling
        # good practice 😁
        if website in data:
            messagebox.showinfo(title=website, message=f"Email: {data[website]['email']}\nPassword: {data[website]['password']}")
        else:
            messagebox.showinfo(title="Site Not Found", message="No details of this website is found,")


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager")
window.config(padx=40, pady=40)

password_logo = PhotoImage(file="logo.png")
# specifying the dimension of the canvas is important
canvas = Canvas(height=200, width=200)
# the specifications are half of the canvas dimension so that we get the image at the very centre coordinates
canvas.create_image(100, 100, image=password_logo)
canvas.grid(row=0, column=1)

website = Label(text="Website: ")
website.grid(row=1, column=0)

user = Label(text="Email/Username: ")
user.grid(row=2, column=0)

password = Label(text="Password:")
password.grid(row=3, column=0)

# entry
website_entry = Entry(width=35)
# the cursor is already placed here so that you can immediately start typing
website_entry.focus()
website_entry.grid(row=1, column=1)

user_entry = Entry(width=54)
# in order to already have something written we use the insert(index,s) method
user_entry.insert(0, "sohamsaha321@gmail.com")
user_entry.grid(row=2, column=1, columnspan=2)

password_entry = Entry(width=35)
password_entry.grid(row=3, column=1)

# button
generate_pass = Button(text="Generate Password", command=generate_password)
generate_pass.grid(row=3, column=2)

add = Button(text="Add", width=46, command=save)
add.grid(row=4, column=1, columnspan=2)

search=Button(text="Search", width=15, command=find_password)
search.grid(row=1, column=2)

window.mainloop()
