import requests

API_KEY = 'c64638c147854d759e279e1bb3fdf789'

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