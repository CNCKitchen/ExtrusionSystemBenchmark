Dim currentOutputLine As Integer

Function writeLine(writeString As String)
    Worksheets("Output").Cells(currentOutputLine, 1) = Replace(writeString, ",", ".")
    currentOutputLine = currentOutputLine + 1
End Function

Sub GenerateGCode()
Dim direction As Integer
Dim bedWidth, bedLength, bedMargin, filamentDiameter, primeLength, primeAmount, primeSpeed, retractionDistance, retractionSpeed, xSpacing, ySpacing, startFlow, flowOffset, flowSteps, endFlow, startTemp, tempOffset, tempSteps, movementSpeed, stabilizationTime, wipeLength, blobHeight, extrusionAmount, extrusionSpeed, fanSpeed, bedTemp, bedLengthSave As Double

currentOutputLine = 1

'Get Inputs
bedWidth = Worksheets("Settings").Cells(2, 2).Value
bedLength = Worksheets("Settings").Cells(3, 2).Value
bedLengthSave = bedLength
bedMargin = Worksheets("Settings").Cells(4, 2).Value
filamentDiameter = Worksheets("Settings").Cells(5, 2).Value
movementSpeed = Worksheets("Settings").Cells(6, 2).Value
stabilizationTime = Worksheets("Settings").Cells(7, 2).Value
bedTemp = Worksheets("Settings").Cells(8, 2).Value
fanSpeed = Worksheets("Settings").Cells(9, 2).Value

primeLength = Worksheets("Settings").Cells(11, 2).Value
primeAmount = Worksheets("Settings").Cells(12, 2).Value
primeSpeed = Worksheets("Settings").Cells(13, 2).Value
wipeLength = Worksheets("Settings").Cells(14, 2).Value
retractionDistance = Worksheets("Settings").Cells(15, 2).Value
retractionSpeed = Worksheets("Settings").Cells(16, 2).Value

blobHeight = Worksheets("Settings").Cells(18, 2).Value
extrusionAmount = Worksheets("Settings").Cells(19, 2).Value

xSpacing = Worksheets("Settings").Cells(22, 2).Value
ySpacing = Worksheets("Settings").Cells(23, 2).Value

startFlow = Worksheets("Settings").Cells(27, 2).Value
flowOffset = Worksheets("Settings").Cells(28, 2).Value
flowSteps = Worksheets("Settings").Cells(29, 2).Value
endFlow = Worksheets("Settings").Cells(30, 2).Value

startTemp = Worksheets("Settings").Cells(33, 2).Value
tempOffset = Worksheets("Settings").Cells(34, 2).Value
tempSteps = Worksheets("Settings").Cells(35, 2).Value

direction = Worksheets("Settings").Cells(21, 2).Value

'Clear output sheet
Sheets("Output").Cells.Clear

'Credits
writeLine ("; *** CNC Kitchen Auto Flow Pattern Generator 0.93")
writeLine ("; *** 02/04/26 Stefan Hermann")
writeLine ("")
'Generation Settings
writeLine (";####### Settings")
writeLine ("; " & Worksheets("Settings").Cells(38, 2).Value)
writeLine ("; bedWidth = " & bedWidth)
writeLine ("; bedLength = " & bedLengthSave)
writeLine ("; bedMargin = " & Abs(bedMargin))
writeLine ("; filamentDiameter = " & filamentDiameter)
writeLine ("; movementSpeed = " & movementSpeed)
writeLine ("; stabilizationTime = " & stabilizationTime)
writeLine ("; bedTemp = " & bedTemp)
writeLine ("; primeLength = " & primeLength)
writeLine ("; primeAmount = " & primeAmount)
writeLine ("; primeSpeed = " & primeSpeed)
writeLine ("; retractionDistance = " & retractionDistance)
writeLine ("; retractionSpeed = " & retractionSpeed)
writeLine ("; blobHeight = " & blobHeight)
writeLine ("; extrusionAmount = " & extrusionAmount)
writeLine ("; xSpacing = " & xSpacing)
writeLine ("; ySpacing = " & ySpacing)
writeLine ("; startFlow = " & startFlow)
writeLine ("; flowOffset = " & flowOffset)
writeLine ("; flowSteps = " & flowSteps)
writeLine ("; startTemp = " & startTemp)
writeLine ("; tempOffset = " & tempOffset)
writeLine ("; tempSteps = " & tempSteps)
writeLine ("; direction = " & direction)
writeLine ("")

'Create the output
'Header
writeLine ("M104 S" & startTemp & " ; Set Nozzle Temperature")
writeLine ("M140 S" & bedTemp & " ; Set Bed Temperature")
writeLine ("G90")
writeLine ("G28 ; Move to home position")
writeLine ("G0 Z10 ; Lift nozzle")
writeLine ("G21; unit in mm")
writeLine ("G92 E0; reset extruder")
writeLine ("M83; set extruder to relative mode")
writeLine ("M190 S" & bedTemp & " ; Set Bed Temperature & Wait")
writeLine ("M106 S" & Round(fanSpeed * 255 / 100, 0) & " ; Set Fan Speed")

'Check if "Fill Mode" is used
If tempSteps = 1 Then
    tempSteps = Application.WorksheetFunction.RoundUp(flowSteps / Application.WorksheetFunction.RoundDown((bedLength - 2 * bedMargin) / ySpacing, 0), 0)
    flowSteps = Application.WorksheetFunction.RoundDown((bedLength - 2 * bedMargin) / ySpacing, 0)
    tempOffset = 0
End If

'change variables depending on direction
If direction = 1 Then
    bedLength = 0
    bedMargin = bedMargin * -1
    ySpacing = ySpacing * -1
End If

'DoE column
For c = 1 To tempSteps
    'Check if "Fill Mode" is active
    If tempOffset = 0 And c > 1 Then
        startFlow = startFlow + flowSteps * flowOffset
    End If
    'Comment
    writeLine ("")
    writeLine (";####### " & (startTemp + (c - 1) * tempOffset) & "C")
    'Set temp
    writeLine ("G4 S0 ; Dwell")
    writeLine (Replace("M109 R" & (startTemp + (c - 1) * tempOffset), ",", "."))
    
    'Output for each test
    For r = 1 To flowSteps
        'Check if "Fill Mode" is active
        If tempOffset = 0 Then
            If c = tempSteps Then
                If (startFlow + (r - 2) * flowOffset) = endFlow Then
                    Exit For
                End If
            End If
        End If
        'Message
        writeLine ("")
        writeLine (";####### " & (startFlow + (r - 1) * flowOffset) & "mm3/s")
        writeLine ("M117 " & (startTemp + (c - 1) * tempOffset) & "°C // " & (startFlow + (r - 1) * flowOffset) & "mm3/s")
        'Move to start
        writeLine ("G0 X" & (Abs(bedMargin) + ((c - 1) * (primeLength + wipeLength + xSpacing))) & " Y" & ((bedLength - bedMargin) - (r - 1) * ySpacing) & " Z" & (0.5 + blobHeight + 5) & " F" & (movementSpeed * 60))
        writeLine ("G4 S" & stabilizationTime & "; Stabalize")
        writeLine ("G0 Z0.3 ; Drop down")
        writeLine ("G1 X" & (Abs(bedMargin) + primeLength + ((c - 1) * (primeLength + wipeLength + xSpacing))) & " E" & primeAmount & " F" & (primeSpeed * 60) & " ;Prime")
        writeLine ("G1 E" & (-1 * retractionDistance) & " F" & (retractionSpeed * 60) & "; Retract")
        writeLine ("G0 X" & (Abs(bedMargin) + primeLength + wipeLength + ((c - 1) * (primeLength + wipeLength + xSpacing))) & " F" & (movementSpeed * 60) & " ; Wipe")
        writeLine ("G0 Z0.5 ; Lift")
        writeLine ("G1 E" & (retractionDistance) & " F" & (retractionSpeed * 60) & " ; De-Retract")
        'calculate Extrusionspeed
        extrusionSpeed = Round(blobHeight / (extrusionAmount / ((startFlow + (r - 1) * flowOffset) / (Atn(1) * filamentDiameter * filamentDiameter) * 60)), 2)
        writeLine ("G1 Z" & (0.5 + blobHeight) & " E" & extrusionAmount & " F" & extrusionSpeed & " ; Extrude")
        writeLine ("G1 E" & (-1 * retractionDistance) & " F" & (retractionSpeed * 60) & " ; Retract")
        writeLine ("G0 Z" & (0.5 + blobHeight + 5) & "; Lift")
        writeLine ("G0 X" & (Abs(bedMargin) + ((c - 1) * (primeLength + wipeLength + xSpacing))) & " Y" & ((bedLength - bedMargin) - (r - 1) * ySpacing) & " F" & (movementSpeed * 60))
        writeLine ("G92 E0 ; Reset Extruder")
    Next r
Next c


'End G-Code
writeLine ("")
writeLine (";####### End G-Code")
writeLine ("G0 X" & (bedWidth - Abs(bedMargin)) & " Y" & (bedLengthSave - Abs(bedMargin)) & " ; Move to Corner")
writeLine ("M104 S0 T0 ; Turn Off Hotend")
writeLine ("M140 S0 ; Turn Off Bed")
writeLine ("M84")

End Sub
