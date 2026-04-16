from datetime import date

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates


db = SQLAlchemy()


class WorkoutExercise(db.Model):
    __tablename__ = 'workout_exercises'
    __table_args__ = (
        db.UniqueConstraint('workout_id', 'exercise_id', name='uix_workout_exercise'),
        db.CheckConstraint('(reps > 0) OR (reps IS NULL)', name='check_reps_positive'),
        db.CheckConstraint('(sets > 0) OR (sets IS NULL)', name='check_sets_positive'),
        db.CheckConstraint('(duration_seconds > 0) OR (duration_seconds IS NULL)', name='check_duration_seconds_positive'),
    )

    id = db.Column(db.Integer, primary_key=True)
    workout_id = db.Column(db.Integer, db.ForeignKey('workouts.id', ondelete='CASCADE'), nullable=False)
    exercise_id = db.Column(db.Integer, db.ForeignKey('exercises.id', ondelete='CASCADE'), nullable=False)
    reps = db.Column(db.Integer)
    sets = db.Column(db.Integer)
    duration_seconds = db.Column(db.Integer)

    workout = db.relationship('Workout', back_populates='workout_exercises')
    exercise = db.relationship('Exercise', back_populates='workout_exercises')

    @validates('reps', 'sets', 'duration_seconds')
    def validate_positive_numbers(self, key, value):
        if value is not None and value <= 0:
            raise ValueError(f'{key} must be greater than 0')
        return value


class Workout(db.Model):
    __tablename__ = 'workouts'
    __table_args__ = (
        db.CheckConstraint('duration_minutes > 0', name='check_workout_duration_positive'),
    )

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    duration_minutes = db.Column(db.Integer, nullable=False)
    notes = db.Column(db.Text, nullable=True)

    workout_exercises = db.relationship(
        'WorkoutExercise',
        back_populates='workout',
        cascade='all, delete-orphan',
        passive_deletes=True,
    )

    exercises = db.relationship(
        'Exercise',
        secondary='workout_exercises',
        back_populates='workouts',
        viewonly=True,
    )

    @validates('duration_minutes')
    def validate_duration(self, key, value):
        if value is None or value <= 0:
            raise ValueError('duration_minutes must be greater than 0')
        return value

    @validates('date')
    def validate_date(self, key, value):
        if not isinstance(value, date):
            raise ValueError('date must be a valid date object')
        return value


class Exercise(db.Model):
    __tablename__ = 'exercises'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False, unique=True)
    category = db.Column(db.String(100), nullable=False)
    equipment_needed = db.Column(db.Boolean, nullable=False, default=False)

    workout_exercises = db.relationship(
        'WorkoutExercise',
        back_populates='exercise',
        cascade='all, delete-orphan',
        passive_deletes=True,
    )

    workouts = db.relationship(
        'Workout',
        secondary='workout_exercises',
        back_populates='exercises',
        viewonly=True,
    )

    @validates('name')
    def validate_name(self, key, value):
        if not value or len(value.strip()) < 2:
            raise ValueError('name must be at least 2 characters long')
        return value.strip()

    @validates('category')
    def validate_category(self, key, value):
        if not value or not value.strip():
            raise ValueError('category is required')
        return value.strip()
