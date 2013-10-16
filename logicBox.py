class Draggable
    constructor: () ->
        super()
        @loc = new PVector(500, 500)
        
class DraggableRectangle extends Draggable
    constructor: () ->
        super()
        @dim = new PVector(100, 100)
        
class DraggableCircle extends Draggable
    constructor: () ->
        super()
        @radius = 10
        
class logicBox extends DraggableRectangle
    constructor: () ->
        super()
        
    show: () ->
        ellipse(@loc.x, @loc.y, @radius * 2, @radius * 2)
        #ellipse(@loc, @dim)
        
    run: () ->
        println("run")
        
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