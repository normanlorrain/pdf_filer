import flet as ft


# References to the fields so we can access & update them
imgPDF = ft.Ref[ft.Image]()
colDestination = ft.Ref[ft.Column]()  # The right-hand column, containing these:
txtSrcFileName = ft.Ref[ft.Text]()  #      - The name of the original file
txtNameDetected = ft.Ref[ft.Text]()  #      - The patient name detected in the file
rgNameMatches = ft.Ref[ft.RadioGroup]()  #  - Selectable matches for that name.
rgFileType = ft.Ref[ft.RadioGroup]()  #     - Selectable type for this file
tfFileTypeOther = ft.Ref[ft.TextField]()  # - Other type of file
txtDstFileName = ft.Ref[ft.Text]()  #       - The destination file name
