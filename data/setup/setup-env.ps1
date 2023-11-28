$pythonVer = New-Object System.Version(3, 11, 3)
$pipPackages = [ordered]@{
    "pydantic" = New-Object System.Version(1, 10, 7);
    "black" = New-Object System.Version(23, 3, 0);
    "click" = New-Object System.Version(8, 1, 3);
    "colorama" = New-Object System.Version(0, 4, 6);
    "debugpy" = New-Object System.Version(1, 6, 7);
    "flake8" = New-Object System.Version(6, 0, 0);
    "mccabe" = New-Object System.Version(0, 7, 0);
    "mypy" = New-Object System.Version(1, 3, 0);
    "mypy-extensions" = New-Object System.Version(1, 0, 0);
    "packaging" = New-Object System.Version(23, 0, 0);
    "pathspec" = New-Object System.Version(0, 11, 1);
    "platformdirs" = New-Object System.Version(3, 2, 0);
    "pycodestyle" = New-Object System.Version(2, 10, 0);
    "pyflakes" = New-Object System.Version(3, 0, 1);
    "pyproject-flake8" = New-Object System.Version(6, 0, 0);
    "PyYAML" = New-Object System.Version(6, 0, 0);
    "tomli" = New-Object System.Version(2, 0, 1);
    "typing_extensions" = New-Object System.Version(4, 5, 0);
    "rich" = New-Object System.Version(13, 7, 0);
}

Write-Output "Starting setup for Candybox(Python)"

# Output the name and version of the Python and package to be installed
Write-Output "Targets:"
Write-Output ("  Python=={0}" -f $pythonVer)
foreach ($pkg in $pipPackages.GetEnumerator()) {
    Write-Output ("  {0}=={1}" -f $pkg.Key, $pkg.Value)
}
Write-Output ""

$rootDir = Convert-Path .

$dataDir = Join-Path $rootDir "data"
$binDir = Join-Path $dataDir "bin"

# Set the location of this script to the current directory
$setupDir = (Get-Item $MyInvocation.MyCommand.Path).DirectoryName
Set-Location $setupDir

$nuGetExe = Join-Path $binDir "nuget.exe"
$CandyboxEnvDir = Join-Path $env:LOCALAPPDATA "Candybox"
$pythonDir = Join-Path $CandyboxEnvDir "python"
$pythonPath = Join-Path $CandyboxEnvDir "python\\tools\\python.exe"

function InstallPython {
    # Installing Python
    # `nuget.exe install python -Version 3.11.3 -ExcludeVersion -OutputDirectory .\deploy`
    $psi = New-Object System.Diagnostics.ProcessStartInfo
    $psi.FileName = $nuGetExe
    $psi.Arguments = "install python -Version {0} -ExcludeVersion -OutputDirectory ""{1}""" -f $pythonVer.ToString(3), $CandyboxEnvDir
    $psi.UseShellExecute = $false
    $psi.CreateNoWindow = $false
    $p = [System.Diagnostics.Process]::Start($psi)
    $p.WaitForExit()

    # Add python to PATH
    $Env:Path = $pythonDir + ";" + $Env:Path

    # Updating pip
    # `python -m pip install --upgrade pip`
    $p = Start-Process -FilePath $pythonPath -ArgumentList "-m pip install --upgrade pip --no-warn-script-location" -NoNewWindow -Wait

    # Installing packages with pip
    foreach ($pkg in $pipPackages.GetEnumerator()) {
        $p = Start-Process -FilePath $pythonPath -ArgumentList ("-m pip install {0}=={1}" -f $pkg.Key, $pkg.Value.ToString(3)) -NoNewWindow -Wait
    }
}

if (Test-Path $pythonDir) {
    Remove-Item $pythonDir -Recurse -Force
}

InstallPython

Write-Output "Completed setup for Candybox (Python)"
