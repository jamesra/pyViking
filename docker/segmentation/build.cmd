@echo off
REM Get the current date in YYYY-MM-DD format for cache busting
for /f "tokens=2 delims==" %%I in ('wmic os get localdatetime /format:list') do set datetime=%%I
set CACHE_DATE=%datetime:~0,4%-%datetime:~4,2%-%datetime:~6,2%

REM Build the Docker image with the current date as the CACHE_DATE build argument
echo Building Docker image with CACHE_DATE=%CACHE_DATE%
docker build -t sam2-local-2 --pull -f Dockerfile.prod --build-arg CACHE_DATE=%CACHE_DATE% .
