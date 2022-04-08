


data.addEventListener("submit", function (e) {

    //Varibles
    let data = document.querySelector('#data');
    let bedWidth = Number(document.querySelector('#bedWidth').value);
    let bedLength = Number(document.querySelector('#bedLength').value);
    let bedMargin = Number(document.querySelector('#bedMargin').value);
    let filamentDiameter = Number(document.querySelector('#filamentDiameter').value);
    let movementSpeed = Number(document.querySelector('#movementSpeed').value);
    let stabilizationTime = Number(document.querySelector('#stabilizationTime').value);
    let bedTemp = Number(document.querySelector('#bedTemp').value);
    let fanSpeed = Number(document.querySelector('#fanSpeed').value);
    let primeLength = Number(document.querySelector('#primeLength').value);
    let primeAmount = Number(document.querySelector('#primeAmount').value);
    let primeSpeed = Number(document.querySelector('#primeSpeed').value);
    let wipeLength = Number(document.querySelector('#wipeLength').value);
    let retractionDistance = Number(document.querySelector('#retractionDistance').value);
    let retractionSpeed = Number(document.querySelector('#retractionSpeed').value);
    let blobHeight = Number(document.querySelector('#blobHeight').value);
    let extrusionAmount = Number(document.querySelector('#extrusionAmount').value);
    let direction = Number(document.querySelector('#direction').value);
    let xSpacing = Number(document.querySelector('#temperatureSpacing').value);
    let ySpacing = Number(document.querySelector('#flowSpacing').value);
    let startFlow = Number(document.querySelector('#startFlow').value);
    let flowOffset = Number(document.querySelector('#flowOffset').value);
    let flowSteps = Number(document.querySelector('#flowSteps').value);
    let endFlow = Number(document.querySelector('#endFlow').value);
    let startTemp = Number(document.querySelector('#startTemp').value);
    let tempOffset = Number(document.querySelector('#tempOffset').value);
    let tempSteps = Number(document.querySelector('#tempSteps').value);
    let endTemp = Number(document.querySelector('#endTemp').value);
    let comment = document.querySelector('#comment');
    let code = document.querySelector('#code');
    let resultado = [];
    let slot = 0;




    e.preventDefault();
    if (tempSteps == 1) {

        tempSteps = Math.ceil(flowSteps / Math.floor((bedLength - 2 * bedMargin) / ySpacing));
        flowSteps = Math.floor((bedLength - 2 * bedMargin) / ySpacing);
        tempOffset = 0;
    }

    if (direction.value == 1) {

        bedLength = 0
        bedMargin = bedMargin * -1
        ySpacing = ySpacing * -1
    }


    for (let i = 1; i <= tempSteps; i++) {
        console.log(i, tempSteps);

        if (tempOffset == 0) {

            startFlow = startFlow + flowSteps * flowOffset;
            console.log(startFlow);

        }

        console.log(` --------####### ${startTemp + (i - 1) * tempOffset} "C"
                      G4 S0 ; Dwell
    
                  M109 R${startTemp + (i - 1) * tempOffset}`
        );

        slot = slot + 1
        resultado[slot] =
            `####### ${startTemp + (i - 1) * tempOffset} C
                        G4 S0; Dwell
                       M109 R${startTemp + (i - 1) * tempOffset}
                       
                       `

        for (j = 1; j < flowSteps; j++) {

            if (tempOffset == 0) {
                if (i == tempSteps) {

                    if (startFlow + (j - 2) * flowOffset == endFlow) {

                    }
                }
            }

            extrusionSpeed = Math.round(blobHeight / (extrusionAmount / ((startFlow + (j - 1) * flowOffset) / (Math.atan(1) * filamentDiameter * filamentDiameter) * 60)), 2)



            console.log(`
            
            
            ####### ${startFlow + (j - 1) * flowOffset} mm3/s
                        M117 ${startTemp + (i - 1) * tempOffset} °C // " ${startFlow + (j - 1) * flowOffset} mm3/s

                        G0 X ${Math.abs(bedMargin) + ((i - 1) * (primeLength + wipeLength + xSpacing))} Y${(bedLength - bedMargin) - (j - 1) * ySpacing} Z${0.5 + blobHeight + 5} F${movementSpeed * 60}
                                
                        G4 S${stabilizationTime}; Stabalize
                        G0 Z0.3; Drop down")
                        G1 X${Math.abs(bedMargin) + primeLength + ((i - 1) * (primeLength + wipeLength + xSpacing))} E${primeAmount} F${(primeSpeed * 60)} ;Prime
                        G1 E${-1 * retractionDistance} F${retractionSpeed * 60}; Retract
                        G0 X${Math.abs(bedMargin) + primeLength + wipeLength + ((i - 1) * (primeLength + wipeLength + xSpacing))} F${movementSpeed * 60}; Wipe
                        G0 Z0.5; Lift")
                        G1 E${retractionDistance} F${retractionSpeed * 60}; De - Retract
                                

                        G1 Z"${0.5 + blobHeight} E${extrusionAmount} F${extrusionSpeed}; Extrude
                        G1 E${-1 * retractionDistance} F${retractionSpeed * 60}; Retract
                        G0 Z${0.5 + blobHeight + 5}; Lift
                        G0 X${Math.abs(bedMargin) + ((i - 1) * (primeLength + wipeLength + xSpacing))} Y${(bedLength - bedMargin) - (j - 1) * ySpacing} F${movementSpeed * 60}
                        G92 E0; Reset Extruder")
                        `);
            slot = slot + 1;
            resultado[slot] =
                `;---------------------------####### ${startFlow + (j - 1) * flowOffset} mm3/s
            M117 ${startTemp + (i - 1) * tempOffset} °C // " ${startFlow + (j - 1) * flowOffset} mm3/s
            G0 X ${Math.abs(bedMargin) + ((i - 1) * (primeLength + wipeLength + xSpacing))} Y${(bedLength - bedMargin) - (j - 1) * ySpacing} Z${0.5 + blobHeight + 5} F${movementSpeed * 60}
            G4 S${stabilizationTime}; Stabalize
            G0 Z0.3; Drop down")
            G1 X${Math.abs(bedMargin) + primeLength + ((i - 1) * (primeLength + wipeLength + xSpacing))} E${primeAmount} F${(primeSpeed * 60)} ;Prime
            G1 E${-1 * retractionDistance} F${retractionSpeed * 60}; Retract
            G0 X${Math.abs(bedMargin) + primeLength + wipeLength + ((i - 1) * (primeLength + wipeLength + xSpacing))} F${movementSpeed * 60}; Wipe
            G0 Z0.5; Lift")
            G1 E${retractionDistance} F${retractionSpeed * 60}; De - Retract
            G1 Z"${0.5 + blobHeight} E${extrusionAmount} F${extrusionSpeed}; Extrude
            G1 E${-1 * retractionDistance} F${retractionSpeed * 60}; Retract
            G0 Z${0.5 + blobHeight + 5}; Lift
            G0 X${Math.abs(bedMargin) + ((i - 1) * (primeLength + wipeLength + xSpacing))} Y${(bedLength - bedMargin) - (j - 1) * ySpacing} F${movementSpeed * 60}
            G92 E0; Reset Extruder")

            `


        }
    }

    code.innerText =
        ` *** CNC Kitchen Auto Flow Pattern Generator 0.93"
*** 02/04/26 Stefan Hermann"
""
Generation Setting
####### Settings
${comment.value}

bedWidth =  ${bedWidth}
bedLength = ${bedLength}
bedMargin =${Math.abs(bedMargin)}
filamentDiameter =${filamentDiameter}
movementSpeed =${movementSpeed}
stabilizationTime =${stabilizationTime}
bedTemp =${bedTemp}
primeLength =${primeLength}
primeAmount =${primeAmount}
primeSpeed =${primeSpeed}
retractionDistance =${retractionDistance}
retractionSpeed =${retractionSpeed}
blobHeight =${blobHeight}
extrusionAmount =${extrusionAmount}
xSpacing =${xSpacing}
ySpacing =${ySpacing}
startFlow =${startFlow}
flowOffset =${flowOffset}
flowSteps =${flowSteps}
startTemp =${startTemp}
tempOffset =${tempOffset}
tempSteps =${tempSteps}
direction =${direction}

M104 S${startTemp} ; Set Nozzle Temperature
M140 S${bedTemp}; Set Bed Temperature
G90
G28 ; Move to home position
G0 Z10 ; Lift nozzle
G21; unit in mm
G92 E0; reset extruder
M83; set extruder to relative mode
M190 S ${bedTemp}; Set Bed Temperature & Wait
M106 S${Math.round(fanSpeed * 255 / 100, 0)} ; Set Fan Speed

${resultado}

`

})
