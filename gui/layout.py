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

def main(page: ft.Page):
    page.window_center()
    page.on_window_event = page_window
    page.window_prevent_close = True

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

