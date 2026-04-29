# User Stories — ByteBite

> **Priority Order**: The stories are listed in the order they should be implemented, from highest to lowest priority.

---

## US-001: User Registration

**As a** new visitor,  
**I want** to create an account with my email and password,  
**So that** I can access the platform and manage my own recipes and meal plans.

### Acceptance Criteria

- A public endpoint `POST /api/v1/auth/register` is available.
- The user provides: `email`, `password`, and optionally `full_name`.
- The password is hashed (bcrypt) before being stored.
- The email must be unique; if it already exists, return a `409 Conflict` error.
- On success, return `201 Created` with the user ID and a success message.
- The new user is stored in the `users` collection.

---

## US-002: Full Recipe CRUD

**As a** logged-in user,  
**I want** to create, view, update, and delete my own recipes,  
**So that** I can manage my personal recipe collection.

### Acceptance Criteria

- `POST /api/v1/recipes` — Create a new recipe with `name`, `ingredients` (list of `ingredient_id` + `quantity`), and optional `references`.
- `GET /api/v1/recipes/` — List all recipes owned by the current user (already exists, maintain).
- `GET /api/v1/recipes/{recipe_id}` — Get a single recipe by ID (only if owned by or shared with the current user).
- `PUT /api/v1/recipes/{recipe_id}` — Update an existing recipe (only the owner).
- `DELETE /api/v1/recipes/{recipe_id}` — Delete a recipe (only the owner).
- All endpoints require authentication.
- Return appropriate HTTP status codes: `200`, `201`, `401`, `403`, `404`.

---

## US-003: Full Ingredient CRUD

**As a** logged-in user,  
**I want** to create, view, update, and delete ingredients,  
**So that** I can maintain the ingredient catalog used across all recipes.

### Acceptance Criteria

- `POST /api/v1/ingredients` — Create a new ingredient with `name` and `category`.
- `GET /api/v1/ingredients/` — List all available ingredients.
- `GET /api/v1/ingredients/{ingredient_id}` — Get a single ingredient by ID.
- `PUT /api/v1/ingredients/{ingredient_id}` — Update an ingredient's name or category.
- `DELETE /api/v1/ingredients/{ingredient_id}` — Delete an ingredient.
- Ingredient names should be unique (case-insensitive).
- Only admin users can create, update, or delete ingredients (ingredient catalog is shared).
- All users can view the ingredient list.
- Return appropriate HTTP status codes: `200`, `201`, `401`, `403`, `404`, `409`.

---

## US-004: List Meal Plans

**As a** logged-in user,  
**I want** to list all my weekly meal plans,  
**So that** I can see my planned weeks in a calendar view and navigate between them.

### Acceptance Criteria

- `GET /api/v1/meal-plans/` — List all meal plans owned by the current user.
- The response is a list of meal plans, each including: `id`, `owner_id`, `year`, `week_number`, and `days` with `lunch_recipe_id` and `dinner_recipe_id`.
- Results are sorted by year and week_number in descending order (most recent first).
- Requires authentication.
- If the user has no meal plans, return an empty list `[]`.

---

## US-005: Get Meal Plan by ID

**As a** logged-in user,  
**I want** to view a specific meal plan by its ID,  
**So that** I can review the details of a particular week.

### Acceptance Criteria

- `GET /api/v1/meal-plans/{meal_plan_id}` — Retrieve a meal plan by ID.
- The meal plan is only accessible by its owner.
- The response includes: `id`, `owner_id`, `year`, `week_number`, and `days` with `lunch_recipe_id` and `dinner_recipe_id`.
- If the meal plan does not exist, return `404 Not Found`.
- If the user is not the owner, return `403 Forbidden`.
- Requires authentication.

---

## US-006: Improved Shopping List Generation

**As a** logged-in user,  
**I want** the shopping list to be grouped by ingredient category and sorted,  
**So that** I can shop more efficiently by going through the store section by section.

### Acceptance Criteria

- The `GET /api/v1/shopping-list/{meal_plan_id}` response now includes a `category` field for each item.
- Items are grouped by category (e.g., "Vegetables & Greens", "Dairy & Eggs", etc.).
- Within each category, items are sorted alphabetically by ingredient name.
- The response structure is updated to return a grouped format:

```json
{
  "meal_plan_id": "uuid",
  "categories": [
    {
      "category": "Vegetables & Greens",
      "items": [
        { "ingredient_id": "uuid", "ingredient_name": "Garlic", "amount": 2, "unit": "CLOVE", "checked": false },
        { "ingredient_id": "uuid", "ingredient_name": "Tomato", "amount": 4, "unit": "UNITS", "checked": false }
      ]
    }
  ]
}
```

- Each item includes a `checked` field (always `false` initially) so that the frontend can implement interactive check-off functionality in the future.
- The endpoint requires authentication and only the owner of the meal plan can access it.
- If the meal plan does not exist, return `404 Not Found`.
- If the user is not the owner, return `403 Forbidden`.
- Existing functionality (consolidating same ingredients across recipes) is preserved.

---

## Future Considerations (Out of Scope for Now)

- Sharing recipes with other users (`invited_users` feature).
- Ingredient exclusion (mark ingredients you already have at home).
- Interactive shopping list: mark items as checked/unchecked (`PATCH /api/v1/shopping-list/{meal_plan_id}/items/{ingredient_id}`).
- Recipe search/filtering by name or ingredient.
