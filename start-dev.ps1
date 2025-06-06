# Start the development environment for both backend and frontend

Write-Host "Starting AI Website Builder Development Environment..." -ForegroundColor Green

# Start backend in one terminal
$backendJob = Start-Process -FilePath "powershell.exe" -ArgumentList "-Command cd C:\projects\Ai-Website-Builder\backend; python main.py" -PassThru

# Start frontend in another terminal
$frontendJob = Start-Process -FilePath "powershell.exe" -ArgumentList "-Command cd C:\projects\Ai-Website-Builder\frontend; npm run dev" -PassThru

Write-Host "Development servers are running!" -ForegroundColor Green
Write-Host "Backend: http://localhost:8000" -ForegroundColor Cyan
Write-Host "Frontend: http://localhost:5173" -ForegroundColor Cyan
Write-Host "Press Ctrl+C to stop all servers..." -ForegroundColor Yellow

try {
    # Keep the script running until Ctrl+C
    Wait-Process -InputObject $backendJob
} catch {
    Write-Host "`nShutting down development environment..." -ForegroundColor Yellow
} finally {
    # Clean up processes
    if ($backendJob -and -not $backendJob.HasExited) { 
        $backendJob.Kill()
    }
    
    if ($frontendJob -and -not $frontendJob.HasExited) {
        $frontendJob.Kill()
    }
    
    Write-Host "Development environment stopped." -ForegroundColor Red
}
