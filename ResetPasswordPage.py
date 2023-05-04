from kivy.core.window import Window
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.lang import Builder
from kivymd.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField
from kivymd.app import MDApp
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton, MDRaisedButton
import mysql.connector

Window.size = (480, 600)


class ResetPasswordPage(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = MDApp.get_running_app()
    
    def reset_password(self):
        # Get the values entered by the user
        username = self.ids.txt_username.text
        password = self.ids.txt_password.text
        confirm_password = self.ids.txt_confirm_password.text
        
        # Check if the username exists in the database
        cnx = mysql.connector.connect(user='root', password='SA9310189666!',
                                      host='localhost',
                                      database='CleanBee')
        cursor = cnx.cursor()
        query = ("SELECT * FROM users WHERE username = %s")
        cursor.execute(query, (username,))
        user = cursor.fetchone()
        
        if user is None:
            cancelbtn = MDFlatButton(text='Retry', on_release=self.close_dialogue)
            self.dialog = MDDialog(title="User Not Found", text="The given username is not registered with us",
                                   size_hint=(0.7, 0.2), buttons=[cancelbtn])
            self.dialog.open()
            cnx.close()
        elif password != confirm_password:
            cancelbtn = MDFlatButton(text='Retry', on_release=self.close_dialogue)
            self.dialog = MDDialog(title="Passwords do not match", text="Please make sure you type the same password",
                                   size_hint=(0.7, 0.2), buttons=[cancelbtn])
            self.dialog.open()
        else:
            # Update the password in the database
            query = ("UPDATE users SET password = %s WHERE username = %s")
            data = (password, username)
            cursor.execute(query, data)
            cnx.commit()
            cancelbtn = MDFlatButton(text='OK', on_release=self.close_dialogue)
            self.dialog = MDDialog(title="Password Updated", text="Password has been updated successfully!",
                                   size_hint=(0.7, 0.2), buttons=[cancelbtn])
            self.dialog.open()
            cnx.close()
    
    def close_dialogue(self, obj):
        self.dialog.dismiss()


class ResetPasswordPageApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Green"
        self.theme_cls.theme_style = "Dark"
        sm=ScreenManager()
        sm.add_widget(ResetPasswordPage(name='resetpasswordpage'))
        return sm

if __name__ == '__main__':
    ResetPasswordPageApp().run()
