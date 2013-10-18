"""
This is the Logic Box game by Rafael Cosman
"""

#Classes
#----------------- 
class RunButton
    constructor: () ->
        @loc = new PVector(1300, 100)
        @dimensions = new PVector(100, 100)
        
    run: () ->
        
    show: () ->
        rectByLocationAndDimensions(@loc, @dimensions)
        
    clicked: () ->
        if @mouseIsOver()
            println("running tests!")#First, let's find the startbox            
            
    unclicked: () ->
            
    mouseIsOver: () ->
        getMouse().y > @loc.y && getMouse().y < @loc.y + @dimensions.y && getMouse().x > @loc.x && getMouse().x < @loc.x + @dimensions.x;

class Draggable
    constructor: () ->
        @dragging = false
        @loc = computeLocationFromIndeces(new PVector(-1, random(0, 9)))
        @rotation = 0
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
        @radius = gridSquareWidth / 2 - border
        
    clicked: () ->
        if @mouseIsOver()
            @dragging = true
            @offset.set(PVector.sub(@loc, getMouse()))
            
    mouseIsOver: () ->
        getMouse().dist(@loc) < @radius
        
class LogicBox extends DraggableCircle
    show: () ->
        translateByLocation(@loc)
        rotate(@rotation)
        ellipseByRadius(@radius)
        line(@loc.x, @loc.y, @loc.x, @loc.y - 10)
        
    processString: (s) ->
        s
        
class CopyBox extends LogicBox
    show: () ->
        fill(0, 0, 255)
        super
        
    processString: (input) ->
        input += input[0]

class DeleteBox extends LogicBox
    show: () ->
        fill(255, 0, 0)
        super
        
    processString: (input) ->
        input.substring(1)
        
class StartBox extends LogicBox
    show: () ->
        fill(0, 0, 0)
        super
        
#Main code
#--------------
gameObjects = []
gridSquareWidth = 90
border = 9
boardOffset = new PVector(gridSquareWidth * 1.5 + border, gridSquareWidth * .5 + border)

setup = () ->
    gameObjects.push(new CopyBox())
    gameObjects.push(new DeleteBox())
    gameObjects.push(new StartBox())

    gameObjects.push(new RunButton())
    
    rectMode(CENTER)
    ellipseMode(CENTER)

draw = () ->
    background(200)

    fill(255)
    rect(gridSquareWidth * .5 + border * .5, height/2, gridSquareWidth - 2 * border, height - 2 * border)
    
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
    unoffsetLocation = PVector.mult(indeces, gridSquareWidth + border)
    PVector.add(boardOffset, unoffsetLocation)
computeIndecesFromLocation = (loc) ->
    indeces = PVector.div(PVector.sub(loc, boardOffset), gridSquareWidth + border)
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
ellipseByDimensions = (dimensions) ->
    ellipse(0, 0, dimensions, dimensions) 
ellipseByRadius = (radius) ->
    ellipse(0, 0, radius * 2, radius * 2)
    
rectByLocationAndDimensions = (location, dimensions) ->
    rect(location.x, location.y, dimensions.x, dimensions.y)

arrow = (x1, y1, x2, y2) ->
    line(x1, y1, x2, y2)
    pushMatrix()
    translate(x2, y2)
    float a = atan2(x1-x2, y2-y1)
    rotate(a)
    line(0, 0, -10, -10)
    line(0, 0, 10, -10)
    popMatrix()
    
translateByLocation = (location) ->
    translate(location.x, location.y)

getMouse = () ->
    new PVector(pcs.mouseX, pcs.mouseY)