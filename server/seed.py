from datetime import date

from .app import app
from .models import db, Exercise, Workout, WorkoutExercise


with app.app_context():
    print('Resetting database...')

    db.drop_all()
    db.create_all()

    squat = Exercise(name='Squats', category='Strength', equipment_needed=False)
    pushups = Exercise(name='Push-ups', category='Strength', equipment_needed=False)
    running = Exercise(name='Running', category='Cardio', equipment_needed=False)
    plank = Exercise(name='Plank', category='Core', equipment_needed=False)

    db.session.add_all([squat, pushups, running, plank])
    db.session.commit()

    leg_day = Workout(
        date=date.today(),
        duration_minutes=50,
        notes='Lower body strength training'
    )
    cardio_day = Workout(
        date=date.today(),
        duration_minutes=35,
        notes='Interval running and core work'
    )

    db.session.add_all([leg_day, cardio_day])
    db.session.commit()

    workouts_exercises = [
        WorkoutExercise(workout_id=leg_day.id, exercise_id=squat.id, reps=12, sets=4),
        WorkoutExercise(workout_id=leg_day.id, exercise_id=pushups.id, reps=15, sets=3),
        WorkoutExercise(workout_id=cardio_day.id, exercise_id=running.id, duration_seconds=900),
        WorkoutExercise(workout_id=cardio_day.id, exercise_id=plank.id, duration_seconds=90),
    ]

    db.session.add_all(workouts_exercises)
    db.session.commit()

    print('Database seeded successfully!')
