foreach ($file in Get-ChildItem *.typ)
{
    # Write-Output -NoEnumerate $file
    typst compile  $file
}