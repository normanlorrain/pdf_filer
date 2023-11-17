from pathlib import Path
import flet as ft
from flet_core.control_event import ControlEvent

import refs
import src
import dst
import pdf
import layout
import util


def alert(text: str):
    dlg = ft.AlertDialog(
        title=ft.Text(text), on_dismiss=lambda e: status("Dialog dismissed!")
    )
    layout._page.dialog = dlg
    dlg.open = True
    layout._page.update()


def createMatchRadioButtons(nameTuple) -> list:
    last, first = nameTuple
    matches = dst.getCloseNames(last, first)
    return list(map(lambda match: ft.Radio(value=match[1], label=match[0]), matches))


def nextFile(e: ControlEvent):
    global page
    if e:
        page = e.page
    try:
        path = src.getNextFile()
        pdf.currentFile = pdf.pdf(path, status=status)
        nameTuple = pdf.currentFile.scanForName()
    except StopIteration:
        alert("Last file!")
        src.init()
        return
    refs.txtSrcFileName.current.value = path
    global currentFile
    refs.imgPDF.current.src_base64 = pdf.currentFile.get_page()

    # Set toolbar buttons
    if pdf.currentFile.page_count > 1:
        refs.btnDown.current.disabled = False
        refs.btnUp.current.disabled = False
    else:
        refs.btnDown.current.disabled = True
        refs.btnUp.current.disabled = True

    # Set working fields
    if nameTuple:
        refs.txtNameDetected.current.value = str(nameTuple)
        refs.rgNameMatches.current.value = ""  # IMPORTANT
        refs.rgcNameMatches.current.controls = createMatchRadioButtons(nameTuple)
    else:
        refs.txtNameDetected.current.value = "NONE.  Try manual: "
        refs.rgNameMatches.current.value = ""
        refs.rgcNameMatches.current.controls = None
    refs.txtDstFileName.current.value = "Destination filename here"
    refs.btnMoveFile.current.disabled = True
    if e:
        e.page.update()


# def pageImage(pageNumber):
def onPgDown(e):
    pdf.currentFile.pageDn()
    refs.imgPDF.current.src_base64 = pdf.currentFile.get_page()
    e.page.update()


def onPgUp(e):
    pdf.currentFile.pageUp()
    refs.imgPDF.current.src_base64 = pdf.currentFile.get_page()
    e.page.update()


def onMoveBtn(e):
    refs.btnMoveFile.current.disabled = True
    e.page.update()

    status(
        f"Logic: Move file: {refs.txtSrcFileName.current.value} , {refs.txtDstFileName.current.value}"
    )

    srcFile = Path(str(refs.txtSrcFileName.current.value))
    dstFile = Path(str(refs.txtDstFileName.current.value))

    i = 1
    while dstFile.exists():
        suffix = dstFile.suffix
        stem = dstFile.stem  # e.g. c:\folder\folder\{stem}.pdf
        newStem = util.incrementStem(stem)
        status(f"Destination file exists.  Trying new stem: {newStem}")
        dstFile = dstFile.with_stem(newStem)

    srcFile.rename(dstFile)

    refs.txtSrcFileName.current.value = None
    refs.imgPDF.current.src_base64 = None
    nextFile(e)
    e.page.update()


def onNameEntry(e):
    name = str(refs.tfNameEntry.current.value)
    if "," in name:
        last, first = name.split(",")
    else:
        last, first = name, ""
    refs.rgNameMatches.current.value = ""  # IMPORTANT
    matches = dst.getCloseNames(last.upper(), first)
    refs.rgcNameMatches.current.controls = list(
        map(lambda match: ft.Radio(value=match[1], label=match[0]), matches)
    )
    e.page.update()


def onMatchSelection(e):
    status(f"Match selected: {refs.rgNameMatches.current.value}")
    updateDestination(e)
    e.page.update()
    pass


def onTypeSelection(e):
    status(f"Type selected: {refs.rgFileType.current.value}")
    updateDestination(e)
    e.page.update()
    pass


def updateDestination(e):
    refs.btnMoveFile.current.disabled = True

    # The Radio Group value for matched name has the destination folder
    dstFolder = str(refs.rgNameMatches.current.value)

    # The Radio Group value selected type contains the format string
    nameFormat = refs.rgFileType.current.value

    # validate the destination Radio Button Group has a selection
    if dstFolder == "" or nameFormat == None:
        refs.txtDstFileName.current.value = (
            "Complete the match / type selection first!!!"
        )
        refs.btnMoveFile.current.disabled = True
        return

    # validate the File Type Radio Button Group has a selection
    if refs.txtSrcFileName.current.value == None:
        refs.txtDstFileName.current.value = "NO SOURCE FILE SELECTED"
        refs.btnMoveFile.current.disabled = True
        return

    # Generate the filename.  We need to convert date prefix of the filename
    srcName = Path(refs.txtSrcFileName.current.value)
    srcDate = dst.generateDstDate(srcName.name)

    other = refs.tfFileTypeOther.current.value  # Ignored if not selected.
    dstName = Path(nameFormat.format(date=srcDate, other=other))  # Create name
    dstName = dstName.with_suffix(srcName.suffix)  # Add ".pdf"
    dstFilePath = Path(dstFolder).joinpath(dstName)

    refs.txtDstFileName.current.value = str(dstFilePath)
    refs.btnMoveFile.current.disabled = False
    e.page.update()


def status(text, end=None) -> None:
    global page
    if status._end or status._end == "":
        refs.txtStatus.current.value = str(refs.txtStatus.current.value) + str(text)
    else:
        refs.txtStatus.current.value = str(text)
    status._end = end
    if page:
        page.update()


status._end = None

if __name__ == "__main__":
    pass
