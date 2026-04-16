from marshmallow import Schema, fields, validate, validates_schema, ValidationError


class ExerciseSummarySchema(Schema): #this class defines a summary schema for the Exercise model. 
    id = fields.Int(dump_only=True)
    name = fields.Str(dump_only=True)
    category = fields.Str(dump_only=True)
    equipment_needed = fields.Bool(dump_only=True)


class WorkoutSummarySchema(Schema): #defines summary schema for the workout model.
    id = fields.Int(dump_only=True)
    date = fields.Date(dump_only=True)
    duration_minutes = fields.Int(dump_only=True)
    notes = fields.Str(dump_only=True)


class WorkoutExerciseSchema(Schema): # defines a schema for the WorkoutExercise association table, which represents the many-to-many relationship between workouts and exercises.
    id = fields.Int(dump_only=True)
    workout_id = fields.Int(required=True)
    exercise_id = fields.Int(required=True)
    reps = fields.Int(validate=validate.Range(min=1), allow_none=True)
    sets = fields.Int(validate=validate.Range(min=1), allow_none=True)
    duration_seconds = fields.Int(validate=validate.Range(min=1), allow_none=True)
    exercise = fields.Nested(ExerciseSummarySchema, dump_only=True)
    workout = fields.Nested(WorkoutSummarySchema, dump_only=True)

    # Custom validation method that ensures that at least one of the fields reps, sets, or duration_seconds is provided when creating or updating a WorkoutExercise association. Raises a ValidationError if none is provided.
    @validates_schema
    def validate_workout_exercise_fields(self, data, **kwargs):
        if not any((data.get('reps'), data.get('sets'), data.get('duration_seconds'))):
            raise ValidationError(
                'At least one of reps, sets, or duration_seconds must be provided.',
                '_schema'
            )


class ExerciseSchema(Schema): 
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(min=2))
    category = fields.Str(required=True, validate=validate.Length(min=2))
    equipment_needed = fields.Bool(missing=False)
    workouts = fields.List(fields.Nested(WorkoutSummarySchema), dump_only=True)


class WorkoutSchema(Schema):
    id = fields.Int(dump_only=True)
    date = fields.Date(required=True)
    duration_minutes = fields.Int(required=True, validate=validate.Range(min=1))
    notes = fields.Str(allow_none=True, missing='')
    workout_exercises = fields.List(fields.Nested(WorkoutExerciseSchema), dump_only=True) # Nested field that includes the associated exercises for each workout. Allows clients to see all exercises associated with a workout when retrieving workout data.
