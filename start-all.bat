@echo off
chcp 65001 > nul
title Cinema Management System - Unit Testing Suite
cd /d "%~dp0"

:MENU
cls
echo ===============================================================================
echo            HE THONG QUAN LY RAP CHIEU PHIM - UNIT TESTING SUITE
echo       Mon hoc: Dam bao chat luong phan mem (Kiem thu phan mem)
echo ===============================================================================
echo.
echo   [1] Chay TAT CA 77 Test Cases (Login + Register + Edit Profile) + Coverage
echo   [2] Chay Unit Test Chuc nang LOGIN (33 TCs)
echo   [3] Chay Unit Test Chuc nang REGISTER (22 TCs)
echo   [4] Chay Unit Test Chuc nang EDIT PERSONAL INFORMATION (22 TCs)
echo   [5] Chay LAN LUOT tung chuc nang va TAM DUNG de chup man hinh
echo   [6] Khoi dong moi truong Docker Services (docker compose up -d)
echo   [0] Thoat
echo.
echo ===============================================================================
set /p opt="Nhap lua chon cua ban [0-6] roi nhan Enter: "

if "%opt%"=="1" goto RUN_ALL
if "%opt%"=="2" goto RUN_LOGIN
if "%opt%"=="3" goto RUN_REGISTER
if "%opt%"=="4" goto RUN_EDIT_PROFILE
if "%opt%"=="5" goto RUN_STEP_BY_STEP
if "%opt%"=="6" goto RUN_DOCKER
if "%opt%"=="0" goto EXIT
echo Lua chon khong hop le! Vui long thu lai.
pause
goto MENU

:RUN_ALL
cls
echo ===============================================================================
echo [1/1] DANG CHAY TOAN BO 77 UNIT TEST CASES VA DO COVERAGE...
echo ===============================================================================
echo.
cd /d "%~dp0auth-service"
call npx jest --verbose --coverage
cd /d "%~dp0"
echo.
echo ===============================================================================
echo Da chay xong toan bo 77 Test Cases!
echo Ban co the chup man hinh danh sach Pass va bang Coverage o tren.
echo ===============================================================================
pause
goto MENU

:RUN_LOGIN
cls
echo ===============================================================================
echo DANG CHAY UNIT TEST CHUC NANG: LOGIN (33 Test Cases)
echo ===============================================================================
echo.
cd /d "%~dp0auth-service"
call npx jest src/__tests__/authController.login.test.ts --verbose --coverage
cd /d "%~dp0"
echo.
echo ===============================================================================
echo Hoan thanh 33 Test Cases chuc nang Login! Ban co the chup man hinh ngay.
echo ===============================================================================
pause
goto MENU

:RUN_REGISTER
cls
echo ===============================================================================
echo DANG CHAY UNIT TEST CHUC NANG: REGISTER (22 Test Cases)
echo ===============================================================================
echo.
cd /d "%~dp0auth-service"
call npx jest src/__tests__/authController.register.test.ts --verbose --coverage
cd /d "%~dp0"
echo.
echo ===============================================================================
echo Hoan thanh 22 Test Cases chuc nang Register! Ban co the chup man hinh ngay.
echo ===============================================================================
pause
goto MENU

:RUN_EDIT_PROFILE
cls
echo ===============================================================================
echo DANG CHAY UNIT TEST CHUC NANG: EDIT PERSONAL INFORMATION (22 Test Cases)
echo ===============================================================================
echo.
cd /d "%~dp0auth-service"
call npx jest --config jest.editProfile.config.cjs --verbose --coverage
cd /d "%~dp0"
echo.
echo ===============================================================================
echo Hoan thanh 22 Test Cases Edit Profile! Ban co the chup man hinh ngay.
echo ===============================================================================
pause
goto MENU

:RUN_STEP_BY_STEP
cls
echo ===============================================================================
echo BIEU DIEN LAN LUOT TUNG CHUC NANG CHO VIEC CHUP MAN HINH
echo ===============================================================================
echo.
echo >>> BUOC 1: CHAY CHUC NANG LOGIN (33 TCs)...
echo.
cd /d "%~dp0auth-service"
call npx jest src/__tests__/authController.login.test.ts --verbose --coverage
echo.
echo [CHUP ANH 1]: Chup danh sach PASS va bang Coverage cua Login o tren.
pause

cls
echo >>> BUOC 2: CHAY CHUC NANG REGISTER (22 TCs)...
echo.
cd /d "%~dp0auth-service"
call npx jest src/__tests__/authController.register.test.ts --verbose --coverage
echo.
echo [CHUP ANH 2]: Chup danh sach PASS va CheckDB/Rollback cua Register o tren.
pause

cls
echo >>> BUOC 3: CHAY CHUC NANG EDIT PERSONAL INFORMATION (22 TCs)...
echo.
cd /d "%~dp0auth-service"
call npx jest --config jest.editProfile.config.cjs --verbose --coverage
echo.
echo [CHUP ANH 3]: Chup danh sach PASS va Coverage 100%% cua Edit Profile o tren.
pause

cd /d "%~dp0"
goto MENU

:RUN_DOCKER
cls
echo ===============================================================================
echo DANG KHOI DONG DOCKER COMPOSE SERVICES...
echo ===============================================================================
cd /d "%~dp0"
docker compose up -d
echo.
docker compose ps
pause
goto MENU

:EXIT
exit
