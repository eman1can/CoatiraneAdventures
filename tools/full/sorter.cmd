@echo off
cls
setlocal

:: <id>_<fname>_full.png
:: <id>_<fname>_slide.png
:: <id>_<fname>_preview.png
:: <id>_<fname>_slide_support.png



:: Check if full image
set filext=*.png
for %1 %%f in (%filext%) do call :EXTRACT "%%f"
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
				echo not valid
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
:: echo "%p_path%%dir%\%name%.png"
if not exist "%p_path%%dir%" mkdir "%p_path%%dir%"
move "%P_path%%name%.png" "%p_path%%dir%\%name%.png"

GOTO :EOF

:FULL
set dir=%name:~0,-5%
goto :EOF

:PREVIEW
set dir=%name:~0,-8%
goto :EOF

:SLIDE_SUPPORT
set dir=%name:~0,-14%
goto :EOF

:SLIDE
set dir=%name:~0,-6%
goto :EOF

:END
endlocal
