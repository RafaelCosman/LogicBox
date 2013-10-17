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
        if (@dragging)
            @loc.set(PVector.add(getMouse(), @offset));
            
    unclicked: () ->
        @dragging = false
        indeces = computeIndecesFromLocation(@loc)
        @loc = computeLocationFromIndeces(indeces)
        
class DraggableRectangle extends Draggable
    constructor: () ->
        super()
        @dim = new PVector(100, 100)
        
    clicked: () ->
        if @mouseIsOver()
            @dragging = true
            @offset.set(PVector.sub(@loc, getMouse()))
            
    mouseIsOver: () ->
        getMouse().y > @loc.y && getMouse().y < @loc.y + @dimensions.y && getMouse().x > @loc.x && @getMouse().x < @loc.x + @dimensions.x;
        
class DraggableCircle extends Draggable
    constructor: () ->
        super()
        @radius = gridSquareWidth / 2
        
    clicked: () ->
        if @mouseIsOver()
            @dragging = true
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
boardOffset = new PVector(100, 0)
gridSquareWidth = 90

setup = () ->
    box = new logicBox
    gameObjects.push(box)
    
    rectMode(CENTER)
    ellipseMode(CENTER)

draw = () ->
    background(200)
    ellipse(pcs.mouseX, pcs.mouseY, 10, 10)
    
    pushMatrix()
    drawGrid()
    popMatrix()
    
    for gameObject in gameObjects
        gameObject.run()
        
        pushMatrix()
        gameObject.show()
        popMatrix()

drawGrid = () ->
    fill(255)
    for x in [0..10]
        for y in [0..10]
            rectByLocationAndDimensions(computeLocationFromIndeces(new PVector(x, y)), new PVector(gridSquareWidth, gridSquareWidth))

computeLocationFromIndeces = (indeces) ->
    unoffsetLocation = PVector.mult(indeces, gridSquareWidth + 2)
    PVector.add(boardOffset, unoffsetLocation)
computeIndecesFromLocation = (loc) ->
    indeces = PVector.div(PVector.sub(loc, boardOffset), gridSquareWidth + 2)
    indeces.x = Math.floor(indeces.x)
    indeces.y = Math.floor(indeces.y)
    indeces
        
#UI STUFF
#-----------------
mousePressed = () ->
    for gameObject in gameObjects
        gameObject.clicked()
        
mouseReleased = () ->
    for gameObject in gameObjects
        gameObject.unclicked()
        
#nice little sugar
#-------
ellipseByLocAndDims = (location, dimensions) ->
    ellipse(location.x, location.y, dimensions.x, dimensions.y)
rectByLocationAndDimensions = (location, dimensions) ->
    rect(location.x, location.y, dimensions.x, dimensions.y)
    
translateByVector = (vector) ->
    translate(vector.x, vector.y)

getMouse = () ->
    new PVector(pcs.mouseX, pcs.mouseY)