@echo off
echo start comparing

set "dir1=.\input"



FOR %%X in ("%dir1%\*.txt") DO (
	echo %%~dpnX.txt
	call set "Myvar=%%Myvar%%,%%~nX.txt"
	)
echo batch do %Myvar:~1%


:: this code takes feature files and sentence-depen files for each author 
:: generates several plotings
python run_plot.py %Myvar:~1%


::
::FOR %%X in ("%dir%\*.txt") DO (
::	echo %%~nX
::	FOR %%Y in ("%dir%\*.txt") DO (
::		echo %%~nY
::		if NOT %%~nX == %%~nY ( python run_compare.py %%~nX %%~nY )
::	)
::)
