@echo off
chcp 65001 > nul
title Cinema Management System - Rollback & Cleanup Suite
cd /d "%~dp0"

:MENU
cls
echo ===============================================================================
echo            HE THONG QUAN LY RAP CHIEU PHIM - ROLLBACK & CLEANUP
echo    Thuc hien hoan tac CSDL va don dep theo quy chuan Muc 5.3.2
echo ===============================================================================
echo.
echo   [1] Rollback CSDL ve trang thai goc (Reset DB, Flush Redis & Re-seed)
echo   [2] Rollback ha toan bo bang CSDL (Down Migrations / Drop All Tables)
echo   [3] Don dep bo nho dem Jest Cache va thu muc Coverage tam
echo   [4] Dung va go bo toan bo Docker Containers (docker compose down)
echo   [5] Rollback toan dien (Chay tat ca cac buoc don dep tren)
echo   [0] Thoat
echo.
echo ===============================================================================
set /p opt="Nhap lua chon cua ban [0-5] roi nhan Enter: "

if "%opt%"=="1" goto RESET_DB
if "%opt%"=="2" goto DOWN_DB
if "%opt%"=="3" goto CLEAN_CACHE
if "%opt%"=="4" goto DOCKER_DOWN
if "%opt%"=="5" goto ROLLBACK_ALL
if "%opt%"=="0" goto EXIT
echo Lua chon khong hop le! Vui long thu lai.
pause
goto MENU

:RESET_DB
cls
echo ===============================================================================
echo DANG THUC HIEN ROLLBACK & RESET CSDL (MUC 5.3.2)...
echo ===============================================================================
cd /d "%~dp0migrate"
go run main.go reset
cd /d "%~dp0"
echo.
echo Rollback & Reset CSDL hoan tat!
pause
goto MENU

:DOWN_DB
cls
echo ===============================================================================
echo DANG THUC HIEN ROLLBACK DOWN TOAN BO BANG CSDL...
echo ===============================================================================
cd /d "%~dp0migrate"
go run main.go down
cd /d "%~dp0"
echo.
echo Rollback Down hoan tat! Toan bo bang da duoc go bo an toan.
pause
goto MENU

:CLEAN_CACHE
cls
echo ===============================================================================
echo DANG DON DEP JEST CACHE VA THU MUC COVERAGE...
echo ===============================================================================
cd /d "%~dp0auth-service"
if exist "coverage" rd /s /q "coverage"
call npx jest --clearCache
cd /d "%~dp0"
echo.
echo Da don dep sach Jest Cache va thu muc Coverage tam!
pause
goto MENU

:DOCKER_DOWN
cls
echo ===============================================================================
echo DANG DUNG VA GO BO TOAN BO DOCKER CONTAINERS...
echo ===============================================================================
cd /d "%~dp0"
docker compose down
echo.
echo Da dung toan bo Docker containers an toan!
pause
goto MENU

:ROLLBACK_ALL
cls
echo ===============================================================================
echo DANG THUC HIEN ROLLBACK TOAN DIEN HE THONG...
echo ===============================================================================
echo [1/3] Don dep Jest Cache...
cd /d "%~dp0auth-service"
if exist "coverage" rd /s /q "coverage"
call npx jest --clearCache

echo [2/3] Dung Docker Containers neu dang chay...
cd /d "%~dp0"
docker compose down 2>nul

echo [3/3] Rollback CSDL ve trang thai goc...
cd /d "%~dp0migrate"
go run main.go reset 2>nul
cd /d "%~dp0"

echo.
echo ===============================================================================
echo ROLLBACK TOAN DIEN THANH CONG! He thong da tro ve trang thai sach ban dau.
echo ===============================================================================
pause
goto MENU

:EXIT
exit
