// Global State
let state = {
    userIngredients: [],
    dietaryPrefs: [],
    recipes: [],
    favorites: JSON.parse(localStorage.getItem('favorites') || '[]'),
    ratings: JSON.parse(localStorage.getItem('ratings') || '{}')
};

// DOM Elements
const textModeBtn = document.getElementById('textModeBtn');
const imageModeBtn = document.getElementById('imageModeBtn');
const textInputMode = document.getElementById('textInputMode');
const imageUploadMode = document.getElementById('imageUploadMode');
const ingredientInput = document.getElementById('ingredientInput');
const addIngredientBtn = document.getElementById('addIngredientBtn');
const ingredientTags = document.getElementById('ingredientTags');
const ingredientCount = document.getElementById('ingredientCount');
const uploadArea = document.getElementById('uploadArea');
const imageInput = document.getElementById('imageInput');
const uploadContent = document.getElementById('uploadContent');
const processingContent = document.getElementById('processingContent');
const searchBtn = document.getElementById('searchBtn');
const toggleFiltersBtn = document.getElementById('toggleFiltersBtn');
const filtersSection = document.getElementById('filtersSection');
const difficultyFilter = document.getElementById('difficultyFilter');
const timeFilter = document.getElementById('timeFilter');
const timeValue = document.getElementById('timeValue');
const resultsSection = document.getElementById('resultsSection');
const resultCount = document.getElementById('resultCount');
const recipesGrid = document.getElementById('recipesGrid');
const recipeModal = document.getElementById('recipeModal');
const modalClose = document.getElementById('modalClose');
const recipeDetail = document.getElementById('recipeDetail');

// Event Listeners
textModeBtn.addEventListener('click', () => switchMode('text'));
imageModeBtn.addEventListener('click', () => switchMode('image'));
addIngredientBtn.addEventListener('click', addIngredient);
ingredientInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') addIngredient();
});
uploadArea.addEventListener('click', () => imageInput.click());
imageInput.addEventListener('change', handleImageUpload);
searchBtn.addEventListener('click', searchRecipes);
toggleFiltersBtn.addEventListener('click', toggleFilters);
timeFilter.addEventListener('input', (e) => {
    timeValue.textContent = e.target.value;
});
modalClose.addEventListener('click', closeModal);
window.addEventListener('click', (e) => {
    if (e.target === recipeModal) closeModal();
});

// Dietary buttons
document.querySelectorAll('.btn-dietary').forEach(btn => {
    btn.addEventListener('click', function() {
        const pref = this.dataset.pref;
        toggleDietary(pref, this);
    });
});

// Functions
function switchMode(mode) {
    if (mode === 'text') {
        textModeBtn.classList.add('active');
        imageModeBtn.classList.remove('active');
        textInputMode.style.display = 'block';
        imageUploadMode.style.display = 'none';
    } else {
        imageModeBtn.classList.add('active');
        textModeBtn.classList.remove('active');
        textInputMode.style.display = 'none';
        imageUploadMode.style.display = 'block';
    }
}

function addIngredient() {
    const value = ingredientInput.value.trim();
    if (value && !state.userIngredients.includes(value)) {
        state.userIngredients.push(value);
        ingredientInput.value = '';
        updateIngredientTags();
        updateSearchButton();
    }
}

function removeIngredient(ingredient) {
    state.userIngredients = state.userIngredients.filter(i => i !== ingredient);
    updateIngredientTags();
    updateSearchButton();
}

function updateIngredientTags() {
    ingredientTags.innerHTML = state.userIngredients.map(ing => `
        <div class="ingredient-tag">
            ${ing}
            <span class="remove-btn" onclick="removeIngredient('${ing}')">&times;</span>
        </div>
    `).join('');
}

function updateSearchButton() {
    ingredientCount.textContent = state.userIngredients.length;
    searchBtn.disabled = state.userIngredients.length === 0;
}

function toggleDietary(pref, btn) {
    if (state.dietaryPrefs.includes(pref)) {
        state.dietaryPrefs = state.dietaryPrefs.filter(p => p !== pref);
        btn.classList.remove('active');
    } else {
        state.dietaryPrefs.push(pref);
        btn.classList.add('active');
    }
}

function toggleFilters() {
    const isVisible = filtersSection.style.display !== 'none';
    filtersSection.style.display = isVisible ? 'none' : 'block';
    toggleFiltersBtn.innerHTML = isVisible 
        ? '<span>🔍</span> Show Filters' 
        : '<span>🔍</span> Hide Filters';
}

function handleImageUpload(e) {
    const file = e.target.files[0];
    if (!file) return;
    
    uploadContent.style.display = 'none';
    processingContent.style.display = 'block';
    
    // Simulate image processing (2 seconds)
    setTimeout(() => {
        const detected = ['tomatoes', 'onions', 'garlic', 'cheese'];
        state.userIngredients = [...new Set([...state.userIngredients, ...detected])];
        updateIngredientTags();
        updateSearchButton();
        
        uploadContent.style.display = 'block';
        processingContent.style.display = 'none';
        imageInput.value = '';
        
        alert(`Detected ingredients: ${detected.join(', ')}`);
    }, 2000);
}

async function searchRecipes() {
    const data = {
        ingredients: state.userIngredients,
        dietary: state.dietaryPrefs,
        difficulty: difficultyFilter.value,
        maxTime: parseInt(timeFilter.value)
    };
    
    try {
        const response = await fetch('/api/search', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        
        state.recipes = await response.json();
        displayRecipes();
    } catch (error) {
        console.error('Search error:', error);
        alert('Error searching recipes. Please try again.');
    }
}

function displayRecipes() {
    resultsSection.style.display = 'block';
    resultCount.textContent = state.recipes.length;
    
    if (state.recipes.length === 0) {
        recipesGrid.innerHTML = '<p style="grid-column: 1/-1; text-align: center; padding: 40px; color: #666;">No recipes found. Try different ingredients!</p>';
        return;
    }
    
    recipesGrid.innerHTML = state.recipes.map(recipe => `
        <div class="recipe-card" onclick="showRecipeDetail(${recipe.id})">
            <div class="recipe-header">👨‍🍳</div>
            <div class="recipe-body">
                <div class="recipe-title">
                    <h3>${recipe.name}</h3>
                    <button class="favorite-btn ${state.favorites.includes(recipe.id) ? 'active' : ''}" 
                            onclick="event.stopPropagation(); toggleFavorite(${recipe.id})">
                        ${state.favorites.includes(recipe.id) ? '❤️' : '🤍'}
                    </button>
                </div>
                <p class="recipe-cuisine">${recipe.cuisine} Cuisine</p>
                <div class="recipe-meta">
                    <span class="meta-item">⏱️ ${recipe.cookingTime}min</span>
                    <span class="meta-item">👥 ${recipe.servings}</span>
                    <span class="difficulty-badge">${recipe.difficulty}</span>
                </div>
                <div class="recipe-footer">
                    <span class="match-score">${recipe.matchScore}% Match</span>
                    <div class="rating-stars">
                        ${generateStars(state.ratings[recipe.id] || 0)}
                    </div>
                </div>
            </div>
        </div>
    `).join('');
    
    // Scroll to results
    resultsSection.scrollIntoView({ behavior: 'smooth' });
}

function generateStars(rating) {
    return Array.from({length: 5}, (_, i) => 
        `<span class="star ${i < rating ? 'filled' : ''}">⭐</span>`
    ).join('');
}

function toggleFavorite(recipeId) {
    if (state.favorites.includes(recipeId)) {
        state.favorites = state.favorites.filter(id => id !== recipeId);
    } else {
        state.favorites.push(recipeId);
    }
    localStorage.setItem('favorites', JSON.stringify(state.favorites));
    displayRecipes();
}

async function showRecipeDetail(recipeId) {
    try {
        const response = await fetch(`/api/recipe/${recipeId}`);
        const recipe = await response.json();
        
        recipeDetail.innerHTML = `
            <div class="recipe-detail-header">
                <div class="recipe-detail-title">
                    <div>
                        <h2>${recipe.name}</h2>
                        <p class="recipe-detail-cuisine">${recipe.cuisine} Cuisine</p>
                    </div>
                    <button class="favorite-btn ${state.favorites.includes(recipe.id) ? 'active' : ''}" 
                            onclick="toggleFavorite(${recipe.id}); showRecipeDetail(${recipe.id})">
                        ${state.favorites.includes(recipe.id) ? '❤️' : '🤍'}
                    </button>
                </div>
            </div>
            
            <div class="recipe-stats">
                <div class="stat-card">
                    <div class="stat-label">Time</div>
                    <div class="stat-value">${recipe.cookingTime} min</div>
                </div>
                <div class="stat-card">
                    <div class="stat-label">Servings</div>
                    <div class="stat-value">${recipe.servings}</div>
                </div>
                <div class="stat-card">
                    <div class="stat-label">Calories</div>
                    <div class="stat-value">${recipe.calories}</div>
                </div>
                <div class="stat-card">
                    <div class="stat-label">Protein</div>
                    <div class="stat-value">${recipe.protein}g</div>
                </div>
            </div>
            
            <div class="recipe-section">
                <h3>Ingredients</h3>
                <ul class="ingredients-list">
                    ${recipe.ingredients.map(ing => `<li>${ing}</li>`).join('')}
                </ul>
            </div>
            
            <div class="recipe-section">
                <h3>Instructions</h3>
                <ol class="instructions-list">
                    ${recipe.instructions.map(step => `<li>${step}</li>`).join('')}
                </ol>
            </div>
            
            <div class="recipe-section">
                <h3>Substitutions</h3>
                <div class="substitutions">
                    ${Object.entries(recipe.substitutions).map(([ing, sub]) => `
                        <div class="substitution-item">
                            <strong>${ing}</strong> → ${sub}
                        </div>
                    `).join('')}
                </div>
            </div>
            
            <div class="rating-section">
                <h3>Rate This Recipe</h3>
                <div class="rating-stars-interactive">
                    ${Array.from({length: 5}, (_, i) => `
                        <span class="star ${(state.ratings[recipe.id] || 0) > i ? 'filled' : ''}" 
                              onclick="rateRecipe(${recipe.id}, ${i + 1})">⭐</span>
                    `).join('')}
                </div>
            </div>
        `;
        
        recipeModal.style.display = 'flex';
    } catch (error) {
        console.error('Error loading recipe:', error);
        alert('Error loading recipe details.');
    }
}

function rateRecipe(recipeId, rating) {
    state.ratings[recipeId] = rating;
    localStorage.setItem('ratings', JSON.stringify(state.ratings));
    showRecipeDetail(recipeId);
    displayRecipes();
}

function closeModal() {
    recipeModal.style.display = 'none';
}

// Make functions globally accessible
window.removeIngredient = removeIngredient;
window.toggleFavorite = toggleFavorite;
window.showRecipeDetail = showRecipeDetail;
window.rateRecipe = rateRecipe;