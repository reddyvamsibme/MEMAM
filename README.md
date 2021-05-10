# MEMAM: Medical Emergencies Management And Alert Mechanism
**Authors: Vamsi Reddy <vreddy17@jhu.edu>, Emad Mohammed Naveed <enaveed1@jhu.edu>**  
**Course: EN.540.635 “Software Carpentry”**  
**Johns Hopkins University, MD**
![alt text](https://github.com/reddyvamsibme/MEMAM/blob/main/pics/MEMAM.jpg "MEMAM graphic")
<p style='text-align: justify;'> This repository is created to develop an automated medical emergencies management and alert mechanism (MEMAM) tool for corporate hospitals using dynamic programming approaches in python. The core motivation of this project is to leverage the fundamentals of python programming to achieve fully-functional commercial hospital management software. MEMAM is a specialized tool to handle the critical emergencies identified by the bedside monitors for real-time observation of the patients’ vitals in a hospital setting. MEMAM has in-built features to replicate pager machines using a custom-built GUI to comprehensively visualize the paging protocols and activities typically executed by the nurses’ operation centers at corporate hospitals. A dynamic auto-update of the database with lists of available attending surgeons, residents, resident interns, and equipment units has been exclusively employed to further demonstrate the scope of MEMAM as a real-world application in hospitals.
The code is documented in PEP8 style formatting with clear comments and designed to be easy to extend. If you use it in your research, please consider citing this repository.
</p>

## Installation & Execution
1. Clone this repository
    ```bash
    git clone https://github.com/reddyvamsibme/MEMAM.git
    ```
2. Install dependencies (for first-time users, optional), install Python 3.7 or above.
   ```bash
   pip3 install -r requirements.txt
   ```
3. Open memam.py and change the excel sheets names and log text filenames, if you wish apply the code on your custom file
4. Run memam.py from the repository root directory, make sure to have patient_log1.xlsx in the root directory.
    ```bash
    python3 memam.py
    ``` 
5. For the encryption to start, close GUI interface (abrupt quitting of application using performance monitors may cause system erros)
6. Select the option when prompted to show the patient data log. Incorrect username or password may restrict the view access
7. Redirect to the root file to see the '.txt' files in the patient#_pass filenames for view encrypted data. 
8. The code is formatted for simultaneous data visualization of two patients in the hospital and can be extended to at least 5-10 patient without GPU. 

## Exceptions
1. Do not edit the patient_log1.xlsx excel sheet, it is a replica of physiological data feedback from bedside monitor
2. The code is designed to only work on '.xlsx' format patient data and the specific data logs in '.txt' file
3. The encryption and decryption is username and password specific, we have displayed the actual combination in the code for beginers to understand and verify the code
4. The excess use of global variables can be avoided but that will fail the GUI refresh rate
5. If the refresh rate is slow on GUI,especially Windows OS, please stop all background processes.
6. Make sure to install either pip or brew install incase of errors with import.

## Code Architecture
* **Class Input**  
   This class handles reading and extraction of patient's vitals(only .xlsx format)
    + Step 1: Read the .xlsx extension files only.
    + Step 2: Identifying specific patient identification details
    + Step 3: Creating time domain data for each vital by extracting rows

* **Class MEMAM**  
    This class has all the major functions those define the specific emergencies, alert functions and internal paging

    *Activity Functions:*
    + normals() - Defines the healthy ranges of the vitals
    + page() - Visulizes the messages on GUI
    + log() - Enter the activity in patient log
    + scrub() - Visualizes the nurse message on patient bedside monitor
    
    *Emergency Functions*:
    + code_blue() - Alerts surgeons, resident interns, residents, equipment team
    + blood_pressure() - Alerts surgeons, resident interns, residents
    + Temperature() - Alerts resident interns, residents
    + Labor_pains() - Alerts surgeons, resident interns, residents
    + breathing() - Alerts resident interns, residents 
    + Spo2_abnormal() - Alerts resident interns, residents
    
    *Alert Mechanism Functions*: (alerts through pager)
    + alert_nurse() - Alerts the central control unit of nurse station
    + nurse_ResInterns() - Nurses alert the resident interns
    + nurse_residents() - Nurses alert the residents
    + nurse_equipment() - Nurses alert the equipment team
    + nurse_surgeons() - Nurses alert the surgeons

         
* **Class Visualization**  
    This class establishes all the pages of the Graphical User Interface (GUI)
    
    + Step 1: Initialise the parameters
    + Step 2: Define the pages needs to be displayed on the GUIDE
    + Step 3: Indicate that the Nurse frame as the start page
    + Step 4: Show the frame
 
* **Class Patient_1**    
    This class is highlights the vitals of Patient 1 including the Patient log
    
    + Step 1: Define the layout of the Page
    + Step 2: Define the vitals of the patient
    + Step 3: Attach the Patient log
    + Step 4: Attach the Scrub Message
    + Step 5: Run the class MEMAM function to get the data

* **Class Patient_2** \
    This class is highlights the vitals of Patient 1 including the Patient log
    
    + Step 1: Define the layout of the Page
    + Step 2: Define the vitals of the patient
    + Step 3: Attach the Patient log
    + Step 4: Attach the Scrub Message
    + Step 5: Run the class MEMAM function to get the data


* **Class Surgeons**\
    This class depicts the surgeons pager's view the atient log
    
    + Step 1: Define the layout of the Page
    + Step 2: Define the list of surgeons
    + Step 3: Page the required surgeon when MEMAM is called


* **Class Residents**\
    This class depicts the residents pager's view the Patient log
    
    + Step 1: Define the layout of the Page
    + Step 2: Define the list of residents
    + Step 3: Page the required residents when MEMAM is called

    
* **Class Interns1**\
    This class depicts the first batch of intens pager's view the Patient log
    
    + Step 1: Define the layout of the Page
    + Step 2: Define the list of interns
    + Step 3: Page the required interns when MEMAM is called

* **Class Nurse**  
    This class depicts the page of the Nurse Station and highlights the availbility of staff and equipment
    
    + Step 1: Initialise the parameters
    + Step 2: Define the layout
    + Step 3: Connect the different pages of the GUIDE with buttons

* **Class Protection**\
    This class handles patient data log protection using username & passwords
    
    + Step 1: Read the .xlsx extension files only.
    + Step 2: Identifying specific patient identification details
    + Step 3: Creating time domain data for each vital by extracting rows

## Graphical User Interface:

![alt text](https://github.com/reddyvamsibme/MEMAM/blob/main/pics/MEMAM_1.jpg "GUI graphic")
![alt text](https://github.com/reddyvamsibme/MEMAM/blob/main/pics/MEMAM_2.jpg "GUI MEMAM graphic")
![alt text](https://github.com/reddyvamsibme/MEMAM/blob/main/pics/MEMAM_3.jpg "GUI MEMAM graphic")
![alt text](https://github.com/reddyvamsibme/MEMAM/blob/main/pics/MEMAM_4.jpg "GUI MEMAM graphic")
![alt text](https://github.com/reddyvamsibme/MEMAM/blob/main/pics/MEMAM_5.jpg "GUI MEMAM graphic")
