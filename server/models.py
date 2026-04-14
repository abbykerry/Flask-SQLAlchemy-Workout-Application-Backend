from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
from sqlalchemy import CheckConstraint

# create database instance
db = SQLAlchemy()

#workout model

class Exercise(db.Model):
    __tablename__ = 'exercises'

    id = db.Column(db.Integer, primary_key=True)

    # name of the exercise
    name = db.Column(db.String, nullable=False)

    # category like "strength", "cardio"
    category = db.Column(db.String, nullable=False)

    
    equipment_needed = db.Column(db.Boolean, nullable=False, default=False)# whether equipment is needed (True/False)

    # relationship to join table
    workout_exercises = db.relationship(
        'WorkoutExercise',
        back_populates='exercise',
        cascade='all, delete-orphan'
    )

    # many-to-many relationship with workouts
    workouts = db.relationship(
        'Workout',
        secondary='workout_exercises',
        back_populates='exercises'
    )

    # validation for name
    @validates('name')
    def validate_name(self, key, value):
        if not value or value.strip() == "":
            raise ValueError("Exercise name cannot be empty")
        return value

    # validation for category
    @validates('category')
    def validate_category(self, key, value):
        if not value or len(value) < 2:
            raise ValueError("Category must be at least 2 characters long")
        return value

    # convert Exercise object to dictionary
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "category": self.category,
            "equipment_needed": self.equipment_needed
        }


class Workout(db.Model):
    __tablename__ = 'workouts'

    id = db.Column(db.Integer, primary_key=True)

    # date of the workout
    date = db.Column(db.Date, nullable=False)

    # duration must always exist
    duration_minutes = db.Column(db.Integer, nullable=False)

    notes = db.Column(db.Text)# optional notes

    # relationship to join table
    workout_exercises = db.relationship(
        'WorkoutExercise',
        back_populates='workout',
        cascade='all, delete-orphan'
    )

    # many-to-many relationship with exercises
    exercises = db.relationship(
        'Exercise',
        secondary='workout_exercises',
        back_populates='workouts'
    )

    # validation for duration
    @validates('duration_minutes')
    def validate_duration(self, key, value):
        if value is None or value <= 0:
            raise ValueError("Workout duration must be greater than 0")
        return value

    # convert Workout object to dictionary
    def to_dict(self):
        return {
            "id": self.id,
            "date": str(self.date),
            "duration_minutes": self.duration_minutes,
            "notes": self.notes,
            "exercises": [e.to_dict() for e in self.exercises]
        }


class WorkoutExercise(db.Model):
    __tablename__ = 'workout_exercises'

    id = db.Column(db.Integer, primary_key=True)

    # foreign keys
    workout_id = db.Column(db.Integer, db.ForeignKey('workouts.id'), nullable=False)
    exercise_id = db.Column(db.Integer, db.ForeignKey('exercises.id'), nullable=False)

    # performance data
    reps = db.Column(db.Integer)
    sets = db.Column(db.Integer)
    duration_seconds = db.Column(db.Integer)

    # table constraints for non-negative values
    __table_args__ = (
        CheckConstraint('reps >= 0', name='check_reps_positive'),
        CheckConstraint('sets >= 0', name='check_sets_positive'),
        CheckConstraint('duration_seconds >= 0', name='check_duration_positive'),
    )

    # relationships back to parent models
    workout = db.relationship('Workout', back_populates='workout_exercises')
    exercise = db.relationship('Exercise', back_populates='workout_exercises')

    # validation: ensure at least one metric is provided
    @validates('reps', 'sets', 'duration_seconds')
    def validate_performance(self, key, value):
        if value is not None and value < 0:
            raise ValueError(f"{key} cannot be negative")
        return value

    # convert WorkoutExercise object to dictionary
    def to_dict(self):
        return {
            "id": self.id,
            "workout_id": self.workout_id,
            "exercise_id": self.exercise_id,
            "reps": self.reps,
            "sets": self.sets,
            "duration_seconds": self.duration_seconds
        }