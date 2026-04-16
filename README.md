# Workout Tracking API

A comprehensive Flask-SQLAlchemy backend API for tracking workouts and exercises with many-to-many relationships, validations, and proper schema serialization.

## Description

This API enables personal trainers and fitness enthusiasts to:
- Create and manage exercises with categories and equipment information
- Track workouts with date, duration, and notes
- Associate exercises with workouts with optional performance metrics (reps, sets, duration)
- Retrieve workouts with nested exercise information
- Retrieve exercises with associated workout history

The application uses Flask for the web framework, SQLAlchemy for ORM, and Marshmallow for schema validation and serialization. All models include comprehensive validations at the table, model, and schema levels.

## Features

- **Exercise Management**: Create, retrieve, and delete exercises with categories and equipment tracking
- **Workout Management**: Create, retrieve, and delete workouts with date and duration
- **Many-to-Many Relationships**: Track exercises within workouts with performance metrics
- **Comprehensive Validations**:
  - Database constraints (NOT NULL, UNIQUE, CHECK)
  - Model validators (datatype validation, length constraints)
  - Schema validators (marshmallow field validation)
- **Error Handling**: Descriptive error messages for validation failures and integrity errors
- **Nested JSON Responses**: Workouts include nested exercise data for single-request access

## Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd Flask-SQLAlchemy-Workout-Application-Backend
   ```

2. **Install dependencies using Pipenv**:
   ```bash
   pipenv install
   pipenv shell
   ```

3. **Initialize the database**:
   ```bash
   flask db upgrade head
   ```

4. **Seed sample data** (optional):
   ```bash
   python -m server.seed
   ```

## Running the Application

Start the development server:
```bash
python app.py
```

The API will be available at `http://localhost:5555`

## API Endpoints

### Exercises

- **GET /exercises** - List all exercises (ordered by name)
  ```bash
  curl http://localhost:5555/exercises
  ```

- **GET /exercises/<id>** - Retrieve a specific exercise with associated workouts
  ```bash
  curl http://localhost:5555/exercises/1
  ```

- **POST /exercises** - Create a new exercise
  ```bash
  curl -X POST http://localhost:5555/exercises \
    -H "Content-Type: application/json" \
    -d '{"name": "Deadlifts", "category": "Strength", "equipment_needed": true}'
  ```

- **DELETE /exercises/<id>** - Delete an exercise and all associations
  ```bash
  curl -X DELETE http://localhost:5555/exercises/1
  ```

### Workouts

- **GET /workouts** - List all workouts (ordered by date, newest first)
  ```bash
  curl http://localhost:5555/workouts
  ```

- **GET /workouts/<id>** - Retrieve a specific workout with nested exercises and performance metrics
  ```bash
  curl http://localhost:5555/workouts/1
  ```

- **POST /workouts** - Create a new workout
  ```bash
  curl -X POST http://localhost:5555/workouts \
    -H "Content-Type: application/json" \
    -d '{"date": "2026-04-16", "duration_minutes": 60, "notes": "Leg day"}'
  ```

- **DELETE /workouts/<id>** - Delete a workout and all associated exercises
  ```bash
  curl -X DELETE http://localhost:5555/workouts/1
  ```

### Workout Exercises (Associations)

- **POST /workout_exercises** - Add an exercise to a workout with metrics
  ```bash
  curl -X POST http://localhost:5555/workout_exercises \
    -H "Content-Type: application/json" \
    -d '{"workout_id": 1, "exercise_id": 1, "reps": 12, "sets": 4}'
  ```

- **POST /workouts/<workout_id>/exercises/<exercise_id>/workout_exercises** - Alternative endpoint to add exercise to workout
  ```bash
  curl -X POST http://localhost:5555/workouts/1/exercises/1/workout_exercises \
    -H "Content-Type: application/json" \
    -d '{"reps": 12, "sets": 4}'
  ```

## Data Models

### Exercise
- `id` (Integer): Primary key
- `name` (String, 150 chars, unique): Exercise name (minimum 2 characters)
- `category` (String, 100 chars): Exercise category (e.g., "Strength", "Cardio", "Core")
- `equipment_needed` (Boolean, default False): Whether equipment is required

### Workout
- `id` (Integer): Primary key
- `date` (Date): Date of the workout
- `duration_minutes` (Integer): Duration in minutes (must be > 0)
- `notes` (Text): Optional notes about the workout

### WorkoutExercise (Join Table)
- `id` (Integer): Primary key
- `workout_id` (Integer, FK): Foreign key to Workout
- `exercise_id` (Integer, FK): Foreign key to Exercise
- `reps` (Integer, optional): Number of repetitions (must be > 0)
- `sets` (Integer, optional): Number of sets (must be > 0)
- `duration_seconds` (Integer, optional): Duration in seconds (must be > 0)

## Validations

### Table Constraints
- Exercise name is unique
- Workout duration must be > 0
- WorkoutExercise reps, sets, duration must be > 0 (if provided)
- All required fields prevent NULL values

### Model Validations
- Exercise name length ≥ 2 characters
- Exercise category is required and non-empty
- Workout duration must be > 0
- Workout date must be a valid date object
- WorkoutExercise metrics must be positive when provided

### Schema Validations
- Exercise name minimum 2 characters
- Workout duration minimum 1 minute
- WorkoutExercise requires at least one metric (reps, sets, or duration_seconds)
- All numeric fields use range validators for positive values

## Example Usage

```bash
# Create an exercise
curl -X POST http://localhost:5555/exercises \
  -H "Content-Type: application/json" \
  -d '{"name": "Squats", "category": "Strength", "equipment_needed": false}'

# Create a workout
curl -X POST http://localhost:5555/workouts \
  -H "Content-Type: application/json" \
  -d '{"date": "2026-04-16", "duration_minutes": 45, "notes": "Leg day"}'

# Add exercise to workout
curl -X POST http://localhost:5555/workout_exercises \
  -H "Content-Type: application/json" \
  -d '{"workout_id": 1, "exercise_id": 1, "reps": 8, "sets": 5}'

# Retrieve workout with exercises
curl http://localhost:5555/workouts/1
```

## Project Structure

```
├── server/
│   ├── __init__.py
│   ├── app.py              # Flask app factory and configuration
│   ├── models.py           # SQLAlchemy models and relationships
│   ├── routes.py           # API endpoints and error handlers
│   ├── schemas.py          # Marshmallow schemas for validation
│   └── seed.py             # Database seeding script
├── migrations/             # Alembic database migrations
├── app.py                  # Entry point
├── Pipfile                 # Project dependencies
├── README.md               # This file
└── .gitignore             # Git ignore rules
```

## Development

Run migrations after model changes:
```bash
flask db migrate -m "Description of changes"
flask db upgrade
```

Access the Flask shell for debugging:
```bash
flask shell
```

## Notes

- The application uses SQLite with a database file at `instance/app.db`
- Cascading deletes are enabled; removing an exercise or workout also removes associations
- Relationships use `viewonly=True` for many-to-many to avoid bidirectional sync issues
- The seed file creates sample data and can be run multiple times safely
