from flask import request, jsonify
from models import db, Exercise, Workout, WorkoutExercise


def register_routes(app):

    @app.route('/')
    def home():
        return {"message": "Workout API is running"}


    # ======================
    # EXERCISES
    # ======================

    @app.route('/exercises', methods=['GET'])
    def get_exercises():
        exercises = Exercise.query.all()

        return jsonify([
            {
                "id": e.id,
                "name": e.name,
                "category": e.category,
                "equipment_needed": e.equipment_needed
            }
            for e in exercises
        ])


    @app.route('/exercises', methods=['POST'])
    def create_exercise():
        data = request.get_json()

        # ✅ Validation
        if not data or not data.get("name") or not data.get("category"):
            return jsonify({"error": "Name and category are required"}), 400

        exercise = Exercise(
            name=data.get("name"),
            category=data.get("category"),
            equipment_needed=data.get("equipment_needed", False)
        )

        db.session.add(exercise)
        db.session.commit()

        return jsonify({
            "id": exercise.id,
            "name": exercise.name,
            "category": exercise.category,
            "equipment_needed": exercise.equipment_needed
        }), 201


    # ======================
    # WORKOUTS
    # ======================

    @app.route('/workouts', methods=['GET'])
    def get_workouts():
        workouts = Workout.query.all()

        return jsonify([
            {
                "id": w.id,
                "date": str(w.date),
                "duration_minutes": w.duration_minutes,
                "notes": w.notes,
                "exercises": [
                    {
                        "id": e.id,
                        "name": e.name,
                        "category": e.category,
                        "equipment_needed": e.equipment_needed
                    }
                    for e in w.exercises
                ]
            }
            for w in workouts
        ])


    @app.route('/workouts', methods=['POST'])
    def create_workout():
        from datetime import datetime

        data = request.get_json()

        # ✅ Validation
        if not data or not data.get("date") or not data.get("duration_minutes"):
            return jsonify({"error": "Date and duration are required"}), 400

        try:
            date = datetime.strptime(data["date"], "%Y-%m-%d").date()
        except ValueError:
            return jsonify({"error": "Invalid date format. Use YYYY-MM-DD"}), 400

        workout = Workout(
            date=date,
            duration_minutes=data.get("duration_minutes"),
            notes=data.get("notes")
        )

        db.session.add(workout)
        db.session.commit()

        return jsonify({
            "id": workout.id,
            "date": str(workout.date),
            "duration_minutes": workout.duration_minutes,
            "notes": workout.notes
        }), 201


    # ======================
    # WORKOUT EXERCISES (JOIN TABLE)
    # ======================

    @app.route('/workout_exercises', methods=['POST'])
    def add_workout_exercise():
        data = request.get_json()

        # ✅ Validation
        if not data or not data.get("workout_id") or not data.get("exercise_id"):
            return jsonify({"error": "workout_id and exercise_id are required"}), 400

        link = WorkoutExercise(
            workout_id=data.get("workout_id"),
            exercise_id=data.get("exercise_id"),
            reps=data.get("reps"),
            sets=data.get("sets"),
            duration_seconds=data.get("duration_seconds")
        )

        db.session.add(link)
        db.session.commit()

        return jsonify({
            "id": link.id,
            "workout_id": link.workout_id,
            "exercise_id": link.exercise_id,
            "reps": link.reps,
            "sets": link.sets,
            "duration_seconds": link.duration_seconds
        }), 201