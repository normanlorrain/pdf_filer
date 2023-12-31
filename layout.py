import flet as ft
import refs
import logic
import config

import util


_page = None

SPLASH = "images/wings2.png"
splash = util.findDataFile(SPLASH)


# We need to catch the window close event, so that we can clean up.  It's not automatic, sadly.
def windowEvent(e):
    print(e.data)
    if e.data == "close":
        # if pdfFile:
        #     del pdfFile
        e.page.window_destroy()


defaultDlg = ft.FilePicker(ref=refs.dlgDefault, on_result=logic.onDefaultResult)


def mainWindow(page: ft.Page):
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

    btnNext = ft.TextButton(
        ref=refs.btnNext, text="Next PDF", on_click=logic.nextFile, disabled=False
    )
    bntUp = ft.TextButton(
        ref=refs.btnUp,
        text="PgUp",
        on_click=logic.onPgUp,
        disabled=True,
    )
    bntDn = ft.TextButton(
        ref=refs.btnDown,
        text="PgDn",
        on_click=logic.onPgDown,
        disabled=True,
    )
    txtStatus = ft.Text(ref=refs.txtStatus, value="Ready to start.")
    buttonRow = ft.Row(spacing=0, controls=[btnNext, bntUp, bntDn, txtStatus])
    page.add(buttonRow)

    contentRow = ft.Row(
        width=2000,
        scroll=ft.ScrollMode.ALWAYS,
        controls=[
            ft.Column(
                controls=[
                    ft.Image(ref=refs.imgPDF, src=splash, fit=ft.ImageFit.FIT_WIDTH)  # type: ignore
                ],
                scroll=ft.ScrollMode.ALWAYS,
                width=1000,
            ),
            ft.Column(
                ref=refs.colDestination,
                controls=[
                    ft.Text(ref=refs.txtSrcFileName, value="src filename"),
                    ft.Row(
                        controls=[
                            ft.Text(
                                ref=refs.txtNameDetected,
                                value="Name detected here",
                                weight=ft.FontWeight.BOLD,
                            ),
                            ft.TextField(
                                ref=refs.tfNameEntry,
                                on_change=logic.onNameEntry,
                            ),
                        ]
                    ),
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
                    ft.TextField(
                        ref=refs.tfFileTypeOther, on_change=logic.updateDestination
                    ),
                    ft.Text(ref=refs.txtDstFileName),
                    ft.ElevatedButton(
                        ref=refs.btnMoveFile,
                        text="Move File",
                        on_click=logic.onMoveBtn,
                        disabled=True,
                    ),
                    ft.ElevatedButton(
                        ref=refs.btnDefault,
                        text="Non-patient",
                        on_click=logic.onDefaultBtn,
                        disabled=False,
                    ),
                ],
                alignment=ft.MainAxisAlignment.START,
            ),
        ],
        vertical_alignment=ft.CrossAxisAlignment.START,
        # scroll=ft.ScrollMode.AUTO,
    )
    page.scroll = ft.ScrollMode.AUTO
    page.overlay.extend([defaultDlg])
    page.add(contentRow)
    page.on_resize = page_resize
    page.window_maximized = True
    page.update()


def page_resize(e):
    print("New page size:", e.page.window_width, e.page.window_height)


def radioButtonFileTypes() -> list:
    radioButtonList = list(
        map(
            lambda item: ft.Radio(value=item[1], label=item[0]),
            config.config["TYPES"].items(),
        )
    )
    radioButtonList.append(ft.Radio(value=refs.OTHER, label="other"))
    return radioButtonList


def start():
    ft.app(target=mainWindow)


if __name__ == "__main__":
    start()
