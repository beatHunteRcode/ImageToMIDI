import playmidi
import image_to_midi as im
import PySimpleGUI as sg
import os.path

file_list_column = [
    [
        sg.Text("Image Folder"),
        sg.In(size=(25, 1), enable_events=True, key="-FOLDER-"),
        sg.FolderBrowse(),
    ],
    [
        sg.Listbox(
            values=[], enable_events=True, size=(40, 20),
            key="-FILE LIST-"
        )
    ],
]

image_viewer_column = [
    [sg.Text("Chose an image from the list of the left")],
    [sg.Text(size=(60, 1), key="-TOUT-")],
    [sg.Image(key="-IMAGE-")],
    [
        sg.Button(
            button_text="Play", enable_events=True, size=(20, 1),
            key="-BUTTON-"
        )
    ],
]

layout = [
    [
        sg.Column(file_list_column),
        sg.VSeparator(),
        sg.Column(image_viewer_column),
    ]
]


def create_GUI():
    window = sg.Window("Image to MIDI", layout)
    filename = ""
    while True:
        event, values = window.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            break
        if event == "-FOLDER-":
            folder = values["-FOLDER-"]
            try:
                file_list = os.listdir(folder)
            except:
                file_list = []

            fnames = [
                f
                for f in file_list
                if os.path.isfile(os.path.join(folder, f))
                and f.lower().endswith((".png"))
            ]
            window["-FILE LIST-"].update(fnames)
        elif event == "-FILE LIST-":
            try:
                filename = os.path.join(
                    values["-FOLDER-"], values["-FILE LIST-"][0]
                )
                window["-TOUT-"].update(filename)
                window["-IMAGE-"].update(filename=filename)
            except:
                pass
        elif event == "-BUTTON-":
            try:
                result = im.image_to_midi(filename)
                im.write(result, name="audio.mid")
                print(filename + " playing")
                playmidi.play("audio.mid")
            except:
                print(filename + " not found")
    window.close()

if __name__ == '__main__':
    create_GUI()
