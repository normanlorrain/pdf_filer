import flet as ft
import pdf
import src
import dst
import util
# difflib.get_close_matches

pdfFile = None

# References to the fields so we can update them
dstCol = ft.Ref[ft.Column]()               # The right-hand column, containing these:
nameDetected = ft.Ref[ft.Text]()           #     - The 
matchRadio = ft.Ref[ft.RadioGroup]()
fileType = ft.Ref[ft.RadioGroup]()
fileTypeOther = ft.Ref[ft.TextField]()
dstName = ft.Ref[ft.Text]()



# We need to catch the window close event, so that we can clean up.  It's not automatic, sadly.
def page_window(e):
    global pdfFile

    print(e.data)
    if e.data == "close":
        if pdfFile:
            del pdfFile
        e.page.window_destroy()


def main(page: ft.Page):
    page.window_center()
    page.on_window_event = page_window
    page.window_prevent_close = True


    # def pick_files_result(e: ft.FilePickerResultEvent):
    #     if not e.files:
    #         print("Cancelled!")
    #         return
    #     fileDetails = e.files[0]

    #     print(f"User opens {fileDetails.name}")
    #     nextFile(fileDetails.path)

    def nextFile(e= None):

        try:
            path = next(src.fileIterator)
        except StopIteration:
            dlg = ft.AlertDialog(
            title=ft.Text("Last file"), on_dismiss=lambda e: print("Dialog dismissed!")
            )
            page.dialog = dlg
            dlg.open = True
            page.update()
            src.init()
            return



        global pdfFile
        pdfFile = pdf.pdf(path )
        btnMove.disabled = True
        bntDn.disabled = False
        bntUp.disabled = False
        # btn180.disabled = False
        pageNumber = 0
        img = ft.Image(
            src_base64=pdfFile.get_page(pageNumber),
            # width=pdf.width,
            # height=pdf.height,
            fit=ft.ImageFit.FIT_HEIGHT,
            expand=True,
        )

        contentRow.controls.pop(0)
        contentRow.controls.insert(0,img)
        page.update()

        name = src.getNameTuple(path)
        if name:
            (last,first) = name
            dstCol.current.controls.clear()
            dstCol.current.controls.append(ft.Text(f"Name detected: {last}, {first}"))
            destination = dst.getName(last,first)
            if destination:
                dstCol.current.controls.append(ft.Text(f"destination: {destination}", width=300))

            dstCol.current.controls.append(ft.Radio(value="letter", label="Letter"))
            dstCol.current.controls.append(ft.Radio(value="rx", label="Rx"))
            dstCol.current.controls.append(ft.Radio(value="other", label="Other"))
            dstCol.current.controls.append(ft.TextField(label="Other"))

            dstCol.current.controls.append(ft.Text(util.generateDstName(path)))




        page.update()
        pass
        

    # def pageImage(pageNumber):
        
    def changePage(down=False):
        global img
        pageNumber = pdfFile.changePage(down)
        page.controls.pop()
        img = pageImage(pageNumber)
        page.add(img)

        page.update()


    def move(foo):
        print("Saving file")
        pdfFile.save()
        btnMove.disabled = True
        page.update()

    # pick_files_dialog = ft.FilePicker(on_result=pick_files_result)
    # page.overlay.append(pick_files_dialog)

    page.title = "PDF Filer"
    page.window_width = 85 * 5  # pdf.width
    page.window_height = 110 * 5  # pdf.height
    # page.window_resizable = False  # window is not resizable

    btnNext = ft.TextButton(text="Next PDF", on_click=nextFile )
    btnMove = ft.TextButton("Move", on_click=move, disabled=True)
    bntUp = ft.TextButton(
        "PgUp", on_click=lambda _: changePage(down=False), disabled=True
    )
    bntDn = ft.TextButton(
        "PgDn", on_click=lambda _: changePage(down=True), disabled=True
    )
    # btn180 = ft.TextButton("180", on_click=rotate, disabled=True)

    buttonRow = ft.Row(spacing=0, controls=[btnNext, btnMove, bntUp, bntDn])
    page.add(buttonRow)


    img = ft.Image(None)
    # txtList = ft.Text("destinations go here", bgcolor="#eeeeee", expand=True)
    
    radios = ft.Column(ref=dstCol, controls= None,alignment=ft.MainAxisAlignment.START )
    # radioGroup = ft.RadioGroup(content = rgc )

    contentRow = ft.Row( controls = [img, radios], vertical_alignment=ft.CrossAxisAlignment.START)
    
    page.add(contentRow)

    page.update()

    nextFile()

def start():
    ft.app(target=main)

if __name__ == "__main__":
    src.init()
    dst.init()
    start()