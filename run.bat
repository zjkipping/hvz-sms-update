@echo off
:loop
start cmd.exe /k "python sms_updater.py"
timeout /t 5 >null
title=dontkillme
FOR /F "tokens=2 delims= " %%A IN ('TASKLIST /FI ^"WINDOWTITLE eq dontkillme^" /NH') DO SET tid=%%A
echo %tid%
taskkill /F /IM cmd.exe /FI ^"PID ne %tid%^"
timeout /t 60 >null
goto loop