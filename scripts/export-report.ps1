$reportPath = (Resolve-Path 'final-report/NeuroPix-Final-Report.docx').Path
$pdfPath = [System.IO.Path]::ChangeExtension($reportPath, '.pdf')
$wordApp = New-Object -ComObject Word.Application
$wordApp.Visible = $false
$wordApp.DisplayAlerts = 0
try {
    $document = $wordApp.Documents.Open($reportPath, $false, $false)
    if ($document.ReadOnly) { throw 'Report opened read-only; refusing to export a stale copy.' }
    $document.Fields.Update() | Out-Null
    foreach ($table in $document.TablesOfContents) { $table.Update() }
    foreach ($table in $document.TablesOfFigures) { $table.Update() }
    $document.Repaginate()
    $document.Save()
    $document.ExportAsFixedFormat($pdfPath, 17)
    Write-Output ('Exported PDF; pages: ' + $document.ComputeStatistics(2))
    $document.Close(0)
} finally {
    $wordApp.Quit()
    [System.Runtime.InteropServices.Marshal]::ReleaseComObject($wordApp) | Out-Null
}
