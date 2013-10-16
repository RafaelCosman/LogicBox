class logicBox
    constructor: () ->
        @loc = new PVector(500, 500)
        @dim = new PVector(100, 100)
        
    show: () ->
        ellipse(@loc.x, @loc.y, @dim.x, @dim.y)
        #ellipse(@loc, @dim)
        
    run: () ->
        
    processString: (s) ->
        s

gameObjects = []
    
setup = () ->
    box = new logicBox
    gameObjects.push(box)

draw = () ->
    background(100)
    ellipse(pcs.mouseX, pcs.mouseY, 10, 10)
    
    for gameObject in gameObjects
        gameObject.run()
        gameObject.show()
    
#sugar
#-------
#ellipse = (loc, dim) ->
#    ellipse(loc.x, loc.y, dim.x, dim.y)