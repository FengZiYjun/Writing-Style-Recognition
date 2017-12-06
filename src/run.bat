@echo off
echo start running.
::title Test
set "dir1=.\input"

:: ------------------------------------Encoding-----------------------------

echo start Encoding

FOR %%X in ("%dir1%\*.txt") DO (
	echo %%~dpnX.txt
	call set "Myvar=%%Myvar%%,%%~nX.txt"
	)
echo batch do %Myvar:~1%

:: This code will generate feature files for each author
:: and cleaned text for each author
python run.py %Myvar:~1%

cd ..
cd javanlp
:: java program should run at javanlp/

echo compiling java file...
javac -classpath "./libs/fnlp-core-2.1-SNAPSHOT.jar;./libs/trove4j-3.0.3.jar;./libs/commons-cli-1.2.jar"  ./src/test/Test.java
echo compilation done

:: this code takes the cleaned text and generates sentence-dependency files for each author
:: and the encoded files for each author.
java -classpath "./src/test/;./models/;./libs/fnlp-core-2.1-SNAPSHOT.jar;./libs/trove4j-3.0.3.jar;./libs/commons-cli-1.2.jar" Test %Myvar:~1%


echo Encoding Succeed.

cd ..
cd src





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