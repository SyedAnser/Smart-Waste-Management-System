import requests
from timeit import default_timer as timer
import cProfile
import re
from pympler import tracker
from kivy.core.window import Window
from kivy.uix.screenmanager import Screen, ScreenManager
from kivymd.uix.card import MDCard
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.list import TwoLineIconListItem, IconLeftWidget
from kivymd.uix.button import MDIconButton, MDFloatingActionButton
from kivy.uix.popup import Popup
from kivy.properties import ObjectProperty
from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.material_resources import dp
from kivymd.uix.dialog import MDDialog
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivymd.uix.label import MDLabel, MDIcon
from kivymd.uix.button import MDFlatButton, MDRaisedButton
from kivymd.uix.progressbar import MDProgressBar
from kivymd.uix.textfield import MDTextField
from kivymd.uix.bottomnavigation import MDBottomNavigation, MDBottomNavigationItem
from kivymd.uix.boxlayout import MDBoxLayout
import mysql.connector as mysql

start = timer()

cProfile.run('re.compile("foo|bar")')

tr = tracker.SummaryTracker()
tr.print_diff()

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

Window.size = (590, 600)

class LoginInterface(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = MDApp.get_running_app()

    def forgot_password(self):
        self.manager.current = 'reset_password'

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
        mycursor.execute("SELECT * FROM User WHERE username=%s AND password=%s", (username, password))
        result = mycursor.fetchone()
        if result:
            # If match, store the username in App class
            self.app.username = username
            self.app.password = password
            self.app.email = result[1]
            self.app.cname = result[3]
            self.app.ccode = result[4]

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
        mycursor.execute("SELECT * FROM User WHERE username=%s", (username,))
        result = mycursor.fetchone()
        if result:
            cancelbtn = MDFlatButton(text='Retry', on_release=self.close_dialogue)
            self.dialog = MDDialog(title="User already exists", text="Please try logging in",
                                   size_hint=(0.7, 0.2), buttons=[cancelbtn])
            self.dialog.open()
            return

        # Validate that the company code is correct
        mycursor.execute("SELECT * FROM Company WHERE CompanyName=%s AND CompanyCode=%s", (cname, ccode))
        result = mycursor.fetchone()
        if not result:
            cancelbtn = MDFlatButton(text='Retry', on_release=self.close_dialogue)
            self.dialog = MDDialog(title="Invalid Company Code", text="The company name and code do not match",
                                   size_hint=(0.7, 0.2), buttons=[cancelbtn])
            self.dialog.open()
            return

        # Insert new user into User table
        insert_query = "INSERT INTO User (username, email, password, Company, CompanyCode) VALUES (%s, %s, %s, %s, %s)"
        insert_values = (username, email, password, cname, ccode)
        mycursor.execute(insert_query, insert_values)

        # Update the employee count for the specific company code
        update_query = "UPDATE Company SET NumEmployees = NumEmployees + 1 WHERE CompanyCode = %s"
        update_value = (ccode,)
        mycursor.execute(update_query, update_value)

        mydb.commit()

        # Navigate to the main screen
        self.app.username = username
        self.app.email = email
        self.app.cname = cname
        self.app.ccode = ccode
        self.app.password = password
        self.manager.current = 'mainscreen'

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
        cnx = mysql.connect(user='root', password='SA9310189666!',
                            host='localhost',
                            database='CleanBee')
        cursor = cnx.cursor()
        query = ("SELECT * FROM user WHERE username = %s")
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
            query = ("UPDATE user SET password = %s WHERE username = %s")
            data = (password, username)
            cursor.execute(query, data)
            cnx.commit()
            cancelbtn = MDFlatButton(text='OK', on_release=self.close_dialogue)
            self.dialog = MDDialog(title="Password Updated", text="Password has been updated successfully!",
                                   size_hint=(0.7, 0.2), buttons=[cancelbtn])
            self.dialog.open()
            self.manager.current = 'loginpage'
            cnx.close()

    def close_dialogue(self, obj):
        self.dialog.dismiss()

class MainScreen(Screen):
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        self.app = MDApp.get_running_app()

    def enable_add_button(self, instance, value):
        if value:
            self.ids.button.disabled = False
        else:
            self.ids.button.disabled = True

    def on_enter(self, *args):
        self.overview_layout = BoxLayout(orientation="vertical", padding="10dp",pos_hint={"center_x": 0.5, "top": 1})
        self.overview_layout.clear_widgets()
        self.overview_scrollview = ScrollView(size_hint=(1, 1), size=(Window.width, Window.height))
        self.overview_scrollview.clear_widgets()
        self.profile_layout = BoxLayout(orientation="vertical", padding="10dp", size_hint=(None, None), size=("300dp", "300dp"), pos_hint={"center_x": 0.5, "top": 1})
        self.profile_layout.clear_widgets()
        self.edit_scrollview = ScrollView(size_hint=(1, None), size=(Window.width, Window.height))
        self.edit_scrollview.clear_widgets()
        self.urgent_layout = BoxLayout(orientation="vertical", padding="10dp",pos_hint={"center_x": 0.5, "top": 1})
        self.urgent_layout.clear_widgets()

        self.update_overview_layout()
        self.update_profile()
        self.update_edit_layout()
        self.update_urgent_layout()

    def showpopup(self, message):
        print("function called")
        content = BoxLayout(orientation = "vertical", size_hint_y=None, height=dp(40))
        dustbin_codetf = MDTextField(id="dustbin_code", hint_text="Dustbin Code", required=True)
        dustbin_typetf = MDTextField(id="dustbin_type", hint_text="Dustbin Type (Public/Private)", required=True)
        locationtf = MDTextField(id="location", hint_text="Location", required=True)
        cancelbutton = MDFlatButton(text="Cancel", on_release=self.dismiss)
        addbutton = MDFlatButton(text="Add", on_release=lambda x: self.add_dustbin(dustbin_codetf,dustbin_typetf,locationtf))
        content.add_widget(dustbin_codetf)
        content.add_widget(dustbin_typetf)
        content.add_widget(locationtf)
        content.add_widget(cancelbutton)
        content.add_widget(addbutton)

        self.popup = Popup(title='Add dustbin', content=content, size=(dp(300), dp(300)))
        self.popup.open()

    def dismiss(self,x):
        self.popup.dismiss()

    def add_dustbin(self, dc,dt,l):
        print(dc.text,dt.text,l.text)
        # Add record to Dustbin table
        dustbin_code = int(dc.text)
        dustbin_type =dt.text
        location = l.text

        insert_query = "INSERT INTO Dustbin (DustbinCode, DustbinType, Location) VALUES (%s, %s, %s)"
        insert_values = (dustbin_code,dustbin_type,location)
        mycursor.execute(insert_query, insert_values)
        mydb.commit()

        self.add_dustbin_status(dustbin_code,0,self.app.ccode)

    def add_dustbin_status(self, dustbin_code, status, company_code):
        print("Adding status")
        insert_query = "INSERT INTO DustbinStatus (DustbinCode, Status, CompanyCode) VALUES (%s, %s, %s)"
        insert_values = (dustbin_code, status, company_code)
        mycursor.execute(insert_query, insert_values)
        mydb.commit()
        self.on_enter()
        self.popup.dismiss()

    def update_overview_layout(self):
        # Clear the existing widgets from the layout
        self.ids.overview_tab.clear_widgets()

        mycursor.execute("SELECT * FROM DustbinStatus WHERE CompanyCode = %s", (self.app.ccode,))
        self.dustbin_data = mycursor.fetchall()

        # Create a box layout to contain all dustbin data
        dustbin_container = BoxLayout(orientation='vertical', size_hint_y=None, padding=(dp(20), dp(10)))
        dustbin_container.bind(minimum_height=dustbin_container.setter('height'))

        # Loop through the dustbin data and create a text field for each entry
        for data in self.dustbin_data:
            dustbin_id = data[0]
            fill_level = data[1]

            # Create the text field for the dustbin data
            dustbin_textfield = MDLabel(text='Dustbin {} - Fill Level: {}% '.format(dustbin_id, fill_level * 10),
                                        size_hint_y=None)

            # Create the progress bar for the dustbin data
            dustbin_progressbar = MDProgressBar(value=fill_level / 10, max=1, size_hint_x=None, width=300)

            # Create the box layout for the dustbin data
            dustbin_boxlayout = MDBoxLayout(orientation='vertical', size_hint_y=None, height=dp(100),
                                            padding=(dp(20), dp(10)), pos_hint={"center_x": 0.5, "top": 1})

            # Add the text field and progress bar to the box layout
            dustbin_boxlayout.add_widget(dustbin_textfield)
            dustbin_boxlayout.add_widget(dustbin_progressbar)

            # Add the box layout to the dustbin container
            dustbin_container.add_widget(dustbin_boxlayout)

        # Create a scroll view to contain the dustbin container
        overview_scrollview = ScrollView()
        overview_scrollview.add_widget(dustbin_container)

        # Add the scroll view to the overview layout
        self.ids.overview_tab.add_widget(overview_scrollview)

    def update_profile(self):
        # Create the profile box layout
        self.ids.profile_tab.clear_widgets()
        profile_boxlayout = MDBoxLayout(orientation='vertical', spacing=dp(10), padding=dp(10),pos_hint={"center_x": 0.5, "top": 1})

        # Create and add the company name and icon
        cname_box = MDBoxLayout(size_hint=(1, None), height=dp(40))
        cname_icon = IconLeftWidget(icon="briefcase")
        cname_text = MDLabel(text=self.app.cname, font_style='H4', halign='left')
        cname_box.add_widget(cname_icon)
        cname_box.add_widget(cname_text)
        profile_boxlayout.add_widget(cname_box)

        # Add some padding
        profile_boxlayout.add_widget(MDBoxLayout(size_hint=(1, None), height=dp(10)))

        # Create and add the username and icon
        username_box = MDBoxLayout(size_hint=(1, None), height=dp(40))
        username_icon = IconLeftWidget(icon="account")
        username_text = MDLabel(text='Username: ' + self.app.username, font_style='Subtitle1', halign='left')
        username_box.add_widget(username_icon)
        username_box.add_widget(username_text)
        profile_boxlayout.add_widget(username_box)

        # Create and add the email and icon
        email_box = MDBoxLayout(size_hint=(1, None), height=dp(40))
        email_icon = IconLeftWidget(icon="email")
        email_text = MDLabel(text='Email: ' + self.app.email, font_style='Subtitle1', halign='left')
        email_box.add_widget(email_icon)
        email_box.add_widget(email_text)
        profile_boxlayout.add_widget(email_box)

        # Add some padding
        profile_boxlayout.add_widget(MDBoxLayout(size_hint=(1, None), height=dp(20)))

        # Create and add the dustbin count text and icon
        dustbin_box = MDBoxLayout(size_hint=(1, None), height=dp(40))
        dustbin_icon = IconLeftWidget(icon="trash-can")
        query = f"SELECT COUNT(*) FROM DustbinStatus WHERE CompanyCode = '{self.app.ccode}'"
        mycursor.execute(query)
        result = mycursor.fetchone()
        dustbin_count = result[0]
        dustbin_count_text = MDLabel(text='Number of Dustbins Used: ' + str(dustbin_count), font_style='Subtitle1',
                                     halign='left')
        dustbin_box.add_widget(dustbin_icon)
        dustbin_box.add_widget(dustbin_count_text)
        profile_boxlayout.add_widget(dustbin_box)

        # Add the profile box layout to the profile layout
        self.profile_layout.add_widget(profile_boxlayout)

        # Add the profile layout to the profile tab
        self.ids.profile_tab.add_widget(self.profile_layout)

    def update_urgent_layout(self):
        # Clear the existing contents of the tab
        self.ids.urgent_tab.clear_widgets()

        # Get the dustbins with status >= 8 and company code equal to self.app.ccode
        query = f"SELECT DustbinCode, Status FROM DustbinStatus WHERE Status >= 8 AND CompanyCode = '{self.app.ccode}'"
        mycursor.execute(query)
        result = mycursor.fetchall()

        if not result:
            # If the result is empty, add a label to the middle of the screen
            self.urgent_layout = BoxLayout(orientation='vertical', padding=50)
            label = MDLabel(text='No urgent matters to attend to', halign='center')
            self.urgent_layout.add_widget(label)
        else:
            # Otherwise, create a layout for each dustbin
            self.urgent_layout = BoxLayout(orientation='vertical')
            for dustbin_code, status in result:
                layout = BoxLayout(orientation='horizontal')
                label = MDLabel(text=f"Dustbin {dustbin_code}: {status}")
                button = MDFlatButton(text="Empty dustbin", md_bg_color=[0, 0.8, 0.2, 1])
                button.bind(on_press=lambda event: self.convert_to_zero(dustbin_code))
                layout.add_widget(label)
                layout.add_widget(button)

                # Add the layout to the tab
                self.urgent_layout.add_widget(layout)

        self.ids.urgent_tab.add_widget(self.urgent_layout)

    def convert_to_zero(self, code):
        query = "UPDATE DustbinStatus SET Status = 0 WHERE DustbinCode = %s"
        mycursor.execute(query, (code,))
        mydb.commit()

        self.on_enter()

    def update_edit_layout(self):
        self.ids.edit_tab.clear_widgets()

        # Create the grid layout for the dustbin data
        grid_layout = MDGridLayout(cols=2, spacing=dp(20), padding=(dp(40),dp(100),dp(40),dp(40)), size_hint_y=None)
        grid_layout.bind(minimum_height=grid_layout.setter('height'))

        # Get the dustbin data from the database
        query = f"SELECT Dustbin.DustbinCode, Dustbin.DustbinType, Dustbin.Location, DustbinStatus.Status FROM Dustbin " \
                f"JOIN DustbinStatus ON Dustbin.DustbinCode = DustbinStatus.DustbinCode " \
                f"WHERE DustbinStatus.CompanyCode = '{self.app.ccode}'"
        mycursor.execute(query)
        result = mycursor.fetchall()

        # Loop through the dustbin data and create a card for each entry
        for data in result:
            dustbin_code = data[0]
            dustbin_type = data[1]
            location = data[2]
            status = data[3]

            # Create the dustbin card
            dustbin_card = MDCard(orientation='vertical', size_hint=(None, None), size=(dp(250), dp(250)),
                                  radius=(25, 0, 25, 0), padding=dp(10))

            # Create the dustbin code label
            dustbin_code_label = MDLabel(text=f'Dustbin Code: {dustbin_code}', font_style='Subtitle1', halign='center')
            dustbin_card.add_widget(dustbin_code_label)

            # Create the dustbin type label
            dustbin_type_label = MDLabel(text=f'Dustbin Type: {dustbin_type}', font_style='Subtitle1', halign='center')
            dustbin_card.add_widget(dustbin_type_label)

            # Create the location label
            location_label = MDLabel(text=f'Location: {location}', font_style='Subtitle1', halign='center')
            dustbin_card.add_widget(location_label)

            # Add the dustbin card to the grid layout
            grid_layout.add_widget(dustbin_card)

        # Add the grid layout to the scroll view
        self.edit_scrollview.add_widget(grid_layout)

        # Add the scroll view to the main layout
        self.ids.edit_tab.add_widget(self.edit_scrollview)
        fab = MDFloatingActionButton(icon='plus', pos_hint={'x': 0.05, 'y': 0.05})
        fab.bind(on_release=self.showpopup)
        self.ids.edit_tab.add_widget(fab)


class CleanBeeApp(MDApp):

    def build(self):
        self.theme_cls.primary_palette = "Green"
        self.theme_cls.theme_style = "Dark"
        self.app = MDApp.get_running_app()

        self.app.username = ""
        self.app.password = ""
        self.app.email = ""
        self.app.ccode = 0
        self.app.cname = ""

        sm = ScreenManager()
        sm.add_widget(LoginInterface(name='loginpage'))
        sm.add_widget(MainScreen(name='mainscreen'))
        sm.add_widget(ProfileScreen(name='profilescreen'))
        sm.add_widget(ResetPasswordPage(name='reset_password'))
        return sm

end = timer()
print("Time taken:", end-start)

if __name__ == "__main__":
    CleanBeeApp().run()
