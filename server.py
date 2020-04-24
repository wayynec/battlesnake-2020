import os
import random
import cherrypy

import math
import time #added


"""
This is a simple Battlesnake server written in Python.
For instructions see https://github.com/BattlesnakeOfficial/starter-snake-python/README.md
"""

# Rules: 0=available space, 1=snake body, 2=Food, 3=head, 4= Bigger enemy's head


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

    
    #---------------------------------------------------------------------
    #Function priority moves: Retruns priority movement
    def priority(matrix, head, possible_moves):
        priority_moves = ["up", "down", "left", "right"]
        # check if the distance between my head and enemy's head (=4) is =< 2
        
        #enemy is at the right within range 2. head[0] is width
        if head[0]+2 <= width-1 and matrix[head[0]+2][head[1]] == 4:
            priority_moves.remove("right")
        
        if head[0]-2 >= 0 and matrix[head[0]-2][head[1]] == 4:
            priority_moves.remove("left")
        
        if head[1]+2 <= height-1 and matrix[head[0]][head[1]+2] == 4:
            priority_moves.remove("down")
        
        if head[1]+2 >= 0 and matrix[head[0]][head[1]-2] == 4:
            priority_moves.remove("up")
        
        # match possible moves and priority moves.
        combined_move = list( set(possible_moves) & set(priority_moves) )
        move =random.choice(combined_move)
        
    return move
    
    #---------------------------------------------------------------------

    
    @cherrypy.expose
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def move(self, possible_move=None):
        # This function is called on every turn of a game. It's how your snake decides where to move.
        # Valid moves are "up", "down", "left", or "right".
        # TODO: Use the information in cherrypy.request.json to decide your next move.
        data = cherrypy.request.json

        # Choose a random direction to move in
        #possible_moves = ["up", "down", "left", "right"]
        #move = random.choice(possible_moves)
        

        #add my code--------------------------------------------
        start_time = time.time()
        
        #board info
        height=data["board"]["height"]
        width=data["board"]["width"]
        
        #Create Adjacency Matrix
        matrix=[0]*(width)
        for i in range(width):
            matrix[i]=[0]*(height)
        
        
        
        # Input my snake location into matrix
        for i in range(len(data["you"]["body"])): #body[i]=head, body, or tail...
            x = data["you"]["body"][i]["x"]
            y = data["you"]["body"][i]["y"]
            matrix[y][x] = 1
        
        # get my_size
        my_size=len(data["you"]["body"])
        
        # Input "other" snakes location into matrix
        for i in range(len(data["board"]["snakes"])): #body[i]=[x,y]
            # j is head, body, or tail...by index
            
            #get enemy's size
            size = len(data["board"]["snakes"][i]["body"])
            
            for j in range(len(data["board"]["snakes"][i]["body"])):
                
                x = data["board"]["snakes"][i]["body"][j]["x"]
                y = data["board"]["snakes"][i]["body"][j]["y"]
                
                if( j==0 and my_size <= size): # j == 0 means head
                    matrix[y][x] = 4
                
                else:
                    matrix[y][x] = 1
        
        # Input food location into matrix
        food = []
        for i in range(len(data["board"]["food"])): #food[i]=[x,y]
            x = data["board"]["food"][i]["x"]
            y = data["board"]["food"][i]["y"]
            food.append([y, x])
            matrix[y][x] = 2

        #get head
        x = data["you"]["body"][0]["x"]
        y = data["you"]["body"][0]["y"]
        matrix[y][x] = 3
        head = (y, x)

        #get health
        h = data["you"]["health"]
        load_factor = 0  #load factor = 0 when health > 50
        if h < 50:
            load_factor = 1
        #head.append(x) #now, head=[row, col]
        shortest = 100
        s_food = None
        for item in food: #items are tuples
            path = abs(head[0] - item[0]) + abs(head[1] - item[1])
            item.append(path)
            #if shortest > path:
            #   shortest = path
            #   s_food = item
        food.sort(key=lambda x: (x[2])) #sort the array using food[2](shortest path)
        #print("s_food =", s_food, "shortest path = ", shortest)
        print(food)
        print("health: ", h) #print health
        print("load factor: ", load_factor)

        #debug
        print("------matrix------")
        for line in matrix:
            print(line)

        if load_factor == 1:
            if (head[1] < food[0][1] and (matrix[head[0]][head[1] + 1] != 1)):  # that means head is left side of food.
                move = "right"
            elif (head[1] > food[0][1] and (matrix[head[0]][head[1] - 1] != 1)):  # that means head is left side of food.
                move = "left"
            else:  # that means head and food are in the same column!

                if (head[0] < food[0][0] and (matrix[head[0] + 1][head[1]] != 1)):  # that means hard is above the food.
                    move = "down"
                elif (head[0] > food[0][0] and (matrix[head[0] - 1][head[1]] != 1)):  # that means hard is below the food.
                    move = "up"
                else:
                    possible_moves = []
                    if matrix[head[0]][head[1] + 1] != 1 and head[1] + 1 != width:
                        possible_moves.append("right")
                    if matrix[head[0]][head[1] - 1] != 1 and head[1] - 1 != 0:
                        possible_moves.append("left")
                    if matrix[head[0] + 1][head[1]] != 1 and head[0] + 1 != height:
                        possible_moves.append("down")
                    if matrix[head[0] - 1][head[1]] != 1 and head[0] - 1 != 0:
                        possible_moves.append("up")
                    move = random.choice(possible_moves)
        elif load_factor == 0:
            print("head[0]: ", head[0], "head[1]: ", head[1])
            possible_moves = []
            #matrix[head[0]][head[1]] is not in [1,2] and head[1] +1 <= width
            """
            if width-1 > head[1] > 0 or height-1 > head[0] > 0: #make sure the snake is within the bound
                if matrix[head[0]][head[1] + 1] != 1:
                    possible_moves.append("right")
                if matrix[head[0]][head[1] - 1] != 1:
                    possible_moves.append("left")
                if matrix[head[0] + 1][head[1]] != 1:
                    possible_moves.append("down")
                if matrix[head[0] - 1][head[1]] != 1:
                    possible_moves.append("up")
            """
            """
            #four corners
            if head[1] == 0 and head[0] == 0:
                print("00000000000")
                if matrix[head[0]+1][head[1]] == 0:
                    possible_moves.append("down")
                else:
                    possible_moves.append("right")
            if head[1] == width-1 and head[0] == 0:
                print("1111111")
                if matrix[head[0]][head[1]-1] == 0:
                    possible_moves.append("left")
                else:
                    possible_moves.append("down")
            if head[0] == height-1 and head[1] == 0:
                print("22222222")
                if matrix[head[0]-1][head[1]] == 0:
                    possible_moves.append("up")
                else:
                    possible_moves.append("right")
            if head[0] == height-1 and head[1] == width-1:
                print("3333333333")
                if matrix[head[0]-1][head[1]] == 0:
                    possible_moves.append("up")
                else:
                    possible_moves.append("left")
            """
            if head[0] - 1 >= 0 and matrix[head[0]-1][head[1]] is not in [1,4]:
                possible_moves.append("up")

            if head[0] + 1 <= height - 1 and matrix[head[0]+1][head[1]] is not in [1,4]:
                possible_moves.append("down")

            if head[1] - 1 >= 0 and matrix[head[0]][head[1] - 1] is not in [1,4]:
                possible_moves.append("left")

            if head[1] + 1 <= width - 1 and matrix[head[0]][head[1] + 1] is not in [1,4]:
                possible_moves.append("right")
            print(possible_moves)

            move = priority(matrix, head, possible_moves)

        
        
        
        print("--- %s seconds ---" % (time.time() - start_time))
        #end of my code--------------------------------------------

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
        {"server.socket_port": int(os.environ.get("PORT", "8080")),}
    )
    print("Starting Battlesnake Server...")
    cherrypy.quickstart(server)
