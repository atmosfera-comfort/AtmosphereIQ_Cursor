# AtmosphereIQ — напоминание после правки писем клиентам (.md)
# Только читает stdin и возвращает JSON; файлы не изменяет.

$ErrorActionPreference = 'Stop'

function Read-HookInput {
    if ($null -ne $input) {
        $text = ($input | Out-String).Trim()
        if (-not [string]::IsNullOrWhiteSpace($text)) {
            return $text
        }
    }

    return [Console]::In.ReadToEnd()
}

function Get-EditedFilePath {
    param($Payload)

    if ($null -ne $Payload.file_path -and -not [string]::IsNullOrWhiteSpace([string]$Payload.file_path)) {
        return [string]$Payload.file_path
    }

    $toolName = [string]$Payload.tool_name
    if ($toolName -notin @('Write', 'StrReplace')) {
        return $null
    }

    $toolInput = $Payload.tool_input
    if ($null -eq $toolInput) {
        return $null
    }

    if ($toolInput -is [string]) {
        try {
            $toolInput = $toolInput | ConvertFrom-Json
        } catch {
            return $null
        }
    }

    if ($null -ne $toolInput.path -and -not [string]::IsNullOrWhiteSpace([string]$toolInput.path)) {
        return [string]$toolInput.path
    }

    return $null
}

$inputRaw = Read-HookInput
if ([string]::IsNullOrWhiteSpace($inputRaw)) {
    Write-Output '{}'
    exit 0
}

try {
    $payload = $inputRaw | ConvertFrom-Json
} catch {
    Write-Output '{}'
    exit 0
}

$filePath = Get-EditedFilePath -Payload $payload
if ([string]::IsNullOrWhiteSpace($filePath)) {
    Write-Output '{}'
    exit 0
}

$extension = [System.IO.Path]::GetExtension($filePath)
if ($extension.ToLowerInvariant() -ne '.md') {
    Write-Output '{}'
    exit 0
}

$reminder = 'Проверьте письмо клиенту: понятен ли следующий шаг, нет ли сложных терминов, указаны ли контакты.'

$output = @{
    additional_context = "AtmosphereIQ — напоминание после правки Markdown ($filePath): $reminder"
}

$output | ConvertTo-Json -Compress
exit 0