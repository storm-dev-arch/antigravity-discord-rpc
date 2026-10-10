@echo off
chcp 65001 >nul
powershell -Command "$procs = Get-CimInstance Win32_Process | Where-Object { $_.CommandLine -like '*rpc_service.py*' }; if ($procs) { Write-Output ('Antigravity Discord RPC is RUNNING (PID: ' + ($procs.ProcessId -join ', ') + ')') } else { Write-Output 'Antigravity Discord RPC is NOT running' }"
echo.
if exist "%~dp0rpc_service.log" (
    echo Last log entries:
    powershell -Command "Get-Content '%~dp0rpc_service.log' -Tail 6"
)
pause