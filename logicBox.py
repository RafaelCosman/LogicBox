class Draggable
    constructor: () ->
        @dragging = false
        @loc = new PVector(100, 100)
        @offset = new PVector()
    
    run = () ->
        if (@dragging)
            @loc.set(PVector.add(getMouse(), @offset));
            
    unclicked = () ->
        @dragging = false
        
    clicked = () ->
        
class DraggableRectangle extends Draggable
    constructor: () ->
        super()
        @dim = new PVector(100, 100)
        
    mouseIsOver: () ->
        return getMouse().y > @loc.y && getMouse().y < @loc.y + @dimensions.y && getMouse().x > @loc.x && @getMouse().x < @loc.x + @dimensions.x;
        
class DraggableCircle extends Draggable
    constructor: () ->
        super()
        @radius = 10
        
    mouseIsOver: () ->
        getMouse().dist(@loc) < @radius
        
class logicBox extends DraggableCircle
    show: () ->
        ellipse(@loc.x, @loc.y, @radius * 2, @radius * 2)
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

getMouse = () ->
    new PVector(pcs.mouseX, pcs.mouseY)