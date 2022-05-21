from kivymd.app import MDApp
import mysql.connector
from kivymd.uix.label import MDLabel, MDIcon
from kivymd.uix.button import MDFlatButton, MDTextButton, MDRoundFlatButton, MDRectangleFlatButton, MDIconButton, MDRaisedButton
from kivy.uix.screenmanager import Screen, ScreenManager
from kivymd.uix.screen import MDScreen
from kivymd.uix.textfield import MDTextField
from kivymd.uix.swiper import MDSwiper, MDSwiperItem
from kivy.lang import Builder
from kivy.uix.image import Image
from kivymd.uix.toolbar import MDToolbar
from kivy.core.window import Window
from kivymd.uix.datatables import MDDataTable
from kivy.uix.anchorlayout import AnchorLayout
from plyer import filechooser
from kivymd.uix.filemanager import MDFileManager
from kivymd.toast import toast
from kivy.utils import platform
from kivymd.uix.picker import MDDatePicker, MDTimePicker
from datetime import datetime
from kivy.metrics import dp
from kivy.properties import ObjectProperty, StringProperty
from kivy.base import runTouchApp
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.dialog import MDDialog
from plyer import filechooser
import os
from os.path import join, dirname


Window.size= (400,600)

sm = ScreenManager()

db = mysql.connector.connect(host="localhost",
                                          port="3306",
                                          user="root",
                                          password="yogita@123", database="hospital")
cursor = db.cursor()
cursor.execute('select * from patients')
fetch_patient_data = cursor.fetchall()
cursor.execute('select * from doctors')
fetch_doctor_data = cursor.fetchall()
cursor.execute('select * from appointments')
fetch_appoint_data = cursor.fetchall()

class MenuScreen(Screen):
    pass
class PatientScreen(Screen):
######################### data table for patients #######################################
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.table = MDDataTable(
            size_hint=(0.98, 0.60),
            pos_hint={'center_x': 0.5, 'center_y': 0.44},
            check=True,
            use_pagination=True,
            rows_num=50,
            column_data=[
                ("First Name", dp(30)),
                ("Last Name", dp(20)),
                ("Address", dp(30)),
                ("Mobile", dp(20))],
            row_data= fetch_patient_data)
        global table1
        table1 = self.table
        self.table.bind(on_check_press=self.check_press)
        self.add_widget(self.table)

    def on_enter(self, *args):
        global table1
        table1.update_row_data(type(table1).__name__, fetch_patient_data)
    def check_press(self, instance_table, current_row):
        print(instance_table, current_row)
    def dlt_row(self):
        global table1
        self.dialog = MDDialog(title='Confirmation', text='Are you sure you want to delete this',
                               buttons=[MDFlatButton(text='Yes', on_release=self.dlt_func), MDFlatButton(text='No', on_release=self.dismis_dialog)])
        self.dialog.open()
    def dlt_func(self, inst):
        try:
            global table1
            self.db = mysql.connector.connect(host="localhost",
                                         port="3306",
                                         user="root",
                                         password="yogita@123", database="hospital")
            cursor = self.db.cursor()
            click_on_row = table1.get_row_checks()
            for i in click_on_row:
                for j in click_on_row:
                    self.dlt = "delete from patients where mobile = '{}'".format(click_on_row[0][3])
                    print(self.dlt)
            cursor.execute(self.dlt)
            self.db.commit()
            cursor.execute("select * from patients")
            patient_data = cursor.fetchall()
            table1.update_row_data(type(table1).__name__, patient_data)
            self.dialog.dismiss()
        except Exception as e:
            print('thisssssssssssssssssss= ', e)

    def dismis_dialog(self, inst):
        self.dialog.dismiss()
        return self.table.row_data



##############################################################################################################################
class AddPatientScreen(Screen):
    pass

class DoctorScreen(Screen):
######################### data table for doctors #######################################
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.table = MDDataTable(
            size_hint=(0.98, 0.60),
            pos_hint={'center_x': 0.5, 'center_y': 0.44},
            check=True,
            use_pagination=True,
            rows_num=50,
            column_data=[
                ("First Name", dp(30)),
                ("Last Name", dp(20)),
                ("Address", dp(30)),
                ("Mobile", dp(20))],
            row_data= fetch_doctor_data)
        global table1
        table1 = self.table
        self.table.bind(on_check_press=self.check_press)
        self.add_widget(self.table)

    def on_enter(self, *args):
        global table1
        table1.update_row_data(type(table1).__name__, fetch_doctor_data)
    def check_press(self, instance_table, current_row):
        print(instance_table, current_row)
    def dlt_row(self):
        global table1
        self.dialog = MDDialog(title='Confirmation', text='Are you sure you want to delete this',
                               buttons=[MDFlatButton(text='Yes', on_release=self.dlt_func), MDFlatButton(text='No', on_release=self.dismis_dialog)])
        self.dialog.open()
    def dlt_func(self, inst):
        try:
            self.db = mysql.connector.connect(host="localhost",
                                         port="3306",
                                         user="root",
                                         password="yogita@123", database="hospital")
            cursor = self.db.cursor()
            click_on_row = table1.get_row_checks()
            for i in click_on_row:
                for j in click_on_row:
                    self.dlt = "delete from doctors where mobile = '{}'".format(click_on_row[0][3])
                    print(self.dlt)
            cursor.execute(self.dlt)
            self.db.commit()
            cursor.execute("select * from doctors")
            doctor_data = cursor.fetchall()
            self.dialog.dismiss()
            table1.update_row_data(type(table1).__name__, doctor_data)
        except Exception as e:
            print('thisssssssssssssssssss= ', e)

    def dismis_dialog(self, inst):
        self.dialog.dismiss()
        return self.table.row_data
##########################################################################################################################
class AddDoctorScreen(Screen):
    pass
class AppointmentScreen(Screen):
############################## data table for appointments #######################################
    def __init__(self, **kwargs):
        super().__init__()
        self.table = MDDataTable(
            size_hint=(0.98, 0.60),
            pos_hint={'center_x': 0.5, 'center_y': 0.45},
            check=True,
            use_pagination=True,
            rows_num=100,
            column_data=[
                ("First Name", dp(30)),
                ("Last Name", dp(20)),
                ("Mobile", dp(20)),
                ("Date", dp(20)),
                ("Time", dp(20))
            ],
            row_data= fetch_appoint_data
        )
        global table1
        table1 = self.table
        self.table.bind(on_check_press=self.check_press)
        self.add_widget(self.table)


    def on_enter(self, *args):
        global table1
        table1.update_row_data(type(table1).__name__, fetch_appoint_data)

    def check_press(self, instance_table, current_row):
        print(instance_table, current_row)

    def dlt_row(self):
        global table1
        self.dialog = MDDialog(title='Confirmation', text='Are you sure you want to delete this',
                           buttons=[MDFlatButton(text='Yes', on_release=self.dlt_func),
                                    MDFlatButton(text='No', on_release=self.dismis_dialog)])
        self.dialog.open()


    def dlt_func(self, inst):
        try:
            self.db = mysql.connector.connect(host="localhost",
                                          port="3306",
                                          user="root",
                                          password="yogita@123", database="hospital")
            cursor = self.db.cursor()
            click_on_row = table1.get_row_checks()
            for i in click_on_row:
                for j in click_on_row:
                    self.dlt = "delete from appointments where mobile = '{}'".format(click_on_row[0][2])
                    print(self.dlt)
            cursor.execute(self.dlt)
            self.db.commit()
            cursor.execute("select * from appointments")
            appoint_data = cursor.fetchall()
            table1.update_row_data(type(table1).__name__, appoint_data)
            self.dialog.dismiss()
        except Exception as e:
            print('thisssssssssssssssssss= ', e)


    def dismis_dialog(self, inst):
        self.dialog.dismiss()
        return self.table.row_data

##########################################################################################################################
class AddAppointmentScreen(Screen):
    pass
class prescription(Screen):
    pass
class displaypre(Screen):
    pass
class lab_report(Screen):
    pass
class displaylab(Screen):
    pass
class ProjectApp(MDApp):
############################################## KV file loading ############################################################
    def build(self):
        with open('layout.kv', encoding='utf-8') as f:
            Builder.load_string(f.read())

        self.theme_cls.primary_palette = 'Teal'
        sm.add_widget(MenuScreen(name='menu'))
        sm.add_widget(PatientScreen(name='patient'))
        sm.add_widget(AddPatientScreen(name='add patient'))
        sm.add_widget(DoctorScreen(name='doctor'))
        sm.add_widget(AddDoctorScreen(name='add doctor'))
        sm.add_widget(AppointmentScreen(name='appointment'))
        sm.add_widget(AddAppointmentScreen(name='add appointment'))
        sm.add_widget(prescription(name='prescription'))
        sm.add_widget(displaypre(name='display_pre'))
        sm.add_widget(lab_report(name='lab_report'))
        sm.add_widget(displaylab(name='display_lab'))
        return sm

 ########################################## file selection ###############################################################
###################################### for prescription uploading ########################################################
    def file_chooser1(self):
        filechooser.open_file(on_selection=self.selected)

    def selected(self, selection):
        try:
            if selection:
                self.root.get_screen('add patient').ids.selected_pre.source = selection[0]
            else:
                close = MDFlatButton(text='Ok', on_release= self.close_dialog)
                self.dialog = MDDialog(title='Oops', text='Something Went Wrong, Reselect the file', buttons= [close])
                self.dialog.open()
        except Exception as e:
            print('this is error = ', e)
    def close_dialog(self, obj):
        self.dialog.dismiss()

#################################### file selection ###############################################################
############################### for lab-report uploading ########################################################
    def file_chooser2(self):
        filechooser.open_file(on_selection=self.selected2)

    def selected2(self, selection):
        try:
            if selection:
                self.root.get_screen('add patient').ids.selected_lab.source = selection[0]
            else:
                close = MDFlatButton(text='Ok', on_release= self.close_dialog)
                self.dialog = MDDialog(title='Oops', text='Something Went Wrong, Reselect the file', buttons= [close])
                self.dialog.open()
        except Exception as e:
            print('this is error = ', e)
    def close_dialog(self, obj):
        self.dialog.dismiss()

#########################################################################################################################
##################################### save date for appointment #########################################################
#########################################################################################################################
    def on_save_date(self, instance, value, date_label):
        print(instance, value, date_label)
        try:
            self.root.get_screen('add appointment').ids.date_label.text = str(value)
        except Exception as e:
            print('this is error = ', e)
    def on_cancel_date(self, instance, value):
        self.date_dialog.dismiss()
    def show_date_picker(self):
        try:
            self.date_dialog = MDDatePicker(min_year=2021, max_year=2030)
            self.date_dialog.bind(on_save=self.on_save_date, on_cancel=self.on_cancel_date)
            self.date_dialog.open()
        except Exception as e:
            print('this is error = ', e)
#########################################################################################################################
##################################### save time for appointment #########################################################
#########################################################################################################################
    def on_save_time(self, instance, time):
        print(instance, time)
        try:
            self.root.get_screen('add appointment').ids.time_label.text = str(time)
        except Exception as e:
            print('this is error = ', e)
    def on_cancel_time(self, instance, time):
        self.time_dialog.dismiss()
    def show_time_picker(self):
        try:
            self.time_dialog = MDTimePicker()
            self.time_dialog.bind(on_save=self.on_save_time, on_cancel=self.on_cancel_time)
            self.time_dialog.open()

        except Exception as e:
            print('this is error = ', e)

######################################################################################################################################
############################################ save patient in data table #####################################################
######################################################################################################################################
    def add_patient(self):
        try:
            self.firstname = self.root.get_screen('add patient').ids.firstname.text
            self.lastname = self.root.get_screen('add patient').ids.lastname.text
            self.address = self.root.get_screen('add patient').ids.address.text
            self.mobile = self.root.get_screen('add patient').ids.mobile.text

            if self.firstname == '' or self.lastname == '' or self.address == '' or self.mobile == '':
                self.dialog = MDDialog(title='Oops', text='Please Fill the Field', buttons=[MDFlatButton(text='OK', on_release=self.dismis_dialog)])
                self.dialog.open()
            elif type(self.firstname) == int and type(self.lastname) == int and type(self.address) == int:
                if type(self.mobile) == str:
                    self.dialog = MDDialog(title='Oops', text='Invalid Input', buttons=[MDFlatButton(text='OK', on_release=self.dismis_dialog)])
                    self.dialog.open()
            elif len(self.mobile) < 10 or len(self.mobile) > 10:
                self.dialog = MDDialog(title='Oops', text='Invalid Mobile no.', buttons=[MDFlatButton(text='OK', on_release=self.dismis_dialog)])
                self.dialog.open()
            else:
                self.db = mysql.connector.connect(host="localhost",
                                                  port="3306",
                                                  user="root",
                                                  password="yogita@123", database="hospital")
                cursor = self.db.cursor()
                store = "insert into patients(first_name, last_name, address, mobile) values('{}', '{}', '{}', '{}')".format(self.firstname,
                                                                                              self.lastname,
                                                                                              self.address, self.mobile)
                cursor.execute(store)
                self.db.commit()
                cursor.execute("select * from patients")
                f_d = cursor.fetchall()
                p = PatientScreen().table
                p.update_row_data(type(p).__name__, f_d)
                self.root.get_screen('patient').manager.current = 'patient'
                self.root.get_screen('patient').manager.transition.direction = 'right'
                self.dialog = MDDialog(title='Great', text='Patient is added',
                                       buttons=[MDFlatButton(text='OK', on_release=self.dis_change)])
                self.dialog.open()
                return PatientScreen().on_enter()
        except Exception as e:
            print('this is error of add patient =', e)
    def dismis_dialog(self, inst):
        self.dialog.dismiss()
    def dis_change(self, *args):
        self.dialog.dismiss()
        self.root.get_screen('add patient').ids.firstname.text = ''
        self.root.get_screen('add patient').ids.lastname.text = ''
        self.root.get_screen('add patient').ids.address.text = ''
        self.root.get_screen('add patient').ids.mobile.text = ''

############################################ save prescrption and lab report in os folder #####################################################
###############################################################################################################################################
    def save_pre_lab(self):
        self.select1 = self.root.get_screen('add patient').ids.selected_pre.source
        self.name_of_pre1 = self.root.get_screen('add patient').ids.firstname.text
        self.name_of_pre2 = self.root.get_screen('add patient').ids.lastname.text

        save_path = 'F:\yogita\IT certi\kivymd mobile app project\precription'
        completeName = os.path.join(save_path, self.name_of_pre1 + _ + self.name_of_pre2 + 'pre')
        file1 = open(completeName, "w")
        file1.write(self.select1)
        file1.close()

        self.select2 = self.root.get_screen('add patient').ids.selected_lab.source

        save_path1 = 'F:\yogita\IT certi\kivymd mobile app project\lab report'
        completeName1 = os.path.join(save_path1, self.name_of_pre1 + _ + self.name_of_pre2 + 'lab')
        file1 = open(completeName1, "w")
        file1.write(self.select2)
        file1.close()

############################################ View prescrption and lab report in os folder #####################################################
###############################################################################################################################################
    def view_lab(self):
        self.firstname = self.root.get_screen('lab_report').ids.firstname.text
        self.lastname = self.root.get_screen('lab_report').ids.lastname.text
        filename = self.firstname + '_' + self.lastname

        with open('F:\yogita\IT certi\kivymd mobile app project\lab report', 'r', encoding='utf-8') as file:
            if filename in file:
                open('file')
            else:
                self.dialog = MDDialog(title='Oops', text='File does not exist',
                                       buttons=[MDFlatButton(text='OK', on_release=self.dismis_dialog)])
        def dismis_dialog(self, inst):
            self.dialog.dismiss()
######################################################################################################################################
############################################ save doctor in data table #####################################################
######################################################################################################################################
    def add_doctor(self):
        try:
            self.firstname = self.root.get_screen('add doctor').ids.firstname.text
            self.lastname = self.root.get_screen('add doctor').ids.lastname.text
            self.address = self.root.get_screen('add doctor').ids.address.text
            self.mobile = self.root.get_screen('add doctor').ids.mobile.text

            if self.firstname == '' or self.lastname == '' or self.address == '' or self.mobile == '':
                self.dialog = MDDialog(title='Oops', text='Please Fill the Field',
                                       buttons=[MDFlatButton(text='OK', on_release=self.dismis_dialog)])
                self.dialog.open()
            elif type(self.firstname) == int and type(self.lastname) == int and type(self.address) == int:
                if type(self.mobile) == str:
                    self.dialog = MDDialog(title='Oops', text='Invalid Input',
                                           buttons=[MDFlatButton(text='OK', on_release=self.dismis_dialog)])
                    self.dialog.open()
            elif len(self.mobile) < 10 or len(self.mobile) > 10:
                self.dialog = MDDialog(title='Oops', text='Invalid Mobile no.',
                                       buttons=[MDFlatButton(text='OK', on_release=self.dismis_dialog)])
                self.dialog.open()
            else:
                self.db = mysql.connector.connect(host="localhost",
                                                  port="3306",
                                                  user="root",
                                                  password="yogita@123", database="hospital")
                cursor = self.db.cursor()
                store = "insert into doctors(first_name, last_name, address, mobile) values('{}', '{}', '{}', '{}')".format(
                    self.firstname,
                    self.lastname,
                    self.address, self.mobile)
                cursor.execute(store)
                self.db.commit()
                cursor.execute("select * from doctors")
                f_d = cursor.fetchall()
                p = PatientScreen().table
                p.update_row_data(type(p).__name__, f_d)
                self.root.get_screen('doctor').manager.current = 'doctor'
                self.root.get_screen('doctor').manager.transition.direction = 'right'
                self.dialog = MDDialog(title='Great', text='Doctor is added',
                                       buttons=[MDFlatButton(text='OK', on_release=self.dis_change)])
                self.dialog.open()
                return PatientScreen().on_enter()
        except Exception as e:
            print('this is error of add doctor =', e)

        def dismis_dialog(self, inst):
            self.dialog.dismiss()

        def dis_change(self, *args):
            self.dialog.dismiss()
            self.root.get_screen('add doctor').ids.firstname.text = ''
            self.root.get_screen('add doctor').ids.lastname.text = ''
            self.root.get_screen('add doctor').ids.address.text = ''
            self.root.get_screen('add doctor').ids.mobile.text = ''

######################################################################################################################################
############################################ save appointment in data table #####################################################
######################################################################################################################################

    def add_appointment(self):
        try:
            self.firstname = self.root.get_screen('add appointment').ids.first_name.text
            self.lastname = self.root.get_screen('add appointment').ids.last_name.text
            self.mobile = self.root.get_screen('add appointment').ids.mobile.text
            self.date = self.root.get_screen('add appointment').ids.date_label.text
            self.time = self.root.get_screen('add appointment').ids.time_label.text

            if self.firstname == '' or self.lastname == '' or self.mobile == '' or self.date == '' or self.time == '':
                self.dialog = MDDialog(title='Oops', text='Please Fill the Field',
                                       buttons=[MDFlatButton(text='OK', on_release=self.dismis_dialog)])
                self.dialog.open()
            elif type(self.firstname) == int and type(self.lastname) == int:
                if type(self.mobile) == str:
                    self.dialog = MDDialog(title='Oops', text='Invalid Input',
                                           buttons=[MDFlatButton(text='OK', on_release=self.dismis_dialog)])
                    self.dialog.open()
            elif len(self.mobile) < 10 or len(self.mobile) > 10:
                self.dialog = MDDialog(title='Oops', text='Invalid Mobile no.',
                                       buttons=[MDFlatButton(text='OK', on_release=self.dismis_dialog)])
                self.dialog.open()
            else:
                self.db = mysql.connector.connect(host="localhost",
                                                  port="3306",
                                                  user="root",
                                                  password="yogita@123", database="hospital")
                cursor = self.db.cursor()
                store = "insert into appointments(first_name, last_name, mobile, date, time) values('{}', '{}', '{}', '{}', '{}')".format(
                    self.firstname,
                    self.lastname, self.mobile,
                    self.date, self.time)
                cursor.execute(store)
                self.db.commit()
                cursor.execute("select * from appointments")
                f_d = cursor.fetchall()
                p = AppointmentScreen().table
                p.update_row_data(type(p).__name__, f_d)
                self.root.get_screen('appointment').manager.current = 'appointment'
                self.root.get_screen('appointment').manager.transition.direction = 'right'
                self.dialog = MDDialog(title='Great', text='Appointment is added',
                                       buttons=[MDFlatButton(text='OK', on_release=self.dis_change)])
                self.dialog.open()
                return AppointmentScreen().on_enter()
        except Exception as e:
            print('this is error of add appointment =', e)

        def dismis_dialog(self, inst):
            self.dialog.dismiss()

        def dis_change(self, *args):
            self.dialog.dismiss()
            self.root.get_screen('add appointment').ids.first_name.text = ''
            self.root.get_screen('add appointment').ids.last_name.text = ''
            self.root.get_screen('add appointment').ids.mobile.text = ''
            self.root.get_screen('add appointment').ids.date_label.text = ''
            self.root.get_screen('add appointment').ids.time_label.text = ''




if __name__=='__main__':
    ProjectApp().run()
