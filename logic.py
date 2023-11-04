import flet as ft
import refs
import src
import pdf


def nextFile(e=None):
    pass
    try:
        path = next(src.fileIterator)
        nameTuple = src.filename_nameTuple_dict[path]
    except StopIteration:
        dlg = ft.AlertDialog(
            title=ft.Text("Last file"), on_dismiss=lambda e: print("Dialog dismissed!")
        )
        e.page.dialog = dlg
        dlg.open = True
        e.page.update()
        src.init()
        return
    refs.txtSrcFileName.current.value = path
    pdfFile = pdf.pdf(path)
    refs.imgPDF.current.src_base64 = pdfFile.get_page(0)
    refs.txtNameDetected.current.value = nameTuple
    refs.rgNameMatches.current.content = createMatches(nameTuple)
    if e:
        e.page.update()


def createMatches(nameTuple):
    return ft.Column(
        [
            ft.Radio(value="red", label=f"Red{nameTuple}"),
            ft.Radio(value="green", label=f"Green{nameTuple}"),
            ft.Radio(value="blue", label=f"Blue{nameTuple}"),
        ]
    )


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
