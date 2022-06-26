# communicator
communicator intends to provide communication between two or more communicator applications running over loopback, local network and world wide web (www requires port forwarding from router to local ip address of host running the communicator). 

-- project in early development :) You have been warned.

-- provides communicator to communicator communication without a honey pot server in between like many social media platforms.

-- two communicators provided. copy and paste communicator onto any compatible machine to create more communicators.

-- upcoming: encryption, address book and extra features.

-- added encryption. if no key is specified in address book then a default key is used.

-- share one key per contact. in address book contact saves key as you, you save key as contact.

SERVER:
listens for incoming connections and if receives a message will try each key including the default communicator key as a dictionary attack function on the encrypted message. if the message is decrypted then the name associated with the key that was successful in decrypting the message will be used to identify the message sender alongside a sender fingerprint header inside the message. Now you can read the message and have reasonable assurance the sender name is authentic.

Communicator - Written by Benjamin Jack Cullen

Communicator Standard Communication:
    1. Messages encrypted with AES-256 32 bytes shared key.
    2. Messages contain encrypted shared fingerprint and encrypted message. Key's are not transmitted by the
    communicator and to read the 32x32 bytes fingerprint contained in a Communicator Standard Communication message you
    will need the key.
    3. The key is intended to make the communication more secure and the fingerprint is intended to provide some
    reasonable assurance that you know who the sender is.
    4. Fingerprint contained in AES-256 encrypted message is used to help assure you of the identity of the sender.
    5. To send a Standard Communicator Communication use the Communicator. First a 32 character key and a 32x32 (1024)
    character fingerprint must be generated and shared between the intended sender and recipient. It is strongly      advised
    to share a different key and fingerprint between each sender and recipient. This way you have a reasonable assurance
    that you know who is communicating with you regardless of IP address and regardless of any other data.
    6. The Communicator Server Data Handler performs dictionary attacks on incoming messages over 1024 bytes in order
    to try and decrypt the message thereby identifying the sender and enabling the message to be read. This requires
    the address book is properly configured.
    7. The above comprises much of the Communicator Standard Communication.
    8. It is also recommended sharing the key and fingerprint offline.
    9. Green notification is for message delivered and Communicator Standard Communication received.


Communicator Non-Standard Communication:
    1. The communicator filters any incoming message below 1024 bytes away from the decryption function, this among
    other reasons allows a 'Communicator Non-Standard Communication' which allows for things like plain text to be sent
    up to 1024 bytes and be received and receive notification.
    2. Great for emergencies as this will not require a key or fingerprint however the communication will be insecure.
    3. Amber notification is for Communicator Non-Standard Communication received. (Potentially insecure message received).
