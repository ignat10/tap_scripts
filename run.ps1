# Run from any directory: & 'C:\tap_scripts\run-main.ps1' -Instance 'LDPlayer'
# Default log names include the instance and launch time.
# Stop with Ctrl+C. A nonzero exit code triggers a restart.
[CmdletBinding()]
param(
    [Parameter(Mandatory = $true, Position = 0)]
    [ValidateNotNullOrEmpty()]
    [string]$Instance,

    [ValidateRange(1, 3600)]
    [int]$RestartDelaySeconds = 5,

    [string]$LogPath
)

$ErrorActionPreference = 'Stop'
$pythonExe = Join-Path $PSScriptRoot '.venv\Scripts\python.exe'
$mainScript = Join-Path $PSScriptRoot 'src\main.py'
foreach ($requiredFile in @($pythonExe, $mainScript)) {
    if (-not (Test-Path -LiteralPath $requiredFile -PathType Leaf)) {
        throw "File not found: $requiredFile"
    }
}

if ([string]::IsNullOrWhiteSpace($LogPath)) {
    $safeInstance = [regex]::Replace($Instance, '[^\p{L}\p{Nd}._-]', '_')
    if ($safeInstance.Length -gt 60) { $safeInstance = $safeInstance.Substring(0, 60) }
    $logDirectory = Join-Path $PSScriptRoot 'logs'
    $logName = '{0}-{1}.log' -f $safeInstance, (Get-Date -Format 'yyyyMMdd-HHmmss')
    $LogPath = Join-Path $logDirectory $logName
}
$LogPath = $ExecutionContext.SessionState.Path.GetUnresolvedProviderPathFromPSPath($LogPath)
$null = New-Item -ItemType Directory -Path (Split-Path -Parent $LogPath) -Force

function Write-RunLog([string]$Message) {
    $line = '[{0}] {1}' -f (Get-Date -Format 'yyyy-MM-dd HH:mm:ss'), $Message
    Add-Content -LiteralPath $LogPath -Value $line -Encoding UTF8 -ErrorAction Stop
    Write-Host $line
}

$oldPythonPath = $env:PYTHONPATH
$oldPythonIoEncoding = $env:PYTHONIOENCODING
$oldConsoleEncoding = [Console]::OutputEncoding
Push-Location -LiteralPath $PSScriptRoot
try {
    Write-Host "Log: $LogPath"
    # main.py also imports src.*; make the project root available to Python.
    $env:PYTHONPATH = $PSScriptRoot
    if ($oldPythonPath) { $env:PYTHONPATH += [IO.Path]::PathSeparator + $oldPythonPath }
    $env:PYTHONIOENCODING = 'utf-8'
    [Console]::OutputEncoding = New-Object System.Text.UTF8Encoding($false)
    # PowerShell 7: handle failures using the process exit code below.
    $PSNativeCommandUseErrorActionPreference = $false

    while ($true) {
        Write-RunLog "Starting main.py; instance=$Instance"
        # Windows PowerShell 5.1 represents redirected stderr as ErrorRecord.
        # Continue lets Python finish and preserves its real exit code.
        $ErrorActionPreference = 'Continue'
        try {
            & $pythonExe -u $mainScript $Instance 2>&1 | ForEach-Object {
                $line = $_.ToString()
                Add-Content -LiteralPath $LogPath -Value $line -Encoding UTF8 -ErrorAction Stop
                Write-Host $line
            }
            $exitCode = $LASTEXITCODE
        }
        finally {
            $ErrorActionPreference = 'Stop'
        }

        if ($exitCode -eq 0) {
            Write-RunLog 'Finished successfully (exit code 0).'
            break
        }
        # Do not restart after a keyboard interrupt.
        if ($exitCode -eq -1073741510 -or $exitCode -eq 130) {
            Write-RunLog "Interrupted (exit code $exitCode)."
            break
        }
        Write-RunLog "Failed (exit code $exitCode). Restarting in $RestartDelaySeconds seconds."
        Start-Sleep -Seconds $RestartDelaySeconds
    }
}
finally {
    $env:PYTHONPATH = $oldPythonPath
    $env:PYTHONIOENCODING = $oldPythonIoEncoding
    [Console]::OutputEncoding = $oldConsoleEncoding
    Pop-Location
}
