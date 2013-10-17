"""
This is the Logic Box game by Rafael Cosman
"""

#Classes
#------------------
class Draggable
    constructor: () ->
        @dragging = false
        @loc = computeLocationFromIndeces(new PVector(0, 1))
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
        
class LogicBox extends DraggableCircle
    show: () ->
        ellipseByLocationAndRadius(@loc, @radius)
        
    processString: (s) ->
        s
        
class CopyBox extends LogicBox
    show: () ->
        fill(200, 0, 0)
        ellipseByLocationAndRadius(@loc, @radius)
        
    processString: (input) ->
        input.append(input[0])

class DeleteBox extends LogicBox
    show: () ->
        fill(200, 0, 0)
        ellipseByLocationAndRadius(@loc, @radius)
        
    processStirng: (input) ->
        input.delete(0)
        
class StartBox extends LogicBox
    show: () ->
        
#Main code
#--------------
gameObjects = []
gridSquareWidth = 90
boardOffset = new PVector(gridSquareWidth * 1.5, gridSquareWidth * .5)

setup = () ->
    gameObjects.push(new CopyBox())
    
    rectMode(CENTER)
    ellipseMode(CENTER)

draw = () ->
    background(200)
    
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
ellipseByLocationAndDimensions = (location, dimensions) ->
    ellipse(location.x, location.y, dimensions.x, dimensions.y)
ellipseByLocationAndRadius = (location , radius) ->
    ellipse(location.x, location.y, radius * 2, radius * 2)
    
rectByLocationAndDimensions = (location, dimensions) ->
    rect(location.x, location.y, dimensions.x, dimensions.y)
    
translateByVector = (vector) ->
    translate(vector.x, vector.y)

getMouse = () ->
    new PVector(pcs.mouseX, pcs.mouseY)