# MTG_Collection_Manager
building out an inventory database with gui for Magic the gathering

# as of april 21 2025 Gui_beta is my best version, test.py has no features aside displaying card information and price, bui_beta allows adding cards ont at a time and updating quantity. in time i will set up price charting and change logs, my goal is to build out a database and gui for a store inventory. 

Overview
The MTG Collection Manager is a Python-based application that allows you to manage, track, and analyze your Magic: The Gathering (MTG) card collection. The application features a GUI built with Tkinter, enabling users to add cards, update quantities, view card details, and track prices over time. The data is stored in an SQLite database, with integration to external APIs for fetching card information and prices.

Key Features:
Add new cards: Add new cards to your collection by providing the set code, collector number, and quantity. Card details are automatically fetched from Scryfall.

Update quantities: Easily update the quantity of cards in your collection.

View card details: View card names, sets, quantities, and images.

Price tracking: Fetch current price data from external sources (like Scryfall) and visualize price trends over time.

Database logging: Track when cards are added or removed, and maintain a change log for all updates made.

Requirements
Before running the application, make sure you have the following Python packages installed:

requests

sqlite3 (comes pre-installed with Python)

tkinter (comes pre-installed with Python)

Pillow (for image handling)

matplotlib (for price charts)

beautifulsoup4 (for web scraping from MTG Goldfish)

You can install the necessary dependencies by running the following:

bash
Copy
Edit
pip install requests Pillow matplotlib beautifulsoup4
Setup
Database Setup: The application uses an SQLite database (mtg_cards.db) to store the card data, including the Cards, Sets, and Collection tables. The schema will be created automatically when you run the application for the first time.

Import Cards: You can import cards from a CSV or text file containing Magic: The Gathering card data. The program will populate the database with card information from Scryfall based on the card's set code and collector number.

Example CSV format:

pgsql
Copy
Edit
name,set_code,collector_number,quantity
Lightning Bolt,core21,123,3
Llanowar Elves,grn,45,5
Running the Application: After installing the required dependencies and setting up the database, you can run the application by executing the mtg_collection_manager.py script. The GUI will open, and you can begin managing your collection.

bash
Copy
Edit
python mtg_collection_manager.py
GUI Features
Filters: You can filter your collection by card name, set, rarity, and type. Filters are dynamically populated based on the data in the database.

Card Selection: Select a card from the list to view its image, quantity, and price (if available). Prices are fetched in real time from Scryfall.

Add New Card: Add new cards to your collection by entering the set code, collector number, and quantity. The rest of the card data is automatically fetched from Scryfall.

Price History: A price chart shows the price of the selected card over time. Data is fetched and displayed from Scryfall.

Database Schema
The SQLite database uses the following tables:

Cards: Stores detailed information about each card.

card_id: Unique identifier for each card.

card_name: The name of the card.

mana_cost: The mana cost of the card (if applicable).

cmc: The converted mana cost of the card.

rarity: The rarity of the card (e.g., Common, Rare).

set_id: Foreign key referencing the Sets table.

type_line: The card's type line (e.g., Creature, Artifact).

oracle_text: The card's Oracle text.

flavor_text: The flavor text of the card (if applicable).

artist: The artist who illustrated the card.

image_url: URL of the card's image.

Sets: Stores information about MTG sets.

set_id: Unique identifier for each set.

set_name: The name of the set.

code: The code for the set (e.g., "core21").

release_date: The release date of the set.

Collection: Stores information about the user's collection.

card_id: Foreign key referencing the Cards table.

quantity: The number of copies of the card in the collection.

date_added: The date the card was added to the collection.

date_removed: The date the card was removed from the collection (if applicable).

Backfilling Data
For existing records in the Collection table, the date_added column is populated with the current timestamp when the record is first created.

Development Setup
If you're contributing to this project or need to modify the application, follow these steps:

Clone the repository:

bash
Copy
Edit
git clone https://github.com/your-username/mtg-collection-manager.git
cd mtg-collection-manager
Create a virtual environment:

bash
Copy
Edit
python -m venv venv
Activate the virtual environment:

On Windows:

bash
Copy
Edit
venv\Scripts\activate
On macOS/Linux:

bash
Copy
Edit
source venv/bin/activate
Install the dependencies:

bash
Copy
Edit
pip install -r requirements.txt
Run the application:

bash
Copy
Edit
python mtg_collection_manager.py
Contributing
If you'd like to contribute to the project, feel free to fork the repository and submit a pull request. Please ensure that your changes are well-documented and tested.

Additional Notes:
Feel free to adjust this README based on any additional features you implement or changes in functionality. It’s important to keep the README updated as you develop new features or improve the application.

Let me know if you need further tweaks to the README!
