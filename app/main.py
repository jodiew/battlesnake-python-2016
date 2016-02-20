import bottle
import os


@bottle.route('/static/<path:path>')
def static(path):
    return bottle.static_file(path, root='static/')


@bottle.get('/')
def index():
    head_url = '%s://%s/static/head.png' % (
        bottle.request.urlparts.scheme,
        bottle.request.urlparts.netloc
    )

    return {
        'color': '#00ffff',
        'head': head_url
    }


@bottle.post('/start')
def start():
    data = bottle.request.json

    # TODO: Do things with data

    return {
        'taunt': 'battlesnake-python!'
    }


@bottle.post('/move')
def move():
    data = bottle.request.json
    
    # our snake
    mysnake = {}
    for snake in data["snakes"]:
        if snake["id"] == "3063baf3-a325-4b3f-bfb8-94434de3316d":
            mysnake = snake
    
    #snake head        
    position = mysnake["coords"][0]
    
    
    def moveCheck(xy):
        result = False
        #check for walls
        if xy[0] > -1 and xy[1] > -1 and xy[0] < data["width"] and xy[1] < data["height"]:
            result = True
        result = result and snakeCheck(xy)
        return result
    
    def snakeCheck(xy):
        result = True
        for snake in data["snakes"]:
            for pos in snake["coords"]:
                if pos[0] == xy[0] and pos[1] == xy[1]:
                    result = False
        return result
        
    mymove = ""
    
    if moveCheck([position[0], position[1] + 1]):
        mymove = "north"
    elif moveCheck([position[0], position[1] - 1]):
        mymove = "south"
    elif moveCheck([position[0] + 1, position[1]]):
        mymove = "east"
    else:
        mymove = "west"
    # TODO: Do things with data
    
    return {
        'move': mymove,
        'taunt': 'battlesnake-python!'
    }
    
@bottle.post('/end')
def end():
    data = bottle.request.json

    # TODO: Do things with data

    return {
        'taunt': 'battlesnake-python!'
    }



# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()
if __name__ == '__main__':
    bottle.run(application, host=os.getenv('IP', '0.0.0.0'), port=os.getenv('PORT', '8080'))
