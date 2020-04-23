import os
import random

import cherrypy

"""
This is a simple Battlesnake server written in Python.
For instructions see https://github.com/BattlesnakeOfficial/starter-snake-python/README.md
"""


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

    @cherrypy.expose
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def move(self):
        # This function is called on every turn of a game. It's how your snake decides where to move.
        # Valid moves are "up", "down", "left", or "right".
        # TODO: Use the information in cherrypy.request.json to decide your next move.
        data = cherrypy.request.json

        # Choose a random direction to move in
        possible_moves = ["up", "down", "left", "right"]
        move = random.choice(possible_moves)
        

        #add my code------------------

        #add my code--------------------------------------------
        
        #board info
        height=data["board"]["height"]-1
        width=data["board"]["width"]-1
        
        """
        #food info
        food=[]
        
        food.append(data["board"]["food"][0]["x"])
        food.append(data["board"]["food"][0]["y"])
        print(food)
        
        
        #body info
        head=data["you"]["body"][0] #head=[x,y]
        
        length=len(data["you"]["body"]) #to obtain tail info
        tail=data["you"]["body"][length]
        """
        
        #Create Adjacency Matrix
        matrix=[0]*width
        for i in range(width):
            matrix[i]=[0]*height
        
        # Input my snake location into matrix
        for i in range(len(data["you"]["body"])): #body[i]=[x,y]
            x = data["you"]["body"][i]["x"]
            y = data["you"]["body"][i]["y"]
            matrix[x][y] = 1
        
        # Input food location into matrix
        for i in range(len(data["board"]["food"])): #food[i]=[x,y]
            x = data["board"]["food"][i]["x"]
            y = data["board"]["food"][i]["y"]
            matrix[y][x] = 2
        
        #debug
        print("------matrix------")
        for line in matrix:
            print(line)
        
        
        if(head["x"]==width):#if x cordinate is width
            possible_moves2 = ["up", "down", "left"]
            move = random.choice(possible_moves2)
        elif(head["x"]==0):#if x cordinate is left most
            possible_moves2 = ["up", "down", "right"]
            move = random.choice(possible_moves2)
        elif(head["y"]==height):
            possible_moves2 = ["up", "left", "right"]
            move = random.choice(possible_moves2)
        elif(head["y"]==0):#if x cordinate is left most
            possible_moves2 = ["down", "down", "right"]
            move = random.choice(possible_moves2)
        

        print("head", head)
        
        
        
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
