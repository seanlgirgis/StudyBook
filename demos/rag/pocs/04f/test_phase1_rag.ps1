<#
.SYNOPSIS
Interactive Phase 1 RAG tester for POC 04f

.DESCRIPTION
Prompts the user for queries, sends them to /ask endpoint, shows the returned answer,
and prints the latest log entry from outputs/ask_logs.json.
#>

$baseDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
$logsPath = Join-Path $baseDir "outputs\ask_logs.json"

Write-Host "=== Phase 1 RAG Interactive Tester ===`n" -ForegroundColor Cyan

while ($true) {
    $query = Read-Host "Enter query (or type 'exit' to quit)"
    if ($query -eq "exit") { break }

    # Send query to /ask
    try {
        $url = "http://localhost:8000/ask?query=$([System.Web.HttpUtility]::UrlEncode($query))"
        $response = Invoke-RestMethod $url
        Write-Host "`nAnswer:" -ForegroundColor Green
        Write-Host $response.answer
    } catch {
        Write-Host "Error sending query to /ask:" -ForegroundColor Red
        Write-Host $_.Exception.Message
        continue
    }

    # Show latest log entry
    if (Test-Path $logsPath) {
        $logLines = Get-Content $logsPath -Tail 1
        Write-Host "`nLatest log entry:" -ForegroundColor Yellow
        $logLines
    } else {
        Write-Host "`nNo logs found yet." -ForegroundColor Yellow
    }

    Write-Host "`n------------------------------------`n"
}

Write-Host "Exiting Phase 1 RAG tester."