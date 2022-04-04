#!/usr/bin/env python
# coding: utf-8

# Extrusion System Benchmark

# Copyright (c) Julian Schill <j.schill@web.de>
# All rights reserved.
# Licensed under the MIT license. See LICENSE file in the project root for details.

from extrusionsystembenchmark import esb
from settings import esb_settings
    
def main():
    esb_generator = esb.generator()
    gcode = esb_generator.generate_gcode(esb_settings)

    f = open(esb_settings.outputFilename, "w")
    f.write(gcode)
    f.close

if __name__ == "__main__":
    main()
