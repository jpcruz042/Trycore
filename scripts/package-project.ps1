param(
    [string]$OutputDirectory = (Split-Path -Parent (Split-Path -Parent $PSScriptRoot))
)

$projectRoot = Split-Path -Parent $PSScriptRoot
$packageName = "Trycore-EVM-Entrega"
$stagingDirectory = Join-Path $env:TEMP $packageName
$zipPath = Join-Path $OutputDirectory "$packageName.zip"
$checksumPath = Join-Path $OutputDirectory "$packageName.zip.sha256"

if (Test-Path $stagingDirectory) {
    Remove-Item $stagingDirectory -Recurse -Force
}
if (Test-Path $zipPath) {
    Remove-Item $zipPath -Force
}
if (Test-Path $checksumPath) {
    Remove-Item $checksumPath -Force
}

New-Item -ItemType Directory -Path $stagingDirectory | Out-Null

Get-ChildItem -LiteralPath $projectRoot -Force | Where-Object {
    $_.Name -notin @('.git', '.vscode', '.env', 'node_modules', 'dist', '.angular') -and
    $_.Name -notmatch '\.(zip|pdf)$' -and
    $_.Name -notmatch '^Trycore-EVM-Entrega.*\.zip$'
} | ForEach-Object {
    Copy-Item -LiteralPath $_.FullName -Destination $stagingDirectory -Recurse -Force
}

Remove-Item (Join-Path $stagingDirectory 'frontend\node_modules') -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item (Join-Path $stagingDirectory 'frontend\dist') -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item (Join-Path $stagingDirectory 'frontend\.angular') -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item (Join-Path $stagingDirectory 'backend\__pycache__') -Recurse -Force -ErrorAction SilentlyContinue
Get-ChildItem -LiteralPath $stagingDirectory -Directory -Recurse -Filter '__pycache__' |
    Remove-Item -Recurse -Force -ErrorAction SilentlyContinue

Compress-Archive -Path (Join-Path $stagingDirectory '*') -DestinationPath $zipPath -CompressionLevel Optimal
Remove-Item $stagingDirectory -Recurse -Force

$hash = (Get-FileHash $zipPath -Algorithm SHA256).Hash.ToLower()
"$hash  $([System.IO.Path]::GetFileName($zipPath))" | Set-Content -LiteralPath $checksumPath -Encoding ASCII

Get-FileHash $zipPath -Algorithm SHA256 | Format-List
Write-Host "Paquete creado: $zipPath"
Write-Host "Checksum creado: $checksumPath"
