#!/usr/bin/env python3

from app import app
from models import db, Exercise, Workout, WorkoutExercise
from datetime import date

# This script resets the database and adds fresh sample data
# It helps us test relationships and confirm everything works correctly

with app.app_context():

    # Clear existing data to avoid duplicates when reseeding
    WorkoutExercise.query.delete()
    Workout.query.delete()
    Exercise.query.delete()

    # Create sample exercises
    squat = Exercise(
        name="Squats",
        category="Strength",
        equipment_needed=False
    )

    pushups = Exercise(
        name="Push-ups",
        category="Strength",
        equipment_needed=False
    )

    running = Exercise(
        name="Running",
        category="Cardio",
        equipment_needed=False
    )

    # Create a sample workout
    workout1 = Workout(
        date=date.today(),
        duration_minutes=60,
        notes="Full body workout session"
    )

    # Add everything to the session
    db.session.add_all([squat, pushups, running, workout1])
    db.session.commit()

    # Link exercises to workout using the join table
    we1 = WorkoutExercise(
        workout_id=workout1.id,
        exercise_id=squat.id,
        sets=4,
        reps=12,
        duration_seconds=None
    )

    we2 = WorkoutExercise(
        workout_id=workout1.id,
        exercise_id=pushups.id,
        sets=3,
        reps=15,
        duration_seconds=None
    )

    we3 = WorkoutExercise(
        workout_id=workout1.id,
        exercise_id=running.id,
        sets=None,
        reps=None,
        duration_seconds=900
    )

    db.session.add_all([we1, we2, we3])
    db.session.commit()

    print("Database seeded successfully")