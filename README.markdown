# MAC Forgery Attack Demonstration

## Overview
This project demonstrates a **Length Extension Attack** on an insecure Message Authentication Code (MAC) implementation. The attack targets a server (`server.py`) that uses a weak MAC construction (`hashlib.md5(SECRET_KEY + message)`). The attacker script (`client.py`) intercepts a valid message and MAC, extends the message with additional data (`&admin=true`), and generates a valid forged MAC without knowing the secret key. The goal is to show that the server accepts the forged message as valid.

## Files
- **`server.py`**: Simulates a server that generates and verifies MACs using an insecure method (`hashlib.md5(SECRET_KEY + message)`).
- **`client.py`**: The attacker script that performs the Length Extension Attack using the `hashpumpy` library.

## Prerequisites
To run this project, you need:
- Python 3.x
- The `hashpumpy` library. Install it using:
  ```
  pip install hashpumpy
  ```

## How the Attack Works
1. **Server Setup**:
   - The server (`server.py`) uses a secret key (`b"supersecretkey"`) and generates a MAC for a message (e.g., `b"amount=100&to=alice"`) using `hashlib.md5(SECRET_KEY + message)`.
   - This method is insecure because MD5 is vulnerable to Length Extension Attacks.

2. **Interception**:
   - The attacker intercepts the message (`b"amount=100&to=alice"`) and its MAC (e.g., `614d28d808af46d3702fe35fae67267c`).

3. **Length Extension Attack**:
   - The attacker uses `hashpumpy` to extend the message by appending `b"&admin=true"`.
   - `hashpumpy` generates a new valid MAC for the extended message without needing the secret key, exploiting the internal state of MD5.

4. **Verification**:
   - The attacker sends the forged message and MAC to the server.
   - The server’s `verify` function accepts the forged message as valid, proving the attack’s success.

## Running the Attack
1. **Run the Server**:
   - Open a terminal and run `server.py` to see the original message and MAC:
     ```
     python server.py
     ```
   - Output example:
     ```
     === Server Simulation ===
     Original message: amount=100&to=alice
     MAC: 614d28d808af46d3702fe35fae67267c
     ...
     ```
   - Copy the MAC (e.g., `614d28d808af46d3702fe35fae67267c`) for use in `client.py`.

2. **Update the Attacker Script**:
   - Open `client.py` and ensure the `intercepted_mac` matches the MAC from `server.py`:
     ```python
     intercepted_mac = "614d28d808af46d3702fe35fae67267c"  # Update this if different
     ```

3. **Run the Attack**:
   - Run `client.py`:
     ```
     python client.py
     ```
   - Expected output:
     ```
     Forged message: b'amount=100&to=alice\x80\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x08\x01\x00\x00\x00\x00\x00\x00&admin=true'
     Forged MAC: <some_new_mac>
     Attack successful! Forged message accepted by server.
     ```
   - The `Attack successful!` message confirms that the server accepted the forged message.

## Why the Attack Succeeds
- The `hashlib.md5(SECRET_KEY + message)` construction is vulnerable because MD5 uses the Merkle-Damgård construction.
- In a Length Extension Attack, the attacker uses the intercepted MAC (the hash’s internal state) to append new data and compute a new valid MAC without knowing the secret key.
- The `hashpumpy` library automates this process by generating the padded extended message and its corresponding MAC.

## Notes
- The forged message contains padding (`\x80\x00\x00...`) added by `hashpumpy` to align with MD5’s block structure. This is normal for Length Extension Attacks.
- The attack only works on `server.py` because it uses a naive MAC construction. A secure implementation (like HMAC) would prevent this attack (see `Sserver.py` for a secure version).

## License
This project is for educational purposes only and is part of a course assignment on Data Integrity and Authentication.