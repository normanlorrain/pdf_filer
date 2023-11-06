import flet as ft
import refs
import logic
import config

_page = None


# We need to catch the window close event, so that we can clean up.  It's not automatic, sadly.
def windowEvent(e):
    print(e.data)
    if e.data == "close":
        # if pdfFile:
        #     del pdfFile
        e.page.window_destroy()


def mainWindow(
    page: ft.Page,
    onNextBtn=logic.nextFile,
    onPgUp=None,
    onPgDown=None,
    onMoveBtn=logic.onMoveBtn,
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
                    ft.Text(value="Candidate matches:"),
                    ft.RadioGroup(
                        ref=refs.rgNameMatches,
                        content=ft.Column(ref=refs.rgcNameMatches),
                        on_change=logic.onMatchSelection,
                    ),
                    ft.Text(value="Type of file:"),
                    ft.RadioGroup(
                        ref=refs.rgFileType,
                        content=ft.Column(
                            ref=refs.rgcFileType, controls=radioButtonFileTypes()
                        ),
                        on_change=logic.onTypeSelection,
                    ),
                    ft.TextField(ref=refs.tfFileTypeOther, on_change=logic.updateFinal),
                    ft.Text(ref=refs.txtDstFileName),
                    ft.ElevatedButton(
                        ref=refs.btnMoveFile,
                        text="Move File",
                        on_click=onMoveBtn,
                        disabled=True,
                    ),
                ],
                alignment=ft.MainAxisAlignment.START,
            ),
        ],
        vertical_alignment=ft.CrossAxisAlignment.START,
    )

    page.add(contentRow)

    page.update()
    logic.nextFile(None)
    page.update()

    # def on_message(msg):
    #     print(msg)
    #     page.update()

    # page.pubsub.subscribe(on_message)  # type: ignore
    # print("sending")
    # page.pubsub.send_all("Test Messsage")  # type: ignore
    # print("Sent")


def radioButtonFileTypes() -> list:
    return list(
        map(
            lambda item: ft.Radio(value=item[1], label=item[0]),
            config.config["TYPES"].items(),
        )
    )


def start():
    ft.app(target=mainWindow)


if __name__ == "__main__":
    start()
