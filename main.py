from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDRaisedButton, MDFillRoundFlatButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.label import MDLabel
from kivymd.uix.selectioncontrol import MDCheckbox
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.core.audio import SoundLoader
from kivy.clock import Clock
import os
import threading
import asyncio
import edge_tts

class NarratorApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Blue"
        self.output_path = "/sdcard/Download/ExpertNarrator_Files"
        if not os.path.exists(self.output_path):
            os.makedirs(self.output_path)
            
        screen = MDScreen()
        layout = BoxLayout(orientation='vertical', padding=30, spacing=20)
        
        # Header
        layout.add_widget(MDLabel(text="EXPERT NARRATOR PRO", halign="center", font_style="H4", theme_text_color="Primary"))
        
        # Input Area
        self.text_input = MDTextField(hint_text="Paste your text here...", multiline=True, mode="fill", fill_color_normal=(0.1, 0.1, 0.1, 1))
        layout.add_widget(self.text_input)
        
        # Filename
        self.filename = MDTextField(hint_text="Project Name", text="My_Audio_1", mode="line")
        layout.add_widget(self.filename)
        
        # Progress & Status
        self.status = MDLabel(text="Ready to Create Magic", halign="center", font_style="Caption")
        layout.add_widget(self.status)
        
        # Action Buttons
        btn_layout = BoxLayout(orientation='horizontal', spacing=20, size_hint_y=None, height="80dp")
        
        self.convert_btn = MDFillRoundFlatButton(text="START CONVERSION", size_hint_x=0.7, font_size="18sp")
        self.convert_btn.bind(on_press=self.start_task)
        
        self.play_btn = MDRaisedButton(text="PLAY", size_hint_x=0.3, md_bg_color=(0.1, 0.8, 0.3, 1), disabled=True)
        self.play_btn.bind(on_press=self.play_file)
        
        btn_layout.add_widget(self.convert_btn)
        btn_layout.add_widget(self.play_btn)
        layout.add_widget(btn_layout)
        
        screen.add_widget(layout)
        return screen

    def start_task(self, *args):
        self.convert_btn.disabled = True
        self.status.text = "Processing... Please wait"
        threading.Thread(target=self.run_tts).start()

    def run_tts(self):
        asyncio.run(self.do_convert())

    async def do_convert(self):
        txt = self.text_input.text
        name = self.filename.text + ".mp3"
        target = os.path.join(self.output_path, name)
        
        # Settings (Defaults for now, can be expanded)
        communicate = edge_tts.Communicate(txt, "ar-EG-SalmaNeural")
        await communicate.save(target)
        
        self.last_file = target
        Clock.schedule_once(self.finish_ui)

    def finish_ui(self, *args):
        self.status.text = "Success! File saved in Downloads"
        self.convert_btn.disabled = False
        self.play_btn.disabled = False
        self.play_file()

    def play_file(self, *args):
        if hasattr(self, 'last_file'):
            sound = SoundLoader.load(self.last_file)
            if sound: sound.play()

if __name__ == "__main__":
    NarratorApp().run()
