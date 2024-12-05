import tkinter as tk
from tkinter import ttk
from tkinter import *
from bs4 import BeautifulSoup
import requests

# Function to extract Product Title and Price for Amazon
def get_title_amazon(soup):
    try:
        title = soup.find("span", attrs={"id": 'productTitle'})
        title_value = title.text
        title_string = title_value.strip()
    except AttributeError:
        title_string = ""
    return title_string

def get_price_amazon(soup):
    try:
        title = soup.find("span", attrs={"class": 'a-offscreen'})
        title_value = title.text
        title_string = title_value.strip()
    except AttributeError:
        title_string = ""
    return title_string

# Function to extract Product Title and Price for Flipkart
def get_title_flipkart(soup):
    try:
        title = soup.find("span", attrs={"class": 'B_NuCI'})
        title_value = title.text
        title_string = title_value.strip()
    except AttributeError:
        title_string = ""
    return title_string

def get_price_flipkart(soup):
    try:
        title = soup.find("div", attrs={"class": '_30jeq3 _16Jk6d'})
        title_value = title.text
        title_string = title_value.strip()
    except AttributeError:
        title_string = ""
    return title_string

# Function to search for products on both Amazon and Flipkart
def search_product():
    product_name = entry.get()
    if product_name:
        amazon_url = f"https://www.amazon.in/s?k={product_name.replace(' ', '+')}&ref=nb_sb_noss_1"
        flipkart_url = f"https://www.flipkart.com/search?q={product_name.replace(' ', '+')}"
        HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    }
        
        amazon_webpage = requests.get(amazon_url, headers=HEADERS)
        print(amazon_webpage)
        amazon_soup = BeautifulSoup(amazon_webpage.content, "html.parser")
        
        flipkart_webpage = requests.get(flipkart_url, headers=HEADERS)
        print(flipkart_webpage)
        flipkart_soup = BeautifulSoup(flipkart_webpage.content, "html.parser")

        # Fetch links as List of Tag Objects for Amazon
        amazon_links = amazon_soup.find_all("a", attrs={'class': 'a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal'})
        # Fetch links as List of Tag Objects for Flipkart
        flipkart_links = flipkart_soup.find_all('a', class_='_1fQZEK')
        
        # Store the first 10 links for Amazon
        amazon_links_list = [link.get('href') for link in amazon_links[:10]]
        # Store the first 10 links for Flipkart
        flipkart_links_list = [link.get('href') for link in flipkart_links[:10]]

        amazon_data = []
        flipkart_data = []

        # Loop for extracting product details from each link on Amazon
        for link in amazon_links_list:
            new_webpage = requests.get("https://www.amazon.in" + link, headers=HEADERS)
            print(new_webpage)
            new_soup = BeautifulSoup(new_webpage.content, "html.parser")

            # Function calls to display all necessary product information
            title = get_title_amazon(new_soup)
            price = get_price_amazon(new_soup)
            amazon_data.append((title, price))

        # Loop for extracting product details from each link on Flipkart
        for link in flipkart_links_list:
            new_webpage = requests.get("https://www.flipkart.com" + link, headers=HEADERS)
            print(new_webpage)
            new_soup = BeautifulSoup(new_webpage.content, "html.parser")

            # Function calls to display all necessary product information
            title = get_title_flipkart(new_soup)
            price = get_price_flipkart(new_soup)
            flipkart_data.append((title, price))

        # Display the result in the Amazon Treeview
        amazon_tree.delete(*amazon_tree.get_children())  # Clear existing rows
        for row in amazon_data:
            amazon_tree.insert("", tk.END, values=row)

        # Display the result in the Flipkart Treeview
        flipkart_tree.delete(*flipkart_tree.get_children())  # Clear existing rows
        for row in flipkart_data:
            flipkart_tree.insert("", tk.END, values=row)
    else:
        amazon_tree.delete(*amazon_tree.get_children())  # Clear existing rows
        flipkart_tree.delete(*flipkart_tree.get_children())  # Clear existing rows

# Function to clear the input field and output tables
def clear_all():
    entry.delete(0, tk.END)
    amazon_tree.delete(*amazon_tree.get_children())  # Clear Amazon table
    flipkart_tree.delete(*flipkart_tree.get_children())  # Clear Flipkart table

# GUI Setup
root = tk.Tk()
root.title("Amazon and Flipkart Price Checker")

# Entry
entry_label = ttk.Label(root, text="Enter Product Name:")

entry = ttk.Entry(root, width=30)


# Defining Frame
frame1 = ttk.Frame(root)
frame2 = ttk.Frame(root, padding=10)
frame3 = ttk.Frame(root, padding=10)

amazon_label = ttk.Label(frame2, text="Amazon", font=24)

flipkart_label = ttk.Label(frame3, text="Flipkart", font=24)

# Search Button
search_button = ttk.Button(frame1, text="Search", command=search_product)
search_button.grid(row=3, column=0, padx=5)

# Clear Button
clear_button = ttk.Button(frame1, text="Clear All", command=clear_all)
clear_button.grid(row=3, column=1, padx=5)

# Treeview for Amazon (Table)
columns_amazon = ("Title", "Price")
amazon_tree = ttk.Treeview(frame2, columns=columns_amazon, show="headings")

# Set the column widths
amazon_tree.column("Title", width=300)  # Larger width for the "Title" column
amazon_tree.column("Price", width=100)  # Smaller width for the "Price" column

for col in columns_amazon:
    amazon_tree.heading(col, text=col)


# Treeview for Flipkart (Table)
columns_flipkart = ("Title", "Price")
flipkart_tree = ttk.Treeview(frame3, columns=columns_flipkart, show="headings")

# Set the column widths
flipkart_tree.column("Title", width=300)  # Larger width for the "Title" column
flipkart_tree.column("Price", width=100)  # Smaller width for the "Price" column

for col in columns_flipkart:
    flipkart_tree.heading(col, text=col)



entry_label.pack()
entry.pack()
frame1.pack(pady=10)
amazon_label.grid(row=0, column=0, columnspan=2, pady=10)
amazon_tree.grid(row=2, column=0, columnspan=2, pady=10)
#amazon_tree.pack()
frame2.pack()
flipkart_label.grid(row=0,column=0, columnspan=2,pady=10)
flipkart_tree.grid(row=2, column=0, columnspan=2, pady=10)
frame3.pack(pady=10)
#flipkart_tree.pack()

root.mainloop()