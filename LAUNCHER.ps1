# Django Task Management System - Quick Launcher
# Double-click this file to start everything

Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing

# Create the main form
$form = New-Object System.Windows.Forms.Form
$form.Text = "Django Task Management System"
$form.Size = New-Object System.Drawing.Size(400, 300)
$form.StartPosition = "CenterScreen"
$form.FormBorderStyle = "FixedDialog"
$form.MaximizeBox = $false

# Title label
$titleLabel = New-Object System.Windows.Forms.Label
$titleLabel.Text = "Task Management System"
$titleLabel.Font = New-Object System.Drawing.Font("Arial", 16, [System.Drawing.FontStyle]::Bold)
$titleLabel.ForeColor = [System.Drawing.Color]::DarkBlue
$titleLabel.Location = New-Object System.Drawing.Point(50, 20)
$titleLabel.Size = New-Object System.Drawing.Size(300, 30)
$form.Controls.Add($titleLabel)

# Status label
$statusLabel = New-Object System.Windows.Forms.Label
$statusLabel.Text = "Ready to start servers..."
$statusLabel.Location = New-Object System.Drawing.Point(50, 80)
$statusLabel.Size = New-Object System.Drawing.Size(300, 20)
$form.Controls.Add($statusLabel)

# Progress bar
$progressBar = New-Object System.Windows.Forms.ProgressBar
$progressBar.Location = New-Object System.Drawing.Point(50, 110)
$progressBar.Size = New-Object System.Drawing.Size(300, 20)
$progressBar.Style = "Continuous"
$form.Controls.Add($progressBar)

# Start button
$startButton = New-Object System.Windows.Forms.Button
$startButton.Text = "Start Servers"
$startButton.Location = New-Object System.Drawing.Point(50, 150)
$startButton.Size = New-Object System.Drawing.Size(120, 40)
$startButton.BackColor = [System.Drawing.Color]::LightGreen
$startButton.Font = New-Object System.Drawing.Font("Arial", 10, [System.Drawing.FontStyle]::Bold)
$form.Controls.Add($startButton)

# Open Browser button
$browserButton = New-Object System.Windows.Forms.Button
$browserButton.Text = "Open App"
$browserButton.Location = New-Object System.Drawing.Point(190, 150)
$browserButton.Size = New-Object System.Drawing.Size(120, 40)
$browserButton.BackColor = [System.Drawing.Color]::LightBlue
$browserButton.Font = New-Object System.Drawing.Font("Arial", 10, [System.Drawing.FontStyle]::Bold)
$browserButton.Enabled = $false
$form.Controls.Add($browserButton)

# URLs label
$urlsLabel = New-Object System.Windows.Forms.Label
$urlsLabel.Text = "Frontend: http://localhost:5173/`nBackend:  http://127.0.0.1:8000/"
$urlsLabel.Location = New-Object System.Drawing.Point(50, 200)
$urlsLabel.Size = New-Object System.Drawing.Size(300, 40)
$urlsLabel.Font = New-Object System.Drawing.Font("Courier New", 8)
$form.Controls.Add($urlsLabel)

# Function to update status
function Update-Status {
    param([string]$Message, [int]$Progress = 0)
    $statusLabel.Text = $Message
    $progressBar.Value = $Progress
    $form.Refresh()
}

# Start button click event
$startButton.Add_Click({
    $startButton.Enabled = $false
    
    # Run the startup script in background
    $job = Start-Job -ScriptBlock {
        Set-Location $using:PWD
        & "$PWD\START_PROJECT.ps1"
    }
    
    # Monitor progress
    Update-Status "Starting servers..." 25
    Start-Sleep -Seconds 2
    
    Update-Status "Backend starting..." 50
    Start-Sleep -Seconds 3
    
    Update-Status "Frontend starting..." 75
    Start-Sleep -Seconds 2
    
    Update-Status "Servers ready!" 100
    $browserButton.Enabled = $true
    $startButton.Text = "Servers Running"
    $startButton.BackColor = [System.Drawing.Color]::LightGreen
    
    # Open browser automatically
    Start-Sleep -Seconds 1
    Start-Process "http://localhost:5173/"
})

# Browser button click event
$browserButton.Add_Click({
    Start-Process "http://localhost:5173/"
})

# Show the form
[void]$form.ShowDialog()
