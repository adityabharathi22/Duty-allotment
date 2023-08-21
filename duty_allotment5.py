"""this program will get a csv file as input, dates of examination along with
the rooms available and generate a """
import ast

import mysql.connector as mc
import random
import datetime


# import date_selection.date_form

def data_gen_id():  # this is to temporarily add al_tag in place of staff id
    n = random.randint(1000, 9999)
    s = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    passlen = 6
    p = "".join(random.sample(s, passlen))
    final_id = str(n) + p

    return final_id


class process:
    def __init__(self):
        self.mycon = mc.connect(host="127.0.0.1", port=3306, user="root", passwd="****", database="da5")
        self.mycursor = self.mycon.cursor(buffered=True)
        # Department wise lists ->
        self.ai_ds = []
        self.it = []
        self.cse = []
        self.cys = []
        self.mde = []
        self.ece = []
        self.eie = []
        self.eee = []
        self.agri = []
        self.mech = []
        self.civil = []

        self.file_name = []

        self.ai_ds_count, self.it_count, self.cse_count, self.cys_count, self.mde_count, \
            self.ece_count, self.eie_count, self.eee_count, self.agri_count, self.mech_count, \
            self.civil_count = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0

        self.priority = {"ai_ds": 1, "cse": 2, "it": 3, "civil": 4, "ece": 5, "eie": 6, "eee": 7, "mech": 8, "cys": 9,
                         "mde": 10, "agri": 11}
        self.flag = False

    def mysql_config(self):
        cmd = "create table counts(ai_ds int, cse int, it int, civil int, ece int, eie int, " \
              "eee int, mech int, cys int, mde int, agri int)"
        self.mycursor.execute(cmd)

        cmd = " create table ext_clg_cookie(college tinytext)"
        self.mycursor.execute(cmd)

        file_cmd = "create table file_details(name tinytext, ftag varchar(30), active_stat int, primary key(ftag))"
        self.mycursor.execute(file_cmd)

        cmd = "create table ext_cookie(slot varchar(20), session varchar(30), college tinytext)"
        self.mycursor.execute(cmd)

        create_cmd = "create table ai_ds(Name varchar(30), Desg varchar(30), priority int(1), " \
                     "Assign_date varchar(30), al_tag varchar(30), tot_duty int(20),contact varchar(20), " \
                     "email tinytext, " \
                     "staff_id int(10), primary key(Name))"
        self.mycursor.execute(create_cmd)

        create_cmd = "create table it(Name varchar(30), Desg varchar(30), priority int(1), " \
                     "Assign_date varchar(30), al_tag varchar(30), tot_duty int(20),contact varchar(20), " \
                     "email tinytext, " \
                     "staff_id int(10), primary key(Name))"
        self.mycursor.execute(create_cmd)

        create_cmd = "create table cse(Name varchar(30), Desg varchar(30), priority int(1)," \
                     "Assign_date varchar(30), al_tag varchar(30), tot_duty int(20),contact varchar(20), " \
                     "email tinytext, " \
                     "staff_id int(10), primary key(Name))"
        self.mycursor.execute(create_cmd)

        create_cmd = "create table agri(Name varchar(30), Desg varchar(30), priority int(1)," \
                     "Assign_date varchar(30), al_tag varchar(30), tot_duty int(20),contact varchar(20), " \
                     "email tinytext, " \
                     "staff_id int(10), primary key(Name))"
        self.mycursor.execute(create_cmd)

        create_cmd = "create table civil(Name varchar(30), Desg varchar(30), priority int(1)," \
                     "Assign_date varchar(30), al_tag varchar(30), tot_duty int(20),contact varchar(20), " \
                     "email tinytext, " \
                     "staff_id int(10), primary key(Name))"
        self.mycursor.execute(create_cmd)

        create_cmd = "create table eee(Name varchar(30), Desg varchar(30), priority int(1)," \
                     "Assign_date varchar(30), al_tag varchar(30), tot_duty int(20),contact varchar(20), " \
                     "email tinytext, " \
                     "staff_id int(10), primary key(Name))"
        self.mycursor.execute(create_cmd)

        create_cmd = "create table eie(Name varchar(30), Desg varchar(30), priority int(1)," \
                     "Assign_date varchar(30), al_tag varchar(30), tot_duty int(20),contact varchar(20), " \
                     "email tinytext, " \
                     "staff_id int(10), primary key(Name))"
        self.mycursor.execute(create_cmd)

        create_cmd = "create table ece(Name varchar(30), Desg varchar(30), priority int(1)," \
                     "Assign_date varchar(30), al_tag varchar(30), tot_duty int(20),contact varchar(20), " \
                     "email tinytext, " \
                     "staff_id int(10), primary key(Name))"
        self.mycursor.execute(create_cmd)

        create_cmd = "create table cys(Name varchar(30), Desg varchar(30), priority int(1)," \
                     "Assign_date varchar(30), al_tag varchar(30), tot_duty int(20),contact varchar(20), " \
                     "email tinytext, " \
                     "staff_id int(10), primary key(Name))"
        self.mycursor.execute(create_cmd)

        create_cmd = "create table mde(Name varchar(30), Desg varchar(30), priority int(1)," \
                     "Assign_date varchar(30), al_tag varchar(30), tot_duty int(20),contact varchar(20), " \
                     "email tinytext, " \
                     "staff_id int(10), primary key(Name))"
        self.mycursor.execute(create_cmd)

        create_cmd = "create table mech(Name varchar(30), Desg varchar(30), priority int(1)," \
                     "Assign_date varchar(30), al_tag varchar(30), tot_duty int(20),contact varchar(20), " \
                     "email tinytext, " \
                     "staff_id int(10), primary key(Name))"
        self.mycursor.execute(create_cmd)

        # ------------------------x---------------------------- External

        create_cmd = "create table ai_ds_ext(Name varchar(30), Desg varchar(30), priority int(1), " \
                     "Assign_date varchar(30), al_tag varchar(30), tot_duty int(20),contact varchar(20), " \
                     "email tinytext, " \
                     "staff_id int(10), primary key(Name))"
        self.mycursor.execute(create_cmd)

        create_cmd = "create table it_ext(Name varchar(30), Desg varchar(30), priority int(1), " \
                     "Assign_date varchar(30), al_tag varchar(30), tot_duty int(20),contact varchar(20), " \
                     "email tinytext, " \
                     "staff_id int(10), primary key(Name))"
        self.mycursor.execute(create_cmd)

        create_cmd = "create table cse_ext(Name varchar(30), Desg varchar(30), priority int(1)," \
                     "Assign_date varchar(30), al_tag varchar(30), tot_duty int(20),contact varchar(20), " \
                     "email tinytext, " \
                     "staff_id int(10), primary key(Name))"
        self.mycursor.execute(create_cmd)

        create_cmd = "create table agri_ext(Name varchar(30), Desg varchar(30), priority int(1)," \
                     "Assign_date varchar(30), al_tag varchar(30), tot_duty int(20),contact varchar(20), " \
                     "email tinytext, " \
                     "staff_id int(10), primary key(Name))"
        self.mycursor.execute(create_cmd)

        create_cmd = "create table civil_ext(Name varchar(30), Desg varchar(30), priority int(1)," \
                     "Assign_date varchar(30), al_tag varchar(30), tot_duty int(20),contact varchar(20), " \
                     "email tinytext, " \
                     "staff_id int(10), primary key(Name))"
        self.mycursor.execute(create_cmd)

        create_cmd = "create table eee_ext(Name varchar(30), Desg varchar(30), priority int(1)," \
                     "Assign_date varchar(30), al_tag varchar(30), tot_duty int(20),contact varchar(20), " \
                     "email tinytext, " \
                     "staff_id int(10), primary key(Name))"
        self.mycursor.execute(create_cmd)

        create_cmd = "create table eie_ext(Name varchar(30), Desg varchar(30), priority int(1)," \
                     "Assign_date varchar(30), al_tag varchar(30), tot_duty int(20),contact varchar(20), " \
                     "email tinytext, " \
                     "staff_id int(10), primary key(Name))"
        self.mycursor.execute(create_cmd)

        create_cmd = "create table ece_ext(Name varchar(30), Desg varchar(30), priority int(1)," \
                     "Assign_date varchar(30), al_tag varchar(30), tot_duty int(20),contact varchar(20), " \
                     "email tinytext, " \
                     "staff_id int(10), primary key(Name))"
        self.mycursor.execute(create_cmd)

        create_cmd = "create table cys_ext(Name varchar(30), Desg varchar(30), priority int(1)," \
                     "Assign_date varchar(30), al_tag varchar(30), tot_duty int(20),contact varchar(20), " \
                     "email tinytext, " \
                     "staff_id int(10), primary key(Name))"
        self.mycursor.execute(create_cmd)

        create_cmd = "create table mde_ext(Name varchar(30), Desg varchar(30), priority int(1)," \
                     "Assign_date varchar(30), al_tag varchar(30), tot_duty int(20),contact varchar(20), " \
                     "email tinytext, " \
                     "staff_id int(10), primary key(Name))"
        self.mycursor.execute(create_cmd)

        create_cmd = "create table mech_ext(Name varchar(30), Desg varchar(30), priority int(1)," \
                     "Assign_date varchar(30), al_tag varchar(30), tot_duty int(20),contact varchar(20), " \
                     "email tinytext, " \
                     "staff_id int(10), primary key(Name))"
        self.mycursor.execute(create_cmd)

        # --------------------------------------x----------------------------------
        exam_table = "create table exam_dates(Date varchar(20))"
        self.mycursor.execute(exam_table)

        print("Department tables created...")

        slot_cmd = "create table slots(slot varchar(20), start_date varchar(20), end_date varchar(20), " \
                   "session varchar(30))"
        self.mycursor.execute(slot_cmd)

        ext_slot = "create table ext_slots(slot varchar(20), start_date varchar(20), end_date varchar(20), " \
                   "session varchar(30), clg_name tinytext)"
        self.mycursor.execute(ext_slot)

        print("Slots table has been created...")

        temp_Date = "create table temp_dates(date varchar(20))"
        self.mycursor.execute(temp_Date)

        print("Temp dates has been created...")

        cookie_table = "create table cookie(slot varchar(20), session varchar(30))"
        self.mycursor.execute(cookie_table)

        print("Table for cookies has been created...")

        exam_table = "create table allot_dates(Date varchar(20), FN int(20), AN int(20), staffs_assigned varchar(30)," \
                     " FN_status int(20), AN_status int(20), process char(10),slot char(10), session varchar(30))"
        self.mycursor.execute(exam_table)

        ext_exam_table = "create table allot_dates_ext(Date varchar(20), FN int(20), AN int(20), staffs_assigned " \
                         "varchar(30), FN_status int(20), AN_status int(20), process char(10),slot char(10), " \
                         "session varchar(30), college tinytext)"
        self.mycursor.execute(ext_exam_table)

        user_table = "create table users(Name varchar(30), password varchar(30))"
        self.mycursor.execute(user_table)

        print("Exam dates and users table created...")

        user_dict = {'Admin': 123, 'Duty Superintend': 456, 'Duty Allotment staff': 789}
        for i in user_dict:
            username = i
            password = user_dict[i]
            user_update = "insert into users(Name, password) values(%s,%s)"
            dt = (username, password)

            self.mycursor.execute(user_update, dt)
            self.mycon.commit()

        print("User details updated in DB...")

        cmd = "create table user_cookie(name varchar(30), primary key(name))"
        self.mycursor.execute(cmd)

        print("User cookie created...")

        cmd = "create table sess_sum(date varchar(30),FN int(20), AN int(20), val int(20))"
        self.mycursor.execute(cmd)

        print("Sess sum table created")

        cmd = "create table dummy_sess_cnt(fn_an int)"
        self.mycursor.execute(cmd)

        cmd = "create table slot_buffer(slot_name varchar(30))"
        self.mycursor.execute(cmd)

        cmd = "create table colleges(name tinytext, c_code varchar(30), cs_name varchar(30), cs_mobile varchar(15), " \
              "cs_landline varchar(20), emailid tinytext)"
        self.mycursor.execute(cmd)

        dept_cmd = "create table DEPT(name varchar(30), allotment_status char(2), stf_avail int(20)," \
                   " priority int(1), decoy int)"
        self.mycursor.execute(dept_cmd)

        dept_cmd_ext = "create table DEPT_ext(name varchar(30), allotment_status char(2), stf_avail int(20)," \
                       " priority int(1), decoy int)"
        self.mycursor.execute(dept_cmd_ext)

        cmd = "create table sel_file_cookie(file tinytext)"
        self.mycursor.execute(cmd)

        cmd = "create table meta_clg(clg_code varchar(30), meta tinytext, PRIMARY KEY(clg_code))"
        self.mycursor.execute(cmd)

        cmd = "create table meta_file(ftag varchar(30), meta tinytext, PRIMARY KEY(ftag))"
        self.mycursor.execute(cmd)

        dept_ins = "insert into DEPT(name,allotment_status,stf_avail,priority,decoy) values(%s,'NA',%s, %s, 1)"

        for i in self.priority:
            data_tup = (i, 0, self.priority[i])
            self.mycursor.execute(dept_ins, data_tup)
            self.mycon.commit()

        dept_ins_ext = "insert into DEPT_ext(name,allotment_status,stf_avail,priority,decoy)" \
                       " values(%s,'NA',%s, %s, 1)"

        for i in self.priority:
            data_tup = (i + "_ext", 0, self.priority[i])
            self.mycursor.execute(dept_ins_ext, data_tup)
            self.mycon.commit()

    def fetch_college(self, clg_name):
        cmd = "select c_code from colleges where name=%s"
        dt = (clg_name,)
        self.mycursor.execute(cmd, dt)

        lst = []
        for i in self.mycursor:
            lst.append(i)
        c_code = ""
        for index, tup in enumerate(lst):
            c_code = tup[0]
        return c_code

    def insert_meta(self, clg_name):
        if self.check_dept_ext_exists() is False:
            extract = "select allotment_status, stf_avail, decoy from dept_ext"
            self.mycursor.execute(extract)

            lst = [i for i in self.mycursor]
            altmnt_status, stf_avail, decoy = [], [], []

            for index, tp in enumerate(lst):
                altmnt_status.append(tp[0])
                stf_avail.append(tp[1])
                decoy.append(tp[2])

            ret_set = [altmnt_status, stf_avail, decoy]
            ins_cmd = "insert ignore into meta_clg(clg_code, meta) values(%s,%s)"
            dt = (self.fetch_college(clg_name), str(ret_set))
            self.mycursor.execute(ins_cmd, dt)
            self.mycon.commit()

            return True

    def ftag_ext(self):
        ftag_ext = "select ftag from file_details where active_stat=1"
        self.mycursor.execute(ftag_ext)

        a = []
        for j in self.mycursor:
            a.append(j)
        ftag = ""
        for ind, tup in enumerate(a):
            ftag = tup[0]
        if ftag != "":
            cmd = "create table if not exists " + ftag + "(al_tag varchar(30), dept varchar(5), PRIMARY KEY(al_tag))"
            self.mycursor.execute(cmd)
        return ftag

    def insert_file_meta(self):
        ftag = self.ftag_ext()
        if ftag:
            if self.check_int_dept_ext_exists() is False:
                extract = "select allotment_status, stf_avail, decoy from dept"
                self.mycursor.execute(extract)

                lst = [i for i in self.mycursor]
                altmnt_status, stf_avail, decoy = [], [], []

                for index, tp in enumerate(lst):
                    altmnt_status.append(tp[0])
                    stf_avail.append(tp[1])
                    decoy.append(tp[2])

                ret_set = [altmnt_status, stf_avail, decoy]
                ins_cmd = "insert ignore into meta_file(ftag, meta) values(%s,%s)"
                dt = (ftag, str(ret_set))
                self.mycursor.execute(ins_cmd, dt)
                self.mycon.commit()

                return True

    def check_int_dept_ext_exists(self):
        cmd = "select * from dept"
        self.mycursor.execute(cmd)

        lst = [i for i in self.mycursor]
        return len(lst) == 0

    def check_dept_ext_exists(self):
        cmd = "select * from dept_ext"
        self.mycursor.execute(cmd)

        lst = [i for i in self.mycursor]
        return len(lst) == 0

    def construct_dept_ext(self, clg_name):
        if self.check_dept_ext_exists() is False:
            cmd = "select meta from meta_clg where clg_code=%s"
            dt = (self.fetch_college(clg_name),)
            self.mycursor.execute(cmd, dt)

            lst = []
            for i in self.mycursor:
                lst.append(i)
            tot = []

            for index, tp in enumerate(lst):
                tot.append(tp[0])
            c = tot[0]
            res = ast.literal_eval(c)

            altmnt_status = res[0]
            stf_avail = res[1]
            decoy = res[2]

            count = 0
            for depts in self.priority:
                upd_cmd = "update dept_ext set allotment_status=%s, stf_avail=%s, decoy=%s where name=%s"
                data_tup = (altmnt_status[count], stf_avail[count], decoy[count], depts + "_ext")

                self.mycursor.execute(upd_cmd, data_tup)
                self.mycon.commit()

                count = count + 1

    def construct_dept_int(self):
        ftag = self.ftag_ext()
        if ftag:
            if self.check_dept_ext_exists() is False:
                cmd = "select meta from meta_file where ftag=%s"
                dt = (ftag,)
                self.mycursor.execute(cmd, dt)

                lst = []
                for i in self.mycursor:
                    lst.append(i)
                tot = []

                for index, tp in enumerate(lst):
                    tot.append(tp[0])
                c = tot[0]
                res = ast.literal_eval(c)

                altmnt_status = res[0]
                stf_avail = res[1]
                decoy = res[2]

                count = 0
                for depts in self.priority:
                    upd_cmd = "update dept set allotment_status=%s, stf_avail=%s, decoy=%s where name=%s"
                    data_tup = (altmnt_status[count], stf_avail[count], decoy[count], depts)

                    self.mycursor.execute(upd_cmd, data_tup)
                    self.mycon.commit()

                    count = count + 1

    def extract_slot_sess(self):
        cmd = "select max(slot) from slots"
        self.mycursor.execute(cmd)

        lst = []
        for i in self.mycursor:
            lst.append(i)

        max_slot = 0
        for index, tup in enumerate(lst):
            max_slot = int(tup[0])

        upd_cmd = "select session from slots where slot = " + str(max_slot)
        self.mycursor.execute(upd_cmd)

        dummy = []
        for j in self.mycursor:
            dummy.append(j)
        session = ""
        for index, tp in enumerate(dummy):
            session = tp[0]

        month = session[0].upper()
        year = str(session[-4])

        al_Tag_init = "S" + str(max_slot) + month + year
        return al_Tag_init + data_gen_id()

    def extract_slot_sess_ext(self):
        cmd = "select max(slot) from ext_slots"
        self.mycursor.execute(cmd)

        lst = []
        for i in self.mycursor:
            lst.append(i)

        max_slot = 0
        for index, tup in enumerate(lst):
            max_slot = int(tup[0])

        upd_cmd = "select session from ext_slots where slot = " + str(max_slot)
        self.mycursor.execute(upd_cmd)

        dummy = []
        for j in self.mycursor:
            dummy.append(j)
        session = ""
        for index, tp in enumerate(dummy):
            session = tp[0]

        month = session[0].upper()
        year = str(session[-4])

        al_Tag_init = "S" + str(max_slot) + month + year
        return al_Tag_init + data_gen_id()

    def dept_table_creation(self):

        try:
            curr_file_tag = ""
            cmd = "select ftag from file_details where active_stat=1"
            self.mycursor.execute(cmd)

            lst = []
            for h in self.mycursor:
                lst.append(h)

            for ind, tp in enumerate(lst):
                curr_file_tag = tp[0]

            self.file_name.append(curr_file_tag)


        except IndexError:
            curr_file_tag = ""

        print("working")
        for i in self.priority:
            cmd = "select " + str(i) + " from counts"
            self.mycursor.execute(cmd)

            dummy = []
            for abcd in self.mycursor:
                dummy.append(abcd)

            staffs_available = 0
            for index, tup in enumerate(dummy):
                staffs_available = int(tup[0])

            dept_ins = "update DEPT set stf_avail = %s where name= %s"

            data_tup = (staffs_available, i)
            self.mycursor.execute(dept_ins, data_tup)
            self.mycon.commit()
            print("Inserted {} into {}".format(staffs_available, i))

            dept_ins = "update DEPT_ext set stf_avail = %s where name= %s"

            data_tup = (staffs_available, i + "_ext")
            self.mycursor.execute(dept_ins, data_tup)
            self.mycon.commit()

    def cummulative_file_lst(self):
        cmd = "select ftag from file_details where active_stat=1"
        self.mycursor.execute(cmd)

        lst = []
        for i in self.mycursor:
            lst.append(i)

        ret = ""
        for index, tp in enumerate(lst):
            ret = tp[0]

        return ret

    def check_staff_exists(self, staff_id, dept, op):
        cmd = ""
        if op == "int":
            cmd = "select * from " + dept + " where staff_id=" + "'" + staff_id + "'"

        elif op == "ext":
            cmd = "select * from " + dept + "_ext" + " where staff_id=" + "'" + staff_id + "'"

        self.mycursor.execute(cmd)

        lst = []
        for i in self.mycursor:
            lst.append(i)

        print("CSE: ", lst)

        return len(lst) == 0  # if False, then the name exists, just update the ftag else create a new record

    def upload_details(self, dept_lst, dept):

        x = datetime.datetime.now()
        date_time = x.strftime("%c")

        priority = 0
        for data in dept_lst:
            al_tag = self.extract_slot_sess()
            if data[1] == "Professor":
                priority = 1
            elif data[1] == "Associate Professor":
                priority = 2
            elif data[1] == "A.P.(Sr.G)" or data[3] == "A.P(Sr.G)":
                priority = 3
            elif data[1] == "A.P.(Sel.G)" or data[3] == "A.P(Sel.G)":
                priority = 4
            elif data[1] == "A.P.(O.G)" or data[3] == "A.P(O.G)":
                priority = 5

            print("Giving staff id: ", data[4], dept)
            check = self.check_staff_exists(data[4], dept, "int")
            main = self.ftag_ext()

            if check is False:
                print("Inside update...")

                al_Tag_ext = "select al_tag from " + dept + " where staff_id=%s"
                dt = (data[4],)
                self.mycursor.execute(al_Tag_ext, dt)

                lst = []
                for l in self.mycursor:
                    lst.append(l)
                al_Tag = ""
                for index, tuple in enumerate(lst):
                    al_Tag = tuple[0]

                cmd = "insert ignore into " + main + " values(%s,%s)"
                data_tup = (al_Tag, dept)
                self.mycursor.execute(cmd, data_tup)
                self.mycon.commit()



            else:
                try:
                    cmd = "insert into " + str(dept) + "(Name, Desg, priority, Assign_date, al_tag, " \
                                                       "tot_duty, contact,email,staff_id) " \
                                                       "values(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                    data_tup = (data[0].upper(), data[1], priority, date_time, al_tag, 0, data[2],
                                data[3], data[4])
                    self.mycursor.execute(cmd, data_tup)
                    self.mycon.commit()

                    main = self.ftag_ext()

                    cmd = "insert into " + main + " values(%s,%s)"
                    data_tup = (al_tag, dept)
                    self.mycursor.execute(cmd, data_tup)
                    self.mycon.commit()

                    staff_id_table = "create table " + al_tag + "(Date varchar(30), session char(2)," \
                                                                " dept varchar(20), slot varchar(20))"
                    self.mycursor.execute(staff_id_table)

                    stf = "create table if not exists " + "S" + str(data[4]) + "(al_tag varchar(30))"
                    self.mycursor.execute(stf)

                    stf_ins = "insert into " + "S" + data[4] + " values(%s)"
                    dt = (al_tag,)
                    self.mycursor.execute(stf_ins, dt)
                    self.mycon.commit()

                except mc.errors.IntegrityError:
                    pass

    def upload_details_ext(self, dept_lst, dept):

        x = datetime.datetime.now()
        date_time = x.strftime("%c")

        priority = 0
        for data in dept_lst:
            al_tag = self.extract_slot_sess_ext()
            if data[1] == "Professor":
                priority = 1
            elif data[1] == "Associate Professor":
                priority = 2
            elif data[1] == "A.P.(Sr.G)" or data[3] == "A.P(Sr.G)":
                priority = 3
            elif data[1] == "A.P.(Sel.G)" or data[3] == "A.P(Sel.G)":
                priority = 4
            elif data[1] == "A.P.(O.G)" or data[3] == "A.P(O.G)":
                priority = 5

            print("Giving staff id: ", data[4], dept)
            check = self.check_staff_exists(data[4], dept, "ext")
            main = self.ftag_ext()

            if check is False:
                print("Inside update...")

                al_Tag_ext = "select al_tag from " + dept + " where staff_id=%s"
                dt = (data[4],)
                self.mycursor.execute(al_Tag_ext, dt)

                lst = []
                for l in self.mycursor:
                    lst.append(l)
                al_Tag = ""
                for index, tuple in enumerate(lst):
                    al_Tag = tuple[0]

                cmd = "insert ignore into " + main + " values(%s,%s)"
                data_tup = (al_Tag, dept)
                self.mycursor.execute(cmd, data_tup)
                self.mycon.commit()

            else:
                try:
                    cmd = "insert into " + str(dept) + "_ext" + "(Name, Desg, priority, Assign_date, al_tag, " \
                                                                "tot_duty, contact,email,staff_id) " \
                                                                "values(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                    data_tup = (data[0].upper(), data[1], priority, date_time, al_tag, 0, data[2],
                                data[3], data[4])
                    self.mycursor.execute(cmd, data_tup)
                    self.mycon.commit()

                    main = self.ftag_ext()

                    cmd = "insert into " + main + " values(%s,%s)"
                    data_tup = (al_tag, dept)
                    self.mycursor.execute(cmd, data_tup)
                    self.mycon.commit()

                    staff_id_table = "create table " + al_tag + "(Date varchar(30), session char(2)," \
                                                                " dept varchar(20), slot varchar(20))"
                    self.mycursor.execute(staff_id_table)

                    stf = "create table if not exists " + "S" + str(data[4]) + "(al_tag varchar(30))"
                    self.mycursor.execute(stf)

                    stf_ins = "insert into " + "S" + data[4] + " values(%s)"
                    dt = (al_tag,)
                    self.mycursor.execute(stf_ins, dt)
                    self.mycon.commit()

                except mc.errors.IntegrityError:
                    pass

    def extract_details(self, user_file, file_name, op):

        init_cmd = "update file_details set active_stat=0"
        self.mycursor.execute(init_cmd)
        self.mycon.commit()

        check = "select ftag from file_details where name=%s"
        dt = (file_name,)
        self.mycursor.execute(check, dt)

        lst = []
        for i in self.mycursor:
            lst.append(i)

        if len(lst) == 0:
            ftag = "F" + data_gen_id()
            cmd = "insert into file_details(name, ftag, active_stat) values(%s,%s,%s)"
            dt = (file_name, ftag, 1)
            self.mycursor.execute(cmd, dt)
            self.mycon.commit()

            self.file_name.append(ftag)
        else:
            ftag = ""
            for inde, tup in enumerate(lst):
                ftag = tup[0]

            up = "update file_details set active_stat=1 where ftag=%s"
            dt = (ftag,)
            self.mycursor.execute(up, dt)
            self.mycon.commit()

        file = open(user_file + file_name, mode="r")
        csvreader = csv.reader(file)

        rows = []
        for data in csvreader:
            rows.append(data)

        for i in rows[1:]:
            current = i
            # [Name, Designation, Contact, Email, Staff_id]

            if current[4] == 'IT':
                self.it.append([current[2], current[3], current[5], current[6], current[1]])
                self.it_count = self.it_count + 1

            elif current[4] == "AI&DS":
                self.ai_ds.append([current[2], current[3], current[5], current[6], current[1]])
                self.ai_ds_count = self.ai_ds_count + 1

            elif current[4] == "CSE":
                self.cse.append([current[2], current[3], current[5], current[6], current[1]])
                self.cse_count = self.cse_count + 1

            elif current[4] == "CYS":
                self.cys.append([current[2], current[3], current[5], current[6], current[1]])
                self.cys_count = self.cys_count + 1

            elif current[4] == "EIE":
                self.eie.append([current[2], current[3], current[5], current[6], current[1]])
                self.eie_count = self.eie_count + 1

            elif current[4] == "EEE":
                self.eee.append([current[2], current[3], current[5], current[6], current[1]])
                self.eee_count = self.eee_count + 1

            elif current[4] == "ECE":
                self.ece.append([current[2], current[3], current[5], current[6], current[1]])
                self.ece_count = self.ece_count + 1

            elif current[4] == "MECH":
                self.mech.append([current[2], current[3], current[5], current[6], current[1]])
                self.mech_count = self.mech_count + 1

            elif current[4] == "CIVIL":
                self.civil.append([current[2], current[3], current[5], current[6], current[1]])
                self.civil_count = self.civil_count + 1

            elif current[4] == "MDE":
                self.mde.append([current[2], current[3], current[5], current[6], current[1]])
                self.mde_count = self.mde_count + 1

            elif current[4] == "AGRI":
                self.agri.append([current[2], current[3], current[5], current[6], current[1]])
                self.agri_count = self.agri_count + 1

        count_ins = "insert into counts(ai_ds, it, cse, cys, mde, ece, eie, eee, agri, mech, civil) values(%s,%s,%s," \
                    "%s,%s,%s,%s,%s,%s,%s,%s)"
        dt = (self.ai_ds_count, self.it_count, self.cse_count, self.cys_count, self.mde_count,
              self.ece_count, self.eie_count, self.eee_count, self.agri_count, self.mech_count,
              self.civil_count)
        self.mycursor.execute(count_ins, dt)
        self.mycon.commit()

        print("Staff counts in each dept is updated")

        if op == "int":
            if len(self.ai_ds) != 0:
                print("AI-DS: ", self.upload_details(self.ai_ds, "ai_ds"))

            if len(self.it) != 0:
                print("IT: ", self.upload_details(self.it, "it"))

            if len(self.cse) != 0:
                print("CSE: ", self.upload_details(self.cse, "cse"))

            if len(self.cys) != 0:
                print("CYS: ", self.upload_details(self.cys, "cys"))

            if len(self.eee) != 0:
                print("EEE: ", self.upload_details(self.eee, "eee"))

            if len(self.eie) != 0:
                print("EIE: ", self.upload_details(self.eie, "eie"))

            if len(self.ece) != 0:
                print("ece: ", self.upload_details(self.ece, "ece"))

            if len(self.mech) != 0:
                print("mech: ", self.upload_details(self.mech, "mech"))

            if len(self.civil) != 0:
                print("civil: ", self.upload_details(self.civil, "civil"))

            if len(self.mde) != 0:
                print("mde: ", self.upload_details(self.mde, "mde"))

            if len(self.agri) != 0:
                print("agri: ", self.upload_details(self.agri, "agri"))

        elif op == "ext":
            if len(self.ai_ds) != 0:
                print("AI-DS: ", self.upload_details_ext(self.ai_ds, "ai_ds"))

            if len(self.it) != 0:
                print("IT: ", self.upload_details_ext(self.it, "it"))

            if len(self.cse) != 0:
                print("CSE: ", self.upload_details_ext(self.cse, "cse"))

            if len(self.cys) != 0:
                print("CYS: ", self.upload_details_ext(self.cys, "cys"))

            if len(self.eee) != 0:
                print("EEE: ", self.upload_details_ext(self.eee, "eee"))

            if len(self.eie) != 0:
                print("EIE: ", self.upload_details_ext(self.eie, "eie"))

            if len(self.ece) != 0:
                print("ece: ", self.upload_details_ext(self.ece, "ece"))

            if len(self.mech) != 0:
                print("mech: ", self.upload_details_ext(self.mech, "mech"))

            if len(self.civil) != 0:
                print("civil: ", self.upload_details_ext(self.civil, "civil"))

            if len(self.mde) != 0:
                print("mde: ", self.upload_details_ext(self.mde, "mde"))

            if len(self.agri) != 0:
                print("agri: ", self.upload_details_ext(self.agri, "agri"))

    def exam_dates(self, exam_lst):

        for dates in exam_lst:
            cmd = "insert into exam_dates values(%s,'NA','NA','NA','NA','NA','NA')"
            data_tup = (dates,)
            self.mycursor.execute(cmd, data_tup)
            self.mycon.commit()
        print("Exam table updated...")

    def process_fn(self, tag):
        cmd = "select FN_status from allot_dates where staffs_assigned = " + "'" + tag + "'"
        self.mycursor.execute(cmd)

        l = []
        for i in self.mycursor:
            l.append(i)

        tot = 0
        for index, tup in enumerate(l):
            tot = tup[0]

        print("{} for tag {}".format(tot, tag))
        if tot == 0:
            cmd = "update allot_dates set process = 'Complete' where staffs_assigned = " + "'" + tag + "'"
            self.mycursor.execute(cmd)
            self.mycon.commit()

            return False
        else:  # this means that not all the duties are alloted
            return True

    def process_an(self, tag):
        cmd = "select AN_status from allot_dates where staffs_assigned = " + "'" + tag + "'"
        self.mycursor.execute(cmd)

        l = []
        for i in self.mycursor:
            l.append(i)

        tot = 0
        for index, tup in enumerate(l):
            tot = tup[0]

        print("{} for tag {}".format(tot, tag))
        if tot == 0:
            cmd = "update allot_dates set process = 'Complete' where staffs_assigned = " + "'" + tag + "'"
            self.mycursor.execute(cmd)
            self.mycon.commit()

            return False
        else:  # this means that not all the duties are alloted
            return True

    def process_fn_ext(self, tag):
        cmd = "select FN_status from allot_dates_ext where staffs_assigned = " + "'" + tag + "'"
        self.mycursor.execute(cmd)

        l = []
        for i in self.mycursor:
            l.append(i)

        tot = 0
        for index, tup in enumerate(l):
            tot = tup[0]

        print("{} for tag {}".format(tot, tag))
        if tot == 0:
            cmd = "update allot_dates_ext set process = 'Complete' where staffs_assigned = " + "'" + tag + "'"
            self.mycursor.execute(cmd)
            self.mycon.commit()

            return False
        else:  # this means that not all the duties are alloted
            return True

    def process_an_ext(self, tag):
        cmd = "select AN_status from allot_dates_ext where staffs_assigned = " + "'" + tag + "'"
        self.mycursor.execute(cmd)

        l = []
        for i in self.mycursor:
            l.append(i)

        tot = 0
        for index, tup in enumerate(l):
            tot = tup[0]

        print("{} for tag {}".format(tot, tag))
        if tot == 0:
            cmd = "update allot_dates_ext set process = 'Complete' where staffs_assigned = " + "'" + tag + "'"
            self.mycursor.execute(cmd)
            self.mycon.commit()

            return False
        else:  # this means that not all the duties are alloted
            return True

    def create_table_for_staff_id(self, al_tag):
        cmd = "create table  IF NOT EXISTS " + al_tag + "(Date varchar(20), Session char(2))"
        self.mycursor.execute(cmd)

    def check_staff_status(self, al_tag, date):
        """
        This method will check whether a staff is about to be alloted a duty in same day or not
        :param date: exam date
        :param al_tag: staff reference id
        :return:
        """

        cmd = "select Date from " + al_tag + " where Date= (%s)"
        dt = (date,)
        self.mycursor.execute(cmd, dt)

        lst = []
        for i in self.mycursor:
            lst.append(i)

        print("{} == {}".format(al_tag, lst))

        return len(lst) == 0  # if 0 then it means True (same date is not there) else False

    def current_sess_extraction(self, op):
        cmd = ""
        if op == "int":
            cmd = "select slot from cookie"
        if op == "ext":
            cmd = "select slot from ext_cookie"

        self.mycursor.execute(cmd)
        lst = []
        for i in self.mycursor:
            lst.append(i)
        sess = ""
        for ind, tup in enumerate(lst):
            sess = tup[0]
        print("Used: ", sess)
        return sess

    def allot_dates(self):
        update_ad_set = set()

        cmd = "select * from allot_dates where process is NULL and FN_status+AN_status<=%s"
        dt = (self.extract_total_staff("int"),)
        self.mycursor.execute(cmd, dt)

        lst = []
        for i in self.mycursor:
            lst.append(i)
        if len(lst) != 0:

            FN, AN = {}, {}
            for index, tup in enumerate(lst):
                FN[tup[0]] = [tup[1], tup[3], tup[7]]
                AN[tup[0]] = [tup[2], tup[3], tup[7]]

            for duty in FN:
                date = duty
                sessions = FN[duty][0]
                tag = FN[duty][1]
                curr_slot = FN[duty][2]

                update_ad_set.add(date)

                dummy_session = sessions

                date_alloc = self.process_fn(tag)
                if date_alloc is True:
                    while dummy_session > 0:
                        staff_id, dept, tot = self.exam_allotment(date)  # this will return a staff with high priority
                        if dept == 1:
                            return "insufficient staffs", tot
                        else:
                            chk = self.check_staff_status(staff_id, date)
                            if chk is True:
                                stf_create = "create table IF NOT EXISTS " + tag + "(staff_id varchar(30),primary key(" \
                                                                                   "staff_id))"
                                self.mycursor.execute(stf_create)

                                stf_Assigned = "insert into " + tag + " values(%s)"
                                data_tup = (staff_id,)
                                self.mycursor.execute(stf_Assigned, data_tup)
                                self.mycon.commit()

                                cmd = "insert into " + staff_id + " values(%s, %s, %s, %s)"
                                dt = (date, 'FN', dept, curr_slot)
                                self.mycursor.execute(cmd, dt)
                                self.mycon.commit()

                                update_dept = "update " + dept + " set tot_duty = tot_duty + 1 " \
                                                                 "where al_tag = " + "'" + staff_id + "'"
                                self.mycursor.execute(update_dept)
                                self.mycon.commit()

                                dummy_session = dummy_session - 1

                                status = "update allot_dates set FN_status = (%s) where staffs_assigned = (%s)"
                                sdt = (dummy_session, tag)
                                self.mycursor.execute(status, sdt)
                                self.mycon.commit()

                                DEPT_cmd = "update DEPT set allotment_status='A' where " \
                                           "name=" + "'" + dept + "'"
                                self.mycursor.execute(DEPT_cmd)
                                self.mycon.commit()

                            else:
                                # if the flow comes to this point then it means that the algo is trying to assign a same
                                # date to a staff
                                continue

                    else:
                        continue
                # self.process_fn(tag)

            for duty in AN:
                date = duty
                sessions = AN[duty][0]
                tag = AN[duty][1]
                curr_slot = AN[duty][2]

                update_ad_set.add(date)

                ds = sessions

                date_alloc = self.process_an(tag)
                if date_alloc is True:

                    while ds > 0:
                        staff_id, dept, tot = self.exam_allotment(date)  # this will return a staff with high priority
                        if dept == 1:
                            return "insufficient staffs", tot
                        else:
                            chk = self.check_staff_status(staff_id, date)

                            if chk is True:
                                stf_create = "create table IF NOT EXISTS " + tag + "(staff_id varchar(30),primary key(" \
                                                                                   "staff_id))"
                                self.mycursor.execute(stf_create)

                                stf_Assigned = "insert into " + tag + " values(%s)"
                                data_tup = (staff_id,)
                                self.mycursor.execute(stf_Assigned, data_tup)
                                self.mycon.commit()

                                cmd = "insert into " + staff_id + " values(%s, %s, %s, %s)"
                                dt = (date, 'AN', dept, curr_slot)
                                self.mycursor.execute(cmd, dt)
                                self.mycon.commit()

                                update_dept = "update " + dept + " set tot_duty = tot_duty + 1 " \
                                                                 "where al_tag = " + "'" + staff_id + "'"
                                self.mycursor.execute(update_dept)
                                self.mycon.commit()

                                ds = ds - 1

                                status = "update allot_dates set AN_status = (%s) where staffs_assigned = (%s)"
                                sdt = (ds, tag)
                                self.mycursor.execute(status, sdt)
                                self.mycon.commit()

                            else:
                                continue
                else:
                    continue
                # self.process_an(tag)

            for dates in update_ad_set:
                cmd = "update allot_dates set process = 'Complete' where Date=%s"
                dt = (dates,)
                self.mycursor.execute(cmd, dt)
                self.mycon.commit()
            return "success", 1
        else:
            return "insufficient staffs", self.extract_total_staff("int")

    def allot_dates_ext(self):
        update_ad_set = set()
        print("INIL: ", self.extract_total_staff("ext"))
        cmd = "select * from allot_dates_ext where process is NULL and FN_status+AN_status<=%s"
        dt = (self.extract_total_staff("ext"),)
        self.mycursor.execute(cmd, dt)

        lst = []
        for i in self.mycursor:
            lst.append(i)
        print(lst)
        if len(lst) != 0:
            FN, AN = {}, {}
            for index, tup in enumerate(lst):
                FN[tup[0]] = [tup[1], tup[3], tup[7]]
                AN[tup[0]] = [tup[2], tup[3], tup[7]]

            for duty in FN:
                date = duty
                sessions = FN[duty][0]
                tag = FN[duty][1]
                curr_slot = FN[duty][2]

                update_ad_set.add(date)

                dummy_session = sessions

                date_alloc = self.process_fn_ext(tag)
                if date_alloc is True:
                    while dummy_session > 0:
                        staff_id, dept, tot = self.exam_allotment_ext(date)  # this will return a staff with high
                        print("IN: ", staff_id, dept, tot)
                        # priority
                        if dept == 1:
                            return "insufficient staffs", tot
                        else:
                            chk = self.check_staff_status(staff_id, date)
                            if chk is True:
                                stf_create = "create table IF NOT EXISTS " + tag + "(staff_id varchar(30),primary key(" \
                                                                                   "staff_id))"
                                self.mycursor.execute(stf_create)

                                stf_Assigned = "insert into " + tag + " values(%s)"
                                data_tup = (staff_id,)
                                self.mycursor.execute(stf_Assigned, data_tup)
                                self.mycon.commit()

                                cmd = "insert into " + staff_id + " values(%s, %s, %s, %s)"
                                dt = (date, 'FN', dept, curr_slot)
                                self.mycursor.execute(cmd, dt)
                                self.mycon.commit()

                                update_dept = "update " + dept + " set tot_duty = tot_duty + 1 " \
                                                                 "where al_tag = " + "'" + staff_id + "'"
                                self.mycursor.execute(update_dept)
                                self.mycon.commit()

                                dummy_session = dummy_session - 1

                                status = "update allot_dates_ext set FN_status = (%s) where staffs_assigned = (%s)"
                                sdt = (dummy_session, tag)
                                self.mycursor.execute(status, sdt)
                                self.mycon.commit()

                                DEPT_cmd = "update DEPT_ext set allotment_status='A' where " \
                                           "name=" + "'" + dept + "'"
                                self.mycursor.execute(DEPT_cmd)
                                self.mycon.commit()


                            else:
                                # if the flow comes to this point then it means that the algo is trying to assign a same
                                # date to a staff
                                continue
                    else:
                        continue

            for duty in AN:
                date = duty
                sessions = AN[duty][0]
                tag = AN[duty][1]
                curr_slot = AN[duty][2]

                ds = sessions

                date_alloc = self.process_an_ext(tag)
                if date_alloc is True:

                    while ds > 0:
                        staff_id, dept, tot = self.exam_allotment_ext(
                            date)  # this will return a staff with high priority
                        if dept == 1:
                            return "insufficient staffs", tot
                        else:
                            chk = self.check_staff_status(staff_id, date)

                            if chk is True:
                                stf_create = "create table IF NOT EXISTS " + tag + "(staff_id varchar(30),primary key(" \
                                                                                   "staff_id))"
                                self.mycursor.execute(stf_create)

                                stf_Assigned = "insert into " + tag + " values(%s)"
                                data_tup = (staff_id,)
                                self.mycursor.execute(stf_Assigned, data_tup)
                                self.mycon.commit()

                                print("Inserted into tag")

                                cmd = "insert into " + staff_id + " values(%s, %s, %s, %s)"
                                dt = (date, 'AN', dept, curr_slot)
                                self.mycursor.execute(cmd, dt)
                                self.mycon.commit()

                                update_dept = "update " + dept + " set tot_duty = tot_duty + 1 " \
                                                                 "where al_tag = " + "'" + staff_id + "'"
                                self.mycursor.execute(update_dept)
                                self.mycon.commit()

                                ds = ds - 1

                                status = "update allot_dates_ext set AN_status = (%s) where staffs_assigned = (%s)"
                                sdt = (ds, tag)
                                self.mycursor.execute(status, sdt)
                                self.mycon.commit()

                            else:
                                continue
                else:
                    continue
            for dates in update_ad_set:
                cmd = "update allot_dates_ext set process = 'Complete' where Date=%s"
                dt = (dates,)
                self.mycursor.execute(cmd, dt)
                self.mycon.commit()

            return "success", 1
        else:
            return "insufficient staffs", self.extract_total_staff("ext")

    def extract_total_staff(self, op):
        cmd = ""
        if op == "int":
            cmd = "select sum(stf_avail) from dept"
        if op == "ext":
            cmd = "select sum(stf_avail) from dept_ext"

        self.mycursor.execute(cmd)
        lst = []
        tot = 0
        for i in self.mycursor:
            lst.append(i)
        for index, tup in enumerate(lst):
            tot = tup[0]
        return tot

    def extract_duties_by_date(self, date, op):
        cmd = ""
        curr_num_of_staffs = 0
        if op == "int":
            cmd = "select FN+AN from allot_dates where Date=%s"
            curr_num_of_staffs = self.extract_total_staff("int")

        if op == "ext":
            cmd = "select FN+AN from allot_dates_ext where Date=%s"
            curr_num_of_staffs = self.extract_total_staff("ext")

        dt = (date,)
        self.mycursor.execute(cmd, dt)

        lst = []
        for i in self.mycursor:
            lst.append(i)
        total_duties = 0
        for ind, tup in enumerate(lst):
            total_duties = tup[0]

        if curr_num_of_staffs < total_duties:
            return False
        else:
            return True

    def extract_duties_by_sess(self, sess, op):
        cmd = ""
        curr_num_of_staffs = 0
        if op == "int":
            cmd = "select FN+AN from allot_dates where session=%s"
            curr_num_of_staffs = self.extract_total_staff("int")

        if op == "ext":
            cmd = "select FN+AN from allot_dates_ext where session=%s"
            curr_num_of_staffs = self.extract_total_staff("ext")

        dt = (sess,)
        self.mycursor.execute(cmd, dt)

        lst = []
        for i in self.mycursor:
            lst.append(i)
        total_duties = 0
        for ind, tup in enumerate(lst):
            total_duties = tup[0]

        if curr_num_of_staffs < total_duties:
            return False
        else:
            return True

    def exam_allotment(self, date):
        """logic: select dept according to priority and choose the person with staff grade"""

        dept_selection = "select min(priority) from DEPT where stf_avail <> 0 and decoy <> 0"
        self.mycursor.execute(dept_selection)
        dept_lst = []
        for depts in self.mycursor:
            dept_lst.append(depts)

        pri = ""
        for index, tup in enumerate(dept_lst):
            pri = tup[0]

        if pri is None:
            """make a reset function that sets back all the departments with staffs to 1"""
            for i in self.priority:
                dept_ins = "update DEPT set decoy=1 where name= %s"
                data_tup = (i,)
                self.mycursor.execute(dept_ins, data_tup)
                self.mycon.commit()

            self.dept_table_creation()

        dept_selection = "select min(priority) from DEPT where stf_avail > 0 and " \
                         "decoy <> 0"
        self.mycursor.execute(dept_selection)
        dept_lst = []
        for depts in self.mycursor:
            dept_lst.append(depts)

        if len(dept_lst) == 0:
            return 1, 1, self.extract_total_staff("int")
        else:
            pri = ""
            for index, tup in enumerate(dept_lst):
                pri = tup[0]

            update_cmd = "update dept set decoy=0 where priority=%s"
            dt = (pri,)
            self.mycursor.execute(update_cmd, dt)
            self.mycon.commit()

            dept_ = "select * from DEPT where priority = " + str(pri)
            # print(dept_)
            self.mycursor.execute(dept_)

            lst = []
            for abcd in self.mycursor:
                lst.append(abcd)
            dept = ""
            for index, tup in enumerate(lst):
                dept = tup[0]

            # ---- now once the department with the highest priority is chosen, the staff has to choose next
            # alloting 'n' number of staff from one department and then moving to another

            cmd = "select min(priority) from " + dept + " where tot_duty BETWEEN 0 and (select min(tot_duty) " \
                                                        "from " + dept + ")"
            self.mycursor.execute(cmd)

            lst = []
            for staff_det in self.mycursor:
                lst.append(staff_det)

            highest_priority = 0
            for idx, tup in enumerate(lst):
                highest_priority = tup[0]

            # TODO: now check whether the table exists or not
            try:
                chk_exists = "select * from dept"
                self.mycursor.execute(chk_exists)

                """This step will see if the staff with the same priority has already been assigned to duty, 
                if yes then the algorithm will deploy a special command in which it will prioritise the staff with 
                the least total duty"""

                check_pri_cmd = "select tot_duty,al_tag from " + dept + " where priority = " + str(highest_priority)
                self.mycursor.execute(check_pri_cmd)

                ring = []
                for b in self.mycursor:
                    ring.append(b)

                if len(ring) == 1:
                    if highest_priority is not None:
                        get_staff = "select al_tag from " + dept + \
                                    " where priority = " + str(highest_priority) + \
                                    " and tot_duty between (select min(tot_duty) from " + dept + ") and 100"
                        self.mycursor.execute(get_staff)

                        dummy = []
                        for staff_det in self.mycursor:
                            dummy.append(staff_det)
                        staff_id = ""
                        for idx, tup in enumerate(dummy):
                            staff_id = tup[0]

                        # now check whether the staff is alloted with same date
                        check_Date = "select Date from " + staff_id + " where Date=%s"
                        dt = (date,)
                        self.mycursor.execute(check_Date, dt)

                        c = []
                        for h in self.mycursor:
                            c.append(h)
                        if len(c) == 0:

                            ftag = self.ftag_ext()
                            check_staff_in_file = "select * from " + ftag + " where al_tag=%s"
                            dt = (staff_id,)
                            self.mycursor.execute(check_staff_in_file, dt)

                            t = []
                            for k in self.mycursor:
                                t.append(k)

                            if len(t) != 0:
                                update_dept = "update dept set allotment_status='A' where name = %s"
                                dt = (dept,)
                                self.mycursor.execute(update_dept, dt)
                                self.mycon.commit()
                                return staff_id, dept, self.extract_total_staff("int")
                            else:
                                return 1, 1, self.extract_total_staff("int")
                        else:
                            return 1, 1, self.extract_total_staff("int")
                else:
                    check_dict = []
                    for index, tup in enumerate(ring):
                        check_dict.append(tup[1])

                    tag_s = check_dict
                    random_index = random.randrange(len(tag_s))

                    staff_id = tag_s[random_index]

                    update_dept = "update dept set allotment_status='A' where name = %s"
                    dt = (dept,)
                    self.mycursor.execute(update_dept, dt)
                    self.mycon.commit()

                    return staff_id, dept, self.extract_total_staff("int")
            except:
                return

    def exam_allotment_ext(self, date):

        """logic: select dept according to priority and choose the person with staff grade"""

        dept_selection = "select min(priority) from DEPT_ext where stf_avail <> 0 and decoy <> 0"
        self.mycursor.execute(dept_selection)
        dept_lst = []
        for depts in self.mycursor:
            dept_lst.append(depts)

        pri = ""
        for index, tup in enumerate(dept_lst):
            pri = tup[0]

        if pri is None:
            """make a reset function that sets back all the departments with staffs to 1"""
            print("PRI IS RESETED PRI IS RESETED PRI IS RESETED PRI IS RESETED")
            for i in self.priority:
                dept_ins = "update DEPT_ext set decoy=1 where name= %s"
                data_tup = (i + "_ext",)
                self.mycursor.execute(dept_ins, data_tup)
                self.mycon.commit()

            self.dept_table_creation()

        dept_selection = "select min(priority) from DEPT_ext where stf_avail > 0 and " \
                         "decoy <> 0"
        self.mycursor.execute(dept_selection)
        dept_lst = []
        for depts in self.mycursor:
            dept_lst.append(depts)
        print("DLDLDLDLDLD: ", dept_lst)
        if len(dept_lst) == 0:
            return 1, 1, self.extract_total_staff("ext")
        else:
            pri = ""
            for index, tup in enumerate(dept_lst):
                pri = tup[0]

            update_cmd = "update dept_ext set decoy=0 where priority=%s"
            dt = (pri,)
            self.mycursor.execute(update_cmd, dt)
            self.mycon.commit()

            dept_ = "select * from DEPT_ext where priority = " + str(pri)
            self.mycursor.execute(dept_)

            lst = []
            for abcd in self.mycursor:
                lst.append(abcd)
            dept = ""
            for index, tup in enumerate(lst):
                dept = tup[0]
            print("SELSELEL: ", dept)

            # ---- now once the department with the highest priority is chosen, the staff has to choose next
            # alloting 'n' number of staff from one department and then moving to another

            cmd = "select min(priority) from " + dept + " where tot_duty BETWEEN 0 and (select min(tot_duty) " \
                                                        "from " + dept + ")"
            self.mycursor.execute(cmd)

            lst = []
            for staff_det in self.mycursor:
                lst.append(staff_det)
            print(lst)
            highest_priority = 0
            for idx, tup in enumerate(lst):
                highest_priority = tup[0]

            # TODO: now check whether the table exists or not
            # try:
            print('eh ma here')
            chk_exists = "select * from dept_ext"
            self.mycursor.execute(chk_exists)

            """This step will see if the staff with the same priority has already been assigned to duty, 
            if yes then the algorithm will deploy a special command in which it will prioritise the staff with 
            the least total duty"""

            check_pri_cmd = "select tot_duty,al_tag from " + dept + " where priority = " + str(
                highest_priority)
            self.mycursor.execute(check_pri_cmd)

            ring = []
            for b in self.mycursor:
                ring.append(b)
            print("RING: ", ring)
            if len(ring) == 1:
                if highest_priority is not None:
                    get_staff = "select al_tag from " + dept + \
                                " where priority = " + str(highest_priority) + \
                                " and tot_duty between (select min(tot_duty) from " + dept + ") and 100"
                    print("GS: ", get_staff)
                    self.mycursor.execute(get_staff)

                    dummy = []
                    for staff_det in self.mycursor:
                        dummy.append(staff_det)
                    staff_id = ""
                    for idx, tup in enumerate(dummy):
                        staff_id = tup[0]

                    # now check whether the staff is alloted with same date
                    check_Date = "select Date from " + staff_id + " where Date=%s"
                    dt = (date,)
                    self.mycursor.execute(check_Date, dt)

                    c = []
                    for h in self.mycursor:
                        c.append(h)
                    print("Cee Cee: ", c)
                    if len(c) == 0:

                        ftag = self.ftag_ext()
                        check_staff_in_file = "select * from " + ftag + " where al_tag=%s"
                        dt = (staff_id,)
                        self.mycursor.execute(check_staff_in_file, dt)

                        t = []
                        for k in self.mycursor:
                            t.append(k)

                        if len(t) != 0:
                            update_dept = "update dept_ext set allotment_status='A' where name = %s"
                            dt = (dept,)
                            self.mycursor.execute(update_dept, dt)
                            self.mycon.commit()
                            return staff_id, dept, self.extract_total_staff("ext")
                        else:
                            return 1, 1, self.extract_total_staff("ext")
                    else:
                        return 1, 1, self.extract_total_staff("ext")
            else:
                check_dict = []
                for index, tup in enumerate(ring):
                    check_dict.append(tup[1])

                tag_s = check_dict
                random_index = random.randrange(len(tag_s))
                staff_id = tag_s[random_index]

                print("RANDOM: ", staff_id)
                update_dept = "update dept_ext set allotment_status='A' where name = %s"
                print("UD: ", update_dept, dept)
                dt = (dept,)
                self.mycursor.execute(update_dept, dt)
                self.mycon.commit()

                return staff_id, dept, self.extract_total_staff("ext")
           # except:
           #     print("Booo")
           #     return 1, 1, self.extract_total_staff("ext")


def basic_config():
    a = process()
    a.mysql_config()
    a.dept_table_creation()
    print("Basic DB CONFIG IS DONE")


def adv_config(file_path, file_name, op):
    a = process()
    # try:
    print("About to extract.....")
    a.extract_details(file_path, file_name, op)
    # except mc.errors.IntegrityError:
    #    pass


mycon = mc.connect(host="127.0.0.1", port=3306, user="root", passwd="****", database="da5")
mycursor = mycon.cursor(buffered=True)


def check_config_status():
    try:
        cmd = "select * from ai_ds"
        mycursor.execute(cmd)

        print("DB already configured...")

    except (mc.errors.InternalError, mc.errors.ProgrammingError):
        basic_config()


def check_adv_config_status(file_path):
    cmd = "show tables"
    mycursor.execute(cmd)

    lst = []
    for i in mycursor:
        lst.append(i)

    tables = []
    for index, tup in enumerate(lst):
        tables.append(tup[0])

    print("tables: ", tables)
    if "dept" not in tables:
        adv_config(file_path)
    else:
        print("DB is already configured...")


def web_input_slot(data):
    sd = data[0]
    ed = data[1]
    sess = data[2]

    val = check_slot_1()
    if val == 1:
        cmd = "insert into slots(slot, start_date, end_date, session) values(%s,%s,%s,%s)"
        data_tup = ("1", sd, ed, sess)

        mycursor.execute(cmd, data_tup)
        mycon.commit()

        return 1
    else:
        cmd = "select max(slot) from slots"
        mycursor.execute(cmd)

        dum_num = []
        for j in mycursor:
            dum_num.append(j)
        num = 0
        for index, tuple in enumerate(dum_num):
            num = int(tuple[0])

        new_slot = num + 1

        cmd = "insert into slots(slot, start_date, end_date, session) values(%s,%s,%s,%s)"
        data_tup = (new_slot, sd, ed, sess)

        mycursor.execute(cmd, data_tup)
        mycon.commit()

        return new_slot


def check_slot_1_ext():
    cmd = "select * from ext_slots"
    mycursor.execute(cmd)

    lst = []
    for i in mycursor:
        lst.append(i)
    ret_lst = []
    for index, tuple in enumerate(lst):
        ret_lst.append(tuple[0])

    if len(lst) == 0:
        return 1


def web_input_slot_ext(data, clg):
    sd = data[0]
    ed = data[1]
    sess = data[2]

    val = check_slot_1_ext()
    if val == 1:
        cmd = "insert into ext_slots(slot, start_date, end_date, session, clg_name) values(%s,%s,%s,%s,%s)"
        data_tup = ("1", sd, ed, sess, clg)

        mycursor.execute(cmd, data_tup)
        mycon.commit()

        return 1
    else:
        cmd = "select max(slot) from ext_slots"
        mycursor.execute(cmd)

        dum_num = []
        for j in mycursor:
            dum_num.append(j)
        num = 0
        for index, tuple in enumerate(dum_num):
            num = int(tuple[0])

        new_slot = num + 1

        cmd = "insert into ext_slots(slot, start_date, end_date, session, clg_name) values(%s,%s,%s,%s,%s)"
        data_tup = (new_slot, sd, ed, sess, clg)

        mycursor.execute(cmd, data_tup)
        mycon.commit()

        return new_slot


def check_slot_1():
    cmd = "select * from slots"
    mycursor.execute(cmd)

    lst = []
    for i in mycursor:
        lst.append(i)
    # print(lst)
    ret_lst = []
    for index, tuple in enumerate(lst):
        ret_lst.append(tuple[0])

    if len(lst) == 0:
        return 1


def date_converter(date):
    date_obj = datetime.datetime.strptime(date, "%Y-%m-%d")

    new_date_string = date_obj.strftime("%d-%m-%Y")

    return new_date_string


def available_slots():
    # this function will return slot name, start date and end date, session
    cmd = "select * from slots"
    mycursor.execute(cmd)

    ds = []
    for i in mycursor:
        ds.append(i)
    data_lst = []
    slots = []
    for ind, tup in enumerate(ds):
        data_lst.append(["Slot " + str(tup[0]) + ": ", date_converter(tup[1]), date_converter(tup[2]), tup[3]])
        slots.append("Slot " + str(tup[0]))

    return slots, data_lst


def available_slots_ext():
    # this function will return slot name, start date and end date, session
    cmd = "select * from ext_slots"
    mycursor.execute(cmd)

    ds = []
    for i in mycursor:
        ds.append(i)
    data_lst = []
    slots = []
    for ind, tup in enumerate(ds):
        data_lst.append(["Slot " + str(tup[0]) + ": ", date_converter(tup[1]), date_converter(tup[2]), tup[3]])
        slots.append("Slot " + str(tup[0]))

    return slots, data_lst


def extract_ext_clg_cookie():
    try:
        cmd = "select * from ext_clg_cookie"
        mycursor.execute(cmd)

        lst = []
        for i in mycursor:
            lst.append(i)

        clg = ""
        for index, tp in enumerate(lst):
            clg = tp[0]

        return clg
    except mc.errors.ProgrammingError:
        return ""


def available_slots_ext(clg_name):
    # this function will return slot name, start date and end date, session
    print("In da: ", clg_name)

    if clg_name is not None:
        cmd = "delete from ext_clg_cookie"
        mycursor.execute(cmd)
        mycon.commit()

        cmd = "insert into ext_clg_cookie values(%s)"
        dt = (clg_name,)
        mycursor.execute(cmd, dt)
        mycon.commit()

    cmd = "select * from ext_slots where clg_name=" + "'" + clg_name + "'"
    mycursor.execute(cmd)

    ds = []
    for i in mycursor:
        ds.append(i)
    data_lst = []
    slots = []
    for ind, tup in enumerate(ds):
        data_lst.append(["Slot " + str(tup[0]) + ": ", date_converter(tup[1]), date_converter(tup[2]), tup[3]])
        slots.append("Slot " + str(tup[0]))

    return slots, data_lst


def fetch_latest_clg():
    cmd = "select * from ext_clg_cookie"
    mycursor.execute(cmd)

    lst = []
    for i in mycursor:
        lst.append(i)
    clg_name = ""
    for index, tup in enumerate(lst):
        clg_name = tup[0]
    return clg_name


def cookie_update(slot_number):
    get_session = "select session from slots where slot=(%s)"
    dt = (slot_number[5:],)
    mycursor.execute(get_session, dt)

    dummy = []
    for i in mycursor:
        dummy.append(i)
    session = ""

    for ind, tup in enumerate(dummy):
        session = tup[0]

    step_1 = "delete from cookie"
    mycursor.execute(step_1)
    mycon.commit()

    cmd = "insert into cookie(slot, session) values(%s,%s)"
    data_tup = (slot_number, session)

    mycursor.execute(cmd, data_tup)
    mycon.commit()


def cookie_update_ext(slot, clg):
    print("Inside cookie update: ", slot, clg)
    get_session = "select session from ext_slots where slot=(%s) and clg_name=(%s)"
    dt = (slot[5:], clg)
    mycursor.execute(get_session, dt)

    dummy = []
    for i in mycursor:
        dummy.append(i)
    session = ""

    for ind, tup in enumerate(dummy):
        session = tup[0]

    step_1 = "delete from ext_cookie"
    mycursor.execute(step_1)
    mycon.commit()

    cmd = "insert into ext_cookie(slot, session,college) values(%s,%s,%s)"
    data_tup = (slot, session, clg)
    mycursor.execute(cmd, data_tup)
    mycon.commit()


def ext_retrive_cookie(clg):
    cmd = "select * from ext_cookie where college=(%s)"
    dt = (clg,)
    mycursor.execute(cmd, dt)

    lst = []
    for i in mycursor:
        lst.append(i)

    slot, session = "", ""

    for index, tuple in enumerate(lst):
        slot = tuple[0]
        session = tuple[1]

    return [slot, session]


def retrive_cookie():
    cmd = "select * from cookie"
    mycursor.execute(cmd)

    lst = []
    for i in mycursor:
        lst.append(i)

    slot, session = "", ""

    for index, tuple in enumerate(lst):
        slot = tuple[0]
        session = tuple[1]

    return [slot, session]


def update_temp_dates(date):
    cmd = "insert into temp_dates(date) values(%s)"
    dt = (date,)

    mycursor.execute(cmd, dt)
    mycon.commit()


def exam_dates_out(exam_lst):
    for dates in exam_lst:
        cmd = "insert into exam_dates values(%s)"
        data_tup = (dates,)
        mycursor.execute(cmd, data_tup)
        mycon.commit()
    print("Exam table updated...")


def ext_exam_dates_out(exam_lst):
    for dates in exam_lst:
        cmd = "insert into ext_exam_dates values(%s)"
        data_tup = (dates,)
        mycursor.execute(cmd, data_tup)
        mycon.commit()
    print("Exam table updated...")


def fetch_temp_dates():
    cmd = "select * from temp_dates"
    mycursor.execute(cmd)

    lst = []
    for i in mycursor:
        lst.append(i)
    dates = []
    for index, tuple in enumerate(lst):
        dates.append(tuple[0])

    return dates


def reset_dates():
    cmd = "delete from temp_dates"
    mycursor.execute(cmd)
    mycon.commit()


def fetch_exam_dates():
    cmd = "select * from temp_dates"
    mycursor.execute(cmd)

    lst = []
    for i in mycursor:
        lst.append(i)

    dates = []
    for index, tuple in enumerate(lst):
        dates.append(tuple[0])

    return dates


def delete_old_dates():
    cmd = "delete from exam_dates"
    mycursor.execute(cmd)


def authenticate(username, password):
    if username is not None:
        cmd = "select password from users where Name =%s"
        dt = (username,)
        mycursor.execute(cmd, dt)

        lst = []
        for i in mycursor:
            lst.append(i)

        print(lst)

        pswd = ""
        for index, tup in enumerate(lst):
            pswd = pswd + tup[0]

        print("IN da3=>", pswd)

        if pswd == password:
            return "Granted"
        else:
            return "Denied"


def staff_data_ext():
    """
    This function will fetch the data from each department and also the al_tags in which the allotment details are there
    :return:
    """
    stf_details = []  # format -> [[Name,desg,assigned date], ...]
    priority = ["ai_ds", "cse", "it", "civil", "ece", "eie", "eee", "mech", "cyber", "mde", "agri"]
    for dept in priority:
        # now I should extract name, desg, and assigned date and time with details from al_tag
        cmd = "select Name,Desg,Assign_date, al_tag from " + dept
        mycursor.execute(cmd)

        dummy = []
        for i in mycursor:
            dummy.append(i)

        # staff id would be a good method to index, but for the data constraint, I am assigning name(key) to al_tag
        for index, tup in enumerate(dummy):
            stf_details.append([tup[3], tup[0], tup[1], tup[2]])
            # tag_link[tup[0]] = tup[3]

    return stf_details


def update_password(username, new_pswd):
    try:
        cmd = "update users set password = %s where Name=%s"
        dt = (new_pswd, username)

        mycursor.execute(cmd, dt)
        mycon.commit()

        return True
    except ValueError:
        return False


def operate_user_cookie(op, username=""):
    if op == "fetch":
        cmd = "select * from user_cookie"
        mycursor.execute(cmd)

        lst = []
        for i in mycursor:
            lst.append(i)
        uname = ""
        for index, tup in enumerate(lst):
            uname = uname + tup[0]

        return uname

    elif op == "drop":
        cmd = "delete ignore from user_cookie"
        mycursor.execute(cmd)
        mycon.commit()

        return "DELETED"

    elif op == "insert":

        if username is not None:
            cmd = "insert into user_cookie values(%s)"
            data_tup = (username,)
            mycursor.execute(cmd, data_tup)
            mycon.commit()


def store_sess_sum_dict(user_dict):
    print("Given value: ", user_dict)
    for i in user_dict:
        date = i
        sess_sum = user_dict[i]

        FN = sess_sum[0]
        AN = sess_sum[1]
        sum_ = sess_sum[2]
        cmd = "insert into sess_sum values(%s, %s, %s, %s)"
        dt = (date, FN, AN, sum_)

        mycursor.execute(cmd, dt)
        mycon.commit()

    return True


def initialise_dict_da(lst):
    ret = {}
    for i in lst:
        ret[i] = [0, 0, 0]
    return ret


glob_dict = {}


def extract_sess_sum_dict():
    global glob_dict
    cmd = "select * from sess_sum"
    mycursor.execute(cmd)

    lst = []
    for i in mycursor:
        lst.append(i)

    ret_dict = {}
    for index, tup in enumerate(lst):
        ret_dict[tup[0]] = [tup[1], tup[2], tup[3]]

    print("IN SESS_SUM: ", ret_dict)
    glob_dict = ret_dict
    if len(ret_dict) == 0:
        dates = fetch_exam_dates()
        return initialise_dict_da(dates)
    else:
        return ret_dict


def delete_sess_sum_dict():
    """
    extract the values, transfer it to exam_dates and delete the current instance
    :return:
    """
    global glob_dict
    slot, session = retrive_cookie()
    print("CALLING from del")
    data = glob_dict

    for i in data:
        tag = "AS" + data_gen_id()
        date = i
        FN = data[i][0]
        AN = data[i][1]

        if FN + AN != 0:
            cmd = "insert ignore into allot_dates(Date, FN, AN, staffs_assigned," \
                  " FN_status, AN_status, slot, session) values(%s,%s,%s,%s,%s,%s,%s,%s)"
            data_tup = (date, FN, AN, tag, FN, AN, slot, session)
            print("CMDCMD: ", data_tup)
            mycursor.execute(cmd, data_tup)
            mycon.commit()

    del_cmd = "delete from sess_sum"
    mycursor.execute(del_cmd)
    mycon.commit()


def delete_sess_sum_dict_ext(clg):
    """
    extract the values, transfer it to exam_dates and delete the current instance
    :return:
    """
    global glob_dict
    slot, session = ext_retrive_cookie(clg)

    data = glob_dict
    print("Extracted data: ", data)
    for i in data:
        print("{} is inserted in ext".format(i))
        tag = "AS" + data_gen_id()
        date = i
        FN = data[i][0]
        AN = data[i][1]

        if FN + AN != 0:
            cmd = "insert ignore into allot_dates_ext(Date, FN, AN, staffs_assigned," \
                  " FN_status, AN_status, slot, session, college) values(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            print("Insertion command: ", cmd)
            data_tup = (date, FN, AN, tag, FN, AN, slot, session, clg)
            mycursor.execute(cmd, data_tup)
            mycon.commit()

    del_cmd = "delete from sess_sum"
    mycursor.execute(del_cmd)
    mycon.commit()


def staff_data_ext_by_date_sess(user_input, option):
    """
    This function will fetch the data from each department and also the al_tags in which the allotment details are there
    :return:
    """
    tot_fn, tot_an, tot = 0, 0, 0
    if option == "date":
        cmd = "select staffs_assigned from allot_dates where Date =%s"
        dt = (user_input,)
        mycursor.execute(cmd, dt)

    elif option == "slot":
        cmd = "select staffs_assigned from allot_dates where slot =%s"
        dt = (user_input,)
        mycursor.execute(cmd, dt)

    lst = []
    for i in mycursor:
        lst.append(i)

    al_tag = []
    for index, tup in enumerate(lst):
        al_tag.append(tup[0])

    if len(al_tag) != 0:
        link = []
        for tags in al_tag:
            curr = tags
            cmd = "select * from " + curr
            mycursor.execute(cmd)

            dummy = []
            for pen in mycursor:
                dummy.append(pen)
            for ind, tp in enumerate(dummy):
                link.append(tp[0])
            dummy = []
            d2 = []

        stf_details = []  # format -> [[Name,desg,assigned date], ...]
        print("LINK: ", link)
        for data in link:
            cmd = ""
            # now I should extract name, desg, and assigned date and time with details from al_tag
            if option == "slot":
                cmd = "select * from " + data + " where slot=%s"
            if option == "date":
                cmd = "select * from " + data + " where date=%s"
            dt = (user_input,)
            mycursor.execute(cmd, dt)

            dummy = []
            for i in mycursor:
                dummy.append(i)

            dates, session, dept = [], "", ""
            for index, tup in enumerate(dummy):
                session, dept = tup[1], tup[2]
                dates.append(tup[0])

            stf_Data = "select Name, Desg, contact, email, staff_id from " + dept + " where al_tag= " + "'" + data + "'"
            mycursor.execute(stf_Data)

            tak = []
            for c in mycursor:
                tak.append(c)
            for date in dates:
                for ind, tup in enumerate(tak):
                    if session == "FN":
                        stf_details.append(
                            [tup[4], tup[0], tup[1], dept, str(date_converter(date)), 1, 0, tup[2], tup[3]])
                    if session == "AN":
                        stf_details.append(
                            [tup[4], tup[0], tup[1], dept, str(date_converter(date)), 0, 1, tup[2], tup[3]])

            if session == "FN":
                tot_fn = tot_fn + 1
            if session == "AN":
                tot_an = tot_an + 1

        tot = tot_fn + tot_an
        tot_lst = [tot_fn, tot_an, tot]

        rem_stf_details = []
        for t in stf_details:
            if t not in rem_stf_details:
                rem_stf_details.append(t)

        return rem_stf_details, tot_lst  # this should contain al_Tag, Name, Occupation, Allotment date and time
    else:
        return None


def name_staff_id(staff_id, dept):
    cmd = "select Name from " + dept + " where al_tag = " + "'" + staff_id + "'"
    mycursor.execute(cmd)

    dummy = []
    for i in mycursor:
        dummy.append(i)

    Name = ""
    for index, tup in enumerate(dummy):
        Name = Name + tup[0]

    return Name


def dict_to_lst(dict):
    l = []
    for i in dict:
        l.append([i, dict[i]])


def fill_dash(lst):
    length = len(lst)
    new = []
    for i in range(6):
        if i < length:
            new.append(lst[i])
        else:
            new.append("-")
    return new


def staff_data_ext_by_staff_id(staff_id):
    """
    This function will fetch the data from each department and also the al_tags in which the allotment details are there
    :return:
    """
    try:

        al_cmd = "select * from " + "S" + staff_id
        mycursor.execute(al_cmd)

        t = []
        for d in mycursor:
            t.append(d)

        print("T: ", t)
        al_tag = ""
        for index, tp in enumerate(t):
            al_tag = tp[0]

        print("Altag: ", al_tag)
        cmd = "select * from " + al_tag
        mycursor.execute(cmd)

        lst = []
        for i in mycursor:
            lst.append(i)

        # print("lst: ", lst)
        if len(lst) == 0:
            return [], [], [], [], [], []
        else:

            d1, d2 = {"1": ['-', '-'], "2": ['-', '-'], "3": ['-', '-']}, {"4": ['-', '-'], "5": ['-', '-'],
                                                                           "6": ['-', '-']}
            # each key should contain -> Date,  session, Name, Department, Current Date

            main_dict = []
            dept = ""
            session = ""
            date = ""
            for index, tup in enumerate(lst):
                dept = tup[2]
                main_dict.append([tup[0], tup[1]])
                date = tup[0]

            # print("MD: ", main_dict)
            ses_sel = "select session from allot_dates where Date = " + "'" + date + "'"
            mycursor.execute(ses_sel)

            dummy = []
            for y in mycursor:
                dummy.append(y)

            for ind, tupl in enumerate(dummy):
                session = tupl[0]

            x = datetime.datetime.now()
            today = x.strftime('%x')

            for i in range(len(main_dict)):
                if i <= 2:
                    d1[str(i + 1)] = main_dict[i]
                elif i >= 3:
                    d2[str(i + 1)] = main_dict[i]

            # print(d1, d2, al_tag, dept)
            name = name_staff_id(al_tag, dept)

            return d1, d2, name, dept, today, session

    except mc.errors.ProgrammingError:
        return [], [], [], [], [], []


# print(staff_data_ext_by_staff_id("81030022"))


def staff_data_ext_by_date(date):
    master_list = []

    try:

        cmd = "select staffs_assigned from allot_dates where Date = " + "'" + date + "'"
        mycursor.execute(cmd)

        main_tag = ""
        lst = []
        for i in mycursor:
            lst.append(i)

        for index, tup in enumerate(lst):
            main_tag = main_tag + tup[0]

        print("MAIN TAG: ", main_tag)
        ext_staffs = "select * from " + main_tag
        mycursor.execute(ext_staffs)

        lst = []
        for i in mycursor:
            lst.append(i)

        al_tags = []
        for index, tup in enumerate(lst):
            al_tags.append(tup[0])

        for staffs in al_tags:
            curr = staffs

            cmd = "select dept from " + curr
            mycursor.execute(cmd)

            dummy = []
            for i in mycursor:
                dummy.append(i)

            dept = ""
            for index, tup in enumerate(dummy):
                dept = tup[0]

            staff_id_ext = "select staff_id from " + dept + " where al_tag = " + "'" + curr + "'"
            mycursor.execute(staff_id_ext)

            main_staff_id = ""
            dummy = []
            for i in mycursor:
                dummy.append(i)

            for index, tup in enumerate(dummy):
                main_staff_id = main_staff_id + str(tup[0])

            d1, d2, name, dept, today, session = staff_data_ext_by_staff_id(main_staff_id)
            # print(d1)

            master_list.append([d1, d2, name, dept, today, session])
            print("master: ", master_list)
        return master_list
    except mc.errors.ProgrammingError:
        return []


# print(staff_data_ext_by_date("2023-03-01"))

def staff_data_ext_by_session(session):
    master_list = []
    try:

        cmd = "select staffs_assigned from allot_dates where slot = " + "'" + session + "'"
        mycursor.execute(cmd)

        print("Given command: ", cmd)
        main_tag = []
        lst = []
        for i in mycursor:
            lst.append(i)

        for index, tup in enumerate(lst):
            main_tag.append(tup[0])

        print("MAIN TAG: ", main_tag)

        for individual in main_tag:
            ext_staffs = "select * from " + individual
            mycursor.execute(ext_staffs)

            lst = []
            for i in mycursor:
                lst.append(i)

            al_tags = []
            for index, tup in enumerate(lst):
                al_tags.append(tup[0])

            print("Al tags: ", al_tags)
            for staffs in al_tags:
                curr = staffs

                cmd = "select dept from " + curr
                mycursor.execute(cmd)

                dummy = []
                for i in mycursor:
                    dummy.append(i)

                dept = ""
                for index, tup in enumerate(dummy):
                    dept = tup[0]

                staff_id_ext = "select staff_id from " + dept + " where al_tag = " + "'" + curr + "'"
                mycursor.execute(staff_id_ext)

                main_staff_id = ""
                dummy = []
                for i in mycursor:
                    dummy.append(i)

                for index, tup in enumerate(dummy):
                    main_staff_id = main_staff_id + str(tup[0])

                print("MAI: ", main_staff_id)

                d1, d2, name, dept, today, session = staff_data_ext_by_staff_id(main_staff_id)

                master_list.append([d1, d2, name, dept, today, session])

        print("master ", master_list)
        return master_list
    except mc.errors.ProgrammingError:
        return []


def dummy_sess_cnt(val, op):
    if op == "ins":
        cmd = "insert into dummy_sess_cnt values(%s)"
        dt = (val,)
        mycursor.execute(cmd, dt)
        mycon.commit()

    if op == "del":
        cmd = "delete from dummy_sess_cnt"
        mycursor.execute(cmd)
        mycon.commit()

    if op == "fetch":
        cmd = "select sum(fn_an) from dummy_sess_cnt"
        mycursor.execute(cmd)

        lst = []
        for i in mycursor:
            lst.append(i)
        ret = 0
        for index, tup in enumerate(lst):
            ret = tup[0]

        return ret


def check_after_exits(after_date, op):
    cmd = ""
    if op == "int":
        cmd = "select * from allot_dates where Date=" + "'" + after_date + "'"
    if op == "ext":
        cmd = "select * from allot_dates where Date=" + "'" + after_date + "'"

    mycursor.execute(cmd)
    lst = []
    for i in mycursor:
        lst.append(i)

    return len(lst) == 0  # if 0 then it is ok to shift the date, else return cannot override


def change_date_db(before, after):
    chk = check_after_exits(after, "int")
    if chk is True:
        cmd = "select staffs_assigned from allot_dates where Date=" + "'" + before + "'"
        mycursor.execute(cmd)

        lst = []
        for i in mycursor:
            lst.append(i)
        print(lst)
        tag = ""
        for index, tup in enumerate(lst):
            tag = tup[0]

        stf_ext = "select * from " + tag
        mycursor.execute(stf_ext)
        dummy = []

        for j in mycursor:
            dummy.append(j)

        staff_tags = []
        for index, tup in enumerate(dummy):
            staff_tags.append(tup[0])

        for staffs in staff_tags:
            cmd = "update " + staffs + " set Date = " + "'" + after + "'" + " where Date = " + "'" + before + "'"
            mycursor.execute(cmd)
            mycon.commit()

        cmd = "update allot_dates set Date=" + "'" + after + "'" + " where Date = " + "'" + before + "'"
        mycursor.execute(cmd)
        mycon.commit()
        return "Granted"
    else:
        return "Denied"


def change_date_db_ext(before, after):
    chk = check_after_exits(after, "ext")
    if chk is True:
        cmd = "select staffs_assigned from allot_dates_ext where Date=" + "'" + before + "'"
        mycursor.execute(cmd)

        lst = []
        for i in mycursor:
            lst.append(i)

        tag = ""
        for index, tup in enumerate(lst):
            tag = tup[0]

        stf_ext = "select * from " + tag
        mycursor.execute(stf_ext)
        dummy = []

        for j in mycursor:
            dummy.append(j)

        staff_tags = []
        for index, tup in enumerate(dummy):
            staff_tags.append(tup[0])

        for staffs in staff_tags:
            cmd = "update " + staffs + " set Date = " + "'" + after + "'" + " where Date = " + "'" + before + "'"
            mycursor.execute(cmd)
            mycon.commit()

        cmd = "update allot_dates_ext set Date=" + "'" + after + "'" + " where Date = " + "'" + before + "'"
        mycursor.execute(cmd)
        mycon.commit()
        return "Granted"

    else:
        return "Denied"


def check_date_exists(date):
    cmd = "select * from allot_dates where Date=" + "'" + date + "'"
    mycursor.execute(cmd)

    l = []
    for i in mycursor:
        l.append(i)

    return len(l) == 0  # if true then date doesn't exist, else False -> date exists


def check_date_exists_ext(date):
    cmd = "select * from allot_dates_ext where Date=" + "'" + date + "'"
    mycursor.execute(cmd)

    l = []
    for i in mycursor:
        l.append(i)

    return len(l) == 0  # if true then date doesn't exist, else False -> date exists


def delete_exam_date(user_date):
    confim = check_date_exists(user_date)
    if confim == False:
        chk = "select * from user_cookie"
        mycursor.execute(chk)

        lst = []
        for i in mycursor:
            lst.append(i)

        current_user = ""
        for index, tup in enumerate(lst):
            current_user = tup[0]

        if current_user == "Admin" or current_user == "Duty Superintend":
            cmd = "select staffs_assigned from allot_dates where Date=" + "'" + user_date + "'"
            mycursor.execute(cmd)

            lst = []
            for i in mycursor:
                lst.append(i)

            tag = ""
            for index, tup in enumerate(lst):
                tag = tup[0]

            stf_ext = "select * from " + tag
            mycursor.execute(stf_ext)
            dummy = []

            for j in mycursor:
                dummy.append(j)

            staff_tags = []
            for index, tup in enumerate(dummy):
                staff_tags.append(tup[0])

            for staffs in staff_tags:
                """
                1. decrement the tot_duty in their dept table
                2. if tot_duty is 0, then increment the DEPT table 
                3. drop the staffs_assigned tag from allot_dates
                4. delete the entire row in allot_dates
                """
                # first find the dept
                cmd = "select dept from " + staffs
                mycursor.execute(cmd)

                d = []
                for t in mycursor:
                    d.append(t)
                dept = ""
                for ind, tp in enumerate(d):
                    dept = tp[0]

                dec_cmd = "update " + dept + " set tot_duty = tot_duty - 1 where al_tag = " + "'" + staffs + "'"
                print(dec_cmd)
                mycursor.execute(dec_cmd)
                mycon.commit()

                chk_for_increment = "select tot_duty from " + dept + " where al_tag = " + "'" + staffs + "'"
                mycursor.execute(chk_for_increment)

                pencil = []
                for c in mycursor:
                    pencil.append(c)

                tot_duty = 0
                for ind, tp in enumerate(pencil):
                    tot_duty = int(tp[0])

                del_cmd = "delete from " + staffs + " where Date = " + "'" + user_date + "'"
                mycursor.execute(del_cmd)
                mycon.commit()

                if tot_duty == 0:
                    upd_cmd = "update DEPT set stf_avail = stf_avail + 1 where name = " + "'" + dept + "'"
                    mycursor.execute(upd_cmd)
                    mycon.commit()

            cmd = "delete from allot_dates where Date=" + "'" + user_date + "'"
            mycursor.execute(cmd)
            mycon.commit()

            return "updated"
        else:
            return "denied"
    else:
        return "no date"


def update_slot_buffer(slot_name, op):
    if op == "ins":
        cmd = "insert into slot_buffer values(%s)"
        dt = (slot_name,)
        mycursor.execute(cmd, dt)
        mycon.commit()

    if op == "fetch":
        cmd = "select * from slot_buffer"
        mycursor.execute(cmd)

        lst = []
        for i in mycursor:
            lst.append(i)

        slot = []
        for index, tup in enumerate(lst):
            slot.append(tup[0])

        init_cmd = "delete from slot_buffer"
        mycursor.execute(init_cmd)
        mycon.commit()

        return slot[-1]


def check_slot_exists(slot):
    cmd = "select * from allot_dates where slot=" + "'" + slot + "'"
    mycursor.execute(cmd)

    l = []
    for i in mycursor:
        l.append(i)

    return len(l) == 0  # if true then date doesn't exist, else False -> date exists


def check_slot_exists_ext(slot, clg):
    cmd = "select * from allot_dates_ext where slot=" + "'" + slot + "'" + " and college=" + "'" + clg + "'"
    mycursor.execute(cmd)

    l = []
    for i in mycursor:
        l.append(i)

    return len(l) == 0  # if true then date doesn't exist, else False -> date exists


def get_date_from_slot(slot):
    cmd = "select Date from allot_dates where slot = " + "'" + slot + "'"
    mycursor.execute(cmd)

    lst = []
    for i in mycursor:
        lst.append(i)

    date = ""
    for index, tup in enumerate(lst):
        date = tup[0]

    return date


def delete_entire_session(user_slot):
    confim = check_slot_exists(user_slot)

    if not confim:
        chk = "select * from user_cookie"
        mycursor.execute(chk)

        lst = []
        for i in mycursor:
            lst.append(i)

        current_user = ""
        for index, tup in enumerate(lst):
            current_user = tup[0]

        if current_user == "Admin" or current_user == "Duty Superintend":
            cmd = "select staffs_assigned from allot_dates where slot=" + "'" + user_slot + "'"
            mycursor.execute(cmd)

            lst = []
            for i in mycursor:
                lst.append(i)

            tag = ""
            for index, tup in enumerate(lst):
                tag = tup[0]

            stf_ext = "select * from " + tag
            mycursor.execute(stf_ext)
            dummy = []

            for j in mycursor:
                dummy.append(j)

            staff_tags = []
            for index, tup in enumerate(dummy):
                staff_tags.append(tup[0])

            for staffs in staff_tags:
                """
                1. decrement the tot_duty in their dept table
                2. if tot_duty is 0, then increment the DEPT table 
                3. drop the staffs_assigned tag from allot_dates
                4. delete the entire row in allot_dates
                """
                # first find the dept
                cmd = "select dept from " + staffs
                mycursor.execute(cmd)

                d = []
                for t in mycursor:
                    d.append(t)
                dept = ""
                for ind, tp in enumerate(d):
                    dept = tp[0]

                dec_cmd = "update " + dept + " set tot_duty = tot_duty - 1 where al_tag = " + "'" + staffs + "'"
                print(dec_cmd)
                mycursor.execute(dec_cmd)
                mycon.commit()

                chk_for_increment = "select tot_duty from " + dept + " where al_tag = " + "'" + staffs + "'"
                mycursor.execute(chk_for_increment)

                pencil = []
                for c in mycursor:
                    pencil.append(c)

                tot_duty = 0
                for ind, tp in enumerate(pencil):
                    tot_duty = int(tp[0])

                del_cmd = "delete from " + staffs + " where Date = " + "'" + get_date_from_slot(user_slot) + "'"
                mycursor.execute(del_cmd)
                mycon.commit()

                if tot_duty == 0:
                    upd_cmd = "update DEPT set stf_avail = stf_avail + 1 where name = " + "'" + dept + "'"
                    mycursor.execute(upd_cmd)
                    mycon.commit()

            cmd = "delete from allot_dates where slot=" + "'" + user_slot + "'"
            mycursor.execute(cmd)
            mycon.commit()

            print("US_!: ", str(user_slot[-1]))

            cookie_del = "delete from slots where slot = " + "'" + str(user_slot[-1]) + "'"
            mycursor.execute(cookie_del)
            mycon.commit()

            return "updated"
        else:
            return "denied"
    else:
        return "no date"


def add_college_to_db(college_name, c_code, cs_name, cs_mobile, cs_landline, emailid):
    cmd = "insert into colleges(name, c_code, cs_name, cs_mobile, cs_landline, emailid) values(%s,%s,%s,%s,%s,%s)"
    dt = (college_name.upper(), c_code, cs_name, cs_mobile, cs_landline, emailid)
    mycursor.execute(cmd, dt)
    mycon.commit()


def extract_clg():
    cmd = "select * from colleges"
    mycursor.execute(cmd)

    lst = []
    for i in mycursor:
        lst.append(i)

    main = []
    only_clg = []
    for index, tup in enumerate(lst):
        only_clg.append(tup[0])
        main.append([tup[0], tup[1], tup[2], tup[3], tup[4], tup[5]])

    return main, only_clg


def file_cookie(file_name, toggle):
    if toggle == 1:
        cmd = "update file_details set active_stat=1 where name =%s"
        dt = (file_name,)
        mycursor.execute(cmd, dt)
        mycon.commit()

    elif toggle == 0:
        cmd = "update file_details set active_stat=0 where name =%s"
        dt = (file_name,)
        mycursor.execute(cmd, dt)
        mycon.commit()


def check_dup(file_name):
    cmd = "select * from file_details where name=" + "'" + file_name + "'"
    mycursor.execute(cmd)

    lst = []
    for i in mycursor:
        lst.append(i)

    return len(lst) == 0  # if False then only allow to add the file


def check_college_exists(clg_name):
    cmd = "select * from ext_slots where clg_name=" + "'" + clg_name + "'"
    mycursor.execute(cmd)

    lst = []
    for i in mycursor:
        lst.append(i)
    # print(lst)
    ret_lst = []
    for index, tuple in enumerate(lst):
        ret_lst.append(tuple[0])

    if len(lst) == 0:
        return 1
    else:
        cmd = "select max(slot) from ext_slots where clg_name=" + "'" + clg_name + "'"
        mycursor.execute(cmd)

        lst = []
        for i in lst:
            mycursor.execute(i)
        max_slot = 0
        for ind, tp in enumerate(lst):
            max_slot = int(tp[0])

        return max_slot


def ext_duty_slot(data):
    sd = data[0]
    ed = data[1]
    sess = data[2]
    clg = data[3]

    val = check_college_exists(clg)
    if val == 1:  # then a new slot has to be created
        cmd = "insert into ext_slots(slot, start_date, end_date, session, clg_name) values(%s,%s,%s,%s,%s)"
        data_tup = ("1", sd, ed, sess, clg)

        mycursor.execute(cmd, data_tup)
        mycon.commit()

        return 1
    else:

        new_slot = val + 1

        cmd = "insert into ext_slots(slot, start_date, end_date, session, clg_name) values(%s,%s,%s,%s,%s)"
        data_tup = (new_slot, sd, ed, sess, clg)

        mycursor.execute(cmd, data_tup)
        mycon.commit()

        return new_slot


def extract_ext_slots(clg):
    cmd = "select * from ext_slots where clg_name=" + "'" + clg + "'"
    mycursor.execute(cmd)

    lst = []
    for i in mycursor:
        lst.append(i)
    data = []

    for index, tup in enumerate(lst):
        data.append([tup[0], tup[1], tup[2], tup[3], tup[4]])

    return data


def get_active_clg():
    cmd = "select name from file_details where active_stat=1"
    mycursor.execute(cmd)

    lst = []
    for i in mycursor:
        lst.append(i)

    file = ""
    for index, tup in enumerate(lst):
        file = tup[0]

    return file


import csv


def extract_file_contents(path, file):
    f = open(path + file, mode="r")

    obj = csv.reader(f)
    ret = list(obj)

    new = []
    for i in ret[1:]:
        dummy = []
        for j in i:
            if j != '':
                dummy.append(j)
        new.append(dummy)
        dummy = []

    return new


def update_file_cookie(file, op):
    if op == "ins":
        ini = "delete from sel_file_cookie"
        mycursor.execute(ini)
        mycon.commit()

        cmd = "insert into sel_file_cookie values(%s)"
        dt = (file,)

        mycursor.execute(cmd, dt)
        mycon.commit()
    elif op == "fetch":
        cmd = "select * from sel_file_cookie"
        mycursor.execute(cmd)

        lst = []
        for i in mycursor:
            lst.append(i)
        curr = ""
        for index, tup in enumerate(lst):
            curr = tup[0]
        return curr


def staff_data_ext_by_date_sess_ext(user_input, option, college):
    """
    This function will fetch the data from each department and also the al_tags in which the allotment details are there
    :return:
    """
    tot_fn, tot_an, tot = 0, 0, 0
    if option == "date":
        cmd = "select staffs_assigned from allot_dates_ext where Date = (%s) and college = (%s)"
        dt = (user_input, college)
        mycursor.execute(cmd, dt)

    elif option == "slot":
        cmd = "select staffs_assigned from allot_dates_ext where slot = (%s) and college = (%s)"
        dt = (user_input, college)
        mycursor.execute(cmd, dt)

    lst = []
    for i in mycursor:
        lst.append(i)

    al_tag = []
    for index, tup in enumerate(lst):
        al_tag.append(tup[0])

    print("Al tags:", al_tag)

    if len(al_tag) != 0:
        link = []
        for tags in al_tag:
            curr = tags
            cmd = "select * from " + curr
            mycursor.execute(cmd)

            dummy = []
            for pen in mycursor:
                dummy.append(pen)
            for ind, tp in enumerate(dummy):
                link.append(tp[0])
            dummy = []
            d2 = []

        stf_details = []  # format -> [[Name,desg,assigned date], ...]

        for data in link:
            # now I should extract name, desg, and assigned date and time with details from al_tag
            cmd = "select * from " + data
            mycursor.execute(cmd)

            dummy = []
            for i in mycursor:
                dummy.append(i)

            date, session, dept = "", "", ""
            for index, tup in enumerate(dummy):
                date, session, dept = tup[0], tup[1], tup[2]

            stf_Data = "select Name, Desg, contact, email, staff_id from" \
                       " " + dept + " where al_tag= " + "'" + data + "'"
            mycursor.execute(stf_Data)

            tak = []
            for c in mycursor:
                tak.append(c)
            for ind, tup in enumerate(tak):
                if session == "FN":
                    tot_fn = tot_fn + 1
                    stf_details.append(
                        [tup[4], tup[0], tup[1], dept[:-4].upper(), str(date_converter(date)), 1, 0, tup[2], tup[3]])
                elif session == "AN":
                    tot_an = tot_an + 1
                    stf_details.append(
                        [tup[4], tup[0], tup[1], dept[:-4].upper(), str(date_converter(date)), 0, 1, tup[2], tup[3]])

        tot = tot_fn + tot_an
        tot_lst = [tot_fn, tot_an, tot]

        return stf_details, tot_lst  # this should contain al_Tag, Name, Occupation, Allotment date and time
    else:
        return None


def staff_data_ext_by_date_ext(date, clg):
    master_list = []

    try:

        cmd = "select staffs_assigned from allot_dates_ext where college = (%s) and date = (%s)"
        dt = (clg, date)
        mycursor.execute(cmd, dt)

        main_tag = ""
        lst = []
        for i in mycursor:
            lst.append(i)

        for index, tup in enumerate(lst):
            main_tag = main_tag + tup[0]

        print("MAIN TAG: ", main_tag)
        ext_staffs = "select * from " + main_tag
        mycursor.execute(ext_staffs)

        lst = []
        for i in mycursor:
            lst.append(i)

        al_tags = []
        for index, tup in enumerate(lst):
            al_tags.append(tup[0])

        print("Al_tags: ", al_tags)
        for staffs in al_tags:
            curr = staffs

            cmd = "select dept from " + curr
            mycursor.execute(cmd)

            dummy = []
            for i in mycursor:
                dummy.append(i)

            dept = ""
            for index, tup in enumerate(dummy):
                dept = tup[0]
            print(dept)
            staff_id_ext = "select staff_id from " + dept + " where al_tag = " + "'" + curr + "'"
            mycursor.execute(staff_id_ext)

            main_staff_id = ""
            dummy = []
            for i in mycursor:
                dummy.append(i)

            for index, tup in enumerate(dummy):
                main_staff_id = str(tup[0])
            print("MSI:", main_staff_id)

            main_dict, staff_name, session, college = staff_data_ext_by_staff_id_ext(main_staff_id)

            master_list.append([main_dict, staff_name, session, college])
        print(master_list)
        return master_list
    except mc.errors.ProgrammingError:
        return []


def staff_data_ext_by_staff_id_ext(staff_id):
    """
    This function will fetch the data from each department and also the al_tags in which the allotment details are there
    :return:
    """
    try:

        al_cmd = "select * from " + "S" + staff_id
        mycursor.execute(al_cmd)

        t = []
        for d in mycursor:
            t.append(d)

        al_tag = ""
        for index, tp in enumerate(t):
            al_tag = tp[0]

        cmd = "select * from " + al_tag
        mycursor.execute(cmd)

        lst = []
        for i in mycursor:
            lst.append(i)

        if len(lst) == 0:
            return [], "", "", ""
        else:

            staff_name = ""
            college = ""
            main_dict = {}  # the main_dict will have the date as key and values as [name, session, fn_an]
            dept = ""
            session = ""
            date = []
            fn_an = ""
            for index, tup in enumerate(lst):
                fn_an = tup[1]
                dept = tup[2]
                main_dict[tup[0]] = tup[1]
                date.append(tup[0])

            for dates in date:
                ses_sel = "select session, college from allot_dates_ext where Date = " + "'" + dates + "'"
                mycursor.execute(ses_sel)

                dummy = []
                for y in mycursor:
                    dummy.append(y)

                for ind, tupl in enumerate(dummy):
                    session = tupl[0]
                    college = tupl[1]

                name_ext = "select Name from " + dept + " where staff_id= (%s)"
                dt = (staff_id,)
                mycursor.execute(name_ext, dt)

                lst = []
                for h in mycursor:
                    lst.append(h)

                staff_name = ""
                for ind, tp in enumerate(lst):
                    staff_name = tp[0]

                main_dict[dates] = fn_an

            return main_dict, staff_name, session, college

    except mc.errors.ProgrammingError:
        return [], "", "", ""


# print(staff_data_ext_by_staff_id_ext("1243056"))

def staff_data_ext_by_session_ext(session, college):
    master_list = []
    try:
        cmd = "select staffs_assigned from allot_dates_ext where college = (%s) and slot = (%s)"
        dt = (college, session)
        mycursor.execute(cmd, dt)

        main_tag = []
        lst = []
        for i in mycursor:
            lst.append(i)

        for index, tup in enumerate(lst):
            main_tag.append(tup[0])

        print("MAIN TAG: ", main_tag)
        for k in main_tag:
            ext_staffs = "select * from " + k
            mycursor.execute(ext_staffs)

            lst = []
            for i in mycursor:
                lst.append(i)

            al_tags = []
            for index, tup in enumerate(lst):
                al_tags.append(tup[0])

            print("Al_tags: ", al_tags)
            for staffs in al_tags:
                curr = staffs

                cmd = "select dept from " + curr
                mycursor.execute(cmd)

                dummy = []
                for i in mycursor:
                    dummy.append(i)

                dept = ""
                for index, tup in enumerate(dummy):
                    dept = tup[0]
                staff_id_ext = "select staff_id from " + dept + " where al_tag = " + "'" + curr + "'"
                mycursor.execute(staff_id_ext)

                main_staff_id = ""
                dummy = []
                for i in mycursor:
                    dummy.append(i)

                for index, tup in enumerate(dummy):
                    main_staff_id = str(tup[0])
                print("MSI:", main_staff_id)

                main_dict, staff_name, session, college = staff_data_ext_by_staff_id_ext(main_staff_id)

                master_list.append([main_dict, staff_name, session, college])
            print(master_list)
        return master_list
    except mc.errors.ProgrammingError:
        return []


def delete_exam_date_ext(user_date, college):
    confim = check_date_exists_ext(user_date)
    if not confim:
        chk = "select * from user_cookie"
        mycursor.execute(chk)

        lst = []
        for i in mycursor:
            lst.append(i)

        current_user = ""
        for index, tup in enumerate(lst):
            current_user = tup[0]

        if current_user == "Admin" or current_user == "Duty Superintend":
            cmd = "select staffs_assigned from allot_dates_ext where " \
                  "Date=" + "'" + user_date + "'" + " and college=" + "'" + college + "'"
            mycursor.execute(cmd)

            lst = []
            for i in mycursor:
                lst.append(i)

            tag = ""
            for index, tup in enumerate(lst):
                tag = tup[0]

            stf_ext = "select * from " + tag
            mycursor.execute(stf_ext)
            dummy = []

            for j in mycursor:
                dummy.append(j)

            staff_tags = []
            for index, tup in enumerate(dummy):
                staff_tags.append(tup[0])

            for staffs in staff_tags:
                """
                1. decrement the tot_duty in their dept table
                2. if tot_duty is 0, then increment the DEPT table 
                3. drop the staffs_assigned tag from allot_dates
                4. delete the entire row in allot_dates
                """
                # first find the dept
                cmd = "select dept from " + staffs
                mycursor.execute(cmd)

                d = []
                for t in mycursor:
                    d.append(t)
                dept = ""
                for ind, tp in enumerate(d):
                    dept = tp[0]

                dec_cmd = "update " + dept + " set tot_duty = tot_duty - 1 where al_tag = " + "'" + staffs + "'"
                print(dec_cmd)
                mycursor.execute(dec_cmd)
                mycon.commit()

                chk_for_increment = "select tot_duty from " + dept + " where al_tag = " + "'" + staffs + "'"
                mycursor.execute(chk_for_increment)

                pencil = []
                for c in mycursor:
                    pencil.append(c)

                tot_duty = 0
                for ind, tp in enumerate(pencil):
                    tot_duty = int(tp[0])

                del_cmd = "delete from " + staffs + " where Date = " + "'" + user_date + "'"
                mycursor.execute(del_cmd)
                mycon.commit()

                if tot_duty == 0:
                    upd_cmd = "update DEPT_ext set stf_avail = stf_avail + 1 where name = " + "'" + dept + "'"
                    mycursor.execute(upd_cmd)
                    mycon.commit()

            cmd = "delete from allot_dates_ext where " \
                  "Date=" + "'" + user_date + "'" + " and college=" + "'" + college + "'"
            mycursor.execute(cmd)
            mycon.commit()

            return "updated"
        else:
            return "denied"
    else:
        return "no date"


def delete_entire_session_ext(user_slot, college):
    confim = check_slot_exists_ext(user_slot, college)

    if not confim:
        chk = "select * from user_cookie"
        mycursor.execute(chk)

        lst = []
        for i in mycursor:
            lst.append(i)

        current_user = ""
        for index, tup in enumerate(lst):
            current_user = tup[0]

        if current_user == "Admin" or current_user == "Duty Superintend":
            cmd = "select staffs_assigned from allot_dates_ext where " \
                  "slot=" + "'" + user_slot + "'" + " and college=" + "'" + college + "'"
            mycursor.execute(cmd)

            lst = []
            for i in mycursor:
                lst.append(i)

            tag = ""
            for index, tup in enumerate(lst):
                tag = tup[0]

            stf_ext = "select * from " + tag
            mycursor.execute(stf_ext)
            dummy = []

            for j in mycursor:
                dummy.append(j)

            staff_tags = []
            for index, tup in enumerate(dummy):
                staff_tags.append(tup[0])

            for staffs in staff_tags:
                """
                1. decrement the tot_duty in their dept table
                2. if tot_duty is 0, then increment the DEPT table 
                3. drop the staffs_assigned tag from allot_dates
                4. delete the entire row in allot_dates
                """
                # first find the dept
                cmd = "select dept from " + staffs
                mycursor.execute(cmd)

                d = []
                for t in mycursor:
                    d.append(t)
                dept = ""
                for ind, tp in enumerate(d):
                    dept = tp[0]

                dec_cmd = "update " + dept + " set tot_duty = tot_duty - 1 where al_tag = " + "'" + staffs + "'"
                print(dec_cmd)
                mycursor.execute(dec_cmd)
                mycon.commit()

                chk_for_increment = "select tot_duty from " + dept + " where al_tag = " + "'" + staffs + "'"
                mycursor.execute(chk_for_increment)

                pencil = []
                for c in mycursor:
                    pencil.append(c)

                tot_duty = 0
                for ind, tp in enumerate(pencil):
                    tot_duty = int(tp[0])

                del_cmd = "delete from " + staffs + " where Date = " + "'" + get_date_from_slot(user_slot) + "'"
                mycursor.execute(del_cmd)
                mycon.commit()

                if tot_duty == 0:
                    upd_cmd = "update DEPT_ext set stf_avail = stf_avail + 1 where name = " + "'" + dept + "'"
                    mycursor.execute(upd_cmd)
                    mycon.commit()

            cmd = "delete from allot_dates_ext where " \
                  "slot=" + "'" + user_slot + "'" + " and college=" + "'" + college + "'"
            mycursor.execute(cmd)
            mycon.commit()

            print("US_!: ", str(user_slot[-1]))

            cookie_del = "delete from ext_slots where slot = " \
                         "" + "'" + str(user_slot[-1]) + "'" + "and clg_name=" + "'" + college + "'"
            mycursor.execute(cookie_del)
            mycon.commit()

            return "updated"
        else:
            return "denied"
    else:
        return "no date"
