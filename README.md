# Mariner

![Picture of Mariner 4](https://upload.wikimedia.org/wikipedia/commons/thumb/b/bc/Mariner_3_and_4.jpg/520px-Mariner_3_and_4.jpg)

Mariner is a proof of concept Urbit chat client.

When run it needs a ship name, which it assumes is available from https://ship.arvo.network, a +code, and the channel you wish to connect to.
It assumes the channel has already been subscribed. Connecting to a new channel is untested. Use at your own risk, ymmv, I'm not responsible if it eats your dog etc, etc.

You can close it with /quit but note that it won't close until you get another message because of python's threads blocking on socket.recv() in native code. Sorry about that. Patches welcome.
