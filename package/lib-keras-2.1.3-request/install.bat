@echo off

rem CK installation script for Keras package from ReQuEST @ ASPLOS'18 submission
rem
rem Developer(s):
rem  * Grigori Fursin, dividiti/cTuning foundation
rem

set PACKAGE_LIB_DIR=%INSTALL_DIR%\lib

rem ######################################################################################
echo.
echo Downloading and installing ...
echo.

%CK_PYTHON_PIP_BIN% install --upgrade pip
%CK_PYTHON_PIP_BIN% install easydict joblib image

%CK_PYTHON_PIP_BIN% install --upgrade -r %PACKAGE_DIR%\requirements.txt -t %PACKAGE_LIB_DIR%

cd /D %INSTALL_DIR%\lib
 echo.
 echo Error: installation failed ...
 exit /b 1
)

exit /b 0
