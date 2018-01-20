:: Batch file for testing


set "dir1=.\test"

FOR %%X in ("%dir1%\*.txt") DO (
	echo %%~dpnX.txt
	call set "Myvar=%%Myvar%%,%%~nX.txt"
	)
echo deal with %Myvar:~1%


python test.py %Myvar:~1%

::cd ..
cd javanlp
:: java program should run at javanlp/

echo compiling java file...
javac -classpath "./libs/fnlp-core-2.1-SNAPSHOT.jar;./libs/trove4j-3.0.3.jar;./libs/commons-cli-1.2.jar"  ./src/test/Test.java
echo compilation done

:: this code takes the cleaned text and generates sentence-dependency files for each author
:: and the encoded files for each author.
java -classpath "./src/test/;./models/;./libs/fnlp-core-2.1-SNAPSHOT.jar;./libs/trove4j-3.0.3.jar;./libs/commons-cli-1.2.jar" Test t

echo Encoding Succeed.

cd ..
::cd src


python machine_learning.py %Myvar:~1%