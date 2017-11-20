@echo off
echo start running.
::title Test
set "dir1=.\input"

echo reading txt files
FOR %%X in ("%dir1%\*.txt") DO (
	echo %%~dpnX.txt
	call set "Myvar=%%Myvar%%,%%~nX.txt"
	
	)
echo %Myvar:~1%
python run.py %Myvar:~1%

cd ..
echo compiling java file...
javac -classpath "./javanlp/libs/fnlp-core-2.1-SNAPSHOT.jar;./javanlp/libs/trove4j-3.0.3.jar;./javanlp/libs/commons-cli-1.2.jar"  ./javanlp/src/test/Test.java
echo compilation done
cd src

java -classpath "../javanlp/src/test/;../javanlp/libs/fnlp-core-2.1-SNAPSHOT.jar;../javanlp/libs/trove4j-3.0.3.jar;../javanlp/libs/commons-cli-1.2.jar" Test %Myvar:~1%


echo Encoding Succeed.


::pause
:::Start
::cls
::echo 1. test loop
::echo 2. Quit
::set /p choice=I choose (1,2):
::if %choice%==1 goto test
::if %choice%==2 exit

:::test
::cls