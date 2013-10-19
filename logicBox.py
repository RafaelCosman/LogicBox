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
        @rotating = false
        
        @indeces = new PVector(-1, random(0, 9))
        @loc = computeLocationFromIndeces(@indeces)
        
        @rotation = 0
        @offset = new PVector()
    
    run: () ->
        if @dragging
            @loc.set(PVector.add(getMouse(), @offset));
        if @rotating
            @rotation = @mouseAngle() + @rotationOffset
            
    unclicked: () ->
        @dragging = false
        @rotating = false
        
        #Quantize location based on grid
        @indeces = computeIndecesFromLocation(@loc)
        @loc = computeLocationFromIndeces(@indeces)
        
        #Quantize rotation to one of the four cardinal directions
        @rotation = Math.round(@rotation / PI/2) * PI/2
        
    mouseAngle: () ->
        heading(PVector.sub(getMouse(), @loc))
        
class DraggableCircle extends Draggable
    constructor: () ->
        super()
        @radius = gridSquareWidth / 2 - 2 * border
    
    show: () ->
        #first draw the circle
        translateByLocation(@loc)
        rotate(@rotation)
        stroke(100)
        ellipseByRadius(@radius)
        
        #Now let's draw the arrow
        strokeWeight(10)
        stroke(0, 200, 0)
        line(0, 0, 0, -@radius)
        translate(0, -@radius)
        
        dx = 7
        dy = 5
        triangle(0, -5, dx, dy, -dx, dy)
        
    clicked: () ->
        if @mouseIsOver()
            @dragging = true
            @offset.set(PVector.sub(@loc, getMouse()))
        if @mouseIsOverRotation()
            @rotating = true
            @rotationOffset = @mouseAngle() - @rotation
            
    mouseIsOver: () ->
        getMouse().dist(@loc) < @radius
        
    mouseIsOverRotation: () ->
        distance = getMouse().dist(@loc)
        distance > @radius and distance < @radius + 20
        
class LogicBox extends DraggableCircle        
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
    
class UnitTest
    constructor: (@input, @output) ->
        @radius = 50
        
    run: () ->
        
    show: () ->
        translate(1200, 100)
        fill(100)
        ellipseByRadius(@radius)
        text(@input)
        
    clicked: () ->
        
    unclicked: () ->
    
class Level
    constructor: () ->
        @gameObjects = []
        @gridWidth = 9
    
    
    
#Main code
#--------------
gridSquareWidth = 90
border = 9
boardOffset = new PVector(gridSquareWidth * 1.5 + border, gridSquareWidth * .5 + border)

currentLevel = new Level()

setup = () ->
    currentLevel.gameObjects.push(new UnitTest("test", "estt"))
    
    currentLevel.gameObjects.push(new CopyBox())
    currentLevel.gameObjects.push(new DeleteBox())
    currentLevel.gameObjects.push(new StartBox())

    currentLevel.gameObjects.push(new RunButton())
    
    rectMode(CENTER)
    ellipseMode(CENTER)

draw = () ->
    background(200)

    fill(255)
    strokeWeight(2)
    stroke(0)
    rect(gridSquareWidth * .5 + border * .5, height/2, gridSquareWidth - 2 * border, height - 2 * border)
    
    pushMatrix()
    drawGrid()
    popMatrix()
    
    for gameObject in currentLevel.gameObjects
        gameObject.run()
        
        pushMatrix()
        gameObject.show()
        popMatrix()

drawGrid = () ->
    fill(255)
    strokeWeight(2)
    stroke(0, 10, 20)
    for x in [0..currentLevel.gridWidth]
        for y in [0..currentLevel.gridWidth]
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
    for gameObject in currentLevel.gameObjects
        gameObject.clicked()
        
mouseReleased = () ->
    for gameObject in currentLevel.gameObjects
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
    
translateByLocation = (location) ->
    translate(location.x, location.y)

getMouse = () ->
    new PVector(pcs.mouseX, pcs.mouseY)
    
heading = (vector) ->
    ding = Math.atan(vector.y / vector.x)
    if vector.x < 0 then ding else ding + 180