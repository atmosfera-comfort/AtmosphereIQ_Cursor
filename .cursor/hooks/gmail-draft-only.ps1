# AtmosphereIQ - Gmail: only drafts, never send.
# beforeMCPExecution / preToolUse: reads stdin JSON, returns permission; does not modify files.

$ErrorActionPreference = 'Stop'

function Read-HookInput {
    # Prefer raw stdin: $input can be empty/unreliable when Cursor launches PowerShell -File.
    $text = [Console]::In.ReadToEnd()
    if (-not [string]::IsNullOrWhiteSpace($text)) {
        return $text.Trim()
    }

    if ($null -ne $input) {
        $fallback = ($input | Out-String).Trim()
        if (-not [string]::IsNullOrWhiteSpace($fallback)) {
            return $fallback
        }
    }

    return ''
}

function Get-NormalizedToolName {
    param($Payload)

    $raw = ''
    if ($null -ne $Payload.tool_name) {
        $raw = [string]$Payload.tool_name
    }
    elseif ($null -ne $Payload.toolName) {
        $raw = [string]$Payload.toolName
    }

    if ([string]::IsNullOrWhiteSpace($raw)) {
        return ''
    }

    $name = $raw.Trim()
    if ($name -match '[:/\\]') {
        $parts = $name -split '[:/\\]'
        $name = $parts[-1]
    }

    return $name.Trim().ToLowerInvariant()
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
    param([hashtable]$Object)

    $json = ConvertTo-AsciiJson -Object $Object
    $utf8 = New-Object System.Text.UTF8Encoding $false
    $bytes = $utf8.GetBytes($json + "`n")
    $stdout = [Console]::OpenStandardOutput()
    $stdout.Write($bytes, 0, $bytes.Length)
}

$denyMessage = [regex]::Unescape('\u041F\u043E \u043F\u0440\u0430\u0432\u0438\u043B\u0430\u043C AtmosphereIQ \u043F\u0438\u0441\u044C\u043C\u0430 \u0442\u043E\u043B\u044C\u043A\u043E \u0447\u0435\u0440\u043D\u043E\u0432\u0438\u043A\u043E\u043C; \u043E\u0442\u043F\u0440\u0430\u0432\u043A\u0443 \u0434\u0435\u043B\u0430\u0435\u0442 \u0447\u0435\u043B\u043E\u0432\u0435\u043A \u043F\u043E\u0441\u043B\u0435 \u043F\u0440\u043E\u0432\u0435\u0440\u043A\u0438 \u0433\u043B\u0430\u0437\u0430\u043C\u0438.')

$sendLikeTools = @(
    'send_message',
    'send_draft',
    'reply_message',
    'forward_message'
)

$draftOkTools = @(
    'create_draft',
    'update_draft'
)

$inputRaw = Read-HookInput
if ([string]::IsNullOrWhiteSpace($inputRaw)) {
    Write-HookJson -Object @{ permission = 'allow' }
    exit 0
}

try {
    $payload = $inputRaw | ConvertFrom-Json
} catch {
    Write-HookJson -Object @{ permission = 'allow' }
    exit 0
}

$toolName = Get-NormalizedToolName -Payload $payload

if ($sendLikeTools -contains $toolName) {
    Write-HookJson -Object @{
        permission    = 'deny'
        user_message  = $denyMessage
        agent_message = $denyMessage
    }
    exit 0
}

if ($draftOkTools -contains $toolName) {
    Write-HookJson -Object @{ permission = 'allow' }
    exit 0
}

# Other Google/MCP tools are out of scope for this guard.
Write-HookJson -Object @{ permission = 'allow' }
exit 0
