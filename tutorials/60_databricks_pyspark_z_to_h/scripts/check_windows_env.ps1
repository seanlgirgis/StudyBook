# Beginner-friendly Windows PowerShell environment checker.
# Reports what exists and what is missing without installing anything.

Write-Host "== Databricks + PySpark Zero-to-Hero: Windows Environment Check =="
Write-Host "Working directory: $(Get-Location)"
Write-Host ""

try {
    Write-Host "[OK] Python active: $(python --version 2>&1)"
} catch {
    Write-Host "[MISSING] Python active: python command not found"
}

try {
    Write-Host "[OK] Java active:"
    java -version 2>&1 | Select-Object -First 2 | ForEach-Object { Write-Host $_ }
} catch {
    Write-Host "[MISSING] Java active: java command not found"
}

if ($env:JAVA_HOME) {
    Write-Host "[OK] JAVA_HOME=$env:JAVA_HOME"
} else {
    Write-Host "[MISSING] JAVA_HOME is not set"
}

Write-Host ""

try {
    python -c "import importlib.util;print('[OK] pyspark import' if importlib.util.find_spec('pyspark') else '[MISSING] pyspark import')"
    python -c "import importlib.util;print('[OK] pytest import' if importlib.util.find_spec('pytest') else '[MISSING] pytest import')"
    python -c "import importlib.util;`nif importlib.util.find_spec('pyspark') is None:`n    print('[SKIP] SparkSession local[*] smoke test: pyspark missing')`nelse:`n    from pyspark.sql import SparkSession`n    s=SparkSession.builder.master('local[*]').appName('sb-win-smoke').getOrCreate()`n    print(f'[OK] SparkSession local[*] smoke PASS: Spark {s.version}')`n    s.stop()"
} catch {
    Write-Host "[FAIL] Python-based import/smoke checks failed: $($_.Exception.Message)"
}
