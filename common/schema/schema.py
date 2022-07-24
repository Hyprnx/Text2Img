SCHEMA_NEWS = {
    "$schema": "http://json-schema.org/draft-04/schema#",
    "type": "object",
    "properties": {
        "source": {
            "type": 'string'
        },
        "title": {
            "type": 'string'
        },
        "sapo": {
            "type": 'string'
        },
        "body": {
            "type": 'string'
        },
        "id": {
            "type": 'number'
        },
        "publish": {
            "type": 'string',
            "format": "date"
        },
        "tags": {
            "type": 'array',
            "items": {
                "type": "string"
            }
        },
        "keywords": {
            "type": 'array',
            "items": {
                "type": "string"
            }
        },
        "cates": {
            "type": 'array',
            "items": {
                "type": "string"
            }
        },

    },
    "required": [
        "source",
        "title",
        "body",
        "sapo",
        "id",
        "publish",
        "tags",
        "keywords",
        "cates"
    ],
    "additionalProperties": False
}