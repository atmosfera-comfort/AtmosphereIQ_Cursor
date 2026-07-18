# AtmosphereIQ daily report reminder on sessionStart.
# Safe reminder only: does not modify files or spreadsheets.
# Russian text is stored as Base64 UTF-8 to avoid PowerShell encoding issues on Windows.

$ErrorActionPreference = 'Stop'

function Get-EffectiveHour {
    $demoPath = Join-Path $PSScriptRoot 'DEMO_TIME.txt'
    if (Test-Path -LiteralPath $demoPath) {
        $demoRaw = (Get-Content -LiteralPath $demoPath -Raw -ErrorAction SilentlyContinue)
        if (-not [string]::IsNullOrWhiteSpace($demoRaw)) {
            $demoValue = $demoRaw.Trim()
            if ($demoValue -eq '16' -or $demoValue -eq '17') {
                return [int]$demoValue
            }
        }
    }

    return [int](Get-Date).Hour
}

function Decode-Utf8Base64 {
    param([string]$Base64)
    return [System.Text.Encoding]::UTF8.GetString([Convert]::FromBase64String($Base64))
}

function ConvertTo-AsciiJson {
    param([hashtable]$Object)

    $json = ($Object | ConvertTo-Json -Compress)
    $sb = New-Object System.Text.StringBuilder
    foreach ($ch in $json.ToCharArray()) {
        $code = [int]$ch
        if ($code -gt 127) {
            [void]$sb.AppendFormat('\u{0:x4}', $code)
        }
        else {
            [void]$sb.Append($ch)
        }
    }
    return $sb.ToString()
}

function Write-HookJson {
    param([string]$Json)

    $utf8 = New-Object System.Text.UTF8Encoding $false
    # Trailing newline helps Cursor parse hook stdout reliably on Windows.
    $bytes = $utf8.GetBytes($Json + "`n")
    $stdout = [Console]::OpenStandardOutput()
    $stdout.Write($bytes, 0, $bytes.Length)
}

$msg16 = Decode-Utf8Base64 '0JIg0L/QtdGA0LLQvtC8INC+0YLQstC10YLQtSDQutC+0YDQvtGC0LrQviDRgdC60LDQttC4INC/0L7Qu9GM0LfQvtCy0LDRgtC10LvRjiDRjdGC0L4g0L3QsNC/0L7QvNC40L3QsNC90LjQtS4gQXRtb3NwaGVyZUlRIC0g0L3QsNC/0L7QvNC40L3QsNC90LjQtSAoMTY6MDAtMTY6NTkpOiDQv9C+0YDQsCDRgdC+0LHRgNCw0YLRjCDQtNC90LXQstC90L7QuSDQvtGC0YfRkdGCLiDQktGL0LfQvtCy0LggU2tpbGwgZGFpbHktc2FsZXMtdG8tc2hlZXQuINCf0L7QutCwINC90LXRgiDQstGB0LXRhSDQv9C+0LvQtdC5IC0g0LIgR29vZ2xlINCi0LDQsdC70LjRhtGDINC90LUg0L/QuNGI0LguINCl0YPQuiDRgtC+0LvRjNC60L4g0L3QsNC/0L7QvNC40L3QsNC10YI6INGB0LDQvCDRhNCw0LnQu9GLINC4INGC0LDQsdC70LjRhtGDINC90LUg0LzQtdC90Y/QuS4='
$msg17 = Decode-Utf8Base64 '0JIg0L/QtdGA0LLQvtC8INC+0YLQstC10YLQtSDQutC+0YDQvtGC0LrQviDRgdC60LDQttC4INC/0L7Qu9GM0LfQvtCy0LDRgtC10LvRjiDRjdGC0L4g0L3QsNC/0L7QvNC40L3QsNC90LjQtS4gQXRtb3NwaGVyZUlRIC0g0L3QsNC/0L7QvNC40L3QsNC90LjQtSAoMTc6MDAg0Lgg0L/QvtC30LbQtSk6INC+0LrQvdC+INGB0LTQsNGH0Lgg0LTQvdC10LLQvdC+0LPQviDQvtGC0YfRkdGC0LAuINCV0YHQu9C4INGG0LjRhNGA0Ysg0LPQvtGC0L7QstGLIC0g0L7QtNC90LAg0YHRgtGA0L7QutCwINC90LAg0LvQuNGB0YIg0JXQttC10LTQvdC10LLQvdC+LiDQptC40YTRgNGLINC90LUg0LLRi9C00YPQvNGL0LLQsNC5LiDQn9C+0YHQu9C1INC30LDQv9C40YHQuCDRh9C10LvQvtCy0LXQuiDQv9GA0L7QstC10YDRj9C10YIg0LPQu9Cw0LfQsNC80LguINCl0YPQuiDRgtC+0LvRjNC60L4g0L3QsNC/0L7QvNC40L3QsNC10YI6INGB0LDQvCDRhNCw0LnQu9GLINC4INGC0LDQsdC70LjRhtGDINC90LUg0LzQtdC90Y/QuS4='

$hour = Get-EffectiveHour
$context = $null

if ($hour -eq 16) {
    $context = $msg16
}
elseif ($hour -ge 17) {
    $context = $msg17
}

if ([string]::IsNullOrWhiteSpace($context)) {
    Write-HookJson -Json '{}'
    exit 0
}

# additional_context -> agent; user_message -> may surface in Cursor UI
$output = @{
    additional_context = $context
    user_message       = $context
}

Write-HookJson -Json (ConvertTo-AsciiJson -Object $output)
exit 0
