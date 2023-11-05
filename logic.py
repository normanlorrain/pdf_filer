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
    # refs.rgNameMatches.current.content.controls = createMatches(nameTuple)
    radiobuttons = createMatches(nameTuple)

    # refs.rgcNameMatches.current.controls.clear()
    refs.rgcNameMatches.current.controls = radiobuttons
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
    # btnMove.disabled = True
    # page.update()


if __name__ == "__main__":
    pass
