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
        'color': '#8ee54b',
        'head': "http://cdn8.staztic.com/app/a/6551/6551890/hungry-frog-10100000-l-140x140.png"
    }


@bottle.post('/start')
def start():
    data = bottle.request.json

    # TODO: Do things with data

    return {
        'taunt': 'Legit ribbit!'
    }


@bottle.post('/move')
def move():
    data = bottle.request.json
    
    #snake head        
    position = []
    for snake in data["snakes"]:
        if snake["id"] == "3063baf3-a325-4b3f-bfb8-94434de3316d":
            position = snake["coords"][0]
    
    
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
    
    def distance(xy1,xy2):
        dis = abs(xy1[0] - xy2[0]) + abs(xy1[1] - xy2[1])
        return dis
        
    def closestFood():
        nearestFood = None
        lastDistance = 100000
        for foodInstance in data["food"]:
            newDistance = distance(position,foodInstance)
            if newDistance < lastDistance:
                lastDistance = newDistance
                nearestFood = foodInstance
        return nearestFood
    
    food = closestFood()
    
    def direcPref(food):
        result = []
        if food == None:
            result = ["south", "east", "west", "north"]
        elif position[0] < food[0]:
            #move east
            result = ["east", "south", "north", "west"]
        elif position[0] > food[0]:
            #move west
            result = ["west", "north", "south", "east"]
        else:
            if position[1] < food[1]:
                #move south
                result = ["south", "east", "west", "north"]
            elif position[1] > food[1]:
                #move north
                result = ["north", "west", "east", "south"]
            else:
                result = ["south", "east", "west", "north"]
        return result
    
    def checkDir(direction):
        result = False
        if direction == "north":
            result = moveCheck([position[0], position[1] - 1])
        elif direction == "south":
            result = moveCheck([position[0], position[1] + 1])
        elif direction == "east":
            result = moveCheck([position[0] + 1, position[1]])
        else:
            result = moveCheck([position[0] - 1, position[1]])
        return result
    
    mymove = ""
    
    pref = direcPref(food)
    
    if checkDir(pref[0]):
        mymove = pref[0]
    elif checkDir(pref[1]):
        mymove = pref[1]
    elif checkDir(pref[2]):
        mymove = pref[2]
    else:
        mymove = pref[3]
    
    # TODO: Do things with data
    
    return {
        'move': mymove,
        'taunt': "Ribbit kill it!!"
    }
    
@bottle.post('/end')
def end():
    data = bottle.request.json

    # TODO: Do things with data

    return {
        'taunt': 'Ribbit killed it!'
    }



# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()
if __name__ == '__main__':
    bottle.run(application, host=os.getenv('IP', '0.0.0.0'), port=os.getenv('PORT', '8080'))
