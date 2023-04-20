from kivy.core.window import Window
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.dialog import MDDialog
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDFlatButton, MDRaisedButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.bottomnavigation import MDBottomNavigation, MDBottomNavigationItem
from kivymd.uix.boxlayout import MDBoxLayout
import mysql.connector as mysql

mydb = mysql.connect(
  host="localhost",
  user="root",
  password="password",
  database="CleanBee"
)
mycursor = mydb.cursor()

class ProfileScreen(Screen):
    pass

class WindowManager(ScreenManager):
    pass

Window.size = (480, 600)


class LoginInterface(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = MDApp.get_running_app()

    def login(self):

        username = self.ids.login_username.text
        password = self.ids.login_password.text
        if username == '' or password == '':
            cancelbtn = MDFlatButton(text='Retry', on_release=self.close_dialogue)
            self.dialog = MDDialog(title="Incomplete Details", text="Please fill all fields", size_hint=(0.7, 0.2),
                                   buttons=[cancelbtn])
            self.dialog.open()
            return

        # Check if username and password match
        mycursor.execute("SELECT * FROM Users WHERE username=%s AND password=%s", (username, password))
        result = mycursor.fetchone()
        if result:
            # If match, store the username in App class
            app = MDApp.get_running_app()
            app.username = username
            app.password = password

            # Navigate to the main screen
            self.manager.current = 'mainscreen'
        else:
            cancelbtn = MDFlatButton(text='Retry', on_release=self.close_dialogue)
            self.dialog = MDDialog(title="Invalid Credentials", text="Incorrect username or password",
                                   size_hint=(0.7, 0.2),
                                   buttons=[cancelbtn])
            self.dialog.open()

    def close_dialogue(self, obj):
        self.dialog.dismiss()

    def creator(self):
        # Get the input values
        username = self.ids.signup_username.text
        password = self.ids.signup_password.text
        email = self.ids.signup_email.text
        cname = self.ids.signup_cname.text
        ccode = self.ids.signup_ccode.text

        # Validate that all fields are filled in
        if not all([username, password, email, cname, ccode]):
            cancelbtn = MDFlatButton(text='Retry', on_release=self.close_dialogue)
            self.dialog = MDDialog(title="Incomplete Details", text="Please fill all fields", size_hint=(0.7, 0.2),
                                   buttons=[cancelbtn])
            self.dialog.open()
            return

        # check if user already exists
        mycursor.execute("SELECT * FROM Users WHERE username=%s", (username,))
        result = mycursor.fetchone()
        if result:
            cancelbtn = MDFlatButton(text='Retry', on_release=self.close_dialogue)
            self.dialog = MDDialog(title="User already exists", text="Please try logging in",
                                   size_hint=(0.7, 0.2), buttons=[cancelbtn])
            self.dialog.open()
            return

        # Validate that the company code is correct
        mycursor.execute("SELECT * FROM Companies WHERE CompanyName=%s AND CompanyCode=%s", (cname, ccode))
        result = mycursor.fetchone()
        if not result:
            cancelbtn = MDFlatButton(text='Retry', on_release=self.close_dialogue)
            self.dialog = MDDialog(title="Invalid Company Code", text="The company name and code do not match",
                                   size_hint=(0.7, 0.2), buttons=[cancelbtn])
            self.dialog.open()
            return

        # Insert new user into User table
        insert_query = "INSERT INTO Users (username, email, password, Company, CompanyCode) VALUES (%s, %s, %s, %s, %s)"
        insert_values = (username, email, password, cname, ccode)
        mycursor.execute(insert_query, insert_values)

        # Update the employee count for the specific company code
        update_query = "UPDATE Companies SET EmployeeCount = EmployeeCount + 1 WHERE CompanyCode = %s"
        update_value = (ccode,)
        mycursor.execute(update_query, update_value)

        mydb.commit()

        # Navigate to the main screen
        app = MDApp.get_running_app()
        app.username = username
        app.email = email
        app.cname = cname
        app.ccode = ccode
        app.password = password
        self.manager.current = 'mainscreen'

class MainScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = MDApp.get_running_app()

    def on_enter(self):
        self.ids.profile_layout.clear_widgets()
        username_label = MDLabel(text="Username: " + self.app.username, font_size="20sp", bold=True, halign="center")
        email_label = MDLabel(text="Password: " + self.app.password, font_size="20sp", bold=True, halign="center")
        self.ids.profile_layout.add_widget(username_label)
        self.ids.profile_layout.add_widget(email_label)

class LoginApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Green"
        self.theme_cls.theme_style = "Dark"
        self.username = ""
        self.password = ""
        self.email = ""

        sm = ScreenManager()
        sm.add_widget(LoginInterface(name='loginpage'))
        sm.add_widget(MainScreen(name='mainscreen'))
        sm.add_widget(ProfileScreen(name='profilescreen'))

        return sm

if __name__ == "__main__":
    LoginApp().run()
