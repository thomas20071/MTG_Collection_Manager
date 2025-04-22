import sqlite3
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import requests
from io import BytesIO
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

# Connect to the SQLite database
conn = sqlite3.connect("mtg_cards.db")
cursor = conn.cursor()

# Create a price history table if it doesn't exist
cursor.execute("""
    CREATE TABLE IF NOT EXISTS PriceHistory (
        card_id INTEGER,
        date TEXT,
        usd_price REAL,
        FOREIGN KEY (card_id) REFERENCES Cards(card_id)
    )
""")
conn.commit()

# Initialize the main window
root = tk.Tk()
root.title("MTG Card Collection")
root.geometry("1000x600")

# Frame for the card list and filters
frame_left = ttk.Frame(root)
frame_left.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

# Frame for displaying image and details
frame_right = ttk.Frame(root)
frame_right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

# Frame to embed matplotlib price chart
chart_frame = tk.Frame(frame_right)
chart_frame.pack(fill=tk.BOTH, expand=False, pady=(10, 0))

# Frame for filters
filters_frame = ttk.Frame(frame_left)
filters_frame.pack(fill=tk.X, pady=5)

# Set filter dropdown
set_var = tk.StringVar()
set_dropdown = ttk.Combobox(filters_frame, textvariable=set_var, state="normal")
set_dropdown.pack(fill=tk.X)

# Rarity filter dropdown
rarity_var = tk.StringVar()
rarity_dropdown = ttk.Combobox(filters_frame, textvariable=rarity_var, state="normal")
rarity_dropdown.pack(fill=tk.X, pady=(5, 0))

# Search bar for name filtering
search_var = tk.StringVar()
search_entry = ttk.Entry(frame_left, textvariable=search_var)
search_entry.pack(fill=tk.X, pady=(5, 0))

# Treeview to display the card list
columns = ("Name", "Set", "Quantity", "Mana Cost", "Rarity")
tree = ttk.Treeview(frame_left, columns=columns, show="headings", height=25)
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=120)
tree.pack(fill=tk.BOTH, expand=True)

# Image label to display card art
image_label = ttk.Label(frame_right)
image_label.pack()

# Label for price display
price_label = ttk.Label(frame_right, font=("Arial", 14))
price_label.pack(pady=10)

# Quantity editing widgets
editor_frame = tk.Frame(root)
editor_frame.pack(fill=tk.X, pady=10)

tk.Label(editor_frame, text="Quantity:").pack(side=tk.LEFT)
quantity_var = tk.IntVar()
tk.Entry(editor_frame, textvariable=quantity_var, width=5).pack(side=tk.LEFT, padx=5)
tk.Button(editor_frame, text="💾 Save", command=lambda: update_quantity()).pack(side=tk.LEFT)
#Add Card button  
add_button = tk.Button(editor_frame, text="➕ Add Card", command=lambda: open_add_popup())
add_button.pack(side=tk.LEFT, padx=10)
#pop up function 
def open_add_popup():
    popup = tk.Toplevel(root)
    popup.title("Add New Card")

    tk.Label(popup, text="Set Code:").grid(row=0, column=0)
    set_code_entry = tk.Entry(popup)
    set_code_entry.grid(row=0, column=1)

    tk.Label(popup, text="Collector Number:").grid(row=1, column=0)
    collector_entry = tk.Entry(popup)
    collector_entry.grid(row=1, column=1)

    tk.Label(popup, text="Quantity:").grid(row=2, column=0)
    quantity_entry = tk.Entry(popup)
    quantity_entry.grid(row=2, column=1)

    def submit():
        set_code = set_code_entry.get().lower().strip()
        collector_number = collector_entry.get().strip()
        quantity = int(quantity_entry.get().strip())

        # Fetch card from Scryfall
        api_url = f"https://api.scryfall.com/cards/{set_code}/{collector_number}"
        response = requests.get(api_url)
        if response.status_code != 200:
            tk.messagebox.showerror("Error", "Card not found on Scryfall.")
            popup.destroy()
            return

        card = response.json()

        # Extract details
        card_name = card.get('name')
        mana_cost = card.get('mana_cost')
        cmc = card.get('cmc')
        power = card.get('power')
        toughness = card.get('toughness')
        loyalty = card.get('loyalty')
        rarity = card.get('rarity').capitalize() if card.get('rarity') else None
        type_line = card.get('type_line')
        oracle_text = card.get('oracle_text')
        flavor_text = card.get('flavor_text')
        artist = card.get('artist')
        image_url = card.get('image_uris', {}).get('normal') if card.get('image_uris') else None

        set_name = card.get('set_name')
        release_date = card.get('released_at')

        # Insert or get set
        cursor.execute("SELECT set_id FROM Sets WHERE code = ?", (set_code,))
        set_row = cursor.fetchone()
        if set_row:
            set_id = set_row[0]
        else:
            cursor.execute("INSERT INTO Sets (set_name, code, release_date) VALUES (?, ?, ?)", (set_name, set_code, release_date))
            set_id = cursor.lastrowid

        # Insert card
        cursor.execute("""
            INSERT OR IGNORE INTO Cards (
                card_name, mana_cost, cmc, power, toughness, loyalty,
                rarity, set_id, type_line, oracle_text, flavor_text,
                artist, image_url
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            card_name, mana_cost, cmc, power, toughness, loyalty,
            rarity, set_id, type_line, oracle_text, flavor_text,
            artist, image_url
        ))

        # Get card_id
        cursor.execute("SELECT card_id FROM Cards WHERE card_name = ? AND set_id = ?", (card_name, set_id))
        card_id = cursor.fetchone()[0]

        # Insert into collection
        cursor.execute("INSERT INTO Collection (card_id, quantity) VALUES (?, ?) ON CONFLICT(card_id) DO UPDATE SET quantity = quantity + ?", (card_id, quantity, quantity))
        conn.commit()

        popup.destroy()
        load_cards()  # Refresh the list

    tk.Button(popup, text="Add", command=submit).grid(row=3, columnspan=2, pady=10)


def populate_filters():
    # Populate set dropdown
    cursor.execute("SELECT DISTINCT code FROM Sets ORDER BY code")
    sets = ["All Sets"] + [row[0] for row in cursor.fetchall()]
    set_dropdown['values'] = sets
    set_var.set("All Sets")

    # Populate rarity dropdown
    cursor.execute("SELECT DISTINCT rarity FROM Cards WHERE rarity IS NOT NULL ORDER BY rarity")
    rarities = ["All Rarities"] + [row[0] for row in cursor.fetchall()]
    rarity_dropdown['values'] = rarities
    rarity_var.set("All Rarities")

def load_cards(filter_text=""):
    tree.delete(*tree.get_children())
    
    query = """
        SELECT Cards.card_id, Cards.card_name, Sets.code, Collection.quantity,Cards.mana_cost, Cards.rarity, Cards.image_url
        FROM Cards
        JOIN Sets ON Cards.set_id = Sets.set_id
        JOIN Collection ON Cards.card_id = Collection.card_id
        WHERE Cards.card_name LIKE ?
    """
    params = [f"%{filter_text}%"]

    if set_var.get() != "All Sets":
        query += " AND Sets.code = ?"
        params.append(set_var.get())

    if rarity_var.get() != "All Rarities":
        query += " AND Cards.rarity = ?"
        params.append(rarity_var.get())

    query += " ORDER BY Cards.card_name"

    cursor.execute(query, params)
    for row in cursor.fetchall():
        card_id, name, set_code, quantity, mana_cost, rarity, image_url = row
        tree.insert("", "end", values=(name, set_code, quantity, mana_cost, rarity), tags=(card_id, image_url))


def on_card_select(event):
    selected = tree.focus()
    if not selected:
        return

    tags = tree.item(selected, "tags")
    if not tags or len(tags) != 2:
        return

    card_id, image_url = tags
    card_id = int(card_id)

    # Show price chart
    show_price_chart(card_id)

    # Load quantity for editor
    cursor.execute("SELECT quantity FROM Collection WHERE card_id = ?", (card_id,))
    row = cursor.fetchone()
    quantity_var.set(row[0] if row else 0)

    # Load card image
    if image_url:
        try:
            img_data = requests.get(image_url).content
            img = Image.open(BytesIO(img_data)).resize((250, 350))
            photo = ImageTk.PhotoImage(img)
            image_label.configure(image=photo, text="")
            image_label.image = photo
        except Exception as e:
            image_label.configure(text="⚠️ Failed to load image", image="")
            print(e)

    # Fetch live price
    cursor.execute("SELECT set_id FROM Cards WHERE card_id = ?", (card_id,))
    set_id = cursor.fetchone()[0]
    cursor.execute("SELECT code FROM Sets WHERE set_id = ?", (set_id,))
    set_code = cursor.fetchone()[0]
    cursor.execute("SELECT card_name FROM Cards WHERE card_id = ?", (card_id,))
    card_name = cursor.fetchone()[0]

    api_url = f"https://api.scryfall.com/cards/named?exact={card_name}&set={set_code}"
    try:
        r = requests.get(api_url)
        data = r.json()
        price = data.get("prices", {}).get("usd")
        price_label.config(text=f"💵 USD Price: ${price}" if price else "No price found.")
    except Exception as e:
        price_label.config(text="⚠️ Price fetch failed.")
        print(e)

def show_price_chart(card_id):
    # Clear existing chart
    for widget in chart_frame.winfo_children():
        widget.destroy()

    cursor.execute("SELECT date, usd_price FROM PriceHistory WHERE card_id = ? ORDER BY date", (card_id,))
    rows = cursor.fetchall()
    if not rows:
        return

    dates, prices = zip(*rows)
    fig, ax = plt.subplots(figsize=(4, 3))
    ax.plot(dates, prices, marker='o')
    ax.set_title("Price Over Time")
    ax.set_xlabel("Date")
    ax.set_ylabel("USD Price")
    ax.tick_params(axis='x', rotation=45)

    canvas = FigureCanvasTkAgg(fig, master=chart_frame)
    canvas.draw()
    canvas.get_tk_widget().pack()

def update_quantity():
    selected = tree.focus()
    if not selected:
        print("No card selected.")
        return

    card_id = int(tree.item(selected, "tags")[0])
    new_quantity = quantity_var.get()

    cursor.execute("UPDATE Collection SET quantity = ? WHERE card_id = ?", (new_quantity, card_id))
    conn.commit()
    load_cards(search_var.get())
    print(f"✅ Updated quantity to {new_quantity}")

# Reactive filtering on type/search input
search_var.trace("w", lambda *args: load_cards(search_var.get()))
set_var.trace("w", lambda *args: load_cards(search_var.get()))
rarity_var.trace("w", lambda *args: load_cards(search_var.get()))

# Bind events
set_dropdown.bind("<<ComboboxSelected>>", lambda e: load_cards(search_var.get()))
rarity_dropdown.bind("<<ComboboxSelected>>", lambda e: load_cards(search_var.get()))
tree.bind("<<TreeviewSelect>>", on_card_select)

# Final setup
populate_filters()
load_cards()
root.mainloop()
