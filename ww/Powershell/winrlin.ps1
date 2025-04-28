param (
    [string]$TargetIP
)

if (-not $TargetIP) {
    Write-Host "Usage: .\check_os.ps1 <IP_ADDRESS>"
    exit
}

# Ping the target and extract TTL value
$pingResult = Test-Connection -ComputerName $TargetIP -Count 1 -Quiet
if ($pingResult -eq $false) {
    Write-Host "Failed to reach target. Check the IP address."
    exit
}

$ttlValue = (ping -n 1 $TargetIP | Select-String "TTL=").ToString() -match "TTL=(\d+)" | Out-Null
$ttl = $matches[1]

# Determine OS based on TTL value
if ($ttl) {
    if ($ttl -ge 100 -and $ttl -le 128) {
        Write-Host "Likely Windows OS (TTL: $ttl)"
    } elseif ($ttl -ge 50 -and $ttl -le 64) {
        Write-Host "Likely Linux OS (TTL: $ttl)"
    } else {
        Write-Host "Unknown OS (TTL: $ttl)"
    }
} else {
    Write-Host "Unable to retrieve TTL value."
}
