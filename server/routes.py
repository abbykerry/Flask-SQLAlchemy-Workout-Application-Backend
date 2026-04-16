from flask import request, jsonify, abort
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError # Importing IntegrityError to handle database integrity issues, such as unique constraint violations

from .models import db, Exercise, Workout, WorkoutExercise
from .schemas import ExerciseSchema, WorkoutSchema, WorkoutExerciseSchema

# This function defines the API routes for the workout application, eg error handlers and CRUD operations for exercises and workouts.
# Uses Marshmallow for data validation and serialization, and SQLAlchemy for database interactions. 
def register_routes(app):
    exercise_schema = ExerciseSchema()
    exercises_schema = ExerciseSchema(many=True)
    workout_schema = WorkoutSchema()
    workouts_schema = WorkoutSchema(many=True)
    workout_exercise_schema = WorkoutExerciseSchema()

    @app.errorhandler(ValidationError)
    def handle_validation_error(error):
        return jsonify({'errors': error.messages}), 400

    @app.errorhandler(IntegrityError)
    def handle_integrity_error(error):
        db.session.rollback() # Roll back the session to prevent it from being in an inconsistent state after an integrity error
        message = 'Database integrity error.'
        if 'UNIQUE constraint failed: exercises.name' in str(error):
            message = 'Exercise name must be unique.'
        if 'uix_workout_exercise' in str(error): # Checking for the unique constraint violation on the workout_exercises association table. If this error occurs, it means that the same exercise is being added to the same workout more than once.
            message = 'This exercise is already attached to the workout.'
        return jsonify({'error': message}), 400

    @app.errorhandler(404)
    def handle_not_found(error):
        return jsonify({'error': 'Resource not found.'}), 404

    @app.errorhandler(400)
    def handle_bad_request(error):
        description = getattr(error, 'description', 'Bad request.')
        return jsonify({'error': description}), 400

    @app.route('/')
    def home():
        return jsonify({'message': 'Workout API is running'})

    @app.route('/exercises', methods=['GET'])
    def get_exercises():
        exercises = Exercise.query.order_by(Exercise.name).all()
        return jsonify(exercises_schema.dump(exercises)), 200

    @app.route('/exercises/<int:exercise_id>', methods=['GET'])
    def get_exercise(exercise_id):
        exercise = Exercise.query.get_or_404(exercise_id)
        return jsonify(exercise_schema.dump(exercise)), 200

    @app.route('/exercises', methods=['POST'])
    def create_exercise():
        json_data = request.get_json()
        if not json_data:
            abort(400, description='Request body must be JSON.')

        payload = exercise_schema.load(json_data)
        exercise = Exercise(**payload)
        db.session.add(exercise)
        db.session.commit()
        return jsonify(exercise_schema.dump(exercise)), 201

    @app.route('/exercises/<int:exercise_id>', methods=['DELETE'])
    def delete_exercise(exercise_id):
        exercise = Exercise.query.get_or_404(exercise_id)
        db.session.delete(exercise)
        db.session.commit()
        return jsonify({'message': 'Exercise deleted successfully.'}), 200

    @app.route('/workouts', methods=['GET'])
    def get_workouts():
        workouts = Workout.query.order_by(Workout.date.desc()).all()
        return jsonify(workouts_schema.dump(workouts)), 200

    @app.route('/workouts/<int:workout_id>', methods=['GET'])
    def get_workout(workout_id):
        workout = Workout.query.get_or_404(workout_id)
        return jsonify(workout_schema.dump(workout)), 200

    @app.route('/workouts', methods=['POST'])
    def create_workout():
        json_data = request.get_json()
        if not json_data:
            abort(400, description='Request body must be JSON.')

        payload = workout_schema.load(json_data)
        workout = Workout(**payload)
        db.session.add(workout)
        db.session.commit()
        return jsonify(workout_schema.dump(workout)), 201

    @app.route('/workouts/<int:workout_id>', methods=['DELETE'])
    def delete_workout(workout_id):
        workout = Workout.query.get_or_404(workout_id)
        db.session.delete(workout)
        db.session.commit()
        return jsonify({'message': 'Workout deleted successfully.'}), 200

    @app.route('/workout_exercises', methods=['POST'])
    def add_workout_exercise():
        json_data = request.get_json()
        if not json_data:
            abort(400, description='Request body must be JSON.')

        payload = workout_exercise_schema.load(json_data)
        Workout.query.get_or_404(payload['workout_id'])
        Exercise.query.get_or_404(payload['exercise_id'])

        association = WorkoutExercise(**payload) # **payload unpacks the validated data from the request and passes it as keyword arguments to the WorkoutExercise constructor.
        db.session.add(association)
        db.session.commit()
        return jsonify(workout_exercise_schema.dump(association)), 201

    @app.route('/workouts/<int:workout_id>/exercises/<int:exercise_id>/workout_exercises', methods=['POST'])
    def add_exercise_to_workout(workout_id, exercise_id):
        json_data = request.get_json() or {}
        Workout.query.get_or_404(workout_id)
        Exercise.query.get_or_404(exercise_id)

        json_data['workout_id'] = workout_id
        json_data['exercise_id'] = exercise_id
        payload = workout_exercise_schema.load(json_data) 

        association = WorkoutExercise(**payload)
        db.session.add(association)
        db.session.commit()
        return jsonify(workout_exercise_schema.dump(association)), 201
