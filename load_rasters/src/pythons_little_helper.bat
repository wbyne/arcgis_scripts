@ echo off
REM the @ turns the command echo off, otherwise it'll echo "echo off" on the first line
REM before turning off the echo.  *_WOW_*
if %1==Aerials start "Randome Title Here" "%HOMEDRIVE%%HOMEPATH%\AppData\Roaming\Microsoft\Windows\start Menu\Programs\LizardTech\LizardTech Geoviewer.appref-ms" %2
if %1==Aerials_07 start "Ranmod Title Here" %2
if %1==Record start "Ranmod Title Here" %2

rem echo Here, need input?
rem choice 
rem use choice to ask for a y/n input (forces program to pause so you can see the screen)