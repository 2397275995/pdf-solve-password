$ErrorActionPreference = "Stop"

# Avoid hardcoding non-ASCII paths (PowerShell 5 can misread script encoding).
# Use the directory where this script lives.
$baseDir = $PSScriptRoot
$inPath  = Join-Path -Path $baseDir -ChildPath "rockyou.txt"
$outPath = Join-Path -Path $baseDir -ChildPath "rockyou_6digits.txt"

if (-not (Test-Path -LiteralPath $inPath)) {
  throw "Input file not found: $inPath"
}

# Stream processing to avoid loading the huge file into memory
$regex = [regex]'^\d{6}$'

$reader = [System.IO.StreamReader]::new($inPath, [System.Text.Encoding]::UTF8, $true)
$writer = [System.IO.StreamWriter]::new($outPath, $false, [System.Text.Encoding]::UTF8)

$matched = 0L
$total = 0L

try {
  while (($line = $reader.ReadLine()) -ne $null) {
    $total++
    if ($regex.IsMatch($line)) {
      $writer.WriteLine($line)
      $matched++
    }
    if (($total % 2000000) -eq 0) {
      Write-Host ("Processed {0:n0} lines, matched {1:n0}" -f $total, $matched)
    }
  }
}
finally {
  $writer.Dispose()
  $reader.Dispose()
}

Write-Host ("DONE. Processed {0:n0} lines, matched {1:n0}" -f $total, $matched)
Write-Host ("Output: {0}" -f $outPath)

