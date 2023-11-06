from pathlib import Path
import flet as ft
from flet_core.control_event import ControlEvent
import refs
import src
import dst
import pdf
import layout


def alert(text):
    dlg = ft.AlertDialog(
        title=ft.Text(text), on_dismiss=lambda e: print("Dialog dismissed!")
    )
    layout._page.dialog = dlg
    dlg.open = True
    layout._page.update()


def createMatchRadioButtons(nameTuple) -> list:
    last, first = nameTuple
    matches = dst.getCloseNames(last, first)
    return list(map(lambda match: ft.Radio(value=match[1], label=match[0]), matches))


def nextFile(e: ControlEvent | None):
    pass
    try:
        path = src.getNextFile()
        if not src.filename_nameTuple_dict[path]:
            src.scanFile(path)
        nameTuple = src.filename_nameTuple_dict[path]
    except StopIteration:
        alert("Last file!")
        src.init()
        return
    refs.txtSrcFileName.current.value = path
    global currentFile
    pdf.currentFile = pdf.pdf(path)
    refs.imgPDF.current.src_base64 = pdf.currentFile.get_page()

    # Set toobar buttons
    if pdf.currentFile.page_count > 1:
        refs.btnDown.current.disabled = False
        refs.btnUp.current.disabled = False
    else:
        refs.btnDown.current.disabled = True
        refs.btnUp.current.disabled = True

    # Set working fields
    refs.txtNameDetected.current.value = nameTuple
    refs.rgNameMatches.current.value = ""  # IMPORTANT
    refs.rgcNameMatches.current.controls = createMatchRadioButtons(nameTuple)
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
    print(
        f"Logic: Move file: {refs.txtSrcFileName.current.value} , {refs.txtDstFileName.current.value}"
    )

    srcFile = Path(refs.txtSrcFileName.current.value)
    dstFile = Path(refs.txtDstFileName.current.value)

    if dstFile.exists():
        alert(e, "Destination exists")
        return

    srcFile.rename(dstFile)

    refs.btnMoveFile.current.disabled = True

    refs.txtSrcFileName.current.value = None
    refs.imgPDF.current.src_base64 = None
    nextFile(e)
    e.page.update()


def onMatchSelection(e):
    print(f"Match selected: {refs.rgNameMatches.current.value}")
    updateDestination(e)
    e.page.update()
    pass


def onTypeSelection(e):
    print(f"Type selected: {refs.rgFileType.current.value}")
    updateDestination(e)
    e.page.update()
    pass


def updateDestination(e):
    refs.btnMoveFile.current.disabled = True

    # The Radio Gruop value for mached name has the destination folder
    dstFolder = refs.rgNameMatches.current.value

    # The Radio Gruop value selected type contains the format string
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


if __name__ == "__main__":
    pass
