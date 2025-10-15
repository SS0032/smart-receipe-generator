from flask import Flask, render_template, request, jsonify
import json

app = Flask(__name__)

# Recipe Database
RECIPES = [
    {
        "id": 1, "name": "Spaghetti Carbonara", "cuisine": "Italian",
        "ingredients": ["spaghetti", "eggs", "bacon", "parmesan", "pepper"],
        "difficulty": "Medium", "cookingTime": 25, "servings": 4,
        "calories": 450, "protein": 22, "dietary": ["non-vegetarian"],
        "instructions": [
            "Boil spaghetti in salted water until al dente",
            "Fry bacon until crispy, set aside",
            "Beat eggs with grated parmesan",
            "Drain pasta, mix with bacon and egg mixture off heat",
            "Season with black pepper and serve immediately"
        ],
        "substitutions": {"bacon": "pancetta or guanciale", "spaghetti": "linguine"}
    },
    {
        "id": 2, "name": "Vegetable Stir Fry", "cuisine": "Asian",
        "ingredients": ["broccoli", "carrots", "peppers", "soy sauce", "garlic", "ginger", "rice"],
        "difficulty": "Easy", "cookingTime": 20, "servings": 3,
        "calories": 280, "protein": 8, "dietary": ["vegetarian", "vegan"],
        "instructions": [
            "Heat oil in wok over high heat",
            "Add garlic and ginger, stir for 30 seconds",
            "Stir fry vegetables for 5 minutes",
            "Add soy sauce and toss",
            "Serve over rice"
        ],
        "substitutions": {"soy sauce": "tamari", "rice": "quinoa"}
    },
    {
        "id": 3, "name": "Chicken Tikka Masala", "cuisine": "Indian",
        "ingredients": ["chicken", "yogurt", "tomatoes", "cream", "onions", "garlic", "spices"],
        "difficulty": "Medium", "cookingTime": 45, "servings": 4,
        "calories": 520, "protein": 35, "dietary": ["non-vegetarian", "gluten-free"],
        "instructions": [
            "Marinate chicken in yogurt and spices",
            "Grill chicken until cooked",
            "Make tomato-based curry sauce",
            "Add cream and chicken",
            "Simmer for 10 minutes"
        ],
        "substitutions": {"chicken": "paneer or tofu", "cream": "coconut cream"}
    },
    {
        "id": 4, "name": "Greek Salad", "cuisine": "Mediterranean",
        "ingredients": ["tomatoes", "cucumber", "olives", "feta", "onions", "olive oil"],
        "difficulty": "Easy", "cookingTime": 10, "servings": 4,
        "calories": 180, "protein": 6, "dietary": ["vegetarian", "gluten-free"],
        "instructions": [
            "Chop tomatoes and cucumbers",
            "Slice onions thinly",
            "Combine with olives and feta",
            "Dress with olive oil and lemon",
            "Season and serve"
        ],
        "substitutions": {"feta": "vegan feta", "olives": "capers"}
    },
    {
        "id": 5, "name": "Beef Tacos", "cuisine": "Mexican",
        "ingredients": ["beef", "tortillas", "lettuce", "tomatoes", "cheese", "spices"],
        "difficulty": "Easy", "cookingTime": 20, "servings": 4,
        "calories": 380, "protein": 28, "dietary": ["non-vegetarian"],
        "instructions": [
            "Brown ground beef with spices",
            "Warm tortillas",
            "Chop vegetables",
            "Assemble tacos with toppings",
            "Serve immediately"
        ],
        "substitutions": {"beef": "chicken or black beans", "tortillas": "lettuce wraps"}
    },
    {
        "id": 6, "name": "Mushroom Risotto", "cuisine": "Italian",
        "ingredients": ["rice", "mushrooms", "onions", "wine", "parmesan", "broth"],
        "difficulty": "Hard", "cookingTime": 40, "servings": 4,
        "calories": 420, "protein": 12, "dietary": ["vegetarian", "gluten-free"],
        "instructions": [
            "Sauté mushrooms until golden",
            "Toast arborio rice",
            "Add wine and stir",
            "Gradually add broth while stirring",
            "Finish with parmesan"
        ],
        "substitutions": {"wine": "vegetable broth", "parmesan": "nutritional yeast"}
    },
    {
        "id": 7, "name": "Pad Thai", "cuisine": "Asian",
        "ingredients": ["noodles", "shrimp", "eggs", "peanuts", "sprouts", "lime"],
        "difficulty": "Medium", "cookingTime": 30, "servings": 3,
        "calories": 480, "protein": 24, "dietary": ["non-vegetarian"],
        "instructions": [
            "Soak rice noodles",
            "Scramble eggs",
            "Stir fry shrimp",
            "Add noodles and sauce",
            "Top with peanuts and lime"
        ],
        "substitutions": {"shrimp": "tofu", "fish sauce": "soy sauce"}
    },
    {
        "id": 8, "name": "Buddha Bowl", "cuisine": "Healthy",
        "ingredients": ["quinoa", "chickpeas", "avocado", "kale", "sweet potato", "tahini"],
        "difficulty": "Easy", "cookingTime": 35, "servings": 2,
        "calories": 520, "protein": 18, "dietary": ["vegetarian", "vegan", "gluten-free"],
        "instructions": [
            "Cook quinoa",
            "Roast sweet potato",
            "Massage kale with lemon",
            "Roast chickpeas",
            "Assemble and drizzle tahini"
        ],
        "substitutions": {"quinoa": "brown rice", "tahini": "peanut butter"}
    },
    {
        "id": 9, "name": "French Onion Soup", "cuisine": "French",
        "ingredients": ["onions", "broth", "bread", "cheese", "butter", "wine"],
        "difficulty": "Medium", "cookingTime": 60, "servings": 4,
        "calories": 340, "protein": 15, "dietary": ["non-vegetarian"],
        "instructions": [
            "Caramelize onions slowly",
            "Add wine and broth",
            "Simmer for 20 minutes",
            "Top with bread and cheese",
            "Broil until golden"
        ],
        "substitutions": {"beef broth": "vegetable broth", "cheese": "vegan cheese"}
    },
    {
        "id": 10, "name": "Salmon with Asparagus", "cuisine": "Healthy",
        "ingredients": ["salmon", "asparagus", "lemon", "garlic", "olive oil", "dill"],
        "difficulty": "Easy", "cookingTime": 20, "servings": 2,
        "calories": 380, "protein": 34, "dietary": ["non-vegetarian", "gluten-free"],
        "instructions": [
            "Preheat oven to 400°F",
            "Season salmon and asparagus",
            "Drizzle with olive oil",
            "Add garlic and dill",
            "Bake for 15-18 minutes"
        ],
        "substitutions": {"salmon": "cod or trout", "asparagus": "green beans"}
    },
    {
        "id": 11, "name": "Veggie Burger", "cuisine": "American",
        "ingredients": ["black beans", "breadcrumbs", "onions", "garlic", "spices", "buns"],
        "difficulty": "Easy", "cookingTime": 25, "servings": 4,
        "calories": 320, "protein": 14, "dietary": ["vegetarian", "vegan"],
        "instructions": [
            "Mash black beans",
            "Mix with breadcrumbs and spices",
            "Form into patties",
            "Pan fry until crispy",
            "Serve on buns"
        ],
        "substitutions": {"black beans": "chickpeas", "breadcrumbs": "oats"}
    },
    {
        "id": 12, "name": "Thai Green Curry", "cuisine": "Asian",
        "ingredients": ["chicken", "coconut milk", "curry paste", "vegetables", "basil"],
        "difficulty": "Medium", "cookingTime": 30, "servings": 4,
        "calories": 440, "protein": 26, "dietary": ["non-vegetarian", "gluten-free"],
        "instructions": [
            "Heat curry paste",
            "Add coconut milk",
            "Cook chicken",
            "Add vegetables",
            "Finish with basil"
        ],
        "substitutions": {"chicken": "tofu", "fish sauce": "soy sauce"}
    },
    {
        "id": 13, "name": "Margherita Pizza", "cuisine": "Italian",
        "ingredients": ["dough", "tomatoes", "mozzarella", "basil", "olive oil"],
        "difficulty": "Medium", "cookingTime": 30, "servings": 4,
        "calories": 380, "protein": 16, "dietary": ["vegetarian"],
        "instructions": [
            "Roll out pizza dough",
            "Spread tomato sauce",
            "Top with mozzarella",
            "Bake at 475°F",
            "Add fresh basil"
        ],
        "substitutions": {"mozzarella": "vegan cheese", "dough": "cauliflower crust"}
    },
    {
        "id": 14, "name": "Lentil Soup", "cuisine": "Mediterranean",
        "ingredients": ["lentils", "carrots", "celery", "onions", "tomatoes", "broth"],
        "difficulty": "Easy", "cookingTime": 40, "servings": 6,
        "calories": 240, "protein": 14, "dietary": ["vegetarian", "vegan", "gluten-free"],
        "instructions": [
            "Sauté vegetables",
            "Add lentils and broth",
            "Simmer for 30 minutes",
            "Season to taste",
            "Serve hot"
        ],
        "substitutions": {"lentils": "split peas", "broth": "water with bouillon"}
    },
    {
        "id": 15, "name": "Caesar Salad", "cuisine": "American",
        "ingredients": ["chicken", "romaine", "parmesan", "bread", "garlic", "lemon"],
        "difficulty": "Easy", "cookingTime": 25, "servings": 3,
        "calories": 420, "protein": 32, "dietary": ["non-vegetarian"],
        "instructions": [
            "Grill chicken breast",
            "Make croutons",
            "Prepare Caesar dressing",
            "Toss lettuce with dressing",
            "Top with chicken"
        ],
        "substitutions": {"chicken": "tofu", "anchovies": "capers"}
    },
    {
        "id": 16, "name": "Beef Stir Fry", "cuisine": "Asian",
        "ingredients": ["beef", "broccoli", "soy sauce", "ginger", "garlic", "rice"],
        "difficulty": "Easy", "cookingTime": 20, "servings": 4,
        "calories": 380, "protein": 28, "dietary": ["non-vegetarian"],
        "instructions": [
            "Marinate sliced beef",
            "Stir fry beef",
            "Add vegetables",
            "Toss with sauce",
            "Serve over rice"
        ],
        "substitutions": {"beef": "tofu", "broccoli": "bok choy"}
    },
    {
        "id": 17, "name": "Caprese Salad", "cuisine": "Italian",
        "ingredients": ["tomatoes", "mozzarella", "basil", "olive oil", "balsamic"],
        "difficulty": "Easy", "cookingTime": 10, "servings": 4,
        "calories": 220, "protein": 12, "dietary": ["vegetarian", "gluten-free"],
        "instructions": [
            "Slice tomatoes and mozzarella",
            "Arrange alternating on plate",
            "Add fresh basil",
            "Drizzle with oil and vinegar",
            "Season with salt and pepper"
        ],
        "substitutions": {"mozzarella": "burrata", "balsamic": "lemon juice"}
    },
    {
        "id": 18, "name": "Shrimp Scampi", "cuisine": "Italian",
        "ingredients": ["shrimp", "pasta", "garlic", "wine", "lemon", "butter"],
        "difficulty": "Easy", "cookingTime": 20, "servings": 4,
        "calories": 440, "protein": 26, "dietary": ["non-vegetarian"],
        "instructions": [
            "Cook pasta",
            "Sauté garlic in butter",
            "Add shrimp",
            "Deglaze with wine",
            "Toss with pasta"
        ],
        "substitutions": {"shrimp": "scallops", "wine": "chicken broth"}
    },
    {
        "id": 19, "name": "Falafel Wrap", "cuisine": "Mediterranean",
        "ingredients": ["chickpeas", "onions", "garlic", "spices", "pita", "tahini"],
        "difficulty": "Medium", "cookingTime": 30, "servings": 4,
        "calories": 380, "protein": 16, "dietary": ["vegetarian", "vegan"],
        "instructions": [
            "Blend chickpeas with spices",
            "Form into balls",
            "Fry until crispy",
            "Warm pita bread",
            "Assemble with tahini"
        ],
        "substitutions": {"chickpeas": "fava beans", "pita": "tortilla"}
    },
    {
        "id": 20, "name": "Teriyaki Chicken", "cuisine": "Asian",
        "ingredients": ["chicken", "soy sauce", "mirin", "sugar", "ginger", "rice"],
        "difficulty": "Easy", "cookingTime": 25, "servings": 4,
        "calories": 420, "protein": 34, "dietary": ["non-vegetarian"],
        "instructions": [
            "Make teriyaki sauce",
            "Cook chicken pieces",
            "Glaze with sauce",
            "Simmer until thick",
            "Serve over rice"
        ],
        "substitutions": {"chicken": "salmon", "mirin": "wine with sugar"}
    },
    {
        "id": 21, "name": "Veggie Lasagna", "cuisine": "Italian",
        "ingredients": ["noodles", "ricotta", "mozzarella", "spinach", "zucchini", "tomatoes"],
        "difficulty": "Hard", "cookingTime": 60, "servings": 8,
        "calories": 420, "protein": 20, "dietary": ["vegetarian"],
        "instructions": [
            "Cook lasagna noodles",
            "Sauté vegetables",
            "Layer noodles, cheese, vegetables",
            "Bake at 375°F for 45 minutes",
            "Let rest before serving"
        ],
        "substitutions": {"ricotta": "cottage cheese", "noodles": "zucchini slices"}
    }
]

def calculate_match(user_ingredients, recipe, dietary_prefs):
    """Calculate recipe match percentage"""
    recipe_ings = [ing.lower() for ing in recipe['ingredients']]
    user_ings = [ing.lower() for ing in user_ingredients]
    
    # Check dietary restrictions
    if dietary_prefs:
        if not all(pref in recipe['dietary'] for pref in dietary_prefs):
            return 0
    
    # Calculate ingredient match
    matched = [ing for ing in recipe_ings if any(ui in ing or ing in ui for ui in user_ings)]
    
    if not recipe_ings:
        return 0
    
    return (len(matched) / len(recipe_ings)) * 100

@app.route('/')
def index():
    """Render main page"""
    return render_template('index.html')

@app.route('/api/search', methods=['POST'])
def search_recipes():
    """Search recipes based on ingredients and filters"""
    data = request.json
    user_ingredients = data.get('ingredients', [])
    dietary_prefs = data.get('dietary', [])
    difficulty_filter = data.get('difficulty', '')
    max_time = data.get('maxTime', 120)
    
    # Calculate matches
    results = []
    for recipe in RECIPES:
        match_score = calculate_match(user_ingredients, recipe, dietary_prefs)
        if match_score > 0:
            recipe_copy = recipe.copy()
            recipe_copy['matchScore'] = round(match_score, 1)
            results.append(recipe_copy)
    
    # Apply filters
    if difficulty_filter:
        results = [r for r in results if r['difficulty'] == difficulty_filter]
    
    if max_time < 120:
        results = [r for r in results if r['cookingTime'] <= max_time]
    
    # Sort by match score
    results.sort(key=lambda x: x['matchScore'], reverse=True)
    
    return jsonify(results)

@app.route('/api/recipe/<int:recipe_id>')
def get_recipe(recipe_id):
    """Get single recipe details"""
    recipe = next((r for r in RECIPES if r['id'] == recipe_id), None)
    if recipe:
        return jsonify(recipe)
    return jsonify({'error': 'Recipe not found'}), 404

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)