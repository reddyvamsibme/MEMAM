'''
Software Carpentry, Fall 2020
MEMAM: Medical Emergencies Management And Alert Mechanism
Submitted by
Vamsi Reddy <vreddy17@jhu.edu>
Emad Mohammed Naveed <enaveed1@jhu.edu>
'''
# Import packages
import os
import random
# Excel sheet manipulations
import xlrd
# Password hashing and no echo
import hashlib
import getpass
import time as tim
# Visualization
import tkinter as tk
from tkmacosx import Button
from datetime import time as timer1

# Defining variables to act as a central database
# Using Global variables to improve quality of live updates

# The list of available resident interns
intern_list = [
    'intern01',
    'intern02',
    'intern03',
    'intern04',
    'intern05',
    'intern06',
    'intern07',
    'intern08',
    'intern09',
    'intern10',
    'intern11',
    'intern12',
    'intern13',
    'intern14',
    'intern15',
    'intern16']
# The list of available surgeons
surgeon_list = [
    'surgeon01',
    'surgeon02',
    'surgeon03',
    'surgeon04',
    'surgeon05',
    'surgeon06']
# The list of available residents
resident_list = [
    'resident01',
    'resident02',
    'resident03',
    'resident04',
    'resident05',
    'resident06',
    'resident07',
    'resident08']
# Patient identification tags and control modes
patient_key = {'JHU1234': '404', 'JHU5678': '567'}
patient_mode = {'JHU1234': [0, 0, 0, 0, 0, 0],
                'JHU5678': [0, 0, 0, 0, 0, 0]}
patient_mode_e = {'JHU1234': [0, 0, 0, 0, 0, 0],
                  'JHU5678': [0, 0, 0, 0, 0, 0]}
# control modes for alert protocols and updating
code_s = [{1: [], 2: [], 4: []}, {1: [], 2: [], 4: []}]
code_ri = [{1: [], 2: [], 3: [], 4: [], 5: [], 6: []},
           {1: [], 2: [], 3: [], 4: [], 5: [], 6: []}]
code_re = [{1: [], 2: [], 3: [], 4: [], 5: [], 6: []},
           {1: [], 2: [], 3: [], 4: [], 5: [], 6: []}]
code_eri = [{1: [], 2: [], 3: [], 4: [], 5: [], 6: []},
            {1: [], 2: [], 3: [], 4: [], 5: [], 6: []}]
code_ere = [{1: [], 2: [], 3: [], 4: [], 5: [], 6: []},
            {1: [], 2: [], 3: [], 4: [], 5: [], 6: []}]
# Callable counters for real-time updation
counter = [{1: 3, 2: 3, 3: 3, 4: 3, 5: 3, 6: 3},
           {1: 3, 2: 3, 3: 3, 4: 3, 5: 3, 6: 3}]
counter_e = [{1: 3, 2: 3, 3: 3, 4: 3, 5: 3, 6: 3},
             {1: 3, 2: 3, 3: 3, 4: 3, 5: 3, 6: 3}]
DATA = [0, 0]
PAGES = [[], []]
# Equipment units available
EQUIPMENT_COUNT = 10



class Input:
    '''
    This class handles reading and extraction of patient's vitals from bedside
    monitor, in this case, we have an excel sheet (in .xlsx format)
    Step 1: Read the .xlsx extension files only.
    Step 2: Identifying specific patient identification details
    Step 3: Creating time domain data for each vital by extracting rows
    '''

    def __init__(self, file, id_record):
        '''
            The __init__ method will initialize the object’s state.
            Initializes the function of the class when
            an object of class is created.
            In this case, the file name and identification tags of patients
            for real-time update
            **Input Parameters**
                file: *str*
                    The filename to read and extract information
                    The filename to save the output image with solution
                id_record: *str*
                    Number for real-time update on GUI
            **Returns**
                None
        '''
        self.file = file
        # Initializing position variables
        self.id_record = id_record

    def __call__(self):
        '''
        The __call__ method will read and extract the specific .xlsx file

        **Input Parameters**
            None
        **Returns**
            pat_id: *list, str, int, optional*
                The patient id corresponds to a specific patient
            patient_record: **
                The patient record has the details about the patient
                age, room number (typical hospital register)
        '''
        # Read the all the sheets and extracting sheet names
        patient_record, all_sheets = self.read_patient(self.file)
        # Finding the number of patients in the hospital
        length = len(all_sheets.sheets())
        # Details about each patient by index
        patient_id = all_sheets.sheet_by_index(self.id_record)
        # Number of patients
        num_rowsid = patient_id.nrows
        pat_id = []
        for i in range(1, num_rowsid):
            time_data = patient_id.row_values(i)
            pat_id.append(time_data)
        return pat_id, patient_record[self.id_record]

    def read_patient(self, file):
        '''
        This function will read and extract the information
        from a given patient log, in actual hospital settings,
        it is just a real-time physiological data feedback

        **Input Parameters**
            file: *str*
                The name of the file
        **Returns**
            patient_record: *list, optional*
                The updated grid system
            all_sheets: *list*
                The path to the sheets in the workbook
        '''
        file = "patient_log1.xlsx"
        all_sheets = xlrd.open_workbook(file)
        patient_record = []
        for sheet in all_sheets.sheets():
            patient_name = sheet.name
            patient_record.append(patient_name)
        return patient_record, all_sheets


class MEMAM:
    '''
    This class has all the major functions those define the
    specific emergencies, alert functions and internal paging

    Activity Functions:
    normals() - Defines the healthy ranges of the vitals
    page() - Visulizes the messages on GUI
    log() - Enter the activity in patient log
    scrub() - Visualizes the nurse message on patient bedside monitor

    Emergency Functions:
    code_blue() - Alerts surgeons, resident interns, residents, equipment team
    blood_pressure() - Alerts surgeons, resident interns, residents
    Temperature() - Alerts resident interns, residents
    Labor_pains() - Alerts surgeons, resident interns, residents
    breathing() - Alerts resident interns, residents
    Spo2_abnormal() - Alerts resident interns, residents

    Alert Mechanism Functions:  (alerts through pager)
    alert_nurse() - Alerts the central control unit of nurse station
    nurse_ResInterns() - Nurses alert the resident interns
    nurse_residents() - Nurses alert the residents
    nurse_equipment() - Nurses alert the equipment team
    nurse_surgeons() - Nurses alert the surgeons

    '''

    def __init__(self, data, patient_record, patient_id):
        '''
        The __init__ method will initialize the object’s state.
        Initializes the function of the class when
        an object of class is created.
        In this case, the data, patient_record, patient_id of a specific patient
        **Input Parameters**
            data: *list,*
                The patient data for a given sheet
            patient_id: *list, str, int, optional*
                The patient id corresponds to a specific patient
            patient_record: **
                The patient record has the details about the patient
                age, room number (typical hospital register)
        **Returns**
            None
        '''
        self.data = data
        self.patient_record = patient_record
        self.patient_id = patient_id
        self.logs = []
        self.pages = []
        self.scrubs = []

    def __call__(self):
        '''
        The __call__ method will read and extract each row from
        specific '.xlsx' sheets, which indeed will used for the
        real-time display on GUI

        **Input Parameters**
            None
        **Returns**
            None
        '''
        global DATA
        global PAGES
        # Extracting patient data
        patient_data = self.patient_record
        # for splitting the sheet name to get details
        details = patient_data.split("_")
        # Defining the patient details
        age = int(details[2])
        name = details[0]
        room_number = patient_key[name]
        # Using normals to get safe ranges for all vitals
        respi_para, HR_para, BP_para = self.normals(age)
        time_data = self.data
        # Extracting time stamps
        time1 = time_data[0]
        # Converting time stamps from the HH:MM:SS 24 hour format
        x = int(time1 * 24 * 3600)  # convert to number of seconds
        timex = timer1(x // 3600, (x % 3600) // 60, x % 60)
        # Creating variables to use in GUI later
        Heart_rate = 'NaN' if time_data[1] == 'NaN' else int(time_data[1])
        BPS = 'NaN' if time_data[2] == 'NaN' else int(time_data[2])
        BPD = 'NaN' if time_data[3] == 'NaN' else int(time_data[3])
        respi_rate = 'NaN' if time_data[4] == 'NaN' else int(time_data[4])
        Spo2 = 'NaN' if time_data[5] == 'NaN' else int(time_data[5])
        temperature = 'NaN' if time_data[6] == 'NaN' else float(time_data[6])
        pain_index = 'NaN' if time_data[7] == 'NaN' else int(time_data[7])
        self.values = (Heart_rate, BPS, BPD, respi_rate, Spo2, temperature)
        # Initializing the check for all emergencies
        if time_data != DATA[self.patient_id]:
            self.code_blue(Heart_rate, timex, HR_para, name)
            self.blood_pressure(BPS, BPD, timex, BP_para, name)
            self.Temperature(temperature, timex, name)
            self.Labor_pains(pain_index, timex, name)
            self.breathing(respi_rate, timex, respi_para, name)
            self.Spo2_abnormal(Spo2, timex, name)
            if self.pages != PAGES[self.patient_id]:
                PAGES[self.patient_id] = self.pages
            DATA[self.patient_id] = time_data

    def normals(self, age):
        '''
        This function will determines ranges for a healthy patient
        based on the age provided in the patient id

        **Input Parameters**
            age: *int*
                The age of the patient
        **Returns**
            respi_para: *list, int*
                The respiration rate high, low
            HR_para: *list, int*
                The Heart rate high , low
            BP_para: *list, int*
                The systolic min, max
                The diastolic min, max
        '''
        # For respiration
        if age < 1:
            respi_high, resp_low = 40, 30
        elif age >= 1 and age < 2:
            respi_high, resp_low = 35, 25
        elif age >= 2 and age < 5:
            respi_high, resp_low = 30, 25
        elif age >= 5 and age < 12:
            respi_high, resp_low = 25, 20
        elif age >= 12:
            respi_high, resp_low = 35, 25

        respi_para = [respi_high, resp_low]

        # For Heart rate
        if age < 1:
            HR_high, HR_low = 180, 100
        elif age >= 1 and age <= 2:
            HR_high, HR_low = 165, 90
        elif age >= 3 and age <= 4:
            HR_high, HR_low = 140, 70
        elif age >= 5 and age <= 7:
            HR_high, HR_low = 140, 65
        elif age >= 8 and age <= 11:
            HR_high, HR_low = 130, 60
        elif age >= 12 and age <= 15:
            HR_high, HR_low = 130, 65
        elif age >= 16:
            HR_high, HR_low = 120, 50

        HR_para = [HR_high, HR_low]

        # For Blood Pressure
        if age < 1:
            sys_min, dia_min = 75, 50
            sys_max, dia_max = 100, 95
        elif age >= 1 and age <= 19:
            sys_min, dia_min = 105, 73
            sys_max, dia_max = 120, 81
        elif age >= 20 and age <= 39:
            sys_min, dia_min = 111, 78
            sys_max, dia_max = 135, 86
        elif age >= 40:
            sys_min, dia_min = 121, 83
            sys_max, dia_max = 147, 91

        BP_para = [sys_min, dia_min, sys_max, dia_max]

        return respi_para, HR_para, BP_para


    def code_blue(self, Heart_rate, time, HR_para, patient_name):
        '''
        This function will monitor the heart rate to alert when
        the patient experiences cardiac arrest i.e. code_blue

        **Input Parameters**
            Heart_rate: *float*
                The heart rate of the patient at a specific second
            time: *str*
                The time stamp of the above vital
            HR_para:*list*
                The boundary conditions of the Heart rate
                The Heart rate high , low
            patient_name:*str*
                The name of the patient being monitored
        **Returns**
            None
        '''
        # global variables
        global EQUIPMENT_COUNT
        global counter
        global counter_e
        code = 1
        # If no discrepancies, typically vitals available
        if Heart_rate != 'NaN':
            if not (Heart_rate > HR_para[1] and Heart_rate < HR_para[0]):
                # Not healthy, alerting mechanism begins
                if counter[self.patient_id][code] == 0:
                    self.alert_nurse('Code_Blue', patient_name, time, code)
                else:
                    counter[self.patient_id][code] -= 1
            # if healthy, call back the staff
            elif patient_mode[patient_name][0] == 1:
                if counter[self.patient_id][code] == 3:
                    patient_mode[patient_name][0] = 0
                    # adding assited staff back to availability
                    for i in code_ri[self.patient_id][code]:
                        self.page(i, '', '')
                        intern_list.extend([i])
                    code_ri[self.patient_id][code] = []
                    for i in code_re[self.patient_id][code]:
                        self.page(i, '', '')
                        resident_list.extend([i])
                    code_re[self.patient_id][code] = []
                    for i in code_s[self.patient_id][code]:
                        self.page(i, '', '')
                        surgeon_list.extend([i])
                    code_s[self.patient_id][code] = []
                else:
                    counter[self.patient_id][code] += 1

            if patient_mode_e[patient_name][0] == 1:
                if counter_e[self.patient_id][code] == 3:
                    patient_mode_e[patient_name][0] = 0
                    for i in code_eri[self.patient_id][code]:
                        self.page(i, '', '')
                        intern_list.extend([i])
                    code_eri[self.patient_id][code] = []
                    for i in code_ere[self.patient_id][code]:
                        self.page(i, '', '')
                        resident_list.extend([i])
                    code_ere[self.patient_id][code] = []
                    EQUIPMENT_COUNT += 1
                else:
                    counter_e[self.patient_id][code] += 1

        else:
            # Indicating equipment failure for NaN values
            if counter_e[self.patient_id][code] == 0:
                self.alert_nurse('equipment_failure', patient_name, time, code)
            else:
                counter_e[self.patient_id][code] -= 1

    def blood_pressure(self, BPS, BPD, time, BP_para, patient_name):
        '''
        This function will monitor the blood pressure to alert when
        the patient experiences high or low BP

        **Input Parameters**
            BPS: *float*
                The systolic blood pressure of the patient at a specific second
            BDS: *float*
                The diastolic blood pressure of the patient at a specific second
            time: *str*
                The time stamp of the above vital
            BP_para:*list*
                The boundary conditions of the blood pressure
                The systolic min, max
                The diastolic min, max
            patient_name:*str*
                The name of the patient being monitored
        **Returns**
            None
        '''
        # global variables
        global EQUIPMENT_COUNT
        global counter
        global counter_e
        code = 2
        sys_min, dia_min = BP_para[0], BP_para[1]
        sys_max, dia_max = BP_para[2], BP_para[2]
        # If no discrepancies, typically vitals available
        if BPS != 'NaN' and BPD != 'NaN':
            # Not healthy, alerting mechanism begins
            if not (
                (BPS > sys_min and BPS < sys_max) and (
                    BPD > dia_min and BPD < dia_max)):
                if counter[self.patient_id][code] == 0:
                    self.alert_nurse(
                        'Blood_Pressure', patient_name, time, code)
                else:
                    counter[self.patient_id][code] -= 1
            # if healthy, call back the staff
            elif patient_mode[patient_name][1] == 1:
                if counter[self.patient_id][code] == 3:
                    patient_mode[patient_name][1] = 0
                    for i in code_ri[self.patient_id][code]:
                        self.page(i, '', '')
                        intern_list.extend([i])
                    code_ri[self.patient_id][code] = []
                    for i in code_re[self.patient_id][code]:
                        self.page(i, '', '')
                        resident_list.extend([i])
                    code_re[self.patient_id][code] = []
                    for i in code_s[self.patient_id][code]:
                        self.page(i, '', '')
                        surgeon_list.extend([i])
                    code_s[self.patient_id][code] = []
                else:
                    counter[self.patient_id][code] += 1
            # adding assited staff back to availability
            if patient_mode_e[patient_name][1] == 1:
                if counter_e[self.patient_id][code] == 3:
                    patient_mode_e[patient_name][1] = 0
                    for i in code_eri[self.patient_id][code]:
                        self.page(i, '', '')
                        intern_list.extend([i])
                    code_eri[self.patient_id][code] = []
                    for i in code_ere[self.patient_id][code]:
                        self.page(i, '', '')
                        resident_list.extend([i])
                    code_ere[self.patient_id][code] = []
                    EQUIPMENT_COUNT += 1
                else:
                    counter_e[self.patient_id][code] += 1

        else:
            # Indicating equipment failure for NaN values
            if counter_e[self.patient_id][code] == 0:
                self.alert_nurse('equipment_failure', patient_name, time, code)
            else:
                counter_e[self.patient_id][code] -= 1

    def Temperature(self, temperature, time, patient_name):
        '''
        This function will monitor the temperature to alert when
        the patient experiences hypothemia or fever

        **Input Parameters**
            temperature: *float*
                The temperature of the patient at a specific second
            time: *str*
                The time stamp of the above vital
            patient_name:*str*
                The name of the patient being monitored
        **Returns**
            None
        '''
        # global variables
        global EQUIPMENT_COUNT
        global counter
        global counter_e
        code = 3
        if temperature != 'NaN':
            # If no discrepancies, typically vitals available
                if counter[self.patient_id][code] == 0:
                    # Not healthy, alerting mechanism begins
                    if temperature < 95 or temperature > 98.6:
                        self.alert_nurse('Temperature', patient_name, time, code)
                else:
                    counter[self.patient_id][code] -= 1
            # if healthy, call back the staff
        elif patient_mode[patient_name][2] == 1:
            if counter[self.patient_id][code] == 3:
                patient_mode[patient_name][2] = 0
                for i in code_ri[self.patient_id][code]:
                    self.page(i, '', '')
                    intern_list.extend([i])
                code_ri[self.patient_id][code] = []
                for i in code_re[self.patient_id][code]:
                    self.page(i, '', '')
                    resident_list.extend([i])
                code_re[self.patient_id][code] = []
            else:
                counter[self.patient_id][code] += 1
            # adding assited staff back to availability
            if patient_mode_e[patient_name][2] == 1:
                if counter_e[self.patient_id][code] == 3:
                    patient_mode_e[patient_name][2] = 0
                    for i in code_eri[self.patient_id][code]:
                        self.page(i, '', '')
                        intern_list.extend([i])
                    code_eri[self.patient_id][code] = []
                    for i in code_ere[self.patient_id][code]:
                        self.page(i, '', '')
                        resident_list.extend([i])
                    code_ere[self.patient_id][code] = []
                    EQUIPMENT_COUNT += 1
                else:
                    counter_e[self.patient_id][code] += 1

        else:
            # Indicating equipment failure for NaN values
            if counter_e[self.patient_id][code] == 0:
                self.alert_nurse('equipment_failure', patient_name, time, code)
            else:
                counter_e[self.patient_id][code] -= 1

    def Labor_pains(self, pain_index, time, patient_name):
        '''
        This function will cast the labor pains to alert when
        the patient expresses his pain, in a hospital setting,
        it is usually a button

        **Input Parameters**
            pain_index: *float*
                The pain indication of the patient at a specific second
                Values are binary 1 or 0
            time: *str*
                The time stamp of the above indication
            patient_name:*str*
                The name of the patient being monitored
        **Returns**
            None
        '''
        # global variables
        global EQUIPMENT_COUNT
        global counter
        global counter_e
        code = 4
        if pain_index != 'NaN':
            if pain_index == 1:
                if counter[self.patient_id][code] == 0:
                    self.alert_nurse('Labor_Pains', patient_name, time, code)
                else:
                    counter[self.patient_id][code] -= 1

            elif patient_mode[patient_name][3] == 1:
                if counter[self.patient_id][code] == 3:
                    patient_mode[patient_name][3] = 0
                    for i in code_ri[self.patient_id][code]:
                        self.page(i, '', '')
                        intern_list.extend([i])
                    code_ri[self.patient_id][code] = []
                    for i in code_re[self.patient_id][code]:
                        self.page(i, '', '')
                        resident_list.extend([i])
                    code_re[self.patient_id][code] = []
                    for i in code_s[self.patient_id][code]:
                        self.page(i, '', '')
                        surgeon_list.extend([i])
                    code_s[self.patient_id][code] = []
                else:
                    counter[self.patient_id][code] += 1

            if patient_mode_e[patient_name][3] == 1:
                if counter_e[self.patient_id][code] == 3:
                    patient_mode_e[patient_name][3] = 0
                    for i in code_eri[self.patient_id][code]:
                        self.page(i, '', '')
                        intern_list.extend([i])
                    code_eri[self.patient_id][code] = []
                    for i in code_ere[self.patient_id][code]:
                        self.page(i, '', '')
                        resident_list.extend([i])
                    code_ere[self.patient_id][code] = []
                    EQUIPMENT_COUNT += 1
                else:
                    counter_e[self.patient_id][code] += 1

        else:
            # Indicating equipment failure for NaN values
            if counter_e[self.patient_id][code] == 0:
                self.alert_nurse('equipment_failure', patient_name, time, code)
            else:
                counter_e[self.patient_id][code] -= 1

    def breathing(self, respi_rate, time, respi_para, patient_name):
        '''
        This function will monitor the respiration rates to alert when
        the patient suffers with breathing issues

        **Input Parameters**
            respi_rate: *float*
                The respiration rate of the patient at a specific second
            time: *str*
                The time stamp of the above vital
            respi_para:*list*
                The boundary conditions of the respiration rates
                The respiration rate high and low
            patient_name:*str*
                The name of the patient being monitored
        **Returns**
            None
        '''
        # global variables
        global EQUIPMENT_COUNT
        global counter
        global counter_e
        code = 5
        if respi_rate != 'NaN':
            if not (respi_rate > respi_para[1] and respi_rate < respi_para[0]):
                if counter[self.patient_id][code] == 0:
                    self.alert_nurse('Breathing', patient_name, time, code)
                else:
                    counter[self.patient_id][code] -= 1

            elif patient_mode[patient_name][4] == 1:
                if counter[self.patient_id][code] == 3:
                    patient_mode[patient_name][4] = 0
                    for i in code_ri[self.patient_id][code]:
                        self.page(i, '', '')
                        intern_list.extend([i])
                    code_ri[self.patient_id][code] = []
                    for i in code_re[self.patient_id][code]:
                        self.page(i, '', '')
                        resident_list.extend([i])
                    code_re[self.patient_id][code] = []
                else:
                    counter[self.patient_id][code] += 1

            if patient_mode_e[patient_name][4] == 1:
                if counter_e[self.patient_id][code] == 3:
                    patient_mode_e[patient_name][4] = 0
                    for i in code_eri[self.patient_id][code]:
                        self.page(i, '', '')
                        intern_list.extend([i])
                    code_eri[self.patient_id][code] = []
                    for i in code_ere[self.patient_id][code]:
                        self.page(i, '', '')
                        resident_list.extend([i])
                    code_ere[self.patient_id][code] = []
                    EQUIPMENT_COUNT += 1
                else:
                    counter_e[self.patient_id][code] += 1

        else:
            # Indicating equipment failure for NaN values
            if counter_e[self.patient_id][code] == 0:
                self.alert_nurse('equipment_failure', patient_name, time, code)
            else:
                counter_e[self.patient_id][code] -= 1

    def Spo2_abnormal(self, Spo2, time, patient_name):
        '''
        This function will monitor the oxygen saturation to alert when
        the patient suffers with breathing issues

        **Input Parameters**
            Spo2: *float*
                The oxygen saturation to the patient at a specific second
            time: *str*
                The time stamp of the above vital
            patient_name:*str*
                The name of the patient being monitored
        **Returns**
            None
        '''
        # global variables
        global EQUIPMENT_COUNT
        global counter
        global counter_e
        code = 6
        if Spo2 != 'NaN':
            if Spo2 < 95:
                if counter[self.patient_id][code] == 0:
                    self.alert_nurse('Spo2_abnormal', patient_name, time, code)
                else:
                    counter[self.patient_id][code] -= 1

            elif patient_mode[patient_name][5] == 1:
                if counter[self.patient_id][code] == 3:
                    patient_mode[patient_name][5] = 0
                    for i in code_ri[self.patient_id][code]:
                        self.page(i, '', '')
                        intern_list.extend([i])
                    code_ri[self.patient_id][code] = []
                    for i in code_re[self.patient_id][code]:
                        self.page(i, '', '')
                        resident_list.extend([i])
                    code_re[self.patient_id][code] = []
                else:
                    counter[self.patient_id][code] += 1

            if patient_mode_e[patient_name][5] == 1:
                if counter_e[self.patient_id][code] == 3:
                    patient_mode_e[patient_name][5] = 0
                    for i in code_eri[self.patient_id][code]:
                        self.page(i, '', '')
                        intern_list.extend([i])
                    code_eri[self.patient_id][code] = []
                    for i in code_ere[self.patient_id][code]:
                        self.page(i, '', '')
                        resident_list.extend([i])
                    code_ere[self.patient_id][code] = []
                    EQUIPMENT_COUNT += 1
                else:
                    counter_e[self.patient_id][code] += 1
        else:
            # Indicating equipment failure for NaN values
            if counter_e[self.patient_id][code] == 0:
                self.alert_nurse('equipment_failure', patient_name, time, code)
            else:
                counter_e[self.patient_id][code] -= 1


    def alert_nurse(self, code_emergency, patient_name, time, codes):
        '''
        This function will alert the nursing station about the patient
        emergency and will start paging protocols

        **Input Parameters**
            code_emergency: *str*
                The name of the emergency
            patient_name:*str*
                The name of the patient being monitored
            time: *str*
                The time stamp of the above vital
            codes: *int*
            The control parameters for alerting mechanism
        **Returns**
            None
        '''
        code = codes
        if code_emergency == 'Code_Blue':
            if patient_mode[patient_name][0] != 1:
                patient_mode[patient_name][0] = 1
                self.log(time, 'Code Blue identified',
                         'Alerting the nursing station', patient_name)
                self.nurse_ResInterns(code_emergency, patient_name, time, code)
                self.nurse_surgeons(code_emergency, patient_name, time, code)
                self.nurse_residents(code_emergency, patient_name, time, code)
                self.log(
                    time,
                    'Code Blue',
                    'Nurse station alerted',
                    patient_name)

        if code_emergency == 'Blood_Pressure':
            if patient_mode[patient_name][1] != 1:
                patient_mode[patient_name][1] = 1
                self.log(
                    time,
                    'Blood pressure',
                    'Alerting the nursing station',
                    patient_name)
                self.nurse_ResInterns(code_emergency, patient_name, time, code)
                self.nurse_surgeons(code_emergency, patient_name, time, code)
                self.nurse_residents(code_emergency, patient_name, time, code)
                self.log(
                    time,
                    'Blood pressure',
                    'Nurse station alerted',
                    patient_name)

        if code_emergency == 'Temperature':
            if patient_mode[patient_name][2] != 1:
                patient_mode[patient_name][2] = 1
                self.log(
                    time,
                    'Temperature',
                    'Alerting the nursing station',
                    patient_name)
                self.nurse_ResInterns(code_emergency, patient_name, time, code)
                self.nurse_residents(code_emergency, patient_name, time, code)
                self.log(time, 'Temperature nurse station',
                         'Nurse station alerted', patient_name)

        if code_emergency == 'Labor_Pains':
            if patient_mode[patient_name][3] != 1:
                patient_mode[patient_name][3] = 1
                self.log(
                    time,
                    'Labor_pains',
                    'Alerting the nursing station',
                    patient_name)
                self.nurse_ResInterns(code_emergency, patient_name, time, code)
                self.nurse_surgeons(code_emergency, patient_name, time, code)
                self.nurse_residents(code_emergency, patient_name, time, code)
                self.log(
                    time,
                    'Labor_pains',
                    'Nurse station alerted',
                    patient_name)

        if code_emergency == 'Breathing':
            if patient_mode[patient_name][4] != 1:
                patient_mode[patient_name][4] = 1
                self.log(time, 'Breathing obstruction',
                         'Alerting the nursing station', patient_name)
                self.nurse_ResInterns(code_emergency, patient_name, time, code)
                self.nurse_residents(code_emergency, patient_name, time, code)
                self.log(time, 'Breathing obstruction',
                         'Nurse station alerted', patient_name)

        if code_emergency == 'Spo2_abnormal':
            if patient_mode[patient_name][5] != 1:
                patient_mode[patient_name][5] = 1
                self.log(
                    time,
                    'Spo2 abnormal',
                    'Alerting the nursing station',
                    patient_name)
                self.nurse_ResInterns(code_emergency, patient_name, time, code)
                self.nurse_residents(code_emergency, patient_name, time, code)
                self.log(
                    time,
                    'Spo2 abnormal',
                    'Nurse station alerted',
                    patient_name)

        if code_emergency == 'equipment_failure':
            if patient_mode_e[patient_name][code - 1] != 1:
                patient_mode_e[patient_name][code - 1] = 1
                self.log(time, 'Equipment Failure detected',
                         'Alerting nurse station', patient_name)
                self.nurse_equipment(code_emergency, patient_name, time, code)
                self.log(
                    time,
                    'Equipment Failure',
                    'Nurse station alerted',
                    patient_name)


    def nurse_ResInterns(self, code_emergency, patient_name, time, codes):
        '''
        This function will let the nurses alert resident interns about the
        patient emergency and will start paging protocols

        **Input Parameters**
            code_emergency: *str*
                The name of the emergency
            patient_name:*str*
                The name of the patient being monitored
            time: *str*
                The time stamp of the above vital
            codes: *int*
            The control parameters for alerting mechanism
        **Returns**
            None
        '''
        # Calculating the number of interns
        code = codes
        intern_count = len(intern_list)
        # If there are available interns
        if intern_count > 1:
            # intern1 = intern_list.pop()
            intern1 = random.choice(intern_list)
            intern_list.remove(intern1)
            # intern2 = intern_list.pop()
            intern2 = random.choice(intern_list)
            intern_list.remove(intern2)
            code_ri[self.patient_id][code].extend([intern1, intern2])

            for i in code_ri[self.patient_id][code]:
                self.page(i, code_emergency, patient_name)
                self.log(time, 'Paging', i, patient_name)

    def nurse_residents(self, code_emergency, patient_name, time, codes):
        '''
        This function will let the nurses alert residents about the
        patient emergency and will start paging protocols

        **Input Parameters**
            code_emergency: *str*
                The name of the emergency
            patient_name:*str*
                The name of the patient being monitored
            time: *str*
                The time stamp of the above vital
            codes: *int*
            The control parameters for alerting mechanism
        **Returns**
            None
        '''
        code = codes
        resident_count = len(resident_list)
        # If there are available interns
        if resident_count > 0:
            # resident = resident_list.pop()
            resident = random.choice(resident_list)
            resident_list.remove(resident)
            code_re[self.patient_id][code].extend([resident])

            for i in code_re[self.patient_id][code]:
                self.page(i, code_emergency, patient_name)
                self.log(time, 'Paging', i, patient_name)

    def nurse_equipment(self, code_emergency, patient_name, time, codes):
        '''
        This function will let the nurses alert equipment team about the
        patient emergency and will start paging protocols

        **Input Parameters**
            code_emergency: *str*
                The name of the emergency
            patient_name:*str*
                The name of the patient being monitored
            time: *str*
                The time stamp of the above vital
            codes: *int*
            The control parameters for alerting mechanism
        **Returns**
            None
        '''
        # Recurring the global values to update
        global EQUIPMENT_COUNT
        code = codes
        intern_count = len(intern_list)
        resident_count = len(resident_list)
        # If there are available interns
        if intern_count > 0:

            intern1 = random.choice(intern_list)
            # intern1 = intern_list.pop()
            intern_list.remove(intern1)
            code_eri[self.patient_id][code].extend([intern1])
            for i in code_eri[self.patient_id][code]:
                self.page(i, code_emergency, patient_name)
                self.log(time, 'Paging', i, patient_name)

        if resident_count > 0:
            resident1 = random.choice(resident_list)
            # resident1 = resident_list.pop()
            resident_list.remove(resident1)
            code_ere[self.patient_id][code].extend([resident1])
            for i in code_ere[self.patient_id][code]:
                self.page(i, code_emergency, patient_name)
                self.log(time, 'Paging', i, patient_name)

        if EQUIPMENT_COUNT > 0:
            self.page('Equipment_team', code_emergency, patient_name)
            self.log(time, 'Paging', 'Equipment Team', patient_name)
            self.scrub(time, 'Equipment dispatched', patient_name)
            # print("Defibrillator dispatch initiated to room %s" %
            #       patient_key[patient_name])
            EQUIPMENT_COUNT -= 1
            self.scrub(time, 'Equipment ready', patient_name)

        else:
            self.scrub(time, 'Manual work', patient_name)
            self.log(time, 'alarm room', 'nurse station', patient_name)

    def nurse_surgeons(self, code_emergency, patient_name, time, codes):
        '''
        This function will let the nurses alert surgeons about the
        patient emergency and will start paging protocols

        **Input Parameters**
            code_emergency: *str*
                The name of the emergency
            patient_name:*str*
                The name of the patient being monitored
            time: *str*
                The time stamp of the above vital
            codes: *int*
            The control parameters for alerting mechanism
        **Returns**
            None
        '''
        code = codes
        surgeon_count = len(surgeon_list)
        # If there are available interns
        if surgeon_count > 0:

            # surgeon = surgeon_list.pop()
            surgeon = random.choice(surgeon_list)
            surgeon_list.remove(surgeon)
            code_s[self.patient_id][code].extend([surgeon])
            for i in code_s[self.patient_id][code]:
                self.page(i, code_emergency, patient_name)
                self.log(time, 'Paging', i, patient_name)

    def page(self, receiver_name, code_emergency, patient_name):
        '''
        This function will alert the specific hospital staff
        and can be visualized the GUI on pagers tab

        **Input Parameters**
            receiver_name: *str*
                The name of the specific hospital staff
            code_emergency: *str*
                The name of the emergency
            patient_name:*str*
                The name of the patient being monitored
        **Returns**
            None
        '''
        if patient_name == '':
            storage = (receiver_name, code_emergency, patient_name, '')
        else:
            storage = (
                receiver_name,
                code_emergency,
                patient_name,
                patient_key[patient_name])
        self.pages.append(storage)

    def log(self, time, activity, specific_person, patient_name):
        '''
        This function will log all the activities done for a
        patient during emergencies

        **Input Parameters**
            time: *str*
                The time stamp of the above emergency
            activity: *str*
                The activity performed during the emergency
            specific_person: *str*
                The name of the specific person
            patient_name:*str*
                The name of the patient being monitored
        **Returns**
            None
        '''
        text = f"{time}  {activity} - {specific_person} for patient {patient_name} \n"
        files = 'patient' + str(self.patient_id + 1) + '.txt'
        self.logs.append(text)
        with open(files, "a") as file:
            file.write(
                f"{time}  {activity} - {specific_person} for patient {patient_name} \n")

    def scrub(self, time, message, patient_name):
        '''
        This function will send an alert to the bedside monitor
        that equipment is not available and manual CPR is needed

        **Input Parameters**
            time: *str*
                The time stamp of the above emergency
            message: *str*
                Indicates no machines available
            patient_name:*str*
                The name of the patient being monitored
        **Returns**
            None
        '''
        # Entering the text file
        text = f"{time} - {message} for patient {patient_name} at room {patient_key[patient_name]}\n"
        self.scrubs.append(text)

class Visualisation(tk.Tk):
    '''
    This class establishes all the pages of the GUIDE
    Step 1: Initialise the parameters
    Step 2: Define the pages needs to be displayed on the GUIDE
    Step 3: Indicate that the Nurse frame as the start page
    Step 4: Show the frame

    '''

    def __init__(self, *args, **kwargs):

        tk.Tk.__init__(self, *args, **kwargs)
        # Title of the page
        tk.Tk.wm_title(self, "MEMAM")
        # initialising the parameters
        box = tk.Frame(self)
        box.pack(side="top", fill="both", expand=True)
        box.grid_rowconfigure(0, weight=1)
        box.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for Framei in (
                Nurse,
                Patient_1,
                Patient_2,
                Surgeons,
                Residents,
                Interns1,
                Interns2):

            frame = Framei(box, self)

            self.frames[Framei] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(Nurse)

    def show_frame(self, cont):

        frame = self.frames[cont]
        frame.tkraise()


class Patient_1(tk.Frame):
    '''
    This class is highlights the vitals of Patient 1 including
    the the Patient log
    Step 1: Define the layout of the Page
    Step 2: Define the vitals of the patient
    Step 3: Attach the Patient log
    Step 4: Attach the Scrub Message
    Step 5: Run the class MEMAM function to get the data

    '''

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        HEIGHT = 800
        WIDTH = 1000

        # Define the canvas of the frame
        C = tk.Canvas(self, height=HEIGHT, width=WIDTH, bg='#2f3442')
        C.pack()
        C = tk.Canvas(self, bg='#2f3442')
        # Position
        C.place(relx=0, rely=0, relwidth=1, relheight=1)

        # Title of the page
        framep = tk.Frame(self, background="#444953")
        framep.place(relx=0.01, rely=0.03, relwidth=0.98, relheight=0.075)
        patient = tk.Label(framep, text='Patient 1', font=(
            "Helvetica", 20, 'bold'), bg="#444953", fg='#ffffff')
        patient.place(relx=0, rely=0.03, relwidth=0.2, relheight=1)

        # Heart rate vital
        framehr = tk.Frame(self, background="#2e3138")
        framehr.place(relx=0.05, rely=0.15, relwidth=0.12, relheight=0.12)
        hrlabel = tk.Label(framehr, text='Heart Rate', font=(
            "Helvetica", 15, 'bold'), bg="#444953", fg='#ffffff')
        hrlabel.place(relx=0, rely=0, relwidth=1, relheight=0.35)
        hr = tk.Label(framehr, text='', font=(
            "Helvetica", 20, 'bold'), bg="#23252b", fg='#47b1bf')
        hr.place(relx=0, rely=0.35, relwidth=1, relheight=0.65)

        # Respiration rate vital
        framerr = tk.Frame(self, background="#2e3138")
        framerr.place(relx=0.2, rely=0.15, relwidth=0.12, relheight=0.12)
        rrlabel = tk.Label(framerr, text='Respiration Rate', font=(
            "Helvetica", 15, 'bold'), bg="#444953", fg='#ffffff')
        rrlabel.place(relx=0, rely=0, relwidth=1, relheight=0.35)
        rr = tk.Label(framerr, text='', font=(
            "Helvetica", 20, 'bold'), bg="#23252b", fg='#47bf59')
        rr.place(relx=0, rely=0.35, relwidth=1, relheight=0.65)

        # BP Systole vital
        framebps = tk.Frame(self, background="#2e3138")
        framebps.place(relx=0.35, rely=0.15, relwidth=0.12, relheight=0.12)
        bpslabel = tk.Label(framebps, text='Systole', font=(
            "Helvetica", 15, 'bold'), bg="#444953", fg='#ffffff')
        bpslabel.place(relx=0, rely=0, relwidth=1, relheight=0.35)
        bps = tk.Label(framebps, text='', font=(
            "Helvetica", 20, 'bold'), bg="#23252b", fg='#47b1bf')
        bps.place(relx=0, rely=0.35, relwidth=1, relheight=0.65)

        # BP Diastole vital
        framebpd = tk.Frame(self, background="#2e3138")
        framebpd.place(relx=0.5, rely=0.15, relwidth=0.12, relheight=0.12)
        bpdlabel = tk.Label(framebpd, text='Diastole', font=(
            "Helvetica", 15, 'bold'), bg="#444953", fg='#ffffff')
        bpdlabel.place(relx=0, rely=0, relwidth=1, relheight=0.35)
        bpd = tk.Label(framebpd, text='', font=(
            "Helvetica", 20, 'bold'), bg="#23252b", fg='#47bf59')
        bpd.place(relx=0, rely=0.35, relwidth=1, relheight=0.65)

        # BP SP02 vital
        framesp = tk.Frame(self, background="#2e3138")
        framesp.place(relx=0.65, rely=0.15, relwidth=0.12, relheight=0.12)
        splabel = tk.Label(framesp, text='SPO2', font=(
            "Helvetica", 15, 'bold'), bg="#444953", fg='#ffffff')
        splabel.place(relx=0, rely=0, relwidth=1, relheight=0.35)
        sp = tk.Label(framesp, text='', font=(
            "Helvetica", 20, 'bold'), bg="#23252b", fg='#47b1bf')
        sp.place(relx=0, rely=0.35, relwidth=1, relheight=0.65)

        # Temperature vital
        frametemp = tk.Frame(self, background="#2e3138")
        frametemp.place(relx=0.8, rely=0.15, relwidth=0.12, relheight=0.12)
        templabel = tk.Label(frametemp, text='Temperature', font=(
            "Helvetica", 15, 'bold'), bg="#444953", fg='#ffffff')
        templabel.place(relx=0, rely=0, relwidth=1, relheight=0.35)
        temp = tk.Label(frametemp, text='', font=(
            "Helvetica", 20, 'bold'), bg="#23252b", fg='#47bf59')
        temp.place(relx=0, rely=0.35, relwidth=1, relheight=0.65)

        # Return to Nurse station
        button = Button(
            framep,
            text="Nurse Station",
            command=lambda: controller.show_frame(Nurse),
            font=(
                "Helvetica",
                20,
                'bold'),
            bg="#444953",
            fg='#ffffff')
        button.place(relx=0.72, rely=0.1, relwidth=0.2, relheight=0.8)

        # Patient log
        loglabel = tk.Label(self, text='Patient Log', font=(
            "Helvetica", 20, 'bold'), bg="#444953", fg='#ffffff')
        loglabel.place(relx=0.05, rely=0.3, relwidth=0.87, relheight=0.05)
        framelog = tk.Frame(self, background="#2e3138")
        framelog.place(relx=0.05, rely=0.35, relwidth=0.87, relheight=0.3)
        loglist = tk.Listbox(framelog, font=(
            "Helvetica", 20, 'bold'), bg="#23252b", fg='#47bf59')
        loglist.place(relx=0, rely=0, relwidth=1, relheight=1)
        scrollbar1 = tk.Scrollbar(framelog, bg="#23252b")
        scrollbar1.pack(side='right', fill='y')

        # Scrub message
        scrublabel = tk.Label(self, text='Scrub Message', font=(
            "Helvetica", 20, 'bold'), bg="#444953", fg='#ffffff')
        scrublabel.place(relx=0.05, rely=0.67, relwidth=0.87, relheight=0.05)
        framescrub = tk.Frame(self, background="#2e3138")
        framescrub.place(relx=0.05, rely=0.72, relwidth=0.87, relheight=0.2)
        scrublist = tk.Listbox(framescrub, font=(
            "Helvetica", 20, 'bold'), bg="#23252b", fg='#47bf59')
        scrublist.place(relx=0, rely=0, relwidth=1, relheight=1)
        scrollbar2 = tk.Scrollbar(framescrub, bg="#23252b")
        scrollbar2.pack(side='right', fill='y')

        def live_update():
            '''
            The function will input patient 1 data in class MEMAM  function
            and get the vitals for visualisation
            **Input Parameters**
                None
            **Returns**
                None
            '''
            # If there is data in patient record
            if patient_1:
                # Remove first row of patient record and store in variable data
                data = patient_1.pop(0)
                # Run the MEMAM class
                obj1 = MEMAM(data, patient_record_1, 0)
                obj1()
                # Acquire the vitals
                hrList, bsList, bpdList, rrList, spList, tempList = obj1.values
                # Visualisation of vitals
                hr['text'] = str(hrList)
                rr['text'] = str(rrList)
                bps['text'] = str(bsList)
                bpd['text'] = str(bpdList)
                sp['text'] = str(spList)
                temp['text'] = str(tempList)
                # Visualisation of patient log
                # If log is not empty
                if obj1.logs:
                    for i in obj1.logs:
                        # Visualisation
                        loglist.insert(tk.END, i)
                loglist.config(yscrollcommand=scrollbar1.set)
                scrollbar1.config(command=loglist.yview)

                # Visualisation of scrub message
                # If scrub message is not empty
                if obj1.scrubs:
                    for i in obj1.scrubs:
                        scrublist.insert(tk.END, i)
                scrublist.config(yscrollcommand=scrollbar2.set)
                scrollbar2.config(command=loglist.yview)
            # Repeat loop for every second
            self.after(1000, live_update)

        # Run the function
        live_update()


class Patient_2(tk.Frame):
    '''
    This class is highlights the vitals of Patient 2 including
    the the Patient log
    Step 1: Define the layout of the Page
    Step 2: Define the vitals of the patient
    Step 3: Attach the Patient log
    Step 4: Attach the Scrub Message
    Step 5: Run the class MEMAM function to get the data

    '''

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        # Define canvas
        C = tk.Canvas(self, bg='#2f3442')
        C.place(relx=0, rely=0, relwidth=1, relheight=1)

        # Title of the page
        framep = tk.Frame(self, background="#444953")
        framep.place(relx=0.01, rely=0.03, relwidth=0.98, relheight=0.075)
        patient = tk.Label(framep, text='Patient 2', font=(
            "Helvetica", 20, 'bold'), bg="#444953", fg='#ffffff')
        patient.place(relx=0, rely=0.03, relwidth=0.2, relheight=1)

        # Heart rate vital
        framehr = tk.Frame(self, background="#2e3138")
        framehr.place(relx=0.05, rely=0.15, relwidth=0.12, relheight=0.12)
        hrlabel = tk.Label(framehr, text='Heart Rate', font=(
            "Helvetica", 15, 'bold'), bg="#444953", fg='#ffffff')
        hrlabel.place(relx=0, rely=0, relwidth=1, relheight=0.35)
        hr = tk.Label(framehr, text='', font=(
            "Helvetica", 20, 'bold'), bg="#23252b", fg='#47b1bf')
        hr.place(relx=0, rely=0.35, relwidth=1, relheight=0.65)

        # Respiration rate vital
        framerr = tk.Frame(self, background="#2e3138")
        framerr.place(relx=0.2, rely=0.15, relwidth=0.12, relheight=0.12)
        rrlabel = tk.Label(framerr, text='Respiration Rate', font=(
            "Helvetica", 15, 'bold'), bg="#444953", fg='#ffffff')
        rrlabel.place(relx=0, rely=0, relwidth=1, relheight=0.35)
        rr = tk.Label(framerr, text='', font=(
            "Helvetica", 20, 'bold'), bg="#23252b", fg='#47bf59')
        rr.place(relx=0, rely=0.35, relwidth=1, relheight=0.65)

        # BP Systole vital
        framebps = tk.Frame(self, background="#2e3138")
        framebps.place(relx=0.35, rely=0.15, relwidth=0.12, relheight=0.12)
        bpslabel = tk.Label(framebps, text='Systole', font=(
            "Helvetica", 15, 'bold'), bg="#444953", fg='#ffffff')
        bpslabel.place(relx=0, rely=0, relwidth=1, relheight=0.35)
        bps = tk.Label(framebps, text='', font=(
            "Helvetica", 20, 'bold'), bg="#23252b", fg='#47b1bf')
        bps.place(relx=0, rely=0.35, relwidth=1, relheight=0.65)

        # BP Diastole vital
        framebpd = tk.Frame(self, background="#2e3138")
        framebpd.place(relx=0.5, rely=0.15, relwidth=0.12, relheight=0.12)
        bpdlabel = tk.Label(framebpd, text='Diastole', font=(
            "Helvetica", 15, 'bold'), bg="#444953", fg='#ffffff')
        bpdlabel.place(relx=0, rely=0, relwidth=1, relheight=0.35)
        bpd = tk.Label(framebpd, text='', font=(
            "Helvetica", 20, 'bold'), bg="#23252b", fg='#47bf59')
        bpd.place(relx=0, rely=0.35, relwidth=1, relheight=0.65)

        # BP Diastole vital
        framesp = tk.Frame(self, background="#2e3138")
        framesp.place(relx=0.65, rely=0.15, relwidth=0.12, relheight=0.12)
        splabel = tk.Label(framesp, text='SPO2', font=(
            "Helvetica", 15, 'bold'), bg="#444953", fg='#ffffff')
        splabel.place(relx=0, rely=0, relwidth=1, relheight=0.35)
        sp = tk.Label(framesp, text='', font=(
            "Helvetica", 20, 'bold'), bg="#23252b", fg='#47b1bf')
        sp.place(relx=0, rely=0.35, relwidth=1, relheight=0.65)

        # Temperature vital
        frametemp = tk.Frame(self, background="#2e3138")
        frametemp.place(relx=0.8, rely=0.15, relwidth=0.12, relheight=0.12)
        templabel = tk.Label(frametemp, text='Temperature', font=(
            "Helvetica", 15, 'bold'), bg="#444953", fg='#ffffff')
        templabel.place(relx=0, rely=0, relwidth=1, relheight=0.35)
        temp = tk.Label(frametemp, text='', font=(
            "Helvetica", 20, 'bold'), bg="#23252b", fg='#47bf59')
        temp.place(relx=0, rely=0.35, relwidth=1, relheight=0.65)

        # Return to Nurse Station
        button = Button(
            framep,
            text="Nurse Station",
            command=lambda: controller.show_frame(Nurse),
            font=(
                "Helvetica",
                20,
                'bold'),
            bg="#444953",
            fg='#ffffff')
        button.place(relx=0.72, rely=0.1, relwidth=0.2, relheight=0.8)

        # Patient log
        loglabel = tk.Label(self, text='Patient Log', font=(
            "Helvetica", 20, 'bold'), bg="#444953", fg='#ffffff')
        loglabel.place(relx=0.05, rely=0.3, relwidth=0.87, relheight=0.05)
        framelog = tk.Frame(self, background="#2e3138")
        framelog.place(relx=0.05, rely=0.35, relwidth=0.87, relheight=0.3)
        loglist = tk.Listbox(framelog, font=(
            "Helvetica", 20, 'bold'), bg="#23252b", fg='#47bf59')
        loglist.place(relx=0, rely=0, relwidth=1, relheight=1)
        scrollbar1 = tk.Scrollbar(framelog, bg="#23252b")
        scrollbar1.pack(side='right', fill='y')

        # Scrub Message
        scrublabel = tk.Label(self, text='Scrub Message', font=(
            "Helvetica", 20, 'bold'), bg="#444953", fg='#ffffff')
        scrublabel.place(relx=0.05, rely=0.67, relwidth=0.87, relheight=0.05)
        framescrub = tk.Frame(self, background="#2e3138")
        framescrub.place(relx=0.05, rely=0.72, relwidth=0.87, relheight=0.2)
        scrublist = tk.Listbox(framescrub, font=(
            "Helvetica", 20, 'bold'), bg="#23252b", fg='#47bf59')
        scrublist.place(relx=0, rely=0, relwidth=1, relheight=1)
        scrollbar2 = tk.Scrollbar(framescrub, bg="#23252b")
        scrollbar2.pack(side='right', fill='y')

        def live_update():
            '''
            The function will input patient 2 data in class MEMAM  function
            and get the vitals for visualisation
            **Input Parameters**
                None
            **Returns**
                None
            '''
            # If there is data in patient record
            if patient_2:
                # Remove first row of record and store in 'data'
                data = patient_2.pop(0)
                # Run MEMAM class to acquire vitals
                obj2 = MEMAM(data, patient_record_2, 1)
                obj2()
                # Vitals visualisation
                hrList, bsList, bpdList, rrList, spList, tempList = obj2.values
                hr['text'] = str(hrList)
                rr['text'] = str(rrList)
                bps['text'] = str(bsList)
                bpd['text'] = str(bpdList)
                sp['text'] = str(spList)
                temp['text'] = str(tempList)
                # Visualisation of patient log
                # If log is not empty
                if obj2.logs:
                    for i in obj2.logs:
                        loglist.insert(tk.END, i)
                loglist.config(yscrollcommand=scrollbar1.set)
                scrollbar1.config(command=loglist.yview)

                # Visualisation of scrub message
                # If scrub message is not empty
                if obj2.scrubs:
                    for i in obj2.scrubs:
                        scrublist.insert(tk.END, i)
                scrublist.config(yscrollcommand=scrollbar2.set)
                scrollbar2.config(command=loglist.yview)
            # Repeat the function after every second
            self.after(1000, live_update)
        # Run the function
        live_update()


class Surgeons(tk.Frame):
    '''
    This class depicts the surgeons pager's view
    the the Patient log
    Step 1: Define the layout of the Page
    Step 2: Define the list of surgeons
    Step 3: Page the required surgeon when MEMAM is called

    '''

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        # Define canvas
        C = tk.Canvas(self, bg='#2f3442')
        C.place(relx=0, rely=0, relwidth=1, relheight=1)

        # Title of the page
        tframe = tk.Frame(self, background="#444953")
        tframe.place(relx=0.01, rely=0.03, relwidth=0.98, relheight=0.075)
        tlabel = tk.Label(tframe, text='SURGEONS PAGER VIEW', font=(
            "Helvetica", 20, 'bold'), bg="#444953", fg='#ffffff')
        tlabel.place(relx=0.05, rely=0.03, relwidth=0.4, relheight=1)

        # Surgeon 1
        frame_1 = tk.Frame(self, background="#647886")
        frame_1.place(relx=0.1, rely=0.2, relwidth=0.2, relheight=0.3)
        label_1 = tk.Label(frame_1, text='Surgeon 1', font=(
            "Helvetica", 20, 'bold'), bg="#444953", fg='#ffffff')
        label_1.place(relx=0, rely=0, relwidth=1, relheight=0.35)
        val_1 = tk.Label(frame_1, text='', font=(
            "Helvetica", 20, 'bold'), bg="#23252b", fg='#47bf59')
        val_1.place(relx=0, rely=0.35, relwidth=1, relheight=0.65)

        # Surgeon 2
        frame_2 = tk.Frame(self, background="#647886")
        frame_2.place(relx=0.1, rely=0.6, relwidth=0.2, relheight=0.3)
        label_2 = tk.Label(frame_2, text='Surgeon 2', font=(
            "Helvetica", 20, 'bold'), bg="#444953", fg='#ffffff')
        label_2.place(relx=0, rely=0, relwidth=1, relheight=0.35)
        val_2 = tk.Label(frame_2, text='', font=(
            "Helvetica", 20, 'bold'), bg="#23252b", fg='#47bf59')
        val_2.place(relx=0, rely=0.35, relwidth=1, relheight=0.65)

        # Surgeon 3
        frame_3 = tk.Frame(self, background="#647886")
        frame_3.place(relx=0.4, rely=0.2, relwidth=0.2, relheight=0.3)
        label_3 = tk.Label(frame_3, text='Surgeon 3', font=(
            "Helvetica", 20, 'bold'), bg="#444953", fg='#ffffff')
        label_3.place(relx=0, rely=0, relwidth=1, relheight=0.35)
        val_3 = tk.Label(frame_3, text='', font=(
            "Helvetica", 20, 'bold'), bg="#23252b", fg='#47bf59')
        val_3.place(relx=0, rely=0.35, relwidth=1, relheight=0.65)

        # Surgeon 4
        frame_4 = tk.Frame(self, background="#647886")
        frame_4.place(relx=0.4, rely=0.6, relwidth=0.2, relheight=0.3)
        label_4 = tk.Label(frame_4, text='Surgeon 4', font=(
            "Helvetica", 20, 'bold'), bg="#444953", fg='#ffffff')
        label_4.place(relx=0, rely=0, relwidth=1, relheight=0.35)
        val_4 = tk.Label(frame_4, text='', font=(
            "Helvetica", 20, 'bold'), bg="#23252b", fg='#47bf59')
        val_4.place(relx=0, rely=0.35, relwidth=1, relheight=0.65)

        # Surgeon 5
        frame_5 = tk.Frame(self, background="#647886")
        frame_5.place(relx=0.7, rely=0.2, relwidth=0.2, relheight=0.3)
        label_5 = tk.Label(frame_5, text='Surgeon 5', font=(
            "Helvetica", 20, 'bold'), bg="#444953", fg='#ffffff')
        label_5.place(relx=0, rely=0, relwidth=1, relheight=0.35)
        val_5 = tk.Label(frame_5, text='', font=(
            "Helvetica", 20, 'bold'), bg="#23252b", fg='#47bf59')
        val_5.place(relx=0, rely=0.35, relwidth=1, relheight=0.65)

        # Surgeon 6
        frame_6 = tk.Frame(self, background="#647886")
        frame_6.place(relx=0.7, rely=0.6, relwidth=0.2, relheight=0.3)
        label_6 = tk.Label(frame_6, text='Surgeon 6', font=(
            "Helvetica", 20, 'bold'), bg="#444953", fg='#ffffff')
        label_6.place(relx=0, rely=0, relwidth=1, relheight=0.35)
        val_6 = tk.Label(frame_6, text='', font=(
            "Helvetica", 20, 'bold'), bg="#23252b", fg='#47bf59')
        val_6.place(relx=0, rely=0.35, relwidth=1, relheight=0.65)

        # key value pair to assign the appropriate surgeon
        key_pair = {1: val_1, 2: val_2, 3: val_3, 4: val_4, 5: val_5, 6: val_6}

        def live_update():
            '''
            The function is meant to page the assinged surgeon with
            the necessary task
            **Input Parameters**
                None
            **Returns**
                None
            '''
            # Paging for patient 1
            for item1 in PAGES[0]:
                name1, code_e1, p1, r1 = item1
                if name1[0] == 's':
                    code = int(name1[-2:])
                    # Assign the assined surgeon to patient 1
                    key_pair[code]['text'] = code_e1 + '\n' + p1 + '\n' + r1
            # Paging for patient 2
            for item2 in PAGES[1]:
                receiver_name, code_emergency, patient_name, room = item2
                if receiver_name[0] == 's':
                    # Assign the assined surgeon to patient 2
                    code = int(receiver_name[-2:])
                    key_pair[code]['text'] = code_emergency + \
                        '\n' + patient_name + '\n' + room
            # Rerun the function after every second
            self.after(1000, live_update)

        live_update()

        # Return to nurse station
        button = Button(
            tframe,
            text="Nurse Station",
            command=lambda: controller.show_frame(Nurse),
            font=(
                "Helvetica",
                20,
                'bold'),
            bg="#444953",
            fg='#ffffff')
        button.place(relx=0.72, rely=0.1, relwidth=0.2, relheight=0.8)


class Residents(tk.Frame):
    '''
    This class depicts the residents pager's view
    the the Patient log
    Step 1: Define the layout of the Page
    Step 2: Define the list of residents
    Step 3: Page the required residents when MEMAM is called

    '''

    def __init__(self, parent, controller):
        # Define canvas
        tk.Frame.__init__(self, parent)
        C = tk.Canvas(self, bg='#2f3442')
        C.place(relx=0, rely=0, relwidth=1, relheight=1)

        # Title of the page
        tframe = tk.Frame(self, background="#444953")
        tframe.place(relx=0.01, rely=0.03, relwidth=0.98, relheight=0.075)
        tlabel = tk.Label(tframe, text='RESIDENTS PAGER VIEW', font=(
            "Helvetica", 20, 'bold'), bg="#444953", fg='#ffffff')
        tlabel.place(relx=0.05, rely=0.03, relwidth=0.4, relheight=1)

        # Resident 1
        frame_1 = tk.Frame(self, background="#647886")
        frame_1.place(relx=0.02, rely=0.2, relwidth=0.2, relheight=0.3)
        label_1 = tk.Label(frame_1, text='Resident 1', font=(
            "Helvetica", 20, 'bold'), bg="#444953", fg='#ffffff')
        label_1.place(relx=0, rely=0, relwidth=1, relheight=0.35)
        val_1 = tk.Label(frame_1, text='', font=(
            "Helvetica", 20, 'bold'), bg="#23252b", fg='#47bf59')
        val_1.place(relx=0, rely=0.35, relwidth=1, relheight=0.65)

        # Resident 2
        frame_2 = tk.Frame(self, background="#647886")
        frame_2.place(relx=0.02, rely=0.6, relwidth=0.2, relheight=0.3)
        label_2 = tk.Label(frame_2, text='Resident 2', font=(
            "Helvetica", 20, 'bold'), bg="#444953", fg='#ffffff')
        label_2.place(relx=0, rely=0, relwidth=1, relheight=0.35)
        val_2 = tk.Label(frame_2, text='', font=(
            "Helvetica", 20, 'bold'), bg="#23252b", fg='#47bf59')
        val_2.place(relx=0, rely=0.35, relwidth=1, relheight=0.65)

        # Resident 3
        frame_3 = tk.Frame(self, background="#647886")
        frame_3.place(relx=0.27, rely=0.2, relwidth=0.2, relheight=0.3)
        label_3 = tk.Label(frame_3, text='Resident 3', font=(
            "Helvetica", 20, 'bold'), bg="#444953", fg='#ffffff')
        label_3.place(relx=0, rely=0, relwidth=1, relheight=0.35)
        val_3 = tk.Label(frame_3, text='', font=(
            "Helvetica", 20, 'bold'), bg="#23252b", fg='#47bf59')
        val_3.place(relx=0, rely=0.35, relwidth=1, relheight=0.65)

        # Resident 4
        frame_4 = tk.Frame(self, background="#647886")
        frame_4.place(relx=0.27, rely=0.6, relwidth=0.2, relheight=0.3)
        label_4 = tk.Label(frame_4, text='Resident 4', font=(
            "Helvetica", 20, 'bold'), bg="#444953", fg='#ffffff')
        label_4.place(relx=0, rely=0, relwidth=1, relheight=0.35)
        val_4 = tk.Label(frame_4, text='', font=(
            "Helvetica", 20, 'bold'), bg="#23252b", fg='#47bf59')
        val_4.place(relx=0, rely=0.35, relwidth=1, relheight=0.65)

        # Resident 5
        frame_5 = tk.Frame(self, background="#647886")
        frame_5.place(relx=0.52, rely=0.2, relwidth=0.2, relheight=0.3)
        label_5 = tk.Label(frame_5, text='Resident 5', font=(
            "Helvetica", 20, 'bold'), bg="#444953", fg='#ffffff')
        label_5.place(relx=0, rely=0, relwidth=1, relheight=0.35)
        val_5 = tk.Label(frame_5, text='', font=(
            "Helvetica", 20, 'bold'), bg="#23252b", fg='#47bf59')
        val_5.place(relx=0, rely=0.35, relwidth=1, relheight=0.65)

        # Resident 6
        frame_6 = tk.Frame(self, background="#647886")
        frame_6.place(relx=0.52, rely=0.6, relwidth=0.2, relheight=0.3)
        label_6 = tk.Label(frame_6, text='Resident 6', font=(
            "Helvetica", 20, 'bold'), bg="#444953", fg='#ffffff')
        label_6.place(relx=0, rely=0, relwidth=1, relheight=0.35)
        val_6 = tk.Label(frame_6, text='', font=(
            "Helvetica", 20, 'bold'), bg="#23252b", fg='#47bf59')
        val_6.place(relx=0, rely=0.35, relwidth=1, relheight=0.65)

        # Resident 7
        frame_7 = tk.Frame(self, background="#647886")
        frame_7.place(relx=0.77, rely=0.2, relwidth=0.2, relheight=0.3)
        label_7 = tk.Label(frame_7, text='Resident 7', font=(
            "Helvetica", 20, 'bold'), bg="#444953", fg='#ffffff')
        label_7.place(relx=0, rely=0, relwidth=1, relheight=0.35)
        val_7 = tk.Label(frame_7, text='', font=(
            "Helvetica", 20, 'bold'), bg="#23252b", fg='#47bf59')
        val_7.place(relx=0, rely=0.35, relwidth=1, relheight=0.65)

        # Resident 8
        frame_8 = tk.Frame(self, background="#647886")
        frame_8.place(relx=0.77, rely=0.6, relwidth=0.2, relheight=0.3)
        label_8 = tk.Label(frame_8, text='Resident 8', font=(
            "Helvetica", 20, 'bold'), bg="#444953", fg='#ffffff')
        label_8.place(relx=0, rely=0, relwidth=1, relheight=0.35)
        val_8 = tk.Message(frame_8, text='', font=(
            "Helvetica", 20, 'bold'), bg="#23252b", fg='#47bf59', width=200)
        val_8.place(relx=0, rely=0.35, relwidth=1, relheight=0.65)

        # key value pair to assign the appropriate resident
        key_pair = {
            1: val_1,
            2: val_2,
            3: val_3,
            4: val_4,
            5: val_5,
            6: val_6,
            7: val_7,
            8: val_8}

        def live_update():
            '''
            The function is meant to page the assinged resident with
            the necessary task
            **Input Parameters**
                None
            **Returns**
                None
            '''
            # Paging for patient 1
            for item1 in PAGES[0]:
                receiver_name, code_emergency, patient_name, room = item1
                if receiver_name[0] == 'r':
                    code = int(receiver_name[-2:])
                    # Assign the assined surgeon to patient 1
                    key_pair[code]['text'] = code_emergency + \
                        '\n' + patient_name + '\n' + room
            # Paging for patient 1
            for item2 in PAGES[1]:
                receiver_name, code_emergency, patient_name, room = item2
                if receiver_name[0] == 'r':
                    code = int(receiver_name[-2:])
                    # Assign the assined surgeon to patient 2
                    key_pair[code]['text'] = code_emergency + \
                        '\n' + patient_name + '\n' + room

            # Rerun the function after every second
            self.after(1000, live_update)

        live_update()

        # Return to Nurse station
        button = Button(
            tframe,
            text="Nurse Station",
            command=lambda: controller.show_frame(Nurse),
            font=(
                "Helvetica",
                20,
                'bold'),
            bg="#444953",
            fg='#ffffff')
        button.place(relx=0.72, rely=0.1, relwidth=0.2, relheight=0.8)


class Interns1(tk.Frame):
    '''
    This class depicts the first batch of intens pager's view
    the the Patient log
    Step 1: Define the layout of the Page
    Step 2: Define the list of interns
    Step 3: Page the required interns when MEMAM is called

    '''

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        # Define the canvas
        C = tk.Canvas(self, bg='#2f3442')
        C.place(relx=0, rely=0, relwidth=1, relheight=1)

        # Title of the page
        tframe = tk.Frame(self, background="#444953")
        tframe.place(relx=0.01, rely=0.03, relwidth=0.98, relheight=0.075)
        tlabel = tk.Label(tframe, text='INTERNS PAGER VIEW 1', font=(
            "Helvetica", 20, 'bold'), bg="#444953", fg='#ffffff')
        tlabel.place(relx=0.05, rely=0.03, relwidth=0.4, relheight=1)

        # Intern 1
        frame_1 = tk.Frame(self, background="#647886")
        frame_1.place(relx=0.02, rely=0.2, relwidth=0.2, relheight=0.3)
        label_1 = tk.Label(frame_1, text='Intern 1', font=(
            "Helvetica", 20, 'bold'), bg="#444953", fg='#ffffff')
        label_1.place(relx=0, rely=0, relwidth=1, relheight=0.35)
        val_1 = tk.Label(frame_1, text='', font=(
            "Helvetica", 20, 'bold'), bg="#23252b", fg='#47bf59')
        val_1.place(relx=0, rely=0.35, relwidth=1, relheight=0.65)

        # Intern 2
        frame_2 = tk.Frame(self, background="#647886")
        frame_2.place(relx=0.02, rely=0.6, relwidth=0.2, relheight=0.3)
        label_2 = tk.Label(frame_2, text='Intern 2', font=(
            "Helvetica", 20, 'bold'), bg="#444953", fg='#ffffff')
        label_2.place(relx=0, rely=0, relwidth=1, relheight=0.35)
        val_2 = tk.Label(frame_2, text='', font=(
            "Helvetica", 20, 'bold'), bg="#23252b", fg='#47bf59')
        val_2.place(relx=0, rely=0.35, relwidth=1, relheight=0.65)

        # Intern 3
        frame_3 = tk.Frame(self, background="#647886")
        frame_3.place(relx=0.27, rely=0.2, relwidth=0.2, relheight=0.3)
        label_3 = tk.Label(frame_3, text='Intern 3', font=(
            "Helvetica", 20, 'bold'), bg="#444953", fg='#ffffff')
        label_3.place(relx=0, rely=0, relwidth=1, relheight=0.35)
        val_3 = tk.Label(frame_3, text='', font=(
            "Helvetica", 20, 'bold'), bg="#23252b", fg='#47bf59')
        val_3.place(relx=0, rely=0.35, relwidth=1, relheight=0.65)

        # Intern 4
        frame_4 = tk.Frame(self, background="#647886")
        frame_4.place(relx=0.27, rely=0.6, relwidth=0.2, relheight=0.3)
        label_4 = tk.Label(frame_4, text='Intern 4', font=(
            "Helvetica", 20, 'bold'), bg="#444953", fg='#ffffff')
        label_4.place(relx=0, rely=0, relwidth=1, relheight=0.35)
        val_4 = tk.Label(frame_4, text='', font=(
            "Helvetica", 20, 'bold'), bg="#23252b", fg='#47bf59')
        val_4.place(relx=0, rely=0.35, relwidth=1, relheight=0.65)

        # Intern 5
        frame_5 = tk.Frame(self, background="#647886")
        frame_5.place(relx=0.52, rely=0.2, relwidth=0.2, relheight=0.3)
        label_5 = tk.Label(frame_5, text='Intern 5', font=(
            "Helvetica", 20, 'bold'), bg="#444953", fg='#ffffff')
        label_5.place(relx=0, rely=0, relwidth=1, relheight=0.35)
        val_5 = tk.Label(frame_5, text='', font=(
            "Helvetica", 20, 'bold'), bg="#23252b", fg='#47bf59')
        val_5.place(relx=0, rely=0.35, relwidth=1, relheight=0.65)

        # Intern 6
        frame_6 = tk.Frame(self, background="#647886")
        frame_6.place(relx=0.52, rely=0.6, relwidth=0.2, relheight=0.3)
        label_6 = tk.Label(frame_6, text='Intern 6', font=(
            "Helvetica", 20, 'bold'), bg="#444953", fg='#ffffff')
        label_6.place(relx=0, rely=0, relwidth=1, relheight=0.35)
        val_6 = tk.Label(frame_6, text='', font=(
            "Helvetica", 20, 'bold'), bg="#23252b", fg='#47bf59')
        val_6.place(relx=0, rely=0.35, relwidth=1, relheight=0.65)

        # Intern 7
        frame_7 = tk.Frame(self, background="#647886")
        frame_7.place(relx=0.77, rely=0.2, relwidth=0.2, relheight=0.3)
        label_7 = tk.Label(frame_7, text='Intern 7', font=(
            "Helvetica", 20, 'bold'), bg="#444953", fg='#ffffff')
        label_7.place(relx=0, rely=0, relwidth=1, relheight=0.35)
        val_7 = tk.Label(frame_7, text='', font=(
            "Helvetica", 20, 'bold'), bg="#23252b", fg='#47bf59')
        val_7.place(relx=0, rely=0.35, relwidth=1, relheight=0.65)

        # Intern 8
        frame_8 = tk.Frame(self, background="#647886")
        frame_8.place(relx=0.77, rely=0.6, relwidth=0.2, relheight=0.3)
        label_8 = tk.Label(frame_8, text='Intern 8', font=(
            "Helvetica", 20, 'bold'), bg="#444953", fg='#ffffff')
        label_8.place(relx=0, rely=0, relwidth=1, relheight=0.35)
        val_8 = tk.Label(frame_8, text='', font=(
            "Helvetica", 20, 'bold'), bg="#23252b", fg='#47bf59', width=200)
        val_8.place(relx=0, rely=0.35, relwidth=1, relheight=0.65)

        # key value pair to assign the appropriate resident
        key_pair = {
            1: val_1,
            2: val_2,
            3: val_3,
            4: val_4,
            5: val_5,
            6: val_6,
            7: val_7,
            8: val_8}

        def live_update():
            '''
            The function is meant to page the assinged intern with
            the necessary task
            **Input Parameters**
                None
            **Returns**
                None
            '''
            # Paging for patient 1
            for item1 in PAGES[0]:
                receiver_name, code_emergency, patient_name, room = item1
                if receiver_name[0] == 'i':
                    code = int(receiver_name[-2:])
                    if code in key_pair:
                        # Assign the assined surgeon to patient 1
                        key_pair[code]['text'] = code_emergency + \
                            '\n' + patient_name + '\n' + room
            # Paging for patient 2
            for item2 in PAGES[1]:
                receiver_name, code_emergency, patient_name, room = item2
                if receiver_name[0] == 'i':
                    code = int(receiver_name[-2:])
                    if code in key_pair:
                        # Assign the assined surgeon to patient 2
                        key_pair[code]['text'] = code_emergency + \
                            '\n' + patient_name + '\n' + room
            # Rerun the function after every second
            self.after(1000, live_update)
        # Run the function
        live_update()

        # Retun to Nurse Station
        button1 = Button(
            tframe,
            text="Nurse Station",
            command=lambda: controller.show_frame(Nurse),
            font=(
                "Helvetica",
                20,
                'bold'),
            bg="#444953",
            fg='#ffffff')
        button1.place(relx=0.78, rely=0.1, relwidth=0.2, relheight=0.8)

        # Show page of Second Batch of Interns
        button2 = Button(
            tframe,
            text="Interns 2",
            command=lambda: controller.show_frame(Interns2),
            font=(
                "Helvetica",
                20,
                'bold'),
            bg="#444953",
            fg='#ffffff')
        button2.place(relx=0.56, rely=0.1, relwidth=0.2, relheight=0.8)


class Interns2(tk.Frame):
    '''
    This class depicts the second batch of intens pager's view
    the the Patient log
    Step 1: Define the layout of the Page
    Step 2: Define the list of interns
    Step 3: Page the required interns when MEMAM is called

    '''

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        # Define the canvas
        C = tk.Canvas(self, bg='#2f3442')
        C.place(relx=0, rely=0, relwidth=1, relheight=1)

        # Title of the page
        tframe = tk.Frame(self, background="#444953")
        tframe.place(relx=0.01, rely=0.03, relwidth=0.98, relheight=0.075)
        tlabel = tk.Label(tframe, text='INTERNS PAGER VIEW 2', font=(
            "Helvetica", 20, 'bold'), bg="#444953", fg='#ffffff')
        tlabel.place(relx=0.05, rely=0.03, relwidth=0.4, relheight=1)

        # Intern 9
        frame_1 = tk.Frame(self, background="#647886")
        frame_1.place(relx=0.02, rely=0.2, relwidth=0.2, relheight=0.3)
        label_1 = tk.Label(frame_1, text='Intern 9', font=(
            "Helvetica", 20, 'bold'), bg="#444953", fg='#ffffff')
        label_1.place(relx=0, rely=0, relwidth=1, relheight=0.35)
        val_1 = tk.Label(frame_1, text='', font=(
            "Helvetica", 20, 'bold'), bg="#23252b", fg='#47bf59')
        val_1.place(relx=0, rely=0.35, relwidth=1, relheight=0.65)

        # Intern 10
        frame_2 = tk.Frame(self, background="#647886")
        frame_2.place(relx=0.02, rely=0.6, relwidth=0.2, relheight=0.3)
        label_2 = tk.Label(frame_2, text='Intern 10', font=(
            "Helvetica", 20, 'bold'), bg="#444953", fg='#ffffff')
        label_2.place(relx=0, rely=0, relwidth=1, relheight=0.35)
        val_2 = tk.Label(frame_2, text='', font=(
            "Helvetica", 20, 'bold'), bg="#23252b", fg='#47bf59')
        val_2.place(relx=0, rely=0.35, relwidth=1, relheight=0.65)

        # Intern 11
        frame_3 = tk.Frame(self, background="#647886")
        frame_3.place(relx=0.27, rely=0.2, relwidth=0.2, relheight=0.3)
        label_3 = tk.Label(frame_3, text='Intern 11', font=(
            "Helvetica", 20, 'bold'), bg="#444953", fg='#ffffff')
        label_3.place(relx=0, rely=0, relwidth=1, relheight=0.35)
        val_3 = tk.Label(frame_3, text='', font=(
            "Helvetica", 20, 'bold'), bg="#23252b", fg='#47bf59')
        val_3.place(relx=0, rely=0.35, relwidth=1, relheight=0.65)

        # Intern 12
        frame_4 = tk.Frame(self, background="#647886")
        frame_4.place(relx=0.27, rely=0.6, relwidth=0.2, relheight=0.3)
        label_4 = tk.Label(frame_4, text='Intern 12', font=(
            "Helvetica", 20, 'bold'), bg="#444953", fg='#ffffff')
        label_4.place(relx=0, rely=0, relwidth=1, relheight=0.35)
        val_4 = tk.Label(frame_4, text='', font=(
            "Helvetica", 20, 'bold'), bg="#23252b", fg='#47bf59')
        val_4.place(relx=0, rely=0.35, relwidth=1, relheight=0.65)

        # Intern 13
        frame_5 = tk.Frame(self, background="#647886")
        frame_5.place(relx=0.52, rely=0.2, relwidth=0.2, relheight=0.3)
        label_5 = tk.Label(frame_5, text='Intern 13', font=(
            "Helvetica", 20, 'bold'), bg="#444953", fg='#ffffff')
        label_5.place(relx=0, rely=0, relwidth=1, relheight=0.35)
        val_5 = tk.Label(frame_5, text='', font=(
            "Helvetica", 20, 'bold'), bg="#23252b", fg='#47bf59')
        val_5.place(relx=0, rely=0.35, relwidth=1, relheight=0.65)

        # Intern 14
        frame_6 = tk.Frame(self, background="#647886")
        frame_6.place(relx=0.52, rely=0.6, relwidth=0.2, relheight=0.3)
        label_6 = tk.Label(frame_6, text='Intern 14', font=(
            "Helvetica", 20, 'bold'), bg="#444953", fg='#ffffff')
        label_6.place(relx=0, rely=0, relwidth=1, relheight=0.35)
        val_6 = tk.Label(frame_6, text='', font=(
            "Helvetica", 20, 'bold'), bg="#23252b", fg='#47bf59')
        val_6.place(relx=0, rely=0.35, relwidth=1, relheight=0.65)

        # Intern 15
        frame_7 = tk.Frame(self, background="#647886")
        frame_7.place(relx=0.77, rely=0.2, relwidth=0.2, relheight=0.3)
        label_7 = tk.Label(frame_7, text='Intern 15', font=(
            "Helvetica", 20, 'bold'), bg="#444953", fg='#ffffff')
        label_7.place(relx=0, rely=0, relwidth=1, relheight=0.35)
        val_7 = tk.Label(frame_7, text='', font=(
            "Helvetica", 20, 'bold'), bg="#23252b", fg='#47bf59')
        val_7.place(relx=0, rely=0.35, relwidth=1, relheight=0.65)

        # Intern 16
        frame_8 = tk.Frame(self, background="#647886")
        frame_8.place(relx=0.77, rely=0.6, relwidth=0.2, relheight=0.3)
        label_8 = tk.Label(frame_8, text='Intern 16', font=(
            "Helvetica", 20, 'bold'), bg="#444953", fg='#ffffff')
        label_8.place(relx=0, rely=0, relwidth=1, relheight=0.35)
        val_8 = tk.Label(frame_8, text='', font=(
            "Helvetica", 20, 'bold'), bg="#23252b", fg='#47bf59')
        val_8.place(relx=0, rely=0.35, relwidth=1, relheight=0.65)

        key_pair = {
            9: val_1,
            10: val_2,
            11: val_3,
            12: val_4,
            13: val_5,
            14: val_6,
            15: val_7,
            16: val_8}

        def live_update():
            '''
            The function is meant to page the assinged intern with
            the necessary task
            **Input Parameters**
                None
            **Returns**
                None
            '''
            # Paging for patient 1
            for item1 in PAGES[0]:
                receiver_name, code_emergency, patient_name, room = item1
                if receiver_name[0] == 'i':
                    code = int(receiver_name[-2:])
                    if code in key_pair:
                        # Assign the assined surgeon to patient 1
                        key_pair[code]['text'] = code_emergency + \
                            '\n' + patient_name + '\n' + room
            # Paging for patient 2
            for item2 in PAGES[1]:
                receiver_name, code_emergency, patient_name, room = item2
                if receiver_name[0] == 'i':
                    code = int(receiver_name[-2:])
                    if code in key_pair:
                        # Assign the assined surgeon to patient 2
                        key_pair[code]['text'] = code_emergency + \
                            '\n' + patient_name + '\n' + room

            # Rerun the function after every second
            self.after(1000, live_update)

        live_update()

        # Return to Nurse Station
        button1 = Button(
            tframe,
            text="Nurse Station",
            command=lambda: controller.show_frame(Nurse),
            font=(
                "Helvetica",
                20,
                'bold'),
            bg="#444953",
            fg='#ffffff')
        button1.place(relx=0.78, rely=0.1, relwidth=0.2, relheight=0.8)

        button2 = Button(
            tframe,
            text="Interns 1",
            command=lambda: controller.show_frame(Interns1),
            font=(
                "Helvetica",
                20,
                'bold'),
            bg="#444953",
            fg='#ffffff')
        button2.place(relx=0.56, rely=0.1, relwidth=0.2, relheight=0.8)


class Nurse(tk.Frame):
    '''
    This class depicts the page of the Nurse Station
    This class also highlights the availbility of staff and equipment
    Step 1: Initialise the parameters
    Step 2: Define the layout
    Step 3: Connect the different pages of the GUIDE with buttons

    '''

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        # Define the canvas
        C = tk.Canvas(self, bg='#2f3442')
        C.place(relx=0, rely=0, relwidth=1, relheight=1)
        framen = tk.Frame(self, background="#444953")
        framen.place(relx=0.01, rely=0.03, relwidth=0.98, relheight=0.075)

        # Title of the page
        nurse = tk.Label(
            framen,
            text='NURSE STATION CENTRAL CONTROL UNIT',
            font=(
                "Helvetica",
                20,
                'bold'),
            bg="#444953",
            fg='#ffffff')
        nurse.place(relx=0.01, rely=0.03, relwidth=0.45, relheight=1)

        # Metadata of patient 1
        def metadata1():
            '''
            The function viualises the metadata of patient 1 if checkbox is on
            **Input Parameters**
                None
            **Returns**
                None
            '''
            # If checkbox is on
            if c1on.get() == 1:
                # Show data
                value = "\n".join(['Patient 1', 'Male', '25'])
                var1.set(value)
            # If checkbox is off
            elif c1on.get() == 0:
                # Hide data
                value = ""
                var1.set(value)

        # Metadata of patient 2
        def metadata2():
            '''
            The function viualises the metadata of patient 1 if checkbox is on
            **Input Parameters**
                None
            **Returns**
                None
            '''
            # If checkbox is on
            if c2on.get() == 1:
                # Show data
                value = "\n".join(['Patient 2', 'Female', '30'])
                var2.set(value)
            # If checkbox is off
            elif c2on.get() == 0:
                # Hide data
                value = ""
                var2.set(value)

        # Patient 1 set
        p1frame = tk.Frame(self, background="#647886")
        p1frame.place(relx=0.05, rely=0.15, relwidth=0.8, relheight=0.15)
        p1button = Button(
            p1frame,
            text="Patient 1",
            command=lambda: controller.show_frame(Patient_1),
            font=(
                "Helvetica",
                15,
                'bold'),
            bg="#647886",
            fg='#ffffff',
            borderless=1,
            relief='raised')
        p1button.place(relx=0, rely=0, relwidth=0.3, relheight=1)
        c1on = tk.IntVar()
        C1 = tk.Checkbutton(
            p1frame,
            text="",
            font=(
                "Helvetica",
                15,
                'bold'),
            variable=c1on,
            bg="#647886",
            fg='#ffffff',
            command=metadata1,
            justify='left')
        C1.place(relx=0.3, rely=0, relwidth=0.3, relheight=1)
        var1 = tk.StringVar()
        T1 = tk.Message(
            p1frame,
            bg='#23252b',
            textvariable=var1,
            width=100,
            fg='#ffffff',
            font=(
                "Baskerville",
                15))
        T1.place(relx=0.6, rely=0, relwidth=0.4, relheight=1)
        meta1 = tk.Label(p1frame, text='Metadata', font=(
            "Helvetica", 15, 'bold'), bg="#647886", fg='#ffffff')
        meta1.place(relx=0.35, rely=0.41, relwidth=0.2, relheight=0.15)

        # Patient 2 set
        p2frame = tk.Frame(self, background="#647886")
        p2frame.place(relx=0.05, rely=0.4, relwidth=0.8, relheight=0.15)
        p2button = Button(
            p2frame,
            text="Patient 2",
            command=lambda: controller.show_frame(Patient_2),
            font=(
                "Helvetica",
                15,
                'bold'),
            bg="#647886",
            fg='#ffffff',
            borderless=1,
            relief='raised')
        p2button.place(relx=0, rely=0, relwidth=0.3, relheight=1)
        c2on = tk.IntVar()
        C2 = tk.Checkbutton(
            p2frame,
            text="",
            font=(
                "Helvetica",
                15,
                'bold'),
            variable=c2on,
            bg="#647886",
            fg='#ffffff',
            command=metadata2,
            justify='left')
        C2.place(relx=0.3, rely=0, relwidth=0.3, relheight=1)
        var2 = tk.StringVar()
        T2 = tk.Message(
            p2frame,
            bg='#23252b',
            textvariable=var2,
            width=100,
            fg='#ffffff',
            font=(
                "Baskerville",
                15))
        T2.place(relx=0.6, rely=0, relwidth=0.4, relheight=1)
        meta2 = tk.Label(p2frame, text='Metadata', font=(
            "Helvetica", 15, 'bold'), bg="#647886", fg='#ffffff')
        meta2.place(relx=0.35, rely=0.41, relwidth=0.2, relheight=0.15)

        # Title for availability of staff
        framea = tk.Frame(self, background="#444953")
        framea.place(relx=0.01, rely=0.6, relwidth=0.98, relheight=0.075)
        available = tk.Label(framea, text='AVAILABLE STAFF', font=(
            "Helvetica", 20, 'bold'), bg="#444953", fg='#ffffff')
        available.place(relx=0, rely=0.03, relwidth=0.2, relheight=1)

        # Available surgeons
        framesur = tk.Frame(self, background="#2e3138")
        framesur.place(relx=0.05, rely=0.7, relwidth=0.2, relheight=0.2)
        # Go to surgeons pager
        surbutton = Button(
            framesur,
            text="Surgeons",
            command=lambda: controller.show_frame(Surgeons),
            font=(
                "Helvetica",
                20,
                'bold'),
            bg="#444953",
            fg='#ffffff',
            borderless=1,
            relief='raised')
        surgeon_a = str(len(surgeon_list))
        surbutton.place(relx=0, rely=0, relwidth=1, relheight=0.35)
        sur = tk.Label(framesur, text=surgeon_a, font=(
            "Helvetica", 30, 'bold'), bg="#23252b", fg='#47b1bf')
        sur.place(relx=0, rely=0.35, relwidth=1, relheight=0.65)

        # Available residents
        framere = tk.Frame(self, background="#2e3138")
        framere.place(relx=0.27, rely=0.7, relwidth=0.2, relheight=0.2)
        # Go to residents pager
        rebutton = Button(
            framere,
            text="Residents",
            command=lambda: controller.show_frame(Residents),
            font=(
                "Helvetica",
                20,
                'bold'),
            bg="#444953",
            fg='#ffffff',
            borderless=1,
            relief='raised')

        resident_a = str(len(resident_list))
        rebutton.place(relx=0, rely=0, relwidth=1, relheight=0.35)
        re = tk.Label(framere, text=resident_a, font=(
            "Helvetica", 30, 'bold'), bg="#23252b", fg='#47bf59')
        re.place(relx=0, rely=0.35, relwidth=1, relheight=0.65)

        # Available interns
        frameri = tk.Frame(self, background="#2e3138")
        frameri.place(relx=0.5, rely=0.7, relwidth=0.2, relheight=0.2)
        # Go to interns pager
        ributton = Button(
            frameri,
            text="Resident Interns",
            command=lambda: controller.show_frame(Interns1),
            font=(
                "Helvetica",
                20,
                'bold'),
            bg="#444953",
            fg='#ffffff',
            borderless=1,
            relief='raised')

        ributton.place(relx=0, rely=0, relwidth=1, relheight=0.35)
        intern_a = str(len(intern_list))
        ri = tk.Label(frameri, text=intern_a, font=(
            "Helvetica", 30, 'bold'), bg="#23252b", fg='#47b1bf')
        ri.place(relx=0, rely=0.35, relwidth=1, relheight=0.65)

        # Available equiments
        frameeq = tk.Frame(self, background="#2e3138")
        frameeq.place(relx=0.73, rely=0.7, relwidth=0.2, relheight=0.2)
        eqlabel = tk.Label(frameeq, text='Equipments', font=(
            "Helvetica", 20, 'bold'), bg="#444953", fg='#ffffff')
        eqlabel.place(relx=0, rely=0, relwidth=1, relheight=0.35)
        equip_a = str(EQUIPMENT_COUNT)
        eq = tk.Label(frameeq, text=equip_a, font=(
            "Helvetica", 30, 'bold'), bg="#23252b", fg='#47bf59')
        eq.place(relx=0, rely=0.35, relwidth=1, relheight=0.65)

        def live_update():
            '''
            The function will indicate staff availability
            **Input Parameters**
                None
            **Returns**
                None
            '''
            # Number of equipments
            eq['text'] = str(EQUIPMENT_COUNT)
            # Number of Interns
            ri['text'] = str(len(intern_list))
            # Number of Residents
            re['text'] = str(len(resident_list))
            # Number of Surgeons
            sur['text'] = str(len(surgeon_list))
            # Rerun the function after every second
            self.after(1000, live_update)

        live_update()

class Protection:
    '''
    This class handles patient data log protection in terms of encrypting
    and decrypting the information based on the provided usernames and
    passwords combinations
    Step 1: Read the .xlsx extension files only.
    Step 2: Identifying specific patient identification details
    Step 3: Creating time domain data for each vital by extracting rows
    '''

    def __init__(self, file):
        '''
        The __init__ method will initialize the object’s state.
        Initializes the function of the class when
        an object of class is created.
        In this case, the data, patient_record, patient_id of a specific patient
        **Input Parameters**
            file: *str*
                The file name to be encrypted
        **Returns**
            None
        '''
        self.file = file

    def encrypt(self, message, N, E):
        '''
        This function will encrypt any string

        **Input Parameters**
            message: *str*
                The message to be encrypted
            N, E: *int* (pre-defined)
                Essential values for encryption
        **Returns**
            encrypted_message: *list, int*
                Each number represents a encrypted message of one character
        '''
        return [(ord(s) ** E) % N for s in message]

    def password(self, enc_msg, usr, passwd, N, D):
        '''
        Code to check username / password combinations goes here.
        Store your usernames, salted password hashes, and
        corresponding salts appropriately.
        Return the decrypted message if the username and password are correct
        **Input Parameters**
            enc_msg: *list, str*
                The encrypted message as a list
            usr: *char, optional*
                The username to access the file
            passwd: *char, optional*
                The password to access the file
            N, D: *int*
                Essential values for decryption
        **Returns**
            Decrypted: *list*
                Returns the message if combination is right
        '''

        def decrypt(enc_msg, N, D):
            '''
            This function will decrypt any encrypted message

            **Input Parameters**
                enc_msg: *List, int, optional*
                    The list of integers for decryption
                N, D: *int*
                    Essential values for decryption
            **Returns**
                decrypted_message: *str*
                    The decrypted message
            '''
            return ''.join([chr((s ** D) % N) for s in enc_msg])

        # Database with two combinations
        # ("hherbol1", 'Fifa'), ("krypto12", 'Superman123')
        # Database Structure
        # key: username, value:[hashed_password,salt]
        user_pass = {
            "hherbol1": [
                '936aae4aa826dc4607b7f51c06a6fc6cc923ffe80d067f6b4ba541d03deca11a0863ab90c61265e3023b761940cb449ed0aebea1aae966c109b78180072e410f',
                'randomsa7hfff8fbaf77392hfhskjhdfkfdshkhdkfhsdsfhso'],
            "krypto12": [
                'ac02ff13718005e12966ed52da93ff1c84c754613e04244a84726745239bc56e24a95235b1021a0a795528dd280b12f098c2f19a05924c35b4953991208eb867',
                'randomsaltsaregood123gbsdxxsfksjfsh&bsdfksdflsjkdf']}
        # For printing incorrect combinations
        error_message = ''
        # if username is valid
        if usr in user_pass:
            """Hash a password for storing."""
            # verify the password
            stored_password = user_pass.get(usr)[0]
            salt = user_pass.get(usr)[1]
            # hashing the provided password
            hashed = hashlib.sha512((passwd + salt).encode())
            hashed_pass = hashed.hexdigest()
            # Compare generated and database password
            if (hashed_pass == stored_password) is True:
                decrypted = decrypt(enc_msg, N, D)
                return decrypted
            else:
                # To return the feedback to the user
                # Ref read_messages function
                error_message = 'incorrect_pass'
                return error_message
        # if username is not valid
        else:
            # To return the feedback to the user
            # Ref read_messages function
            error_message = 'incorrect_username'
            return error_message

    def start_messenger(self, N=17947, E=7):
        '''
        This function reads in each line of input from the user,encrypts each
        line, and stores them in a list. Each line of encrypted text is written
        to a text file, the name of which is specified by "msg ftpr".

        **Input Parameters**

            N, E: *int*
                Essential values for encryption
        **Returns**
           msg_fptr: *file*
                the text file with encrypted data
        '''
        if ".txt" in self.file:
            filename = self.file.split(".txt")[0]
        msg_fptr = filename + '_pass' + '.txt'
        new_file = open(msg_fptr, 'w')

        # while True:
        #     word = str(input("Enter message or STOP to end:"))
        #     if word == 'STOP':
        #         break
        #     else:
        file1 = open(self.file, 'r')
        Lines = file1.readlines()
        count = 0
        # Strips the newline character
        for line in Lines:
            list = self.encrypt(line, N, E)
            for item in list:
                new_file.write(str(item) + '\t')
            new_file.write("\n")
        new_file.close()
        return msg_fptr

    def read_messages(self, usr, passwd, msg_fptr, N=17947, D=10103):
        '''
        Asks the user for their username and password. Reads the encrypted text
        from "msg fptr" and decrypts it if the username / password combination is
        correct.
        **Input Parameters**
            usr: *char, optional*
                The username to access the file
            passwd: *char, optional*
                The password to access the file
            msg_fptr: *str*
                Name of the text file
            N, D: *int*
                Essential values for decryption
        **Returns**
           None
        '''

        # prompt for username and password
        # usr = input("Enter the username:")
        # No echoing on
        # passwd = getpass.getpass(prompt="Enter the password:")
        # passwd = getpass.getpass(passwd)
        # Handling exceptions for inputs
        if len(usr) == 0 and len(passwd) != 0:
            print('Username not entered')
        elif len(usr) != 0 and len(passwd) == 0:
            print('Password not entered')
        elif len(usr) == 0 and len(passwd) == 0:
            print('Username and Password not entered')
        else:
            mfile = open(msg_fptr)
            lines = mfile.readlines()
            int_list = []
            for line in lines:
                list = line.split()
                temp_list = []
                for item in list:
                    temp_list.append(int(item))
                int_list.append(temp_list)

            for i in range(len(int_list)):
                message_list = self.password(int_list[i], usr, passwd, N, D)
                if i == 0:
                    if message_list == 'incorrect_pass':
                        print("Oops! The password is incorrect for the username")
                    elif message_list == 'incorrect_username':
                        print("Oops! The username does not exist in the database")
                    else:
                        print("The username and password are valid")
                string1 = 'incorrect_username'
                string2 = 'incorrect_pass'
                if message_list != string1 and message_list != string2:
                    print(message_list)


def unit_tests():
    '''
    This functions handles the unit tests to verify independent codes
    **Input Parameters**
        None
    **Returns**
       None
    '''
    # Case1: True Positive
    message1 = "Test"
    enc1 = Protection(message1)
    encrypted_message = enc1.encrypt(message1, N=17947, E=7)
    decrypted_message = enc1.password(
        encrypted_message, "hherbol1", "Fifa", N=17947, D=10103)
    if (message1 == decrypted_message):
        print("Case 1: Unit test succeded")
    else:
        print("Case 1: Unit test failed")

    # Case 2: False Positive
    message = "Test"
    enc2 = Protection(message)
    encrypted_message = enc2.encrypt(message, N=17947, E=7)
    message2 = "Test2"
    encrypted_message1 = enc2.encrypt(message2, N=17947, E=7)
    decrypted_message = enc2.password(
        encrypted_message, "krypto12", "Fifa", N=17947, D=10103)
    if (message == decrypted_message):
        print("Case 2: Unit test failed")
    else:
        print("Case 2: Unit test succeded")


if __name__ == '__main__':
    # Start the main program
    print('MEMAM is executing')
    show = False
    # prompt the user if they want see the log printed in terminal
    val = input('Do you want to print the patient log data (y/n): ')
    if val == 'n':
        print('MEMAM has your data protected')
    elif val == 'y':
        # ("hherbol1", 'Fifa'), ("krypto12", 'Superman123')
        username = input('Enter usename: ')
        password = getpass.getpass(prompt="Enter the password:")
        show = True
    else:
        raise SystemExit('Invalid choice: Rerun the code')
    # Checking for existence of files
    filename = 'patient1.txt'
    if os.path.exists(filename):
        os.remove(filename)
    else:
        pass
    filename = 'patient2.txt'
    if os.path.exists(filename):
        os.remove(filename)
    else:
        pass
    # Initiating the main real-time update
    # using GUI
    path = "patient_log1.xlsx"
    # Update the records
    record1 = Input(path, 0)
    record2 = Input(path, 1)
    patient_1, patient_record_1 = record1()
    patient_2, patient_record_2 = record2()
    # Main visualization
    app = Visualisation()
    app.mainloop()
    # tim.sleep(10)
    enc1 = Protection('patient1.txt')
    encrypted1 = enc1.start_messenger()
    enc2 = Protection('patient2.txt')
    encrypted2 = enc2.start_messenger()
    if show:
        print('Printing patient 1: log data')
        messages = enc1.read_messages(username, password, encrypted1)
        print('-------------------------------')
        print('Printing patient 2: log data')
        messages = enc2.read_messages(username, password, encrypted2)

    print('Testing Unit Test Function')
    # Unit tests to valid, optional
    # Comment i to stop
    unit_tests()

