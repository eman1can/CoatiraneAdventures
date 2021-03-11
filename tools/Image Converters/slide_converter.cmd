@echo off
cls
setlocal

:: --- Configuration --->

:: Temp-/Infofile path/name
set info=%temp%\info.txt

:: IrfanView
set iview=C:\IrfanView\i_view64.exe

:: Image Magick
set imagick_convert=C:\ImageMagick\convert.exe

:: File extensions
set filext=*.png

:: <--- Configuration ---

for /r %cd%\slide_input\ %%a in (%filext%) do call :EXTRACT "%%a"
goto :END

:EXTRACT
"%iview%" %1 /info="%info%"

for /f "tokens=4,6" %%a in ('type %info% ^| find.exe /i "Image dimensions"') do (set /a width=%%a) & (set /a height=%%b)

echo Found Dimensions for %~1
echo Width: %width%, Height: %height%

set /a dig1=%width%/250
set /a temp=%width%*10/250
set /a dig2=%temp%-%dig1%*10
if %dig2% GEQ 2 (
	set /a multiplier=%dig1%+1
) else ( 
	set /a multiplier=%dig1%
)

set /a new_width=%multiplier%*240
echo First Resize:
echo    -Scale to new width of: %new_width%
"%imagick_convert%" %1 -resize %new_width%x -depth 16 -quality 100 %1

set /a canvas_width=(%multiplier%*250-%new_width%)/2
echo First Canvas Edit:
echo   -Expand Sides by %canvas_width%
"%imagick_convert%" %1 -matte -bordercolor none -border %canvas_width%x0 %1

set /a canvas_height=%multiplier%*60
echo Second Canvas Edit:
echo -Expand Top and Bottom by %canvas_height%
"%imagick_convert%" %1 -matte -bordercolor none -border 0x%canvas_height% %1

set /a final_width=250*%multiplier%
set /a final_height=935*%multiplier%
echo Third Canvas Edit:
echo -Expand Bottom until we reach aspect - %final_width%, %final_height%
"%imagick_convert%" %1 -matte -background none -extent %final_width%x%final_height% %1
move "%1" "%cd%\output\%~n1.png"
echo Finished!

goto :EOF

:END
if exist %info% del %info%
PAUSE
endlocal