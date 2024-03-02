import hashlib

class encryption:
    def convert(self, data):
        data = hashlib.md5(data.encode())
        data = data.hexdigest()
        return data
