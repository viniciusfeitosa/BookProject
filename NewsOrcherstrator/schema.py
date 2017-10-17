from marshmallow import Schema, fields


class News(Schema):
    title = fields.Str(required=True, max_length=200)
    content = fields.Str(required=True)
    author = fields.Str(required=True, max_length=50)
    created_at = fields.DateTime()
    published_at = fields.DateTime()
    news_type = fields.Str(default="famous")
    tags = fields.List(fields.Str())
