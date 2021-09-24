@echo off
cls
setlocal

:: <id>_<fname>_full.png
:: The file that is displayed on the status page
:: <id>_<fname>_inspect.png
:: The file that is displayed when the image is inspected on the status page
:: <id>_<fname>_bustup.png
:: The image to use for cutin animations
:: <id>_<fname>_slide.png
:: The slide image to use on the preview character slides
:: <id>_<fname>_preview.png
:: The preview image to use in the battle hud
:: <id>_<fname>_slide_support.png
:: The preview image to use in preview character slides

:: Check if full image
set filext=*.png
for /r "%cd%\output\" %%a in (%filext%) do call :EXTRACT "%%a"
goto :END

:EXTRACT
echo got %1
set p_path=%~dp1
set name=%~n1
:: echo path = %p_path%
:: echo %name%

echo %name%|findstr /r ".*_full"
if errorlevel 1 (
	echo %name%|findstr /r ".*_preview"
	if errorlevel 1 (
		echo %name%|findstr /r ".*_slide_support"
		if errorlevel 1 (
			echo %name%|findstr /r ".*_slide"
			if errorlevel 1 (
				echo %name%|findstr /r ".*_bustup"
				if errorlevel 1 (
					echo %name%|findstr /r ".*_inspect"
					if errorlevel 1 (
						echo %name% is not valid
					) else (
						call :INSPECT
					)
				) else (
					call :BUSTUP
				)
			) else (
				call :SLIDE
			)
		) else (
			call :SLIDE_SUPPORT
		)
	) else (
		call :PREVIEW
	)
) else (
	call :FULL
)
:: echo "%cd%\sorted_output\%dir%\%name%.png"
if not exist "%cd%\sorted_output\%dir%" mkdir "%cd%\sorted_output\%dir%"
move "%P_path%%name%.png" "%cd%\sorted_output\%dir%\%name%.png"
GOTO :EOF

:FULL
set dir=%name:~0,-5%
goto :EOF

:SLIDE
set dir=%name:~0,-6%
goto :EOF

:BUSTUP
set dir=%name:~0,-7%
goto :EOF

:PREVIEW
:INSPECT
set dir=%name:~0,-8%
goto :EOF

:SLIDE_SUPPORT
set dir=%name:~0,-14%
goto :EOF



:END
PAUSE
endlocal
