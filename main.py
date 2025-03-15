import hashlib
import json
import time

def has_leading_zero_bits(hash_bytes, zeros):
    count = 0
    for byte in hash_bytes:
        for bit in range(7, -1, -1):
            if (byte >> bit) & 1 == 0:
                count += 1
                if count >= zeros:
                    return True
            else:
                return count >= zeros
    return count >= zeros

def create_block(data, starting_zeros):
    nonce = 0
    timestamp = int(time.time() * 1000)  # В мілісекундах
    while True:
        combined = f"{data}{timestamp}{nonce}".encode()
        hash_bytes = hashlib.sha256(combined).digest()
        hash_hex = hash_bytes.hex()
        if has_leading_zero_bits(hash_bytes, starting_zeros):
            print(f"Found nonce: {nonce} with hash: {hash_hex}")
            break
        nonce += 1
    return {"hash": hash_hex, "data": data, "nonce": nonce, "timestamp": timestamp}

def verify_block(file_path):
    try:
        with open(file_path, "r") as f:
            block = json.load(f)
        computed_hash = hashlib.sha256(f"{block['data']}{block['timestamp']}{block['nonce']}".encode()).hexdigest()
        if computed_hash == block["hash"]:
            print("Block is valid.")
            return True
        else:
            print("Block is invalid.")
            return False
    except Exception as e:
        print(f"Error reading or parsing file: {e}")
        return False

data = "This is a sample block data."
starting_zeros = 16

print("Creating block...")
block = create_block(data, starting_zeros)
print("Block created:", block)

file_path = "block.json"
with open(file_path, "w") as f:
    json.dump(block, f, indent=4)
print(f"Block saved to {file_path}")

print("Verifying block from file...")
verify_block(file_path)
