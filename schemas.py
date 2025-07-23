from marshmallow import Schema, fields

class PlainStoreSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.String(required=True)


class PlainItemSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.String(required=True)
    price = fields.Float(required=True)
    store_id = fields.String(dump_only=True)

class PlainTagSchema(PlainItemSchema):
    id = fields.Int(dump_only=True)
    name = fields.Str()

class ItemUpdateSchema(Schema):
    id = fields.String()
    price = fields.Float()
    store_id = fields.Int()


class ItemSchema(PlainItemSchema):
    store_id = fields.Int(required=True, load_only=True)
    store = fields.Nested((lambda: PlainStoreSchema()), dump_only=True)
    tags = fields.Nested((lambda: PlainTagSchema()), dump_only=True)

class TagSchema(PlainTagSchema):
    store_id = fields.Int(load_only=True)
    store = fields.Nested((lambda: PlainStoreSchema()), dump_only=True)
    item = fields.Nested((lambda: PlainTagSchema()), dump_only=True)


class StoreSchema(PlainStoreSchema):
    items = fields.Nested((lambda: PlainItemSchema()), dump_only=True)
    tags = fields.Nested((lambda: PlainTagSchema()), dump_only=True)

class ItemsAndTagSchema(PlainTagSchema):
    message = fields.Str()
    items = fields.Nested(ItemSchema)
    tags = fields.Nested(TagSchema)

class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.String(required=True)
    password = fields.String(required=True, load_only=True)


class UserRegisterSchema(Schema):
    email = fields.Email(required=True)



