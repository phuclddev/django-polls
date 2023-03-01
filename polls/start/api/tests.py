from jsonschema import Draft202012Validator

schema = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "age": {"type": "number"},
    },
    "required": ["name"],
}

Draft202012Validator.check_schema(schema)
# No output means the schema is valid, otherwise `SchemaError` will be raised.

# Create an instance of the validator using a valid schema.
draft_202012_validator = Draft202012Validator(schema)

instance1={"name": "John", "age": 30}
instance2={"name": "John", "age": '30'}
instance3={"age": 30}

# Use the same instance of the validator to check JSON documents
# against the same schema more efficiently.
x = draft_202012_validator.is_valid(instance1)
print(x)