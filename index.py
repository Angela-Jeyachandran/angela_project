import requests
from keys import API_KEY
import json, os

USER_FILE = "users.json"

def search_recipes():
    # Ingredients to search for based on user input 
    ingredients = input("Enter ingredients separated by commas: ").split(',')
    ingredients = [i.strip() for i in ingredients]

    # Comma separated string for API
    ingredients_query = ','.join(ingredients)

    # API endpoint for searching recipes by ingredients
    url = 'https://api.spoonacular.com/recipes/findByIngredients'

    # Parameters for the request
    params = {
        'ingredients': ingredients_query,
        'number': 10,  # Number of recipes to return
        'ranking': 1,  # 1 = maximize used ingredients, 2 = minimize missing ingredients
        'ignorePantry': True,
        'apiKey': API_KEY
    }

    # Make the request
    response = requests.get(url, params=params)

    # Check for success
    if response.status_code == 200:
        recipes = response.json()
        for i, recipe in enumerate(recipes, start=1):
            print(f"{i}. {recipe['title']}")
            print(f"   Used Ingredients: {[ing['name'] for ing in recipe['usedIngredients']]}")
            print(f"   Missed Ingredients: {[ing['name'] for ing in recipe['missedIngredients']]}")
            print(f"   Recipe ID: {recipe['id']}")
            print(f"   Image URL: {recipe['image']}")
            print()
    else:
        print(f"Error: {response.status_code} - {response.text}")

def load_users():
    # If the user file does not exist, create it with an empty "users" list
    if not os.path.exists(USER_FILE):
        with open(USER_FILE, "w") as f:
            json.dump({"users": []}, f)
    # Read and return the JSON data from the file
    with open(USER_FILE, "r") as f:
        return json.load(f)

def save_users(users):
    # Save the given user dictionary back to the JSON file with indentation
    with open(USER_FILE, "w") as f:
        json.dump(users, f, indent=4)

def signup(username, password):
    # Loads existing users
    users = load_users()
    # Checks if username already exists
    for user in users["users"]:
        if user["username"] == username:
            return False, "Username already exists."
    # Adds the new username and password to the list
    users["users"].append({"username": username, "password": password})
    # Save updated list to json file
    save_users(users)
    return True, "Signup successful."

def login(username, password):
    # Loads existing users
    users = load_users()
    # Looks for a matching username and password
    for user in users["users"]:
        if user["username"] == username and user["password"] == password:
            return True, f"Welcome back, {username}!"
    # If not found, login fails
    return False, "Invalid username or password."

def main_menu(username):
    # Menu shown after a user logs in
    while True:
        print("Main Menu")
        print("1. Search Recipes")   # Option to call the recipe search feature
        print("2. Logout")           # Option to log out
        choice = input("Choose an option (1 or 2): ")

        if choice == "1":
            search_recipes()
        elif choice == "2":
            print(f"You are exiting the application")
            # Exit back to program end
            break  
        else:
            print("Invalid choice, try again.")

if __name__ == "__main__":
    # Entry point of the program
    print("1. Signup")
    print("2. Login")
    choice = input("Choose an option (1 or 2): ")

    # User chooses signup
    if choice == "1":
        u = input("Enter username: ")
        p = input("Enter password: ")
        success, msg = signup(u, p)
        print(msg)
        if success:
            # Go to main menu if signup worked
            main_menu(u)
    # User chooses login 
    elif choice == "2":
        u = input("Enter username: ")
        p = input("Enter password: ")
        success, msg = login(u, p)
        print(msg)
        if success:
            # Go to main menu if login successful
            main_menu(u)
    else:
        print("Invalid choice.")
