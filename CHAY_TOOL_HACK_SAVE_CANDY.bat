@echo off
chcp 65001 >nul
title Candy Crush Saga - Save Game Hack & Booster Editor
color 0D

echo =====================================================================
echo    CANDY CRUSH SAGA - BỘ TOOL HACK MẠNG VÀ TẤT CẢ BÙA HỖ TRỢ
echo =====================================================================
echo.
echo  * Hỗ trợ chỉnh sửa trực tiếp file save_*.dat
echo  * Bơm 65,535 Lượt Mạng (Lives) và tất cả bùa (Lollipop Hammer, Color Bomb,...)
echo  * Hỗ trợ tự động quét tìm save trên Windows PC hoặc kéo/đẩy qua ADB Android
echo.
echo  Đang khởi động giao diện điều khiển (GUI)...
echo.

python "%~dp0candy_save_hack_gui.py"

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [LOI] Co van de xay ra khi chay Python. Vui long kiem tra lai.
    pause
)
