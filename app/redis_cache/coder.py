# from fastapi_cache import coder

# class JSONEncoder(json.JSONEncoder):
#     """JSON Encoder for Redis caching."""

#     def default(self, obj: Any) -> dict:
#         """Default method to encode."""
#         return jsonable_encoder(obj)


# class JSONCoder(Coder):
#     """JSONCoder for FastAPI_Cache using `jsonable_encoder`."""

#     @classmethod
#     def encode(cls, value: Any) -> str:
#         """Encode an object into a string."""
#         return json.dumps(value, cls=JSONEncoder)

#     @classmethod
#     def decode(cls, value: str) -> dict:
#         """Decode a string into a dictionary."""
#         return json.loads(value)