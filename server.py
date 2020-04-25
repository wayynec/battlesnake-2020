import os
import random
import cherrypy

import math
import time  # added

"""
This is a simple Battlesnake server written in Python.
For instructions see https://github.com/BattlesnakeOfficial/starter-snake-python/README.md
"""


# Rules: 0=available space, 1=snake body, 2=Food, 3=head, 4= Bigger enemy's head
# 5 = smaller head

class Battlesnake(object):
    @cherrypy.expose
    def index(self):
        # If you open your snake URL in a browser you should see this message.
        return "Your Battlesnake is alive!"

    @cherrypy.expose
    def ping(self):
        # The Battlesnake engine calls this function to make sure your snake is working.
        return "pong"

    @cherrypy.expose
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def start(self):
        # This function is called everytime your snake is entered into a game.
        # cherrypy.request.json contains information about the game that's about to be played.
        # TODO: Use this function to decide how your snake is going to look on the board.
        data = cherrypy.request.json
        print("START")
        return {"color": "#736CCB", "headType": "silly", "tailType": "bolt"}

    # ---------------------------------------------------------------------
    # Function priority moves: Retruns priority movement
    # flag = 0 need prob.
    def priority(self, matrix, head, possible_moves, height, width, flag):

        priority_moves = ["up", "down", "left", "right"]
        # check if the distance between my head and enemy's head (=4) is =< 2

        # enemy is at the right within range 2. head[0] is height, head[1] is width
        # head[1]+2 =>col +2
        if head[1] + 2 <= width - 1 and matrix[head[0]][head[1] + 2] == 4:
            priority_moves.remove("right")

        if head[1] - 2 >= 0 and matrix[head[0]][head[1] - 2] == 4:
            priority_moves.remove("left")

        if head[0] + 2 <= height - 1 and matrix[head[0] + 2][head[1]] == 4:
            priority_moves.remove("down")

        if head[0] - 2 >= 0 and matrix[head[0] - 2][head[1]] == 4:
            priority_moves.remove("up")

        print("priority_moves=", priority_moves)

        # match possible moves and priority moves.

        # avoid nessy, blind spot
        avoid = []
        if head[1] + 1 <= width - 1 and head[0] - 1 >= 0 and matrix[head[0] - 1][head[1] + 1] == 4:  # row-1, col+1
            # avoid.append("up")
            # avoid.append("right")
            avoid.append("left")
            avoid.append("down")
        if head[1] - 1 >= 0 and head[0] - 1 >= 0 and matrix[head[0] - 1][head[1] - 1] == 4:
            # avoid.append("top")
            # avoid.append("left")
            avoid.append("down")
            avoid.append("right")
        if head[1] - 1 >= 0 and head[0] + 1 <= height - 1 and matrix[head[0] + 1][head[1] - 1] == 4:
            # avoid.append("left")
            # avoid.append("down")
            avoid.append("right")
            avoid.append("up")
        if head[1] + 1 <= width - 1 and head[0] + 1 <= height - 1 and matrix[head[0] + 1][head[1] + 1] == 4:
            # avoid.append("right")
            # avoid.append("down")
            avoid.append("left")
            avoid.append("up")
        # debug
        print("Avoid: ", avoid)

        if( len(list(set(possible_moves) & set(priority_moves))) > 0 ):# then
            combined_move = list(set(possible_moves) & set(priority_moves))

        if (len(list(set(combined_move) & set(avoid))) > 0):  # then
            combined_move = list(set(combined_move) & set(avoid))

        if flag == 0:
            # avoid eating food when health > 50
            if len(combined_move) > 1:  # at least we have two choice.
                print("combined move in avoid eating food: ", combined_move, "len: ", len(combined_move))
                for i in range(len(combined_move)):
                    if combined_move[i] == "up":
                        if head[0] - 1 >= 0 and matrix[head[0] - 1][head[1]] == 2:
                            combined_move.remove("up")
                            print("call combined_move remove up")
                            break

                    elif combined_move[i] == "down":
                        if head[0] + 1 <= height - 1 and matrix[head[0] + 1][head[1]] == 2:
                            combined_move.remove("down")
                            print("call combined_move remove down")
                            break
                    elif combined_move[i] == "right":
                        if head[1] + 1 <= width - 1 and matrix[head[0]][head[1] + 1] == 2:
                            combined_move.remove("right")
                            print("call combined_move remove right")
                            break

                    elif combined_move[i] == "left":
                        if head[1] - 1 >= 0 and matrix[head[0]][head[1] - 1] == 2:
                            combined_move.remove("left")
                            print("call combined_move remove left")
                            break
                print("combined move in avoid eating food(after): ", combined_move)

        ####Prob start####
        if flag == 0:
            # choose the best move from combined_move
            number_of_0 = 0
            for row in range(height // 2):
                for col in range(width // 2):  # Upper left
                    if (matrix[row][col] not in [1, 4]):
                        number_of_0 += 1
            ratio1 = number_of_0 / ((height // 2) * (width // 2))

            number_of_0 = 0
            for row in range(height // 2):
                for col in range(width // 2, width):  # Upper right
                    if (matrix[row][col] not in [1, 4]):
                        number_of_0 += 1
            ratio2 = number_of_0 / ((height // 2) * (width - width // 2))

            number_of_0 = 0
            for row in range(height // 2, height):
                for col in range(width // 2):  # Lower left
                    if (matrix[row][col] not in [1, 4]):
                        number_of_0 += 1
            ratio3 = number_of_0 / ((height - height // 2) * (width // 2))

            number_of_0 = 0
            for row in range(height // 2, height):
                for col in range(width // 2, width):  # Lower right
                    if (matrix[row][col] not in [1, 4]):
                        number_of_0 += 1
            ratio4 = number_of_0 / ((height - height // 2) * (width - width // 2))

            list_ratio = [ratio1, ratio2, ratio3, ratio4]
            list_ratio.sort()

            # debug
            best_cordinate = (0, 0)
            if (max(list_ratio) == ratio1):
                print("best ratio is:", "ratio1")
                best_cordinate = (0, 0)
            elif (max(list_ratio) == ratio2):
                print("best ratio is:", "ratio2")
                best_cordinate = (0, width - 1)
            elif (max(list_ratio) == ratio3):
                print("best ratio is:", "ratio3")
                best_cordinate = (height - 1, 0)
            else:
                print("best ratio is:", "ratio4")
                best_cordinate = (height - 1, width - 1)

            # compute distance of each possible moves?
            # From combined_move, We want corner_dist =[left:1000, right:1000]
            corner_dist = [100] * len(combined_move)  # between each combined_move

            for i in range(len(combined_move)):
                if (combined_move[i] == "right"):  # head[1] is width
                    corner_dist[i] = abs(best_cordinate[1] - (head[1] + 1)) + abs(best_cordinate[0] - (head[0]))
                elif (combined_move[i] == "left"):  # head[1] is width
                    corner_dist[i] = abs(best_cordinate[1] - (head[1] - 1)) + abs(best_cordinate[0] - (head[0]))
                elif (combined_move[i] == "up"):  # head[0] is height
                    corner_dist[i] = abs(best_cordinate[1] - (head[1])) + abs(best_cordinate[0] - (head[0] - 1))
                elif (combined_move[i] == "down"):  # head[0] is height
                    corner_dist[i] = abs(best_cordinate[1] - (head[1])) + abs(best_cordinate[0] - (head[0] + 1))
            # find shortest
            min = 100
            min_move = ""
            for i in range(len(combined_move)):
                if min > corner_dist[i]:
                    # corner_dist and combined_move have same order
                    min = corner_dist[i]
                    min_move = combined_move[i]

            # debug
            print("combined_move=", combined_move)
            print("corner_dist=", corner_dist)

            move = min_move
        ################End of Prob########
        else:
            move = combined_move

        return move

    # ---------------------------------------------------------------------

    @cherrypy.expose
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def move(self, possible_move=None):

        # This function is called on every turn of a game. It's how your snake decides where to move.
        # Valid moves are "up", "down", "left", or "right".
        # TODO: Use the information in cherrypy.request.json to decide your next move.
        data = cherrypy.request.json

        # Choose a random direction to move in
        # possible_moves = ["up", "down", "left", "right"]
        # move = random.choice(possible_moves)

        # add my code--------------------------------------------
        # debug (delete later)
        print("turn: ", data["turn"])

        start_time = time.time()

        # board info
        height = data["board"]["height"]
        width = data["board"]["width"]

        # Create Adjacency Matrix
        matrix = [0] * (width)
        for i in range(width):
            matrix[i] = [0] * (height)

        # Input my snake location into matrix
        for i in range(len(data["you"]["body"])):  # body[i]=head, body, or tail...
            x = data["you"]["body"][i]["x"]
            y = data["you"]["body"][i]["y"]
            matrix[y][x] = 1

        # get my_size
        my_size = len(data["you"]["body"])

        # Input "other" snakes location into matrix
        for i in range(len(data["board"]["snakes"])):  # body[i]=[x,y]
            # j is head, body, or tail...by index

            # get enemy's size
            size = len(data["board"]["snakes"][i]["body"])

            for j in range(len(data["board"]["snakes"][i]["body"])):

                x = data["board"]["snakes"][i]["body"][j]["x"]
                y = data["board"]["snakes"][i]["body"][j]["y"]

                if j == 0 and my_size <= size:  # j == 0 means head
                    matrix[y][x] = 4

                elif j == 0 and my_size > size:  # j == 0 means head
                    matrix[y][x] = 5


                else:
                    if data["turn"] > 0:
                        matrix[y][x] = 1

        # Input food location into matrix
        food = []
        for i in range(len(data["board"]["food"])):  # food[i]=[x,y]
            x = data["board"]["food"][i]["x"]
            y = data["board"]["food"][i]["y"]
            food.append([y, x])
            matrix[y][x] = 2

        # get head
        x = data["you"]["body"][0]["x"]
        y = data["you"]["body"][0]["y"]
        matrix[y][x] = 3
        head = (y, x)

        # get health
        h = data["you"]["health"]
        load_factor = 0  # load factor = 0 when health > 50
        if h < 200:
            load_factor = 1
        # head.append(x) #now, head=[row, col]
        shortest = 100
        s_food = None
        for item in food:  # items are tuples
            path = abs(head[0] - item[0]) + abs(head[1] - item[1])
            item.append(path)
            # if shortest > path:
            #   shortest = path
            #   s_food = item
        food.sort(key=lambda x: (x[2]))  # sort the array using food[2](shortest path)
        # print("s_food =", s_food, "shortest path = ", shortest)
        print(food)
        print("health: ", h)  # print health
        print("load factor: ", load_factor)

        # debug
        print("------matrix------")
        for line in matrix:
            print(line)

        if load_factor == 1:

            possible_moves = []

            if head[0] - 1 >= 0 and matrix[head[0] - 1][head[1]] not in [1, 4]:
                possible_moves.append("up")

            if head[0] + 1 <= height - 1 and matrix[head[0] + 1][head[1]] not in [1, 4]:
                possible_moves.append("down")

            if head[1] - 1 >= 0 and matrix[head[0]][head[1] - 1] not in [1, 4]:
                possible_moves.append("left")

            if head[1] + 1 <= width - 1 and matrix[head[0]][head[1] + 1] not in [1, 4]:
                possible_moves.append("right")
            print("possible_moves=", possible_moves)

            if head[1] < food[0][1] and (matrix[head[0]][head[1] + 1] != 1):  # that means head is left side of food.
                movement = "right"
                move = self.priority(matrix, head, possible_moves, height, width, load_factor)
                print("move: ", move)
                if movement in move:
                    move = movement
                else:
                    move = random.choice(move)
                print("final move: ", move)

            elif head[1] > food[0][1] and (matrix[head[0]][head[1] - 1] != 1):  # that means head is left side of food.
                movement = "left"
                move = self.priority(matrix, head, possible_moves, height, width, load_factor)
                print("move: ", move)
                if movement in move:
                    move = movement
                else:
                    move = random.choice(move)
                print("final move: ", move)

            else:  # that means head and food are in the same column!
                if head[0] < food[0][0] and (matrix[head[0] + 1][head[1]] != 1):  # that means hard is above the food.
                    movement = "down"
                    move = self.priority(matrix, head, possible_moves, height, width, load_factor)
                    print("move: ", move)
                    if movement in move:
                        move = movement
                    else:
                        move = random.choice(move)
                    print("final move: ", move)
                elif head[0] > food[0][0] and (matrix[head[0] - 1][head[1]] != 1):  # that means hard is below the food.
                    movement = "up"
                    move = self.priority(matrix, head, possible_moves, height, width, load_factor)
                    print("move: ", move)
                    if movement in move:
                        move = movement
                    else:
                        move = random.choice(move)
                    print("final move: ", move)
                else:
                    possible_moves = []
                    if head[1] + 1 != width and matrix[head[0]][head[1] + 1] not in [1, 4]:
                        possible_moves.append("right")
                    if head[1] - 1 >= 0 and matrix[head[0]][head[1] - 1] not in [1, 4]:
                        possible_moves.append("left")
                    if head[0] + 1 != height and matrix[head[0] + 1][head[1]] not in [1, 4]:
                        possible_moves.append("down")
                    if head[0] - 1 >= 0 and matrix[head[0] - 1][head[1]] not in [1, 4]:
                        possible_moves.append("up")

                    if len(possible_moves) > 0:
                        move = self.priority(matrix, head, possible_moves, height, width, load_factor)
                    move = random.choice(move)
                    print("final move: ", move)
        elif load_factor == 0:
            print("head[0]: ", head[0], "head[1]: ", head[1])
            possible_moves = []

            if head[0] - 1 >= 0 and matrix[head[0] - 1][head[1]] not in [1, 4]:
                possible_moves.append("up")

            if head[0] + 1 <= height - 1 and matrix[head[0] + 1][head[1]] not in [1, 4]:
                possible_moves.append("down")

            if head[1] - 1 >= 0 and matrix[head[0]][head[1] - 1] not in [1, 4]:
                possible_moves.append("left")

            if head[1] + 1 <= width - 1 and matrix[head[0]][head[1] + 1] not in [1, 4]:
                possible_moves.append("right")
            print("possible_moves=", possible_moves)

            move = self.priority(matrix, head, possible_moves, height, width, load_factor)

        print("--- %s seconds ---" % (time.time() - start_time))
        # end of my code--------------------------------------------

        print(f"MOVE: {move}")
        return {"move": move}

    @cherrypy.expose
    @cherrypy.tools.json_in()
    def end(self):
        # This function is called when a game your snake was in ends.
        # It's purely for informational purposes, you don't have to make any decisions here.
        data = cherrypy.request.json
        print("END")
        return "ok"


if __name__ == "__main__":
    server = Battlesnake()
    cherrypy.config.update({"server.socket_host": "0.0.0.0"})
    cherrypy.config.update(
        {"server.socket_port": int(os.environ.get("PORT", "8080")), }
    )
    print("Starting Battlesnake Server...")
    cherrypy.quickstart(server)
