Communicator - Written by Benjamin Jack Cullen

A Very Powerful Communications Tool - Project in early development.
Security is only as good as the implementation.

Please use with caution and read the code if implementing the Communicator. The Communicator is experimental.

The communicator is not perfect but it is communications freedom.

Communicator is capable of potentially communicating with any IPv4, Domain Name, IPv6 and MAC addresses
running and or not running a Communicator, this makes the Communicator very powerful. Use wisely.

The Communicator is a very powerful Communications Tool. The Communicator is not a place to meet people, it not a
chat lobby or meeting place and is certainly not a chat app.

Communicate with Machines and Humanoids. MAC support. Test A smart device that
supports wake on lan. Chinese encoded with utf-16, using af.inet, sock.dgram, and correct socket options
￿￿￿呰蒴︠呰蒴︠呰蒴︠呰蒴︠呰蒴︠呰蒴︠呰蒴︠呰蒴︠呰蒴︠呰蒴︠呰蒴︠呰蒴︠呰蒴︠呰蒴︠呰蒴︠呰蒴︠
This example is how you would wake up a device. Be careful or you can break all the things, borg queen style.

Communicator Standard Communication:
1. Messages encrypted with AES-256 32 bytes shared key.
2. Messages contain encrypted shared fingerprint and encrypted message. Key's are not transmitted by the
communicator and to read the 32x32 bytes fingerprint contained in a Communicator Standard Communication message you
will need the key.
3. The key is intended to make the communication more secure and the fingerprint is intended to provide some
reasonable assurance that you know who the sender is.
4. Fingerprint contained in AES-256 encrypted message is used to help assure you of the identity of the sender.
5. To send a Standard Communicator Communication use the Communicator. First a 32 character key and a 32x32 (1024)
character fingerprint must be generated and shared between the intended sender and recipient. It is strongly advised
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
3. Amber notification is for Communicator Non-Standard Communication received. Potentially insecure message received
or key/fingerprint not found for message.


Key Trust Logic:
The Key Trust logic. A scenario involving two people and a stranger.
1. Person 1 creates a key and fingerprint for person 1 and person 2 to use.
2. Person 1 shares the key and fingerprint with person 2.
3. Person 2 could break the trust and share the key and fingerprint with the stranger however now the only person
who can be impersonated is person 2, which person 2 might likely not want.
4. If person 2 still went ahead and shared the key and fingerprint then not only can stranger (and anyone else who
now has the key and fingerprint) pretend to be person 2, they can also decrypt BOTH person 1 AND person 2's messages,
which is in neither persons favour.
5. Share a different key and fingerprint for each contact in the address book.


DOS & DDOS Protection Framework:
1. Easily Tunable Communicator Anti-DOS & Anti-DDOS Framework provides a certain level of protection.
2. Testing for DOS proves working. DDOS remains untested.


Uplink (A Central serverless design):
Scenario. A scenario involving 2 Communicators.
Communicator A's public IP address changes and so Communicator A sends Communicator B the new IP. Providing
both communicator A and Communicator B's IP's do not change at the same time then the uplink should be successful.
If Communicator B's IP changed at the same time then Communicator A will not know. This means you should be aware that
Communicator A would send an encrypted message containing the fingerprint and new IP to an unknown new occupier of
Communicator B's old IP.
Communicator can uplink public ip changes per address book entry. Please note that to use uplink, the address book
entry should contain a key and fingerprint so that the recipient can identify the sender and for security
measures. There is also a global Uplink switch to enable/disable Uplink entirely.
Uplink feature experimental and in development. My challenge to myself is central serverless com tool.


UPNP:
The router. Communicator intends to use a router to obtain public IP address via UPNP. This requires UPNP be enabled
on the router. This is to avoid using a '3rd person' to obtain the public IP address of your equipment.
Root Description File. The root description xml file may change across rebooting the router. The Communicator is
designed to handle this by enumerating/re-enumerating the router automatically under certain circumstances in order
to continue using the correct root description file url for UPNP communication with the router.

MECHANIZED TRANSMISSION:
Dynamically multi-plexed mechanization.
The Communicator is in the early stages of its mechanized transmit feature. This feature is intended to be a friendly
feature and I do not in any way condone weaponizing the Communicator but it is possible that the Communicator can
even attack itself if configured too. The Communicator is intended to be an extremely versatile, dynamic and flexible
communications tool capable of a wide variety if not infinite applications.
Mechanization allows for an infinite amount of things to be done to an infinite amount of things simultanioulsy,
specifically and potentially extremely quickly.

OMEGA DECODER:
A tactical decoder for humans for responses and other incoming bytes. (Expensive).

Aesthetic:
Aesthetic purely functional.

If you poke around in the dark, you might poke a bear. Please use with caution and treat as experimental.


Python version - 3.10.3
Platform - Developed on Windows 10.

Pycrypto Installation:
1. If encounter error: error: command 'C:\\Program Files\\Microsoft Visual Studio\\2022\\Professional\\VC\\Tools\\MSVC\\14.31.31103\\bin\\HostX86\\x64\\cl.exe' failed with exit code 2
2. In Admin CMD Run: (adjust path according to your MVS version)
"C:\Program Files\Microsoft Visual Studio\2022\Professional\VC\Auxiliary\Build\vcvarsx86_amd64.bat"
3. Then Run: (adjust path according to your MVS version)
set CL=-FI"%VCINSTALLDIR%Tools\MSVC\14.16.27023\include\stdint.h
4. Then pip install pycrypto.
