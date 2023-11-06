from pathlib import Path
import flet as ft
from flet_core.control_event import ControlEvent
import refs
import src
import dst
import pdf


def createMatches(nameTuple) -> list:
    last, first = nameTuple
    matches = dst.getCloseNames(last, first)
    return list(map(lambda match: ft.Radio(value=match[1], label=match[0]), matches))


def nextFile(e: ControlEvent | None):
    pass
    try:
        path = next(src.fileIterator)
        if not src.filename_nameTuple_dict[path]:
            src.scanFile(path)
        nameTuple = src.filename_nameTuple_dict[path]
    except StopIteration:
        dlg = ft.AlertDialog(
            title=ft.Text("Last file"), on_dismiss=lambda e: print("Dialog dismissed!")
        )
        if e:
            e.page.dialog = dlg
            dlg.open = True
            e.page.update()
        src.init()
        return
    refs.txtSrcFileName.current.value = path
    pdfFile = pdf.pdf(path)
    refs.imgPDF.current.src_base64 = pdfFile.get_page(0)
    refs.txtNameDetected.current.value = nameTuple
    radiobuttons = createMatches(nameTuple)
    refs.rgcNameMatches.current.controls = radiobuttons
    refs.rgNameMatches.current.value = None
    refs.txtDstFileName.current.value = "Final filename here"
    refs.btnMoveFile.current.disabled = True
    # updateFinal(e)
    if e:
        e.page.update()


# def pageImage(pageNumber):
def onPgDown(e):
    pass


def onPgUp(e):
    pass
    # global img
    # pageNumber = pdfFile.changePage(down)
    # page.controls.pop()
    # img = pageImage(pageNumber)
    # page.add(img)

    # page.update()


def onMoveBtn(e):
    print(
        f"Logic: Move file: {refs.txtSrcFileName.current.value} , {refs.rgNameMatches.current.value}"
    )

    # pdfFile.save()

    refs.btnMoveFile.current.disabled = True
    e.page.update()


def onMatchSelection(e):
    print(f"Match selected: {refs.rgNameMatches.current.value}")
    updateFinal(e)
    e.page.update()
    pass


def onTypeSelection(e):
    print(f"Type selected: {refs.rgFileType.current.value}")
    updateFinal(e)
    e.page.update()
    pass


def updateFinal(e):
    if e:
        e.page.update()
    refs.btnMoveFile.current.disabled = True

    # The Radio Gruop value for mached name has the destination folder
    dstFolder = refs.rgNameMatches.current.value

    # The Radio Gruop value selected type contains the format string
    nameFormat = refs.rgFileType.current.value

    if dstFolder == None or nameFormat == None:
        refs.txtDstFileName.current.value = (
            "Complete the match / type selection first!!!"
        )
        refs.btnMoveFile.current.disabled = True

        return
    other = refs.tfFileTypeOther.current.value

    if refs.txtSrcFileName.current.value == None:
        refs.txtDstFileName.current.value = "NO SOURCE FILE SELECTED"
        refs.btnMoveFile.current.disabled = True
        return
    srcName = Path(refs.txtSrcFileName.current.value)
    srcDate = dst.generateDstDate(srcName.name)

    dstName = Path(
        nameFormat.format(date=srcDate, other=refs.tfFileTypeOther.current.value)
    )

    dstPath = Path(dstFolder).joinpath(dstName.with_suffix(srcName.suffix))

    refs.txtDstFileName.current.value = str(dstPath)
    refs.btnMoveFile.current.disabled = False
    e.page.update()


if __name__ == "__main__":
    pass
