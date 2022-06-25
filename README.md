# communicator
communicator intends to provide communication between two or more communicator applications running over loopback, local network and world wide web (www requires port forwarding from router to local ip address of host running the communicator). 

-- project in early development --> zero security (no SSL, no keys, nothing! :) You have been warned.

-- provides communicator to communicator communication without a honey pot server in between like many social media platforms.

-- two communicators provided. copy and paste communicator onto any compatible machine to create more communicators.

-- upcoming: encryption, address book and extra features.

-- added encryption. if no key is specified in address book then a default key is used.

-- ONLY keys in address book are used to attempt identity recognition.

-- share one key per contact. in address book contact saves key as you, you save key as contact.

-- share your key = share your identity...

SERVER:
listens for incoming connections and if receives a message will try each key including the default communicator key as a dictionary attack function on the encrypted message. if the message is decrypted then the name associated with the key that was successful in decrypting the message will be used to identify the message sender.

1. create and share a key with ONE contact.

2. add name + ip + port + key to adress book (for you name is name of contact and for contact name is name of you! but same key)

