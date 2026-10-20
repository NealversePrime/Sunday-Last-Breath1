@echo off
title Deploy Sunday: Last Breath to Itch.io
echo ========================================================
echo   Deploying Sunday: Last Breath to Itch.io (HTML5)
echo   Target: nealverse/sundays-last-breath:html5
echo ========================================================
echo.

echo [1/2] Synchronizing passages and code into index.html...
python "%~dp0scratch\sync_all.py"
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Synchronization failed! Aborting deploy.
    pause
    exit /b %ERRORLEVEL%
)

echo.
echo [2/2] Pushing build via Butler...
butler push "%~dp0." nealverse/sundays-last-breath:html5 --ignore "src" --ignore ".git" --ignore "scratch" --ignore ".vscode" --ignore "Wiki" --ignore ".gitattributes" --ignore ".gitignore" --ignore "*.py" --ignore "*.twee" --ignore "*.tw" --ignore "*.yml"
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Butler push failed!
    pause
    exit /b %ERRORLEVEL%
)

echo.
echo ========================================================
echo   Deployment Successful! Check your itch.io dashboard.
echo ========================================================
pause

