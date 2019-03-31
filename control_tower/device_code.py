from hashlib import sha256


def get_code(device_id):
    hasher = sha256()
    hasher.update(device_id.encode())
    return hasher.hexdigest()
