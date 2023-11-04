import flet as ft
import refs
import src
import pdf


# def pick_files_result(e: ft.FilePickerResultEvent):
#     if not e.files:
#         print("Cancelled!")
#         return
#     fileDetails = e.files[0]

#     print(f"User opens {fileDetails.name}")
#     nextFile(fileDetails.path)


def nextFile(e=None):
    pass
    try:
        path = next(src.fileIterator)
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
    pageNumber = 0
    refs.imgPDF.current.src_base64 = pdfFile.get_page(pageNumber)
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
    print(f"Logic: Move file: {refs.txtSrcFileName.current.value}")
    # pdfFile.save()
    # btnMove.disabled = True
    # page.update()


if __name__ == "__main__":
    pass
