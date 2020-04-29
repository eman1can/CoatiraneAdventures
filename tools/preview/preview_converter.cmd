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

for /r %1 %%a in (%filext%) do call :EXTRACT "%%a"
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
"%imagick_convert%" %1 -resize %new_width%x%new_width% -depth 16 -quality 100 %1

set /a canvas_width=(%multiplier%*250-%new_width%)/2
echo First Canvas Edit:
echo   -Expand All Sides by %canvas_width%
"%imagick_convert%" %1 -matte -bordercolor none -border %canvas_width%x%canvas_width% %1

echo Finished!
echo \n

goto :EOF

:END
if exist %info% del %info%

endlocal