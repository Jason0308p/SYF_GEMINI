@echo off
REM -----------------------------
REM 自動推送三個 Git 專案
REM -----------------------------

REM 設定 commit 訊息
set COMMIT_MSG=Auto commit %date% %time%



REM Project n8n專案
cd /d C:\Users\syf\Desktop\code\vs_code\n8n_project
git add .
git diff --cached --quiet
if errorlevel 1 (
    git commit -m "%COMMIT_MSG%"
) else (
    echo No changes to commit in %cd%
)
git push

REM Project VS code專案
cd /d C:\Users\syf\Desktop\code\vs_code\SYF
git add .
git diff --cached --quiet
if errorlevel 1 (
    git commit -m "%COMMIT_MSG%"
) else (
    echo No changes to commit in %cd%
)
git push
REM Project Gemini專案
cd /d C:\Users\syf\Desktop\my_Gemini_project
git add .
git diff --cached --quiet
if errorlevel 1 (
    git commit -m "%COMMIT_MSG%"
) else (
    echo No changes to commit in %cd%
)
git push

REM Project Pycharm專案
cd /d C:\Users\syf\PycharmProjects\pythonProject
git add .
git diff --cached --quiet
if errorlevel 1 (
    git commit -m "%COMMIT_MSG%"
) else (
    echo No changes to commit in %cd%
)
git push
echo All projects have been pushed!
pause
