class esb_settings:
# Put your settings here:
# IMPORTANT: Don't change the indentation!

# General Settings
    bedWidth = 220
    bedLength = 220
    
    bedMargin = 5
    filamentDiameter = 1.75
    movementSpeed = 100
    stabilizationTime = 20
    bedTemp = 40
    fanSpeed = 0

    primeLength = 25
    primeAmount = 20
    primeSpeed = 5
    wipeLength = 15
    retractionDistance = 4
    retractionSpeed = 60

    blobHeight = 10
    extrusionAmount = 200

    direction = -1           #1=front to back, -1=back to front
    xSpacing = 40
    ySpacing = 25
    
# Flow Variation
    startFlow = 2
    flowOffset = 2
    flowSteps = 8


# Temperature Variation
    startTemp = 240
    tempOffset = -20
    tempSteps = 3           #If Steps = 1 "Fill Mode" is used
    
    comment = "Ender3"

    endFlow = startFlow+(flowSteps-1)*flowOffset # Don't change
    endTemp = startTemp+(tempSteps-1)*tempOffset # Don't change

    #outputFilename = "esb.gcode"
    outputFilename = "{}_{}-{}mm3_{}-{}C.gcode".format(comment,startFlow,endFlow,startTemp,endTemp)
