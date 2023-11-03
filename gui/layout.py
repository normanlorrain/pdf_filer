import flet as ft
import refs
import logic

_page = None


# We need to catch the window close event, so that we can clean up.  It's not automatic, sadly.
def windowEvent(e):
    print(e.data)
    if e.data == "close":
        # if pdfFile:
        #     del pdfFile
        e.page.window_destroy()


def mainWindow(
    page: ft.Page, onNextBtn=None, onPgUp=None, onPgDown=None, onMoveBtn=logic.onMoveBtn
):
    global _page
    _page = page

    page.window_center()
    page.on_window_event = windowEvent
    page.window_prevent_close = True

    # pick_files_dialog = ft.FilePicker(on_result=pick_files_result)
    # page.overlay.append(pick_files_dialog)

    page.title = "PDF Filer"
    # page.window_width = 85 * 15
    # page.window_height = 110 * 5
    # page.window_resizable = False  # window is not resizable

    btnNext = ft.TextButton(text="Next PDF", on_click=onNextBtn)
    bntUp = ft.TextButton(
        "PgUp",
        on_click=onPgUp,
        disabled=True,
    )
    bntDn = ft.TextButton(
        "PgDn",
        on_click=onPgDown,
        disabled=True,
    )
    buttonRow = ft.Row(spacing=0, controls=[btnNext, bntUp, bntDn])
    page.add(buttonRow)

    contentRow = ft.Row(
        controls=[
            ft.Image(ref=refs.imgPDF),
            ft.Column(
                ref=refs.colDestination,
                controls=[
                    ft.Text(ref=refs.txtSrcFileName, value="src filename"),
                    ft.Text(ref=refs.txtNameDetected, value="Name detected here"),
                    ft.RadioGroup(ref=refs.rgNameMatches),
                    ft.RadioGroup(ref=refs.rgFileType),
                    ft.TextField(ref=refs.tfFileTypeOther),
                    ft.Text(ref=refs.txtDstFileName, value="Final filename here"),
                    ft.ElevatedButton("Move File", on_click=onMoveBtn),
                ],
                alignment=ft.MainAxisAlignment.START,
            ),
        ],
        vertical_alignment=ft.CrossAxisAlignment.START,
    )

    page.add(contentRow)

    page.update()

    # def on_message(msg):
    #     print(msg)
    #     page.update()

    # page.pubsub.subscribe(on_message)  # type: ignore
    # print("sending")
    # page.pubsub.send_all("Test Messsage")  # type: ignore
    # print("Sent")


if __name__ == "__main__":
    ft.app(target=mainWindow)
