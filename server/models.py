from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates

# This is our database object that will be used across the app
db = SQLAlchemy()


# Exercise Model

class Exercise(db.Model):
    __tablename__ = "exercises"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    category = db.Column(db.String, nullable=False)
    equipment_needed = db.Column(db.Boolean, nullable=False)

    # Relationship: one exercise can appear in many workout_exercises
    workout_exercises = db.relationship(
        "WorkoutExercise",
        back_populates="exercise",
        cascade="all, delete-orphan"
    )

    # Model-level validation: ensure name is not empty
    @validates("name")
    def validate_name(self, key, value):
        if not value or len(value.strip()) == 0:
            raise ValueError("Exercise name cannot be empty")
        return value

    # Model-level validation: category must also be valid
    @validates("category")
    def validate_category(self, key, value):
        if not value or len(value.strip()) == 0:
            raise ValueError("Category cannot be empty")
        return value



# Workout Model
class Workout(db.Model):
    __tablename__ = "workouts"

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    duration_minutes = db.Column(db.Integer, nullable=False)
    notes = db.Column(db.Text)

    # Relationship: one workout has many workout_exercises
    workout_exercises = db.relationship(
        "WorkoutExercise",
        back_populates="workout",
        cascade="all, delete-orphan"
    )

    # Relationship: many-to-many through WorkoutExercise
    exercises = db.relationship(
        "Exercise",
        secondary="workout_exercises",
        backref="workouts"
    )

    # Model validation: duration must be positive
    @validates("duration_minutes")
    def validate_duration(self, key, value):
        if value <= 0:
            raise ValueError("Duration must be greater than 0")
        return value


# WorkoutExercise (JOIN TABLE)

class WorkoutExercise(db.Model):
    __tablename__ = "workout_exercises"

    id = db.Column(db.Integer, primary_key=True)

    workout_id = db.Column(db.Integer, db.ForeignKey("workouts.id"), nullable=False)
    exercise_id = db.Column(db.Integer, db.ForeignKey("exercises.id"), nullable=False)

    reps = db.Column(db.Integer)
    sets = db.Column(db.Integer)
    duration_seconds = db.Column(db.Integer)

    # Relationships back to parent tables
    workout = db.relationship("Workout", back_populates="workout_exercises")
    exercise = db.relationship("Exercise", back_populates="workout_exercises")

    # Table constraint validation: reps cannot be negative
    @validates("reps", "sets", "duration_seconds")
    def validate_positive_values(self, key, value):
        if value is not None and value < 0:
            raise ValueError(f"{key} cannot be negative")
        return value