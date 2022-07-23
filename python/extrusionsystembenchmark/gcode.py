# GCode Helper

# Copyright (c) Julian Schill <j.schill@web.de>
# All rights reserved.
# Licensed under the MIT license. See LICENSE file in the project root for details.

import math

class gcode_helper:
    def __init__(self):
        self.gcode = ""

    def gcode_line(self, line):
        self.gcode += line + '\n'

    def get_gcode(self):
        return self.gcode

    def start_print(self, nozzle_temp, bed_temp, fan_speed):
        self.gcode_line("M104 S{} ; Set Nozzle Temperature".format(nozzle_temp))
        self.gcode_line("M140 S{} ; Set Bed Temperature".format(bed_temp))
        self.gcode_line("G90")
        self.gcode_line("G28 ; Move to home position")
        self.move_z(10)
        self.gcode_line("G21; unit in mm")
        self.reset_extruder()
        self.gcode_line("M83; set extruder to relative mode")
        self.gcode_line("M190 S{} ; Set Bed Temperature & Wait".format(bed_temp))
        self.gcode_line("M106 S{} ; Set Fan Speed".format(int(fan_speed * 255 / 100)))

    def end_print(self, park_position_x, park_position_y, speed):
        self.comment("")
        self.comment("####### End G-Code")
        self.move_xy(park_position_x,park_position_y,speed)
        self.gcode_line("M104 S0 T0 ; Turn Off Hotend")
        self.gcode_line("M140 S0 ; Turn Off Bed")
        self.gcode_line("M84")

    def move_xy(self, x, y, speed):
        self.gcode_line("G0 X{} Y{} F{}".format(x, y , (speed * 60)))

    def move_xyz(self, x, y, z, speed):
        self.gcode_line("G0 X{} Y{} Z{} F{}".format(x,y,z, (speed * 60)))

    def comment(self, comment):
        self.gcode_line(";"+comment)

    def set_extruder_temp(self, temp):
        self.gcode_line("")
        self.comment("####### {}C".format(temp))
        self.gcode_line("G4 S0 ; Dwell")
        self.gcode_line("M109 S{} R{}".format(temp, temp))

    def retract(self, distance, speed):
        self.gcode_line("G1 E{} F{} ; Retract".format((-1 * distance),(speed * 60)))

    def deretract(self, distance, speed):
        self.gcode_line("G1 E{} F{} ; De-Retract".format(distance, speed * 60))

    def move_z(self, z):
        self.gcode_line("G0 Z{}".format(z))

    def stabilize(self, time):
        self.gcode_line("G4 S{}; Stabilize".format(time))

    def prime(self, start, length, amount, prime_speed, retract_distance, retract_speed, wipe_length, wipe_speed):
        self.gcode_line("G1 X{} E{} F{} ; Prime".format(start + length, amount, prime_speed * 60))
        self.retract(retract_distance, retract_speed)
        self.gcode_line("G0 X{} F{} ; Wipe".format(start + length + wipe_length, wipe_speed * 60))
        self.move_z(0.5)

    def make_blob(self, height, extrusion_length, feedrate):
        self.gcode_line("G1 Z{} E{} F{} ; Extrude".format((0.5 + height), extrusion_length, feedrate))

    def reset_extruder(self):
        self.gcode_line( "G92 E0 ; Reset Extruder")

    def flow_and_temp_msg(self, flow, temp):
        self.gcode_line( "")
        self.comment("####### {}mm3/s".format(flow))
        self.gcode_line( "M117 {}C // {}mm3/s".format(temp, flow))
    
    def feedrate_from_flow(self, flow_rate, amount, movement_length, filament_diameter):
        filament_cross_section = math.pi/4.0 * filament_diameter**2 
        extruder_feedrate = flow_rate / filament_cross_section
        extrude_time = amount / extruder_feedrate
        return round((movement_length / extrude_time) * 60, 2)