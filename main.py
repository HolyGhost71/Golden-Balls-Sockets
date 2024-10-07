import random
import socket 
import threading

HEADER = 64
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

# =================== SERVER SHIT ======================

def handle_client(conn, addr, game):

    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            
            if msg.split()[0] == "VOTE1":
                game.guesses.append(msg.split(" ")[1])
                message = f"You have voted for: " + game.player_array[msg.split(" ")[1]]
                conn.send(message.encode(FORMAT))
                if len(game.guesses) == 4:
                    game.remove_player(1)
                    
            if msg.split()[0] == "VOTE2":
                game.guesses.append(msg.split(" ")[1])
                if len(game.guesses) == 4:
                    game.remove_player(2)
            
            if msg == DISCONNECT_MESSAGE:
                connected = False

            print(f"[{addr}] {msg}")      

    conn.close()
        

def start():
    global clients
    clients = []
    game = GoldenBalls()
    
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}\n")
    while True:
        conn, addr = server.accept()
        clients.append(conn)
        thread = threading.Thread(target=handle_client, args=(conn, addr, game))
        thread.start()
        print(f"[NEW CONNECTION] {addr} connected.")
        num = threading.activeCount() - 1
        print(f"[ACTIVE CONNECTIONS] {num}\n")
        if num == 4:
            game.play()


# =================== GAME SHIT ======================


class Player:
    def __init__(self, name):
        self.name = name
        self.balls = []
    
    def add_balls(self, balls_list, num):
        for i in range (num):
            self.balls.append(balls_list.pop())
        
class Bank:
    def __init__(self):
        self.ball_array = open("ball_values.txt").read().split(", ")
        
    def select_balls(self, num):
        balls = []
        for i in range(num):
            balls.append(self.ball_array.pop())
        return balls
    
    def randomize(self):
        random.shuffle(self.ball_array)

class GoldenBalls:
    def __init__(self):
        self.player_array = [Player("James"), Player("Luke"), Player("Emily"), Player("Jack")]
        self.bank = Bank()
        self.bank.randomize()
        self.balls_in_play = ['KILLER', 'KILLER', 'KILLER', 'KILLER'] + (self.bank.select_balls(12))
        random.shuffle(self.balls_in_play)
        self.total = 0
        self.guesses = []
        
    def concat(self, list):
        message = ""
        for w in list:
            message += (str(w) + " ")
        return message
    
    def play(self):

        for i, player in enumerate(self.player_array):
            player.add_balls(self.balls_in_play, 4)
            balls = self.concat(player.balls)
            print(f"{i} | {balls}")
            
        self.show_balls_to_players()

    def round_two(self):
        
        self.repopulate()
        self.balls_in_play.append("KILLER")
        self.balls_in_play += self.bank.select_balls(2)
        random.shuffle(self.balls_in_play)
        print("")
        
        for i, player in enumerate(self.player_array):
            player.add_balls(self.balls_in_play, 5)
            balls = self.concat(player.balls)
            print(f"{i} | {balls}")
           
        self.show_balls_to_players()
        
    def bin_or_win(self):
        
        random.shuffle(self.balls_in_play)
        print("")
        
        for i in range(0,10):
            if i % 2 == 0:
                while True:
                    try:
                        b = int(input("Choose a ball to win: "))
                        if 1 <= b <= len(self.balls_in_play) and self.balls_in_play[b-1] is not None:
                            break
                        
                        print("Invalid input\n")
                            
                    except ValueError:
                        print("Invalid input\n")
                
                select = self.balls_in_play[b-1]
                
                if select == "KILLER":
                    print(f"You have selected the KILLER, total is divided by 10")
                    self.total /= 10
                else:
                    print(f"You add ${select} to your total")
                    self.total += int(select)
                
                self.balls_in_play[b-1] = None
                print(f"Total: {self.total}")
                    
            if i % 2 == 1:
                while True:
                    try:
                        b = int(input("Choose a ball to bin: "))
                        if 1 <= b <= len(self.balls_in_play) and self.balls_in_play[b-1] is not None:
                            break
                        
                        print("Invalid input\n")
                            
                    except ValueError:
                        print("Invalid input\n")
                        
                select = self.balls_in_play[b-1]

                print(f"You binned the {select}")
                self.balls_in_play[b-1] = None
                
            print("")
    
    def remove_player(self, round):
        global clients

        current = 0
        for guess in self.guesses:
            guess = int(guess)
            if guess > current:
                current = guess
                
        self.player_array.remove(self.player_array[current])
        clients.remove(clients[current])
        
        if round == 1:
            self.round_two()
        if round == 2:
            self.bin_or_win
                
    
    def repopulate(self):
        for player in self.player_array:
            for ball in player.balls:
                self.balls_in_play.append(ball)
                player.balls = []
                
                
    def show_balls_to_players(self):
        for i, a_player in enumerate(self.player_array):
            clients[i].send("\n".encode(FORMAT))
            for j, b_player in enumerate(self.player_array):
                if i == j:
                    message = f"Your balls:\t{self.concat(a_player.balls)}\n"
                else:
                    message = f"{b_player.name}'s balls:\t{b_player.balls[0]} {b_player.balls[1]}\n"
                clients[i].send(message.encode(FORMAT))
                
        for client in clients:
            client.send("VOTE".encode(FORMAT))


print("[STARTING] Server is starting...")
start()