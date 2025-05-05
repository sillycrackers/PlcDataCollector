import ttkbootstrap as ttk

import src.gui.exit_prompt


def change_theme(theme):
    if theme == 'dark':

        style_object = ttk.Style(theme='darkly')

        style_object.configure('TLabelframe.Label', font=('Calibri', 12,))
        style_object.configure('custom.TButton', font=('Calibri', 12,))
        #style_object.configure(style='custom.TFrame', background="#2f2f2f")
        style_object.configure(style='alarm.Treeview', font=('Calibri', 12,), foreground="red", rowheight=20)
        style_object.configure(style='TFrame', bordercolor="#737373")
        style_object.configure(style="TMenubutton", font=('Calibri', 12,))

    elif theme == 'light':

        style_object = ttk.Style(theme='flatly')

        style_object.configure('TLabelframe.Label', font=('Calibri', 12,))
        style_object.configure('custom.TButton', font=('Calibri', 12,))
        style_object.configure(style='alarm.Treeview', font=('Calibri', 12,), foreground="red", rowheight=20)
        style_object.configure(style='TFrame', bordercolor="#737373")
        style_object.configure(style="TMenubutton", font=('Calibri', 12,))


def disable_event(parent):
   src.gui.exit_prompt.ExitPrompt(parent)
