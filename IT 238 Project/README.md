# Running
1. update the `config.py` accordingly.
2. run one of the commands:
```sh
python3 main.py <name> # creates a game lobby where peers can connect
"python3 main.py <name> <server_addr> <server_port> # a peer connects to the given lobby
```
3. Wait for all players to connect. Type `ready` and press enter as soon as everybody is in the lobby.


# Game
The game ends when there is only one player standing. Each player who defeated another player will be awarded 100 points, however, the last player will be declared winner regardless of points.


# Networking
Each node in the P2P network uses UDP as its transport protocol. This is to easily implement both sending and receiving functionalities.
To further improve the fairness/security of the network, the packets sent over the network should be confirmed by the majority.

The current implementation of the network is like this:
* All the tanks and their movement are sent over the network.
* Bullets, on the otherhand, are mostly client-side rendered. Only the starting point and direction of the bullet is sent over the network. The first object hit and flying time is rendered on the client.
* Only the player checks if their own tank hits/collides with a bullet. If it happens, the player sends a score update and a tank remove packet to notify that the player is out of the game. This is problematic because the player might not send the said packets properly.

Confirmation of the packets, such as if the the tank-bullet collision also happened to majority (51% or more) of the peers, is needed in order to update/interpret the valid packets. However, this makes the network vulnerable to the "51% attack" which needs another solution.
