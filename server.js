require('dotenv').config();
const express = require('express');
const app = express();
const axios = require('axios');

const PORT = process.env.PORT || 5001;

app.get('/', (req, res) => {
    res.send('Hello World');
});

app.listen(PORT, () => {
    console.log(`Server is running on port ${PORT}`);
});

app.get('/api/recipes', async (req, res) => {
    const ingredients = req.query.ingredients; // comma-separated
    const number = parseInt(req.query.number) || 3;
    const cuisine = req.query.cuisine ? req.query.cuisine.split(',').map(c => c.toLowerCase()) : [];
    const apiKey = process.env.API_KEY;

    if (!ingredients) return res.status(400).json({ error: 'Please provide ingredients' });

    try {
        // Fetch recipes by ingredients
        const response = await axios.get(
            'https://api.spoonacular.com/recipes/findByIngredients',
            {
                params: {
                    ingredients: ingredients,
                    number,
                    ranking: 1,
                    ignorePantry: true,
                    apiKey
                }
            }
        );

        let recipes = response.data;

        // Filter by cuisine if requested
        if (cuisine.length) {
            // Fetch recipe info in parallel
            const detailPromises = recipes.map(recipe =>
                axios.get(`https://api.spoonacular.com/recipes/${recipe.id}/information`, { params: { apiKey } })
            );

            const details = await Promise.all(detailPromises);

            recipes = details
                .map(detail => detail.data)
                .filter(info => info.cuisines.some(c => cuisine.includes(c.toLowerCase())))
                .slice(0, number); // only return requested number
        }

        res.json(recipes);

    } catch (err) {
        console.error(err.message);
        res.status(500).json({ error: 'Failed to fetch recipes' });
    }
});