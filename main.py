import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

products = [
    {"name": "Magic Sword", "price": 100, "image": "images/produkt1.png", "description": "Potężny miecz zwiększający obrażenia o 20 punktów.", "stock": 5},
    {"name": "Healing Potion", "price": 50, "image": "images/produkt2.png", "description": "Przywraca 50 punktów zdrowia.", "stock": 10},
    {"name": "Shield of Valor", "price": 150, "image": "images/produkt3.png", "description": "Solidna tarcza zwiększająca obronę o 30 punktów.", "stock": 2},
    {"name": "Elixir of Speed", "price": 75, "image": "images/produkt4.png", "description": "Zwiększa prędkość ruchu o 20% przez 5 minut.", "stock": 8},
    {"name": "Fire Sword", "price": 200, "image": "images/produkt5.png", "description": "Miecz zadający dodatkowe obrażenia od ognia.", "stock": 3},
    {"name": "Crystal Shield", "price": 180, "image": "images/produkt6.png", "description": "Tarcza zwiększająca odporność na magię.", "stock": 4}
]

cart = []
history = []
inventory = []
player_balance = 500

def add_to_cart(product):
    if product['stock'] > 0:
        if player_balance >= product['price']:
            cart.append(product)
            product['stock'] -= 1
            update_ui()
            messagebox.showinfo("Koszyk", f"Dodano {product['name']} do koszyka!")
        else:
            messagebox.showwarning("Brak środków", "Nie masz wystarczającej ilości złotych monet!")
    else:
        messagebox.showwarning("Brak na stanie", f"Produkt {product['name']} jest wyprzedany!")

def remove_from_cart(item_index):
    product = cart.pop(item_index)
    product['stock'] += 1
    update_ui()
    messagebox.showinfo("Koszyk", f"Usunięto {product['name']} z koszyka!")

def show_cart():
    cart_window = tk.Toplevel(root)
    cart_window.title("Twój koszyk")

    total_price = 0

    for index, item in enumerate(cart):
        frame = tk.Frame(cart_window)
        frame.pack(pady=5)

        tk.Label(frame, text=f"{item['name']} - {item['price']} zł", font=("Verdana", 10, "bold")).pack(side="left")
        tk.Button(frame, text="Usuń", command=lambda idx=index: [remove_from_cart(idx), cart_window.destroy(), show_cart()], bg="red", fg="white", relief="flat", padx=5, pady=2).pack(side="right")

        total_price += item['price']

    tk.Label(cart_window, text=f"\nŁączna cena: {total_price} zł", font=("Verdana", 12, "bold")).pack()
    tk.Button(cart_window, text="Kup teraz", command=lambda: buy_items(cart_window), bg="green", fg="white", relief="flat", padx=5, pady=2).pack()

def buy_items(window):
    global player_balance
    total_price = sum(item['price'] for item in cart)

    if total_price > player_balance:
        messagebox.showwarning("Brak środków", "Nie masz wystarczających środków na zakup!")
    elif cart:
        player_balance -= total_price
        inventory.extend(cart.copy())
        history.extend(cart.copy())
        cart.clear()
        update_ui()
        window.destroy()
        messagebox.showinfo("Zakup", "Dziękujemy za zakupy! Przedmioty dodano do ekwipunku.")
    else:
        messagebox.showwarning("Zakup", "Twój koszyk jest pusty!")

def sell_item(item_index):
    global player_balance
    item = inventory.pop(item_index)
    player_balance += int(item['price'] * 0.5)  # Cena sprzedaży to 50% ceny zakupu
    update_ui()
    messagebox.showinfo("Sprzedaż", f"Sprzedano {item['name']} za {int(item['price'] * 0.5)} zł!")

def show_inventory():
    inventory_window = tk.Toplevel(root)
    inventory_window.title("Twój ekwipunek")

    if inventory:
        for index, item in enumerate(inventory):
            frame = tk.Frame(inventory_window)
            frame.pack(pady=5)

            tk.Label(frame, text=f"{item['name']} - {item['description']}", font=("Verdana", 10)).pack(side="left")
            tk.Button(frame, text="Sprzedaj", command=lambda idx=index: [sell_item(idx), inventory_window.destroy(), show_inventory()], bg="orange", fg="white", relief="flat", padx=5, pady=2).pack(side="right")
    else:
        tk.Label(inventory_window, text="Ekwipunek jest pusty.", font=("Verdana", 12)).pack()

def history_window():
    history_win = tk.Toplevel(root)
    history_win.title("Historia zakupów")

    if history:
        for item in history:
            tk.Label(history_win, text=f"{item['name']} - {item['price']} zł", font=("Verdana", 10)).pack()
    else:
        tk.Label(history_win, text="Historia jest pusta.", font=("Verdana", 12)).pack()

def filter_products(min_price=0, max_price=float('inf')):
    return [product for product in products if min_price <= product["price"] <= max_price]

def sort_products(by="price", reverse=False):
    return sorted(products, key=lambda x: x[by], reverse=reverse)


def display_products(filtered_products=None):
    for widget in product_frame.winfo_children():
        widget.destroy()

    to_display = filtered_products if filtered_products is not None else products

    if not to_display:
        tk.Label(product_frame, text="Brak produktów spełniających kryteria filtru.",
                 font=("Verdana", 12), bg="white", fg="red").pack(pady=10)
        return

    for product in to_display:
        frame = tk.Frame(product_frame, borderwidth=2, relief="flat", bg="white", padx=10, pady=10)
        frame.pack(side="left", padx=10, pady=10)
        img = Image.open(product["image"])
        img = img.resize((100, 100))
        photo = ImageTk.PhotoImage(img)
        img_label = tk.Label(frame, image=photo, bg="white")
        img_label.image = photo
        img_label.pack()
        tk.Label(frame, text=product["name"], font=("Verdana", 12, "bold"), bg="white").pack()
        tk.Label(frame, text=f"Cena: {product['price']} zł", font=("Verdana", 10), bg="white").pack()
        tk.Label(frame, text=f"Na stanie: {product['stock']}", font=("Verdana", 10), bg="white").pack()
        tk.Label(frame, text=product['description'], font=("Verdana", 8), wraplength=150, bg="white").pack()
        tk.Button(frame, text="Dodaj do koszyka", command=lambda p=product: add_to_cart(p), bg="blue", fg="white",
                  relief="flat", padx=5, pady=2).pack(pady=5)


def update_ui():
    balance_label.config(text=f"Twój balans: {player_balance} zł")
    display_products()

root = tk.Tk()
root.title("Sklep w grze")
root.geometry("1100x600")
root.iconbitmap("images/logo.ico")
root.resizable = False

background_image = Image.open("images/background.png")
background_image = background_image.resize((1100, 600))  # Dopasowanie tła do rozmiaru okna
background_photo = ImageTk.PhotoImage(background_image)

background_label = tk.Label(root, image=background_photo)
background_label.place(x=0, y=0, relwidth=1, relheight=1)


top_frame = tk.Frame(root, bg="gray")
top_frame.pack(side="top", fill="x")

balance_label = tk.Label(top_frame, text=f"Twój balans: {player_balance} zł", font=("Verdana", 12), bg="gray", fg="white")
balance_label.pack(side="left", padx=10)

tk.Button(top_frame, text="Koszyk", command=show_cart, bg="blue", fg="white", relief="flat", padx=5, pady=2).pack(side="right", padx=10)
tk.Button(top_frame, text="Ekwipunek", command=show_inventory, bg="orange", fg="white", relief="flat", padx=5, pady=2).pack(side="right", padx=10)
tk.Button(top_frame, text="Historia", command=history_window, bg="green", fg="white", relief="flat", padx=5, pady=2).pack(side="right", padx=10)

filter_frame = tk.Frame(root, bg="lightgray")
filter_frame.pack(side="top", fill="x", pady=5)

tk.Label(filter_frame, text="Filtruj cenę:", font=("Verdana", 10), bg="lightgray").pack(side="left", padx=5)
min_price_entry = tk.Entry(filter_frame, width=10)
min_price_entry.pack(side="left", padx=5)
tk.Label(filter_frame, text="do", font=("Verdana", 10), bg="lightgray").pack(side="left", padx=5)
max_price_entry = tk.Entry(filter_frame, width=10)
max_price_entry.pack(side="left", padx=5)
tk.Button(filter_frame, text="Zastosuj filtr", command=lambda: display_products(
    filter_products(
        min_price=int(min_price_entry.get()) if min_price_entry.get().isdigit() else 0,
        max_price=int(max_price_entry.get()) if max_price_entry.get().isdigit() else float('inf')
    )
), bg="blue", fg="white", relief="flat").pack(side="left", padx=5)




tk.Label(filter_frame, text="Sortuj:", font=("Verdana", 10), bg="lightgray").pack(side="left", padx=5)
sort_by_var = tk.StringVar(value="price")
tk.OptionMenu(filter_frame, sort_by_var, "price", "name").pack(side="left", padx=5)
tk.Button(filter_frame, text="Sortuj rosnąco", command=lambda: display_products(sort_products(by=sort_by_var.get())), bg="green", fg="white", relief="flat").pack(side="left", padx=5)
tk.Button(filter_frame, text="Sortuj malejąco", command=lambda: display_products(sort_products(by=sort_by_var.get(), reverse=True)), bg="red", fg="white", relief="flat").pack(side="left", padx=5)

product_frame = tk.Frame(root, bg="", highlightbackground="gray", highlightthickness=1)
product_frame.pack(fill="both", expand=True)


display_products()

root.mainloop()
