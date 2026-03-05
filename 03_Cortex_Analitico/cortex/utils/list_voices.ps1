try {
    # Carregar o tipo explicitamente
    $Type = [Windows.Media.SpeechSynthesis.SpeechSynthesizer, Windows.Media, ContentType = WindowsRuntime]
    $synth = New-Object Windows.Media.SpeechSynthesis.SpeechSynthesizer
    
    Write-Host "--- VOZES DISPONIVEIS ---"
    $synth.AllVoices | ForEach-Object {
        Write-Host ("# ID: " + $_.Id)
        Write-Host ("# Nome: " + $_.DisplayName)
        Write-Host ("# Lingua: " + $_.Language)
        Write-Host ("--------------------------")
    }
}
catch {
    Write-Error "Falha ao acessar o motor de sintese: $_"
}
