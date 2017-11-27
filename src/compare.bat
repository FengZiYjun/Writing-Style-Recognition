@echo off
echo start comparing

set "dir=.\input"

:: compare two by two

FOR %%X in ("%dir%\*.txt") DO (
	echo %%~nX
	FOR %%Y in ("%dir%\*.txt") DO (
		echo %%~nY
		if NOT %%~nX == %%~nY ( python run_compare.py %%~nX %%~nY )
	)
)
