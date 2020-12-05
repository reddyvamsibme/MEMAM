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
