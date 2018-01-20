
@echo off
set "dir1=.\input"

:: ------------------------------------Encoding-----------------------------

echo start Encoding

FOR %%X in ("%dir1%\*.txt") DO (
	echo %%~dpnX.txt
	call set "Myvar=%%Myvar%%,%%~nX.txt"
	)
echo batch do %Myvar:~1%