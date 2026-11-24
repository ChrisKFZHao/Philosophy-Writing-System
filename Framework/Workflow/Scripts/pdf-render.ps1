# Render PDF pages to PNG with the Windows.Data.Pdf WinRT API.
#
# PowerShell 5.1 cannot await WinRT async calls directly, so the two
# System.WindowsRuntimeSystemExtensions.AsTask helpers are reflected once and
# invoked through .NET Tasks. No native binary is installed, which keeps the
# script compatible with Smart App Control.
[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)][string]$Pdf,
    [Parameter(Mandatory = $true)][string]$Pages,
    [Parameter(Mandatory = $true)][string]$OutDir,
    [int]$Width = 1800
)

$ErrorActionPreference = "Stop"

function Get-PngSize([string]$Path) {
    $bytes = [System.IO.File]::ReadAllBytes($Path)
    if ($bytes.Length -lt 24 -or
        $bytes[0] -ne 0x89 -or $bytes[1] -ne 0x50 -or
        $bytes[2] -ne 0x4E -or $bytes[3] -ne 0x47) {
        throw "renderer did not produce a PNG: $Path"
    }
    $width = ([int]$bytes[16] -shl 24) -bor ([int]$bytes[17] -shl 16) -bor
             ([int]$bytes[18] -shl 8) -bor [int]$bytes[19]
    $height = ([int]$bytes[20] -shl 24) -bor ([int]$bytes[21] -shl 16) -bor
              ([int]$bytes[22] -shl 8) -bor [int]$bytes[23]
    return @($width, $height)
}

try {
    Add-Type -AssemblyName System.Runtime.WindowsRuntime
    $null = [Windows.Data.Pdf.PdfDocument, Windows.Data.Pdf, ContentType = WindowsRuntime]
    $null = [Windows.Data.Pdf.PdfPageRenderOptions, Windows.Data.Pdf, ContentType = WindowsRuntime]
    $null = [Windows.Storage.StorageFile, Windows.Storage, ContentType = WindowsRuntime]
    $null = [Windows.Storage.FileAccessMode, Windows.Storage, ContentType = WindowsRuntime]
    $null = [Windows.Storage.Streams.IRandomAccessStream, Windows.Storage.Streams, ContentType = WindowsRuntime]

    $operationAsTask = $null
    $actionAsTask = $null
    foreach ($method in [System.WindowsRuntimeSystemExtensions].GetMethods()) {
        if ($method.Name -ne "AsTask" -or $method.GetParameters().Count -ne 1) {
            continue
        }
        $parameterType = $method.GetParameters()[0].ParameterType
        if ($parameterType.IsGenericType -and
            $parameterType.GetGenericTypeDefinition().Name -eq 'IAsyncOperation`1' -and
            $method.GetGenericArguments().Count -eq 1) {
            $operationAsTask = $method
        }
        elseif ($parameterType.Name -eq "IAsyncAction") {
            $actionAsTask = $method
        }
    }
    if ($null -eq $operationAsTask -or $null -eq $actionAsTask) {
        throw "could not find the AsTask helpers for WinRT async calls"
    }

    function Await-Operation($Operation, [Type]$ResultType) {
        $asTask = $operationAsTask.MakeGenericMethod($ResultType)
        $task = $asTask.Invoke($null, @($Operation))
        $null = $task.Wait(-1)
        return $task.Result
    }

    function Await-Action($Action) {
        $task = $actionAsTask.Invoke($null, @($Action))
        $null = $task.Wait(-1)
    }

    if (-not (Test-Path -LiteralPath $OutDir)) {
        $null = New-Item -ItemType Directory -Path $OutDir -Force
    }
    $fullPdf = (Resolve-Path -LiteralPath $Pdf).Path
    $fullOut = (Resolve-Path -LiteralPath $OutDir).Path

    $pageNumbers = @()
    foreach ($token in ($Pages -split ",")) {
        $trimmed = $token.Trim()
        if ($trimmed -ne "") {
            $pageNumbers += [int]$trimmed
        }
    }
    if ($pageNumbers.Count -eq 0) {
        throw "no pages were requested"
    }
    if ($Width -lt 1) {
        throw "Width must be positive"
    }

    $file = Await-Operation `
        ([Windows.Storage.StorageFile]::GetFileFromPathAsync($fullPdf)) `
        ([Windows.Storage.StorageFile])
    $document = Await-Operation `
        ([Windows.Data.Pdf.PdfDocument]::LoadFromFileAsync($file)) `
        ([Windows.Data.Pdf.PdfDocument])

    function Render-ToPng($Page, [string]$Png, [int]$DestWidth) {
        if (Test-Path -LiteralPath $Png) {
            Remove-Item -LiteralPath $Png -Force
        }
        $null = New-Item -ItemType File -Path $Png -Force
        $outFile = Await-Operation `
            ([Windows.Storage.StorageFile]::GetFileFromPathAsync($Png)) `
            ([Windows.Storage.StorageFile])
        $stream = Await-Operation `
            ($outFile.OpenAsync([Windows.Storage.FileAccessMode]::ReadWrite)) `
            ([Windows.Storage.Streams.IRandomAccessStream])
        try {
            $options = New-Object Windows.Data.Pdf.PdfPageRenderOptions
            $options.DestinationWidth = [uint32]$DestWidth
            Await-Action ($Page.RenderToStreamAsync($stream, $options))
            $null = Await-Operation ($stream.FlushAsync()) ([bool])
        }
        finally {
            $stream.Dispose()
        }
        return Get-PngSize $Png
    }

    # DestinationWidth is interpreted in device-independent units, and the
    # renderer converts to pixels with the session's display scale (1.5 here).
    # Calibrate on the first page, then render everything at the corrected
    # width so the PNG really is $Width pixels wide.
    $renderWidth = $Width
    $first = $pageNumbers[0]
    if ($first -lt 1 -or $first -gt $document.PageCount) {
        throw "page $first is outside the document (1-$($document.PageCount))"
    }
    $firstPage = $document.GetPage([uint32]($first - 1))
    try {
        $firstPng = Join-Path $fullOut ("p{0:D4}.png" -f $first)
        $probe = Render-ToPng $firstPage $firstPng $Width
    }
    finally {
        $firstPage.Dispose()
    }
    if ($probe[0] -gt 0 -and [Math]::Abs($probe[0] - $Width) -gt 1) {
        $renderWidth = [int][Math]::Max(
            1, [Math]::Round($Width * $Width / $probe[0])
        )
    }

    foreach ($pageNumber in $pageNumbers) {
        if ($pageNumber -lt 1 -or $pageNumber -gt $document.PageCount) {
            throw "page $pageNumber is outside the document (1-$($document.PageCount))"
        }
        $page = $document.GetPage([uint32]($pageNumber - 1))
        try {
            $png = Join-Path $fullOut ("p{0:D4}.png" -f $pageNumber)
            $size = Render-ToPng $page $png $renderWidth
            $line = [ordered]@{
                page   = $pageNumber
                png    = $png
                width  = $size[0]
                height = $size[1]
            }
            Write-Output ($line | ConvertTo-Json -Compress)
        }
        finally {
            $page.Dispose()
        }
    }
}
catch {
    [Console]::Error.WriteLine("pdf-render.ps1: " + $_.Exception.Message)
    exit 1
}
