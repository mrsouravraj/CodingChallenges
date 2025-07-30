# Fowler–Noll–Vo hash function
# https://en.wikipedia.org/wiki/Fowler%E2%80%93Noll%E2%80%93Vo_hash_function

def fnv1a_hash(data):
    # FNV-1a constants
    FNV_prime = 0x1000193
    FNV_offset_basis = 0x811c9dc5

    hash_value = FNV_offset_basis

    # Iterate through each byte of the data
    for byte in data.encode('utf-8'):
        hash_value ^= byte  # XOR the byte with the hash
        hash_value *= FNV_prime  # Multiply by the prime
    return hash_value & 0xffffffff  # Return a 32-bit hash


# # Example usage
# hashed_value = fnv1a_hash("Hello, World!")
# print(f"FNV-1a Hash: {hashed_value}")