## Golden Balls

### Explanation
Golden Balls was a TV game show where players worked together to earn money for a cashpot while deceiving each other into staying into the game for the longest. This was done through a combination of public and private "balls", each of which contained a certain amount of money. A ball with the word KILLER inside was bad, and should be removed by the players.

### How Does it Work
I am currently using Python with Sockets for this. I have one file for the server and one file for the clients. The server sends the public data to the client and the client can respond with a vote for who to remove.
This currently works quite well as a locally hosted text-based program emulating a childhood classic.

However, I want to improve this. My goal is to use my current fullstack knowledge to port this to a fully visual web application. This will be done with the following steps:
- Convert server.py into a Flask server that handles information and broadcasts it
- Convert client.py into a React.js web app. This may be tricky due to language conversion
- Create another client for a shared screen, similar to a Jackbox Party Pack game
- Convert the whole project from using the basic Sockets library to SocketsIO

These changes will appear on the master branch
