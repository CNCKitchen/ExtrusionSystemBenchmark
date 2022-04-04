import math
from . import gcode

class generator:
    def __init__(self):
        self.settings = None
        self.gcode = gcode.gcode_helper()
        
    def print_header(self):
        self.gcode.comment("*** CNC Kitchen Auto Flow Pattern Generator 0.93")
        self.gcode.comment("*** 02/04/22 Stefan Hermann")
        self.gcode.comment("*** Python Version: 04/04/22 by Julian Schill")
        self.gcode.comment("")

    def print_settings(self):
        #Generation Settings
        self.gcode.comment("####### Settings")
        self.gcode.comment(" {}".format(self.settings.comment))
        self.gcode.comment(" bedWidth = {}".format(self.settings.bedWidth))
        self.gcode.comment(" bedLength = {}".format(self.settings.bedLength))
        self.gcode.comment(" bedMargin = {}".format(abs(self.settings.bedMargin)))
        self.gcode.comment(" filamentDiameter = {}".format(self.settings.filamentDiameter))
        self.gcode.comment(" movementSpeed = {}".format(self.settings.movementSpeed))
        self.gcode.comment(" stabilizationTime = {}".format(self.settings.stabilizationTime))
        self.gcode.comment(" bedTemp = {}".format(self.settings.bedTemp))
        self.gcode.comment(" primeLength = {}".format(self.settings.primeLength))
        self.gcode.comment(" primeAmount = {}".format(self.settings.primeAmount))
        self.gcode.comment(" primeSpeed = {}".format(self.settings.primeSpeed))
        self.gcode.comment(" retractionDistance = {}".format(self.settings.retractionDistance))
        self.gcode.comment(" retractionSpeed = {}".format(self.settings.retractionSpeed))
        self.gcode.comment(" blobHeight = {}".format(self.settings.blobHeight))
        self.gcode.comment(" extrusionAmount = {}".format(self.settings.extrusionAmount))
        self.gcode.comment(" xSpacing = {}".format(self.settings.xSpacing))
        self.gcode.comment(" ySpacing = {}".format(self.settings.ySpacing))
        self.gcode.comment(" startFlow = {}".format(self.settings.startFlow))
        self.gcode.comment(" flowOffset = {}".format(self.settings.flowOffset))
        self.gcode.comment(" flowSteps = {}".format(self.settings.flowSteps))
        self.gcode.comment(" startTemp = {}".format(self.settings.startTemp))
        self.gcode.comment(" tempOffset = {}".format(self.settings.tempOffset))
        self.gcode.comment(" tempSteps = {}".format(self.settings.tempSteps))
        self.gcode.comment(" direction = {}".format(self.settings.direction))
        self.gcode.comment("")

    def do_test(self, x, y, flow, temp):
        self.gcode.flow_and_temp_msg(flow, temp)
        # move in position
        self.gcode.move_xyz(x, y, (0.5 + self.settings.blobHeight + 5), self.settings.movementSpeed)
        self.gcode.stabilize(self.settings.stabilizationTime)
        # prime
        self.gcode.move_z(0.3)
        self.gcode.prime(x, self.settings.primeLength, self.settings.primeAmount, self.settings.primeSpeed, self.settings.retractionDistance, self.settings.retractionSpeed, self.settings.wipeLength, self.settings.movementSpeed)
        # make a blob
        lift_speed=self.gcode.feedrate_from_flow(flow, self.settings.extrusionAmount, self.settings.blobHeight, self.settings.filamentDiameter)
        self.gcode.deretract(self.settings.retractionDistance, self.settings.retractionSpeed)
        self.gcode.make_blob(self.settings.blobHeight, self.settings.extrusionAmount, lift_speed)
        self.gcode.retract(self.settings.retractionDistance, self.settings.retractionSpeed )
        self.gcode.move_z(0.5 + self.settings.blobHeight + 5)
        # move back to wipe
        self.gcode.move_xy(x, y, self.settings.movementSpeed)
        self.gcode.reset_extruder()

    def generate_gcode(self, settings):
        self.settings = settings
        start_flow = self.settings.startFlow
        flow_steps = self.settings.flowSteps

        temp_steps = self.settings.tempSteps
        y_spacing = self.settings.ySpacing

        bed_length = self.settings.bedLength
        bed_margin = self.settings.bedMargin
        test_width = self.settings.primeLength + self.settings.wipeLength + self.settings.xSpacing
        temp_offset = self.settings.tempOffset
        end_flow = self.settings.startFlow+(flow_steps-1)*self.settings.flowOffset

        #Check if "Fill Mode" is used
        if self.settings.tempSteps == 1:
            flow_steps = math.floor((bed_length - 2 * bed_margin) / y_spacing)
            temp_steps = math.ceil(self.settings.flowSteps / flow_steps)
            temp_offset = 0

        #change variables depending on direction
        if self.settings.direction == 1:
            bed_length = 0
            bed_margin = -bed_margin
            y_spacing = -y_spacing

        self.print_header()
        self.print_settings()
        self.gcode.start_print(self.settings.startTemp, self.settings.bedTemp, self.settings.fanSpeed)

        for column in range(temp_steps):
            x = abs(bed_margin) + (column * test_width)
            # Check if "Fill Mode" is active
            if temp_offset == 0 and column > 0:
                start_flow = start_flow + flow_steps * self.settings.flowOffset

            temp = self.settings.startTemp + column * temp_offset
            self.gcode.set_extruder_temp(temp)

            for row in range(flow_steps):
                # Check if "Fill Mode" is active
                if temp_offset == 0:
                    if column == temp_steps:
                        if (start_flow + (row - 1) * self.settings.flowOffset) == end_flow:
                            break

                y = (bed_length - bed_margin) - row * y_spacing
                flow = start_flow + row * self.settings.flowOffset
                self.do_test(x,y,flow, temp)

        corner_x = self.settings.bedWidth - abs(bed_margin)
        corner_y = self.settings.bedLength - abs(bed_margin)

        self.gcode.end_print( corner_x, corner_y, self.settings.movementSpeed)

        return self.gcode.get_gcode()
