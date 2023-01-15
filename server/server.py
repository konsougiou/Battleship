from fastapi import FastAPI
from game_class import Game
from pydantic import BaseModel

app = FastAPI()
app.counter: int = 0
games: dict = {}

class Grid(BaseModel):
    data: list[list[int]]


@app.get("/initialize")
async def initialize(key: int = -1):

    if key == -1:
        app.counter += 1
        tmp_counter = app.counter
        new_game = Game(tmp_counter)
        games.update({tmp_counter: new_game})
        return {"key": tmp_counter}
    else:
        game = games.get(key)
        if game == None:
            return {"message": 1}
        else:
            game.set_state("setup")
            return {"message": 0}


@app.get("/ping_initialize")
async def ping_initialize(key: int = -1):
        game = games.get(key)
        if game.get_state() == "setup":
            return {"message": 0}
        else:
            return {"message": 1}




@app.post("/setup")
async def setup(player: int, input_grid: Grid, key: int):
    grid = input_grid.data
    game = games.get(key)
    if player == 1:
        game.set_map1(grid)
    else:
        game.set_map2(grid)
        
    if game.get_map1() != None and game.get_map2() != None:
        game.set_state("host turn")
        return {"message": "begin"}
    else:
        return {"message": "wait"}



@app.get("/ping_setup")
async def ping_setup(player: int, key: int):
    game = games.get(key)
    if game.get_map1() != None and game.get_map2() != None:
        game.set_state(1)
        return {"message": "begin"}
    else:
        return {"message": "wait"} 



@app.get("/get_grid")
async def get_grid(player: int, key: int):
    game = games.get(key)
    if player == 1:
        return {"message": game.get_map2()}
    if player == 2:
        return {"message": game.get_map1()}



@app.get("/fire")
async def fire(player: int, key: int, x: int, y: int):
    game = games.get(key)
    hit = False
    map = game.get_map2() if player == 1 else game.get_map1()
    game.set_previous_target((x, y))
    if player == 1:
        game.set_state(2)
        map = game.get_map2()
    else:
        game.set_state(1)
        map = game.get_map1()

    position =  map[y][x]
    if position == 0:
        hit = False
    else:
        if player == 1:
            game.increment_count1()
            if game.get_count1() == 14:
                return {"message": hit, "end": True}
        else:
            game.increment_count2()
            if game.get_count2() == 14:
                return {"message": hit, "end": True}


        hit = True
        map[y][x] = 0

    return {"message": hit, "end": False}



@app.get("/ping_fire")
async def ping_fire( key: int):
    game = games.get(key)
    previous_target = game.get_previous_target()
    if game.get_count1() == 14 or game.get_count2() == 14:
        return {"state": 3, "previous_x": -1, "previous_y": -1}
    return {"state": game.get_state(), "previous_x": previous_target[0], "previous_y": previous_target[1]} if previous_target != None else {"state": game.get_state(), "previous_x": -1, "previous_y": -1}




