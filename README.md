# ExtrusionSystemBenchmark
 A tool that generates G-Code for Hotend benchmarking
 Check this video for more information:
 https://youtu.be/lBi0-NotcP0
# WEB Tool
iFallUpHill created an awesome tool based on my initial work: https://hotend-flow-tester.netlify.app/
GitHub: https://github.com/iFallUpHill/flow-calculator 
# Sample G-Code
 If you're not comfortable using Excel sheets with macros you can find some samples uploaded here:
 https://www.printables.com/model/160335-hotened-benchmark-test-g-codes
 You can find a separate sample evaluation sheet in the files section that doesn't contain any macros.
# Usage
 - Change the settings in on the first worksheet.
 - Generate the G-Code by pressing the button
 - Copy the generated G-Code from the second worksheet into a text file and run it on your printer
# Modes
 - (Normal mode) If more than 1 temperature step is defined, the tool will print with a separate temperature in every column
 - (Fill mode) If only one temperature is defined, the columns will be filled with the flow increments. This is especially handy with printheads that need a lot of clearance (e.g. Prusa Mk3)
