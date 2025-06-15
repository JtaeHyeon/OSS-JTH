from sqlalchemy.types import TypeDecorator, String as StringType

class ListOfString(TypeDecorator):
    impl = StringType
    cache_ok = False

    def process_bind_param(self, value, dialect):
        if value is not None:
            if not isinstance(value, list) or not all(isinstance(item, str) for item in value):
                raise TypeError("Expected a list of strings.")
            return ",".join(value)
        return None

    def process_result_value(self, value, dialect):
        if value is not None:
            return value.split(",")
        return []
