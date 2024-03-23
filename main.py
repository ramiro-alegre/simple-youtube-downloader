import flet as ft
from pytube import YouTube

link_text_field = ft.TextField(
    label="Enter link"
)

container = ft.Container(
    ft.Column([
        ft.Container(
          ft.Text("Youtube downloader",size = 30),
          alignment=ft.alignment.center  
        ),
        ft.Container(
            link_text_field,
        )
        ], 
        width = 500
    ),
    alignment=ft.alignment.center
)


def main(page: ft.Page):
    page.title = "Youtube downloader"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.MainAxisAlignment.CENTER
    page.window_max_height = 1000
    page.window_max_width = 1000
    
    def show_message(msg:str, is_error:bool):
        page.snack_bar = ft.SnackBar(ft.Text(msg))
        if is_error:
            page.snack_bar.bgcolor = ft.colors.RED_100
        else:
            page.snack_bar.bgcolor = ft.colors.GREEN_100
        page.snack_bar.open = True
        page.update()
    
    def download(e):
        youtubeObj = YouTube(e.control.value)
        stream = youtubeObj.streams.filter(res='720p').first()
        if stream is None:
            print("doesn't have 720p video")
            stream = youtubeObj.streams.get_highest_resolution()
        file_size = stream.filesize / (1024**2)
        print(file_size)
        print(stream.title.strip())
        if file_size > 25:
            show_message(msg="The result file is very large, more than 25mb", is_error=True)
            return
        try:
            stream.download(output_path='.')
        except Exception as e:
            show_message(msg='something wrong', is_error=True)
    
    link_text_field.on_change = download
    
    page.add(
        container
    )

ft.app(target=main)