import flet as ft


# References to the fields so we can access & update them
btnNext = ft.Ref[ft.TextButton]()
btnUp = ft.Ref[ft.TextButton]()
btnDown = ft.Ref[ft.TextButton]()
txtStatus = ft.Ref[ft.Text]()

imgPDF = ft.Ref[ft.Image]()
colDestination = ft.Ref[ft.Column]()  # The right-hand column, containing these:
txtSrcFileName = ft.Ref[ft.Text]()  #      - The name of the original file
txtNameDetected = ft.Ref[ft.Text]()  #      - The patient name detected in the file
tfNameEntry = ft.Ref[ft.TextField]()  #     - A place to enter a name manually
rgNameMatches = ft.Ref[ft.RadioGroup]()  #  - Selectable matches for that name.
rgcNameMatches = ft.Ref[ft.Column]()  #      + A column of radio buttons for the matches
rgFileType = ft.Ref[ft.RadioGroup]()  #     - Selectable type for this file
rgcFileType = ft.Ref[ft.Column]()  #         + A column of radio buttons for the type
tfFileTypeOther = ft.Ref[ft.TextField]()  # - Other type of file
txtDstFileName = ft.Ref[ft.Text]()  #       - The destination file name
btnMoveFile = ft.Ref[ft.ElevatedButton]()
btnDefault = ft.Ref[ft.ElevatedButton]()  #   - Putting non-patients in "default" dir
dlgDefault = ft.Ref[ft.FilePicker]()  # File picker


# String used by the file Type radio group.  Need reference to it.
OTHER = "{other} faxed {date}"
