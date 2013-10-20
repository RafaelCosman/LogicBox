"""
This is the Logic Box game by Rafael Cosman
"""

#Classes
#----------------- 
class RunButton
    constructor: () ->
        @loc = new PVector(1400, 100)
        @radius = 100
        
    run: () ->
        
    show: () ->
        translateByLocation(@loc)
        ellipseByRadius(@radius)
        
        fill(100)
        text("Run all tests", 0, 0)
        
    clicked: () ->
        if @mouseIsOver()
            for gameObject in currentLevel.gameObjects
                if gameObject instanceof UnitTest
                    gameObject.runTest()
            
    unclicked: () ->
            
    mouseIsOver: () ->
        getMouse().dist(@loc) < @radius
        
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
            @loc.set(PVector.add(getMouse(), @offset))
        if @rotating
            @rotation = @mouseAngle() + @rotationOffset
            
    clicked: () ->
        if @mouseIsOver()
            @dragging = true
            @offset.set(PVector.sub(@loc, getMouse()))
        if @mouseIsOverRotation()
            @rotating = true
            @rotationOffset = @mouseAngle() - @rotation
            
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
        
    run: () ->
        super
        println("mouseAngle: " + @mouseAngle())
        println("rotation  : " + @rotation)
    
class StringInProgress
    constructor: (@string, @loc) ->
        @indices = computeIndecesFromLocation(@loc)
        @vel = new PVector(0, 0)
        @run()
        
    run: () ->
        @loc.add(@vel)
        
        currentLogicBox = currentLevel.findLogicBoxByLocation(@loc)
        
        if currentLogicBox != null
            @vel = makeVectorFromHeading(currentLogicBox.rotation)
            @string = currentLogicBox.processString(@string)
        
    show: () ->
        translateByLocation(@loc)
        fill(200)
        text(@string, 0, 0)
        
    clicked: () ->
        
    unclicked: () ->
    
class UnitTest
    constructor: (@input, @output, @loc) ->
        @radius = 50
        
    run: () ->
        
    show: () ->
        translateByLocation(@loc)
        fill(100)
        ellipseByRadius(@radius)
        
        stroke(200)
        fill(200)
        text(@input, 0, 0)
        text(@output, 0, 25)
        
    clicked: () ->
        if @mouseIsOver()
            @runTest()
            
    runTest: () ->
        currentLevel.gameObjects.push(new StringInProgress(@input, currentLevel.startBox.loc))
        
    unclicked: () ->
        
    mouseIsOver: () ->
        getMouse().dist(@loc) < @radius
    
class Level extends StartBox
    constructor: () ->
        @gameObjects = []
        @gridWidth = 9
        @startBox = new StartBox()
        @gameObjects.push(@startBox)
        
    findLogicBoxByLocation: (location) ->
        for gameObject in @gameObjects
            if gameObject instanceof LogicBox
                if gameObject.loc.dist(location) == 0
                    return gameObject
                
        return null
    
#Main code
#--------------
gridSquareWidth = 90
border = 9
boardOffset = new PVector(gridSquareWidth * 1.5 + border, gridSquareWidth * .5 + border)

currentLevel = null

setup = () ->
    textFont(createFont("FFScala", 32))
    
    rectMode(CENTER)
    ellipseMode(CENTER)
    textAlign(CENTER)

    currentLevel = new Level()
    
    currentLevel.gameObjects.push(new CopyBox())
    currentLevel.gameObjects.push(new DeleteBox())

    currentLevel.gameObjects.push(new UnitTest("abc", "bca", new PVector(1200, 100)))
    currentLevel.gameObjects.push(new UnitTest("test", "estt", new PVector(1300, 100)))
    currentLevel.gameObjects.push(new RunButton())
        
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

#Draws the grid for the user to code on. This grid should be drawn behind all other game objects.
drawGrid = () ->
    fill(255)
    strokeWeight(2)
    stroke(0, 10, 20)
    for x in [0..currentLevel.gridWidth]
        for y in [0..currentLevel.gridWidth]
            rectByLocationAndDimensions(computeLocationFromIndeces(new PVector(x, y)), new PVector(gridSquareWidth, gridSquareWidth))

#Helper functions
#------------------
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
        
#Little one-line wrapper functions
#-----------------------------
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
    if vector.x < 0 then ding - HALF_PI else ding + HALF_PI
        
makeVectorFromHeading = (heading) ->
    return new PVector(cos(heading), sin(heading))