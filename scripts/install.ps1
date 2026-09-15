$ErrorActionPreference = "Stop"
Set-Location (Split-Path $PSScriptRoot -Parent)
Write-Host "== Modern Network installer =="
if (-not (Get-Command docker -ErrorAction SilentlyContinue)) {
  Write-Error "Install Docker Desktop first."
}
if (-not (Test-Path ".env")) { Copy-Item ".env.example" ".env" }
if (Test-Path "scripts/new-secret.sh") {
  try { bash scripts/new-secret.sh } catch { Write-Host "Generate VELOCITY_SECRET in .env if bash is missing." }
}
Write-Host "Starting stack..."
docker compose up -d --build
Write-Host ""
Write-Host "Java:          localhost:25565"
Write-Host "Bedrock:       localhost:19132"
Write-Host "Website/store: http://localhost:8080"
Write-Host "Admin console: http://localhost:8080/console"
