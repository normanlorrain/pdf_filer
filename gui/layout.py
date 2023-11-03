import flet as ft
import gui.logic as logic

_page = None
# References to the fields so we can update them
imgPDF = ft.Ref[ft.Image]()
colDestination = ft.Ref[ft.Column]()  # The right-hand column, containing these:
txtNameDetected = ft.Ref[ft.Text]()  #     - The
rgNameMatches = ft.Ref[ft.RadioGroup]()
rgFileType = ft.Ref[ft.RadioGroup]()
tfFileTypeOther = ft.Ref[ft.TextField]()
txtDstFileName = ft.Ref[ft.Text]()


# We need to catch the window close event, so that we can clean up.  It's not automatic, sadly.
def windowEvent(e):
    print(e.data)
    if e.data == "close":
        # if pdfFile:
        #     del pdfFile
        e.page.window_destroy()


def mainWindow(
    page: ft.Page, onNextBtn=None, onPgUp=None, onPgDown=None, onMoveBtn=None
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
            ft.Image(ref=imgPDF),
            ft.Column(
                ref=colDestination,
                controls=[
                    ft.Text(ref=txtNameDetected, value="Name detected here"),
                    ft.RadioGroup(ref=rgNameMatches),
                    ft.RadioGroup(ref=rgFileType),
                    ft.TextField(ref=tfFileTypeOther),
                    ft.Text(ref=txtDstFileName, value="Final filename here"),
                    ft.ElevatedButton("Move File", on_click=onMoveBtn),
                ],
                alignment=ft.MainAxisAlignment.START,
            ),
        ],
        vertical_alignment=ft.CrossAxisAlignment.START,
    )

    page.add(contentRow)

    page.update()

    def on_message(msg):
        print(msg)
        page.update()

    page.pubsub.subscribe(on_message)  # type: ignore
    print("sending")
    page.pubsub.send_all("Test Messsage")  # type: ignore
    print("Sent")


if __name__ == "__main__":
    import threading

    ft.app(target=mainWindow)
    # thread = threading.Thread(target=ft.app, kwargs={"target": mainWindow})
    # thread.start()
    # print("thread started")
    # _page.pubsub.send_all("Sending from outside thread")
    # thread.join()
