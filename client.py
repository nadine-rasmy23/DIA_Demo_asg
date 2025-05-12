import hashpumpy
from server import verify  # Import verify from server.py

def perform_attack():
    # Intercepted message and MAC from server.py
    intercepted_message = b"amount=100&to=alice"
    intercepted_mac = "614d28d808af46d3702fe35fae67267c"  # MAC from server.py output
    data_to_append = b"&admin=true"
    key_length = 14  # Length of SECRET_KEY (b"supersecretkey" is 14 bytes)

    # Perform Length Extension Attack
    forged_mac, forged_message = hashpumpy.hashpump(intercepted_mac, intercepted_message, data_to_append, key_length)

    # Print results
    print("Forged message:", forged_message)
    print("Forged MAC:", forged_mac)

    # Verify the forged message and MAC using the server's verify function
    if verify(forged_message, forged_mac):
        print("Attack successful! Forged message accepted by server.")
    else:
        print("Attack failed. Forged message rejected.")

if __name__ == "__main__":
    perform_attack()
