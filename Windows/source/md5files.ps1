#PowerShell script to generate a file that contains the MD5 hash of all
# the files in each subdirectory.
#
# https://web1.cs.wright.edu/~pmateti/Courses/233/Labs/Scripting/bashVsPowerShellTable.html
#
# 11 july 2019
# 
# Digitization Program Office, 
# OCIO,
# Smithsonian Institution
#
$script_title = "DPO MD5 Utility for Windows"
$ver = "0.1"
$vercheck = "https://raw.githubusercontent.com/Smithsonian/MD5_tool/master/md5toolversion.txt"
$repo = "https://github.com/Smithsonian/MD5_tool/"
$lic = "Available under the Apache 2.0 License"

Add-Type -AssemblyName System.Windows.Forms

#Check for updates
$scriptver = (New-Object System.Net.WebClient).Downloadstring($vercheck)

if (-NOT ([string]::Join("", $ver, "`n") -eq $scriptver)){
  [System.Windows.Forms.MessageBox]::Show("$script_title ver. $ver`n$repo`n$lic`n`nThis version is outdated. Please download the updated version at: $repo", 'Update Required')
  exit
}else{
  [System.Windows.Forms.MessageBox]::Show("$script_title ver. $ver`n$repo`n$lic`n`nIn the next window select the top folder to generate the MD5 files", 'Info')
}

#Ask for a directory, C: as default
# From https://www.powershellmagazine.com/2013/06/28/pstip-using-the-system-windows-forms-folderbrowserdialog-class/
$FolderBrowser = New-Object System.Windows.Forms.FolderBrowserDialog -Property @{
    SelectedPath = 'C:\'
}
 
[void]$FolderBrowser.ShowDialog()



#Exclude extensions
Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing

$form = New-Object System.Windows.Forms.Form
$form.Text = 'File extensions to skip'
$form.Size = New-Object System.Drawing.Size(300,200)
$form.StartPosition = 'CenterScreen'

$OKButton = New-Object System.Windows.Forms.Button
$OKButton.Location = New-Object System.Drawing.Point(75,120)
$OKButton.Size = New-Object System.Drawing.Size(75,23)
$OKButton.Text = 'OK'
$OKButton.DialogResult = [System.Windows.Forms.DialogResult]::OK
$form.AcceptButton = $OKButton
$form.Controls.Add($OKButton)

$label = New-Object System.Windows.Forms.Label
$label.Location = New-Object System.Drawing.Point(10,20)
$label.Size = New-Object System.Drawing.Size(280,40)
$label.Text = 'OPTIONAL: Enter a file extension to skip (e.g.: .xml or .tmp). Leave empty to list all files.'
$form.Controls.Add($label)

$textBox = New-Object System.Windows.Forms.TextBox
$textBox.Location = New-Object System.Drawing.Point(10,80)
$textBox.Size = New-Object System.Drawing.Size(260,20)
$form.Controls.Add($textBox)

$form.Topmost = $true

#Focus form
$form.Add_Shown({$form.Activate(); $textBox.focus()})
$result = $form.ShowDialog()

if ($result -eq [System.Windows.Forms.DialogResult]::OK)
{
    $extx = $textBox.Text
}




#Select output format
Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing

$form = New-Object System.Windows.Forms.Form
$form.Text = 'Select the output format'
$form.Size = New-Object System.Drawing.Size(300,200)
$form.StartPosition = 'CenterScreen'

$OKButton = New-Object System.Windows.Forms.Button
$OKButton.Location = New-Object System.Drawing.Point(75,120)
$OKButton.Size = New-Object System.Drawing.Size(75,23)
$OKButton.Text = 'OK'
$OKButton.DialogResult = [System.Windows.Forms.DialogResult]::OK
$form.AcceptButton = $OKButton
$form.Controls.Add($OKButton)

$CancelButton = New-Object System.Windows.Forms.Button
$CancelButton.Location = New-Object System.Drawing.Point(150,120)
$CancelButton.Size = New-Object System.Drawing.Size(75,23)
$CancelButton.Text = 'Cancel'
$CancelButton.DialogResult = [System.Windows.Forms.DialogResult]::Cancel
$form.CancelButton = $CancelButton
$form.Controls.Add($CancelButton)

$label = New-Object System.Windows.Forms.Label
$label.Location = New-Object System.Drawing.Point(10,20)
$label.Size = New-Object System.Drawing.Size(280,20)
$label.Text = 'Please select a format to print the output:'
$form.Controls.Add($label)

$listBox = New-Object System.Windows.Forms.ListBox
$listBox.Location = New-Object System.Drawing.Point(10,40)
$listBox.Size = New-Object System.Drawing.Size(260,20)
$listBox.Height = 80

[void] $listBox.Items.Add('md5 filename')
[void] $listBox.Items.Add('md5,filename')
[void] $listBox.Items.Add('filename md5')
[void] $listBox.Items.Add('filename,md5')

#Set first as default
$listBox.SelectedItem = $listBox.Items[0]

$form.Controls.Add($listBox)
$form.Topmost = $true
$result = $form.ShowDialog()

if ($result -eq [System.Windows.Forms.DialogResult]::OK)
{
    $md5fmt = $listBox.SelectedItem
}




# Recursively select all directories that contain 1 or more files:
# from https://github.com/CaelanBorowiec/PowerShell-Recursive-Compression-Backup
$dirs = Get-ChildItem -Path $FolderBrowser.SelectedPath -Recurse | where {$_.psiscontainer -AND (Get-ChildItem -File $_.fullName).count -ne 0 }



#Current datetime
$datetime = Get-Date -Format "yyyyMMdd-HHmm"

Foreach ($dir in $dirs)
{
  $name = $dir.name
  $dirpath = $dir.FullName
  
  #Print path
  $dirpath

  #Get the hash of each file in the folder
  $files = Get-ChildItem -File -Path $dirpath
  $outputfile = [string]::Join("", $dirpath, "\", $name, "_", $datetime, ".md5")
  #Delete file if exists
  if (Test-Path $outputfile) {
    Remove-Item -Path $outputfile
  }
  Foreach ($file in $files){
    #Calculate file MD5 hash
    $hash = Get-FileHash $dirpath\$file -Algorithm MD5
    $filehash = $hash.Hash

    #Format output
    if ($md5fmt -eq "md5 filename"){
      $arrayToPrint = $filehash.ToLower(), $file
      $separator = " "
      $output = [string]::Join($separator, $arrayToPrint)
    }elseif($md5fmt -eq "md5,filename"){
      $arrayToPrint = $filehash.ToLower(), $file
      $separator = ","
      $output = [string]::Join($separator, $arrayToPrint)
    }elseif($md5fmt -eq "filename md5"){
      $arrayToPrint = $file, $filehash.ToLower()
      $separator = " "
      $output = [string]::Join($separator, $arrayToPrint)
    }elseif($md5fmt -eq "filename,md5"){
      $arrayToPrint = $file, $filehash.ToLower()
      $separator = ","
      $output = [string]::Join($separator, $arrayToPrint)
    }else{
      #No output format selected
      write-host "`n`nMust select an option for output format. Press any key to close...`n"
      [void][System.Console]::ReadKey($true)
      exit
    }

    $fileext = [System.IO.Path]::GetExtension($file)
    #Don't hash md5 files
    if (-NOT ($fileext -eq ".md5")){
      #Skip files with extension to exclude
      if (-NOT ($fileext -eq $extx)){
        $output
        $output | out-file -filepath $outputfile -append
      }
    }
  }
}

write-host "`n`nProcess complete. Press any key to close...`n"
[void][System.Console]::ReadKey($true)
