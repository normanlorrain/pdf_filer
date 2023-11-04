import refs

# difflib.get_close_matches


# def pick_files_result(e: ft.FilePickerResultEvent):
#     if not e.files:
#         print("Cancelled!")
#         return
#     fileDetails = e.files[0]

#     print(f"User opens {fileDetails.name}")
#     nextFile(fileDetails.path)


def nextFile(e=None):
    pass
    # try:
    #     path = next(src.fileIterator)
    # except StopIteration:
    #     dlg = ft.AlertDialog(
    #     title=ft.Text("Last file"), on_dismiss=lambda e: print("Dialog dismissed!")
    #     )
    #     page.dialog = dlg
    #     dlg.open = True
    #     page.update()
    #     src.init()
    #     return

    # global pdfFile
    # pdfFile = pdf.pdf(path )
    # btnMove.disabled = True
    # bntDn.disabled = False
    # bntUp.disabled = False
    # # btn180.disabled = False
    # pageNumber = 0
    # img = ft.Image(
    #     src_base64=pdfFile.get_page(pageNumber),
    #     # width=pdf.width,
    #     # height=pdf.height,
    #     fit=ft.ImageFit.FIT_HEIGHT,
    #     expand=True,
    # )

    # contentRow.controls.pop(0)
    # contentRow.controls.insert(0,img)
    # page.update()

    # name = src.getNameTuple(path)
    # if name:
    #     (last,first) = name
    #     dstCol.current.controls.clear()
    #     dstCol.current.controls.append(ft.Text(f"Name detected: {last}, {first}"))
    #     destination = dst.getName(last,first)
    #     if destination:
    #         dstCol.current.controls.append(ft.Text(f"destination: {destination}", width=300))

    #     dstCol.current.controls.append(ft.Radio(value="letter", label="Letter"))
    #     dstCol.current.controls.append(ft.Radio(value="rx", label="Rx"))
    #     dstCol.current.controls.append(ft.Radio(value="other", label="Other"))
    #     dstCol.current.controls.append(ft.TextField(label="Other"))

    #     dstCol.current.controls.append(ft.Text(util.generateDstName(path)))

    # page.update()
    # pass


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
