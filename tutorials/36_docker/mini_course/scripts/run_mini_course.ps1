# Run from mini_course folder:
# ./scripts/run_mini_course.ps1

$ErrorActionPreference = "Stop"

Write-Host "Building docker-mini:1.0..."
docker build -t docker-mini:1.0 ./assets

Write-Host "Running container with data volume..."
docker run --rm -v ${PWD}/assets/data:/data docker-mini:1.0

Write-Host "Done. Check assets/data/output.txt"
