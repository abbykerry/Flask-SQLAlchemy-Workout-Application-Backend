from app import app
from models import db, Exercise, Workout
from datetime import date

def seed_database():
    with app.app_context():
        print("Resetting database...")

        db.drop_all()
        db.create_all()

        print("Creating exercises...")

        squat = Exercise(name="Squats", category="Strength", equipment_needed=False)
        pushups = Exercise(name="Push-ups", category="Strength", equipment_needed=False)
        running = Exercise(name="Running", category="Cardio", equipment_needed=False)

        db.session.add_all([squat, pushups, running])
        db.session.commit()

        print("Creating workout...")

        workout = Workout(
            date=date.today(),
            duration_minutes=60,
            notes="Full body workout session"
        )

        workout.exercises = [squat, pushups, running]

        db.session.add(workout)
        db.session.commit()

        print("Database seeded successfully!")

if __name__ == "__main__":
    seed_database()