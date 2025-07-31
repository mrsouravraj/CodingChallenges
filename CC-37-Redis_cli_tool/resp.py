class RESPError(Exception):
    pass

def serialize(data):
    if isinstance(data, list):  # Array
        out = f"*{len(data)}\r\n"
        for item in data:
            out += serialize(item)
        return out
    elif isinstance(data, str):  # Bulk string
        return f"${len(data)}\r\n{data}\r\n"
    elif data is None:
        return "$-1\r\n"
    else:
        raise RESPError("Unsupported data type for serialization")

def deserialize(data):
    if not data:
        raise RESPError("Empty response")

    def parse(index=0):
        if index >= len(data):
            raise RESPError("Unexpected end of input")

        token = data[index]
        index += 1

        if token == "+":
            end = data.find("\r\n", index)
            if end == -1:
                raise RESPError("Malformed simple string")
            return data[index:end], end + 2

        elif token == "-":
            end = data.find("\r\n", index)
            if end == -1:
                raise RESPError("Malformed error message")
            return {"error": data[index:end]}, end + 2

        elif token == ":":
            end = data.find("\r\n", index)
            if end == -1:
                raise RESPError("Malformed integer")
            return int(data[index:end]), end + 2

        elif token == "$":
            end = data.find("\r\n", index)
            if end == -1:
                raise RESPError("Malformed bulk string header")
            length = int(data[index:end])
            index = end + 2
            if length == -1:
                return None, index
            if index + length + 2 > len(data):
                raise RESPError("Bulk string data incomplete")
            return data[index:index+length], index + length + 2

        elif token == "*":
            end = data.find("\r\n", index)
            if end == -1:
                raise RESPError("Malformed array header")
            count = int(data[index:end])
            index = end + 2
            if count == -1:
                return None, index
            array = []
            for _ in range(count):
                if index >= len(data):
                    raise RESPError("Array element missing or incomplete")
                item, index = parse(index)
                array.append(item)
            return array, index

        else:
            raise RESPError(f"Invalid RESP type: {token}")

    result, _ = parse()
    return result

