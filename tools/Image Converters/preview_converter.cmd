@echo off
cls
setlocal

:: --- Configuration --->

:: Temp-/Infofile path/name
set info="%cd%\info.txt"

:: IrfanView
set iview=C:\IrfanView\i_view64.exe

:: Image Magick
set imagick_convert=C:\ImageMagick\convert.exe

:: File extensions
set filext=.png
:: <--- Configuration ---

echo Storing Output at %info%

for /r "%cd%\preview_input\" %%a in (*%filext%) do call :EXTRACT "%%a"
goto :END

:EXTRACT
for /F "delims=" %%i in (%1) do set name=%%~ni
set output_file=%cd%\output\%name%_preview%filext%
echo Copy %~1 to %output_file%
xcopy /Y %1 "%output_file%*"
echo Converting %output_file%
"%iview%" "%output_file%" /info=%info%
for /f "tokens=4,6" %%a in ('type %info% ^| find.exe /i "Image dimensions"') do (set /a width=%%a) & (set /a height=%%b)

echo Found Dimensions for %name%%filext%
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
echo   -Scale to new width of: %new_width%
"%imagick_convert%" "%output_file%" -resize %new_width%x%new_width% -depth 16 -quality 100 "%output_file%"

set /a canvas_width=(%multiplier%*250-%new_width%)/2
echo First Canvas Edit:
echo   -Expand All Sides by %canvas_width%
"%imagick_convert%" "%output_file%" -matte -bordercolor none -border %canvas_width%x%canvas_width% "%output_file%"
echo Finished!
goto :EOF

:END
if exist %info% del %info%
PAUSE
endlocal