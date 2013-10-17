"""
This is the Logic Box game by Rafael Cosman
"""

#Classes
#------------------
class Draggable
    constructor: () ->
        @dragging = false
        @loc = new PVector(100, 100)
        @offset = new PVector()
    
    run: () ->
        println(@dragging)
        if (@dragging)
            @loc.set(PVector.add(getMouse(), @offset));
            
    unclicked: () ->
        @dragging = false
        
class DraggableRectangle extends Draggable
    constructor: () ->
        super()
        @dim = new PVector(100, 100)
        
    clicked: () ->
        if @mouseIsOver()
            dragging = true
            @offset.set(PVector.sub(@loc, getMouse()))
            
    mouseIsOver: () ->
        return getMouse().y > @loc.y && getMouse().y < @loc.y + @dimensions.y && getMouse().x > @loc.x && @getMouse().x < @loc.x + @dimensions.x;
        
class DraggableCircle extends Draggable
    constructor: () ->
        super()
        @radius = 10
        
    clicked: () ->
        if @mouseIsOver()
            dragging = true
            @offset.set(PVector.sub(@loc, getMouse()))
            
    mouseIsOver: () ->
        getMouse().dist(@loc) < @radius
        
class logicBox extends DraggableCircle
    show: () ->
        ellipse(@loc.x, @loc.y, @radius * 2, @radius * 2)
        #ellipse(@loc, @dim)
        
    processString: (s) ->
        s
        
        
#Main code
#--------------
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

#UI STUFF
#-----------------
mousePressed = () ->
    for gameObject in gameObjects
        gameObject.clicked()
        
mouseReleased = () ->
    for gameObject in gameObjects
        gameObject.unclicked()
        
#sugar
#-------
#ellipse = (loc, dim) ->
#    ellipse(loc.x, loc.y, dim.x, dim.y)

getMouse = () ->
    new PVector(pcs.mouseX, pcs.mouseY)