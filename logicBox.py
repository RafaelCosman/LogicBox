"""
This is the Logic Box game by Rafael Cosman
"""

#Classes
#-----------------
class Circle
    constructor: (@loc, @radius) ->
        
    mouseIsOver: () ->
        getMouse().dist(@getLoc()) < @getRadius()
        
    getLoc: () ->
        @loc
        
    getRadius: () ->
        @radius
        
    show: () ->
        if @mouseIsOver()
            radius = @getRadius() * 1.1
        else
            radius = @getRadius()
            
        ellipseByRadius(radius)
        
class RunButton
    constructor: () ->
        @circle = new Circle(new PVector(1500, 100), 100)
        
    run: () ->
        
    show: () ->
        stroke(0)
        @circle.show()
        
        fill(100)
        text("Run all tests", 0, 0)
        
    clicked: () ->
        if @circle.mouseIsOver()
            for gameObject in currentLevel.gameObjects
                if gameObject instanceof UnitTest
                    gameObject.runTest()
            
    unclicked: () ->
        
    getLoc: () ->
        @circle.getLoc()
        
class Draggable
    constructor: () ->
        @dragging = false
        @rotating = false
        
        @indeces = new PVector(-1, random(0, 9))
        
        @circle = new Circle(computeLocationFromIndeces(@indeces), gridSquareWidth / 2 - 2 * border)
        @rotationCircle = new Circle(computeLocationFromIndeces(@indeces), gridSquareWidth / 2 - 2 * border + 20)
        
        @rotation = 0
        @offset = new PVector()
    
    run: () ->
        if @dragging
            @circle.loc.set(PVector.add(getMouse(), @offset))
            @rotationCircle.loc.set(PVector.add(getMouse(), @offset))
        if @rotating
            @rotation = @mouseAngle() + @rotationOffset
            
    clicked: () ->
        if @circle.mouseIsOver()
            @dragging = true
            @offset.set(PVector.sub(@getLoc(), getMouse()))
        else if @rotationCircle.mouseIsOver()
            @rotating = true
            @rotationOffset = @mouseAngle() - @rotation
            
    unclicked: () ->
        @dragging = false
        @rotating = false
        
        #Quantize location based on grid
        @indeces = computeIndecesFromLocation(@getLoc())
        @circle.loc = computeLocationFromIndeces(@indeces)
        
        #Quantize rotation to one of the four cardinal directions
        @rotation = Math.round(@rotation / HALF_PI) * HALF_PI
        
    mouseAngle: () ->
        heading(PVector.sub(getMouse(), @getLoc()))
        
    show: () ->
        #first draw the circle
        rotate(@rotation)
        stroke(100)
        @circle.show()
        
        #Now let's draw the arrow
        strokeWeight(10)
        stroke(0, 200, 0)
        line(0, 0, 0, -@circle.radius)
        translate(0, -@circle.radius)
        
        dx = 7
        dy = 5
        triangle(0, -5, dx, dy, -dx, dy)
        
    getLoc: () ->
        return @circle.getLoc()
        
class LogicBox extends Draggable     
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
    
class StringInProgress
    constructor: (@string, @loc, @unitTest) ->
        @indices = computeIndecesFromLocation(@loc)
        @vel = new PVector(0, 0)
        @run()
        
    run: () ->
        @loc.add(@vel)
        
        if not locationIsOnGrid(@loc)
            if @string is @unitTest.output
                @unitTest.passed()
            else
                @unitTest.failed()
        
        currentLogicBox = currentLevel.findLogicBoxByLocation(@loc)
        
        if currentLogicBox != null
            @vel = makeVectorFromHeading(currentLogicBox.rotation)
            @string = currentLogicBox.processString(@string)
        
    show: () ->
        fill(200)
        text(@string, 0, 0)
        
    clicked: () ->
        
    unclicked: () ->
        
    getLoc: () ->
        @loc
        
class UnitTest
    constructor: (@input, @output, loc) ->
        @circle = new Circle(loc, 50)
        
    run: () ->
        
    show: () ->
        fill(@fillColor)
        stroke(0)
        @circle.show()
        
        stroke(200)
        fill(200)
        text(@input, 0, 0)
        text(@output, 0, 25)
        
    clicked: () ->
        if @circle.mouseIsOver()
            @runTest()
            
    runTest: () ->
        currentLevel.gameObjects.push(new StringInProgress(@input, currentLevel.startBox.getLoc(), this))
        
    unclicked: () ->
                
    passed: () ->
        @fillColor = color(255)
    failed: () ->
        @fillColor = color(255, 0 , 0)
        
    getLoc: () ->
        return @circle.getLoc()
    
class Level extends StartBox
    constructor: () ->
        @gameObjects = []
        @gridWidth = 9
        @startBox = new StartBox()
        @gameObjects.push(@startBox)
        
    findLogicBoxByLocation: (location) ->
        for gameObject in @gameObjects
            if gameObject instanceof LogicBox
                if gameObject.getLoc().dist(location) == 0
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
        translateByLocation(gameObject.getLoc())
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
    indeces.x = Math.round(indeces.x)
    indeces.y = Math.round(indeces.y)
    indeces
    
heading = (vector) ->
    ding = Math.atan(vector.y / vector.x)
    if vector.x < 0 then ding - HALF_PI else ding + HALF_PI
makeVectorFromHeading = (heading) ->
    heading -= HALF_PI #TODO: why do I seem to have to do this?
    return new PVector(cos(heading), sin(heading))

locationIsOnGrid = (location) ->
    indecesOfFarCorner = new PVector(currentLevel.gridWidth, currentLevel.gridWidth)
    locationOfFarCorner = computeLocationFromIndeces(indecesOfFarCorner)
    
    print(location)
    print(boardOffset)
    print(locationOfFarCorner)
    
    location.x >= boardOffset.x and
    location.y >= boardOffset.y and
    location.x <= locationOfFarCorner.x and
    location.y <= locationOfFarCorner.y
        
#Mouse STUFF
#-----------------
mousePressed = () ->
    for gameObject in currentLevel.gameObjects
        gameObject.clicked()
        
mouseReleased = () ->
    for gameObject in currentLevel.gameObjects
        gameObject.unclicked()
        
getMouse = () ->
    new PVector(pcs.mouseX, pcs.mouseY)
    
        
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