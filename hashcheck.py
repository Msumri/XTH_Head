import hashlib

# Function to calculate hash of a file
def calculate_file_hash(file_path, hash_algorithm='sha256', chunk_size=4096):
    # Select the hash algorithm (default is SHA-256)
    hash_func = hashlib.new(hash_algorithm)
    
    # Open the file in binary mode
    with open(file_path, 'rb') as file:
        # Read the file in chunks to avoid loading the entire file into memory
        while chunk := file.read(chunk_size):
            hash_func.update(chunk)
    
    # Return the hash value in hexadecimal format
    return hash_func.hexdigest()





if __name__ == '__main__':
    calculate_file_hash()