# 🍳 Smart Recipe Generator

> AI-powered recipe recommendation system that suggests recipes based on your available ingredients with dietary preferences and smart filtering.

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0.0-green.svg)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Live Demo](https://img.shields.io/badge/Live-Demo-orange.svg)](YOUR_DEPLOYED_URL)

## 🌐 Live Demo

👉 **[Try the App Live!](https://smart-receipe-generator-kvz4.onrender.com/)**

---

## 📸 Screenshots

### Homepage
![Homepage](https://via.placeholder.com/800x400/ff6b35/ffffff?text=Add+your+screenshots+here)

### Recipe Results
![Recipe Results](https://via.placeholder.com/800x400/f7931e/ffffff?text=Recipe+Search+Results)

### Recipe Details
![Recipe Details](https://via.placeholder.com/800x400/ec407a/ffffff?text=Recipe+Detail+View)

---

## ✨ Features

### Core Functionality
- 🔍 **Smart Recipe Matching** - Intelligent algorithm matches recipes based on ingredient availability
- 📝 **Dual Input Modes** - Text input or image upload (AI simulation)
- 🥗 **21+ Recipe Database** - Diverse cuisines including Italian, Asian, Mediterranean, Indian, Mexican, French, and more
- 🎯 **Dietary Filters** - Vegetarian, Vegan, Gluten-Free, Non-Vegetarian options

### Advanced Features
- ⏱️ **Time & Difficulty Filters** - Filter by cooking time (10-120 min) and difficulty level
- 💚 **Favorites System** - Save your favorite recipes for quick access
- ⭐ **Rating System** - Rate recipes and see your ratings persist
- 🔄 **Ingredient Substitutions** - Smart suggestions for ingredient alternatives
- 📊 **Nutritional Information** - Calories and protein content for each recipe
- 👥 **Serving Adjustments** - Scale recipes up or down
- 📱 **Mobile Responsive** - Beautiful UI that works on all devices

### User Experience
- 🎨 **Modern UI Design** - Clean, intuitive interface with gradient themes
- 💾 **Local Storage** - Favorites and ratings saved in browser
- ⚡ **Fast Performance** - Instant search results
- 🌈 **Visual Recipe Cards** - Easy-to-scan recipe information

---

## 🛠️ Tech Stack

**Backend:**
- Python 3.8+
- Flask 3.0.0
- Gunicorn (Production server)

**Frontend:**
- HTML5
- CSS3 (Custom styling, no frameworks)
- Vanilla JavaScript (ES6+)
- Local Storage API

**Deployment:**
- Render / PythonAnywhere / Railway
- Git & GitHub

---

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Git (optional, for cloning)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/YOUR_USERNAME/smart-recipe-generator.git
cd smart-recipe-generator
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Run the application**
```bash
python app.py
```

4. **Open your browser**
```
Navigate to: http://localhost:5000
```

That's it! 🎉

---

## 📁 Project Structure

```
smart-recipe-generator/
│
├── app.py                      # Flask backend with API endpoints
├── requirements.txt            # Python dependencies
├── Procfile                    # Deployment configuration
├── README.md                   # This file
│
├── templates/
│   └── index.html             # Main HTML template
│
└── static/
    ├── css/
    │   └── style.css          # Custom styling
    └── js/
        └── script.js          # Frontend logic
```

---

## 🎯 How It Works

### 1. Recipe Matching Algorithm

The app uses a **percentage-based matching algorithm**:

```python
def calculate_match(user_ingredients, recipe, dietary_prefs):
    # Filter by dietary restrictions (hard filter)
    if dietary_prefs:
        if not all(pref in recipe['dietary'] for pref in dietary_prefs):
            return 0
    
    # Calculate ingredient overlap
    matched = [ing for ing in recipe_ingredients 
               if any(user_ing in ing or ing in user_ing 
                      for user_ing in user_ingredients)]
    
    # Return match percentage
    return (len(matched) / len(recipe_ingredients)) * 100
```

**Key Features:**
- Fuzzy string matching (e.g., "chicken" matches "chicken breast")
- Dietary restrictions as hard filters
- Results sorted by match percentage

### 2. API Endpoints

**POST** `/api/search`
- Search recipes based on ingredients
- Request body:
```json
{
  "ingredients": ["chicken", "tomatoes"],
  "dietary": ["non-vegetarian"],
  "difficulty": "Easy",
  "maxTime": 30
}
```

**GET** `/api/recipe/<id>`
- Get detailed information for a specific recipe

### 3. Frontend Architecture

- **State Management**: JavaScript object stores app state
- **Local Storage**: Persists favorites and ratings
- **Event-Driven**: User interactions trigger API calls
- **Dynamic Rendering**: DOM updates based on search results

---

## 🔧 Configuration

### Adding New Recipes

Edit `app.py` and add to the `RECIPES` list:

```python
{
    "id": 22,
    "name": "Recipe Name",
    "cuisine": "Cuisine Type",
    "ingredients": ["ingredient1", "ingredient2", "ingredient3"],
    "difficulty": "Easy",  # Easy, Medium, or Hard
    "cookingTime": 30,     # in minutes
    "servings": 4,
    "calories": 400,
    "protein": 20,         # in grams
    "dietary": ["vegetarian", "gluten-free"],
    "instructions": [
        "Step 1 description",
        "Step 2 description",
        "Step 3 description"
    ],
    "substitutions": {
        "ingredient1": "alternative ingredient"
    }
}
```

### Customizing Colors

Edit `static/css/style.css`:

```css
/* Primary gradient colors */
.btn-search {
    background: linear-gradient(135deg, #your-color1 0%, #your-color2 100%);
}

/* Logo color */
.logo h1 {
    color: #your-brand-color;
}
```

---

## 🌐 Deployment

### Deploy to Render (Recommended - FREE)

1. **Push to GitHub**
```bash
git add .
git commit -m "Initial commit"
git push origin main
```

2. **Deploy on Render**
- Go to [render.com](https://render.com)
- Click "New +" → "Web Service"
- Connect your GitHub repository
- Build Command: `pip install -r requirements.txt`
- Start Command: `gunicorn app:app`
- Click "Create Web Service"

3. **Your app is live!** 🎉

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed instructions and alternative platforms.

---

## 📊 Recipe Database

The app includes **21 diverse recipes** across multiple categories:

| Cuisine | Recipes | Dietary Options |
|---------|---------|-----------------|
| Italian | 6 recipes | Vegetarian, Non-Veg |
| Asian | 5 recipes | Vegan, Non-Veg |
| Mediterranean | 4 recipes | Vegetarian, Vegan, GF |
| Indian | 1 recipe | Non-Veg, GF |
| Mexican | 1 recipe | Non-Veg |
| French | 1 recipe | Non-Veg |
| American | 2 recipes | Vegetarian, Non-Veg |
| Healthy | 1 recipe | Vegan, Vegetarian, GF |

**Dietary Coverage:**
- Vegetarian: 9 recipes
- Vegan: 5 recipes
- Gluten-Free: 8 recipes
- Non-Vegetarian: 12 recipes

---

## 🎓 Technical Assessment Summary

### Problem-Solving Approach

This Smart Recipe Generator implements a **multi-criteria filtering system** with intelligent ingredient matching:

1. **Primary Filter**: Ingredient-based fuzzy matching calculates overlap percentage
2. **Hard Filters**: Dietary restrictions eliminate incompatible recipes
3. **Soft Filters**: Time and difficulty preferences further refine results
4. **Ranking**: Results sorted by match percentage for optimal user experience

### Architecture Decisions

**Why Flask?**
- Lightweight and fast
- Easy to deploy
- Simple API structure
- No unnecessary overhead

**Why Vanilla JavaScript?**
- No build process required
- Faster page loads
- Easier to understand and modify
- No framework dependencies

**Why Client-Side Storage?**
- Reduces server load
- Instant response times
- No database setup needed
- Perfect for MVP demonstration

### Key Features Implementation

1. **Ingredient Recognition**: Simulated AI detection with 2-second processing delay (can be enhanced with TensorFlow.js or cloud vision APIs)
2. **Smart Filtering**: Multi-level filtering system with real-time updates
3. **User Feedback Loop**: LocalStorage persists user preferences across sessions
4. **Substitution Engine**: Provides alternatives for dietary restrictions or missing ingredients

### Error Handling

- Input validation prevents empty searches
- Try-catch blocks on all API calls
- User-friendly error messages
- Graceful fallbacks for no results

### Performance Optimizations

- Client-side state management
- Efficient DOM manipulation
- CSS transitions for smooth UX
- Lazy loading of recipe details

### Scalability Considerations

The modular architecture allows easy additions:
- Real ML-based ingredient detection
- User accounts and cloud storage
- Recipe recommendations based on history
- Social features (sharing, comments)
- Nutritional goal tracking
- Meal planning features

**Development Time**: ~6-8 hours  
**Lines of Code**: ~1,200 (Python: 400, JavaScript: 400, HTML: 200, CSS: 200)

---

