# Property types
STRING = {"type": "string"}
NUMBER = {"type": "number"}
BOOLEAN = {"type": "boolean"}
ARRAY = {"type": "array"}

# API Schema
question_create_schema = {
    "type": "object",
    "properties": {
        "question_text": STRING,
        "expire_date": STRING,
        "status": BOOLEAN,
        "type": NUMBER,
        "choice": ARRAY
    },
    "required": ["question_text", "expire_date", "status", "type", "choice"],
    "additionalProperties": False
}

question_update_schema = {
    "type": "object",
    "properties": {
        "question_text": STRING,
        "expire_date": STRING,
        "status": BOOLEAN,
        "type": NUMBER,
        "choice": ARRAY
    },
    "required": [],
    "additionalProperties": False
}

vote_schema = {
    "type": "object",
    "properties": {
        "question_id": NUMBER,
        "choice_id": NUMBER
    },
    "required": ["question_id", "choice_id"],
    "additionalProperties": False
}
