FIELD_ERROR = r"\"{}\" field is not set"


def validate_battery_level(data):
    data_fields = ["level", "device_id", "charging"]
    return "\n".join([FIELD_ERROR.format(x) for x in data_fields if x not in data])
