# cleanup-sam2-containers.ps1

Write-Host "Looking for containers using the sam2-local-2 image..." -ForegroundColor Cyan

# Find and remove containers using the sam2-local-2 image
$containers = docker ps -a --filter "ancestor=sam2-local-2" --format "{{.ID}}"

if ($containers) {
    Write-Host "Found containers to remove:" -ForegroundColor Yellow
    foreach ($container in $containers) {
        Write-Host "Removing container $container..." -ForegroundColor Yellow
        docker rm -f $container
    }
    Write-Host "All containers using sam2-local-2 have been removed." -ForegroundColor Green
} else {
    Write-Host "No containers found using the sam2-local-2 image." -ForegroundColor Green
}

# Check if the image exists
$imageExists = docker images sam2-local-2 --format "{{.Repository}}"

if ($imageExists) {
    Write-Host "Removing sam2-local-2 image..." -ForegroundColor Yellow
    docker rmi -f sam2-local-2
    Write-Host "sam2-local-2 image has been removed." -ForegroundColor Green
} else {
    Write-Host "No sam2-local-2 image found." -ForegroundColor Green
}

Write-Host "Cleanup completed successfully!" -ForegroundColor Cyan