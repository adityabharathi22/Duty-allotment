from flask import Flask, request, redirect, url_for, render_template, make_response
import pdfkit
from duty_allotment5 import process, check_config_status, web_input_slot, available_slots, cookie_update, \
    retrive_cookie, update_temp_dates, fetch_temp_dates, reset_dates, fetch_exam_dates, delete_old_dates, \
    authenticate, staff_data_ext, exam_dates_out, update_password, operate_user_cookie, store_sess_sum_dict, \
    extract_sess_sum_dict, delete_sess_sum_dict, staff_data_ext_by_staff_id, staff_data_ext_by_date_sess, \
    staff_data_ext_by_date, staff_data_ext_by_session, adv_config, dummy_sess_cnt, \
    change_date_db, delete_exam_date, delete_entire_session, add_college_to_db, \
    file_cookie, extract_clg, ext_duty_slot, extract_ext_slots, delete_sess_sum_dict_ext, \
    extract_file_contents, update_file_cookie, cookie_update_ext, ext_retrive_cookie, \
    ext_exam_dates_out, web_input_slot_ext, available_slots_ext, extract_ext_clg_cookie, \
    initialise_dict_da, fetch_latest_clg, staff_data_ext_by_date_sess_ext, staff_data_ext_by_date_ext, \
    staff_data_ext_by_staff_id_ext, staff_data_ext_by_session_ext, change_date_db_ext, delete_exam_date_ext, \
    delete_entire_session_ext

import os
import datetime

app = Flask(__name__,
            template_folder='C:/Users/Aditya Bharathi/PycharmProjects/duty_allotment/duty_allotment-main/Templates')

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
len_date_list = 0
temp_dates = []

file = ""
path = "C:/Users/Aditya Bharathi/PycharmProjects/duty_allotment/duty_allotment-main/staff_data/"


def get_curr_file():
    global file
    files = os.listdir(
        'C:/Users/Aditya Bharathi/PycharmProjects/duty_allotment/duty_allotment-main/staff_data/')

    if len(files) != 0:
        file = files[-1]
        return True
    else:
        return False


@app.route("/success")
def success():
    print("inside success...")
    # return "Exam duty has been successfully alloted..."

    return render_template("altmnt_status.html")


@app.route("/success_ext")
def success_ext():
    print("inside ext success...")
    # return "Exam duty has been successfully alloted..."

    return render_template("altmnt_status_ext.html")


@app.route("/sess_sum_stat")
def sess_sum_stat():
    return render_template('sum_status.html')


@app.route("/date_input")
def date_input():
    slots, data = available_slots()
    return render_template('date_input.html', data=data)


@app.route('/fail')
def fail():
    return render_template('sum_status.html')


@app.route("/upload", methods=['POST'])
def upload():
    filename = ""
    print("INside upload")
    target = os.path.join(APP_ROOT, 'staff_data')
    if not os.path.isdir(target):
        os.mkdir(target)


    for file_ in request.files.getlist("file"):
        filename = file_.filename
        destination = '/'.join([target, filename])
        print("dest: ", destination)
        file_.save(destination)

    # print("HERE: ", path+filename)
    if filename != "":
        adv_config(path, filename, "int")

    # return "Your file has been successfully uploaded..."
    return render_template('file_status.html', filename=filename)


@app.route("/ext_upload", methods=['POST'])
def ext_upload():
    filename = ""
    print("INside ext upload")
    target = os.path.join(APP_ROOT, 'staff_data')
    if not os.path.isdir(target):
        os.mkdir(target)

    for file_ in request.files.getlist("file"):
        filename = file_.filename
        destination = "/".join([target, filename])
        print("destination: ", destination)
        file_.save(destination)

    print("HERE: ", path+filename)
    if filename != "":
        adv_config(path, filename, "ext")

    # return "Your file has been successfully uploaded..."
    return render_template('file_status_ext.html', filename=filename)


def fetch_file():
    files = os.listdir('C:/Users/Aditya Bharathi/PycharmProjects/duty_allotment/duty_allotment-main/staff_data')
    file_name = files[1]
    print(file_name)
    return file_name


@app.route("/slot", methods=["POST", "GET"])
def slot():
    start_Date = request.form.get('start')
    end_Date = request.form.get('end')
    session = request.form.get('session')

    d_lst = [start_Date, end_Date, session.upper()]
    slot_num = web_input_slot(d_lst)

    if request.form.get('submit'):
        return render_template('slot_status_int.html', output=slot_num)

    slots, data = available_slots()
    print("Existing data: ", data)
    return render_template('date_input.html', data=data)


@app.route("/slot_select", methods=["POST", "GET"])
def exam_dates():
    data, un = available_slots()
    print("Data: ", data)
    op = ""
    if request.form.get("options"):
        cookie_update(request.form.get("options"))
        op = request.form.get("options")

    if request.form.get("submit"):
        return render_template("slot_select.html", data=data, op=op, display=un)

    return render_template("slot_select.html", data=data, op=op, display=un)


@app.route("/left_iframe_Data")
def display_slots():
    slots, data = available_slots()

    return render_template("left_iframe_Data.html", data=data)


@app.route("/date_insert")
def insert_date():
    data = retrive_cookie()
    global len_date_list, all_files
    if request.args.get('date'):
        update_temp_dates(request.args.get('date'))
        return render_template("exam_dates_input.html", data=fetch_temp_dates(), meta=data)

    if request.args.get('reset'):
        reset_dates()

    if request.args.get('confirm'):
        print("Now confirmed...")
        delete_old_dates()
        dates = fetch_exam_dates()
        print("Dates in DB: ", dates)
        len_date_list = len(dates)
        exam_dates_out(dates)

        db_dict = extract_sess_sum_dict()
        print("DB_dict: ", db_dict)
        delete_sess_sum_dict()
        return render_template('main.html', data=data, date=dates, db_dict=db_dict, files=all_files, sel_file="")

    return render_template("exam_dates_input.html", meta=data)


@app.route("/db_dates")
def display_dates():
    dates = fetch_temp_dates()

    return render_template("db_dates.html", data=dates)


def initialise_dict(lst):
    ret = {}
    for i in lst:
        ret[i] = []
    return ret


toggle = 0
all_files = os.listdir(
    'C:/Users/Aditya Bharathi/PycharmProjects/duty_allotment/duty_allotment-main/staff_data/')

sel_file = ""


@app.route("/home", methods=["POST", "GET"])
def home():
    global file, toggle, path, all_files, sel_file

    dates = fetch_exam_dates()
    data = retrive_cookie()
    data_dict = initialise_dict_da(dates)
    print("DD before: ", data_dict)
    print(data)
    if request.method == "POST":
        print("IN post")
        dummy_sess_cnt("1", "del")

        if request.form.get("confirm"):

            for row in data_dict:
                get_fn = 'FN_' + row
                get_an = 'AN_' + row
                print("YOURS before: {} {}".format(get_fn, get_an))
                try:
                    FN = int(request.form.get(get_fn))
                    AN = int(request.form.get(get_an))
                except (ValueError, TypeError):
                    FN, AN = 0, 0

                print("YOURS: {} + {} = {}".format(FN, AN, FN + AN))
                session_sum = FN + AN
                dummy_sess_cnt(session_sum, "ins")
                data_dict[row] = [FN, AN, session_sum]

            """All the methods are failing, so the last option is to store the dictionary in data base and 
            then recontruct it and display it using an iframe"""
            store_sess_sum_dict(data_dict)
            db_dict = extract_sess_sum_dict()
            delete_sess_sum_dict()

            all_duty = dummy_sess_cnt("1", "fetch")
            return render_template('main.html', data=data, date=data_dict, db_dict=db_dict, total_duty=all_duty,
                                   files=all_files, sel_file=sel_file)

        if get_curr_file() is True:
            main_obj = process()

            if request.form.get('allot_duty'):  # == 'submit':
                main_obj.insert_file_meta()
                main_obj.construct_dept_int()
                check, tot = main_obj.allot_dates()

                if check == "success":
                    return redirect(url_for('success'))
                else:
                    return render_template("staff_error.html", tot=str(tot))

        if request.form.get('ex_file_sel'):
            if request.form.get('files'):
                sel_file = request.form.get('files')
                print("Selected file here: ", sel_file)

                file_cookie(sel_file, toggle=1)
                db_dict = extract_sess_sum_dict()
                all_duty = 0

                if sel_file != "":
                    adv_config(path, sel_file, "int")
                    a = process()
                    a.dept_table_creation()
                return render_template('main.html', data=data, date=data_dict, db_dict=db_dict, total_duty=all_duty,
                                       files=all_files, sel_file=sel_file)

        if request.form.get('file_upload'):
            a = process()
            a.dept_table_creation()
            return redirect(url_for('upload'))
        else:
            return redirect(url_for('fail'))

    all_duty = dummy_sess_cnt("1", "fetch")
    dummy_sess_cnt("1", "del")
    db_dict = extract_sess_sum_dict()
    return render_template('main.html', data=data, date=data_dict, db_dict=db_dict, total_duty=all_duty,
                           files=all_files, sel_file=sel_file)


@app.route("/main_page")
def main_page():
    global auth_lst, all_files
    if request.args.get("ex_file_sel"):
        update_file_cookie(request.args.get("files"), "ins")
        return render_template("main_page.html", username=operate_user_cookie("fetch"),
                               file=update_file_cookie(request.args.get("files"), "fetch"),
                               files=all_files, sel_file=request.args.get("files"))

    return render_template("main_page.html", username=operate_user_cookie("fetch"),
                           file=update_file_cookie(request.args.get("files"), "fetch"), files=all_files)


@app.route("/file_contents")
def file_contents():
    user_ = update_file_cookie("", "fetch")
    if user_:
        return render_template("file_contents.html", data=extract_file_contents(path, user_), file=user_)
    else:
        return "error"


@app.route("/display_details")
def display_details():
    main_lst = staff_data_ext()

    return render_template('display_details.html', data=main_lst)


@app.route('/user_page', methods=["POST"])
def user_page():
    if request.method == "POST":
        logout = request.form.get("Logout")
        if logout:
            operate_user_cookie("drop")
            return render_template("login_page.html")
        else:
            return render_template("user_page.html")


auth_lst = []


@app.route("/")
def login():
    global auth_lst
    check_config_status()
    operate_user_cookie("drop")
    if request.method == "GET":
        user = request.args.get('user')
        print("Inputted name: ", user)

        if user:
            operate_user_cookie("insert", username=user)
        if request.args.get('change'):
            return render_template('reset_password.html', username=user)

        password = request.args.get('password')
        if password != "":
            chk = authenticate(user, password)

            x = datetime.datetime.now()
            cur_date = x.strftime('%x')

            auth_lst = [user, cur_date]

            if chk == "Granted":
                return render_template('user_page.html', data_wrap=auth_lst)

            if chk is not None and chk == "Denied":
                return render_template('login_page.html', pass_incrt="Incorrect Password")
        else:
            return render_template('login_page.html', pass_incrt="", no_pass="Password field is mandatory")

        # return render_template('login_page.html', user=user)

    return render_template('login_page.html')


@app.route('/reset_password')
def reset_password():
    username = operate_user_cookie("fetch")
    if request.method == "GET":
        old = request.args.get('password')
        new = request.args.get('new_pswd')

        if old != "" and new != "":
            print("Current user: ", username)
            if request.args.get('Submit'):
                operate_user_cookie("drop", username=username)

                print("{}, {}, {}".format(username, old, new))
                chk = authenticate(username, old)
                print("CHECK: ", chk)
                if chk == "Granted":
                    val = update_password(username, new)
                    if val is True:
                        return render_template("login_page.html")
                    else:
                        return render_template("Error in updating... Contact the web administrator")
                elif chk == "Denied":
                    return render_template("reset_password.html", data='Old password is incorrect', username=username)
            else:
                return render_template("reset_password.html", username=username)
        else:
            return render_template("reset_password.html", err="Empty fields are not accepted", username=username)


date = ""
main_lst = []
main_lst_slot = []
user_slot = ""


@app.route("/sel_date_view")
def sel_date_view():
    global date, main_lst

    if request.method == "GET":
        if request.args.get('submit'):
            date = request.args.get('date')

            try:
                main_lst, tot_lst = staff_data_ext_by_date_sess(date, "date")
                print("Staff data in {} :{}".format(date, main_lst))
                tot_lst.append("SRM VEC")
                return render_template('display_details.html', data=main_lst, date_info=date, tot_lst=tot_lst)
            except TypeError:
                return "No duties are alloted in this date"


@app.route("/sel_date_view_ext")
def sel_date_view_ext():
    global date, main_lst

    if request.method == "GET":
        if request.args.get('submit'):
            date = request.args.get('date')

            try:
                main_lst, tot_lst = staff_data_ext_by_date_sess_ext(date, "date", fetch_latest_clg())
                tot_lst.append(fetch_latest_clg())
                print("Staff data in {} :{}".format(date, main_lst))
                return render_template('display_details.html', data=main_lst, date_info=date, tot_lst=tot_lst)
            except TypeError:
                return "No duties are alloted in this date"


@app.route("/sel_sess_view")
def sel_sess_view():
    global main_lst_slot, user_slot
    if request.method == "GET":
        if request.args.get('submit'):
            user_slot = request.args.get('options')
            try:
                main_lst_slot, tot_lst = staff_data_ext_by_date_sess(user_slot, "slot")
                tot_lst.append("SRM VEC")
                print("Staff data in {} :{}".format(user_slot, main_lst))

                return render_template('display_details.html', data=main_lst_slot, date_info=user_slot, tot_lst=tot_lst)
            except TypeError:
                return "no duties are alloted..."


@app.route("/sel_sess_view_ext")
def sel_sess_view_ext():
    global main_lst_slot, user_slot
    if request.method == "GET":
        if request.args.get('submit'):
            user_slot = request.args.get('options')
            try:
                main_lst_slot, tot_lst = staff_data_ext_by_date_sess_ext(user_slot, "slot", fetch_latest_clg())
                tot_lst.append(fetch_latest_clg())
                print("Staff data in {} :{}".format(user_slot, main_lst))

                return render_template('display_details.html', data=main_lst_slot, date_info=user_slot, tot_lst=tot_lst)
            except TypeError:
                return "no duties are alloted..."


@app.route("/view_print_data")
def view_print_data():
    global date, main_lst, main_lst_slot, user_slot

    if len(main_lst) != 0:
        html = render_template('view_print_data.html', data=main_lst, date_info=date)

        path_wkhtmltopdf = "C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe"
        config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)

        pdf = pdfkit.from_string(html, False, configuration=config)
        response = make_response(pdf)
        response.headers["Content-Type"] = "application/pdf"
        response.headers["Content-Disposition"] = "inline; filename=output.pdf"

        main_lst = []
        return response

    if len(main_lst_slot) != 0:
        html = render_template('view_print_slot_data.html', data=main_lst_slot, date_info=user_slot)

        path_wkhtmltopdf = "C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe"
        config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)

        pdf = pdfkit.from_string(html, False, configuration=config)
        response = make_response(pdf)
        response.headers["Content-Type"] = "application/pdf"
        response.headers["Content-Disposition"] = "inline; filename=output.pdf"

        main_lst_slot = []
        return response


@app.route("/view_print_slot")
def view_print_slot():
    global date, main_lst_slot

    if len(main_lst) != 0:
        html = render_template('view_print_data.html', data=main_lst_slot, date_info=date)

        path_wkhtmltopdf = "C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe"
        config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)

        pdf = pdfkit.from_string(html, False, configuration=config)
        response = make_response(pdf)
        response.headers["Content-Type"] = "application/pdf"
        response.headers["Content-Disposition"] = "inline; filename=output.pdf"
        return response


d1, d2, name_curr, dept_curr, current_date, session = {}, {}, "", "", "", ""


@app.route("/report_pdf_staff")
def report_pdf_staff():
    global d1, d2, name_curr, dept_curr, current_date, session

    html = render_template("pdf_report_details.html", d1=d1, d2=d2, name=name_curr,
                           dept=dept_curr, date=current_date, session=session)
    path_wkhtmltopdf = "C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe"
    config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)

    pdf = pdfkit.from_string(html, False, configuration=config)
    response = make_response(pdf)
    response.headers["Content-Type"] = "application/pdf"
    response.headers["Content-Disposition"] = "inline; filename=output.pdf"
    return response


main_lst_date = []
rep = ""


@app.route("/report_pdf_staff_date")
def report_pdf_staff_date():
    global main_lst_date, rep
    print("Main_lst_date: ", main_lst_date)
    html = render_template("pdf_date_wise_report.html", lst=main_lst_date, rep=rep)
    path_wkhtmltopdf = "C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe"
    config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)

    pdf = pdfkit.from_string(html, False, configuration=config)
    response = make_response(pdf)
    response.headers["Content-Type"] = "application/pdf"
    response.headers["Content-Disposition"] = "inline; filename=output.pdf"
    return response


@app.route("/view_options", methods=['POST', 'GET'])
def view_options():
    try:
        data, un = available_slots()
        if request.method == "GET":
            if request.args.get('op_dates'):
                return render_template('sel_date_view.html')
            elif request.args.get('op_sess'):
                print("Data: ", data, un)
                return render_template("sel_sess_view.html", data=data, slots=un)

        return render_template("view_options.html")
    except TypeError:
        return "no duties is alloted..."


sess_ = ""
main_lst_session = ""
rep_sess = ""


@app.route("/report_sess_view")
def report_sess_view():
    global sess_, main_lst_date, rep
    if request.method == "GET":
        if request.args.get('submit'):
            sess_ = request.args.get('options')
            main_lst_date = staff_data_ext_by_session(sess_)
            rep = len(main_lst_date)
            print("MAIN_LST_DATE: ", main_lst_date)

            if rep != 0:
                return render_template('date_wise_report_details.html', rep=rep, lst=main_lst_date)
            else:
                return "No staffs alloted on the date..."


@app.route("/staff_duty_id", methods=["POST", "GET"])
def staff_duty_id():
    global d1, d2, name_curr, dept_curr, current_date, session

    """
    This function will get the staff id and generate a list containing S.no, Date, Session, Name,
    Department, Current Date

    I have to split the list into 2 parts and then give it
    :return:
    """
    global d1, d2, name_curr, dept_curr, current_date, session
    if request.method == "GET":
        if request.args.get('submit'):
            staff_id = request.args.get('staff_id')
            print("Staff id is: ", staff_id)
            d1, d2, name_curr, dept_curr, current_date, session = staff_data_ext_by_staff_id(staff_id)

            print("D!: ", d1)
            if len(d1) != 0:
                return render_template("report_details.html", d1=d1, d2=d2, name=name_curr, rep=3,
                                       dept=dept_curr, date=current_date, session=session)
            else:
                return "The Staff has not been alloted for invigilation"


main_dict_staff_duty_id_ext, name_staff_duty_id_ex, session_staff_duty_id_ex, college_staff_duty_id_ex = {}, "", "", ""
cur_date = ""


@app.route("/staff_duty_id_ext", methods=["POST", "GET"])
def staff_duty_id_ext():
    global main_dict_staff_duty_id_ext, name_staff_duty_id_ex, session_staff_duty_id_ex, \
        college_staff_duty_id_ex, cur_date
    if request.method == "GET":
        if request.args.get('submit'):
            staff_id = request.args.get('staff_id')
            print("Staff id is: ", staff_id)
            main_dict_staff_duty_id_ext, name_staff_duty_id_ex, \
                session_staff_duty_id_ex, college_staff_duty_id_ex = staff_data_ext_by_staff_id_ext(staff_id)
            x = datetime.datetime.now()
            cur_date = x.strftime('%x')

            if len(main_dict_staff_duty_id_ext) != 0:
                return render_template("report_details_ext.html", main=main_dict_staff_duty_id_ext,
                                       Staff_name=name_staff_duty_id_ex, session=session_staff_duty_id_ex,
                                       Date=cur_date, to_clg=college_staff_duty_id_ex)
            else:
                return "The Staff has not been alloted for invigilation"


@app.route("/report_pdf_staff_id_ext")
def report_pdf_staff_id_ext():
    global main_dict_staff_duty_id_ext, name_staff_duty_id_ex, session_staff_duty_id_ex, \
        college_staff_duty_id_ex, cur_date
    html = render_template("report_details_ext_pdf.html", main=main_dict_staff_duty_id_ext,
                           Staff_name=name_staff_duty_id_ex, session=session_staff_duty_id_ex,
                           Date=cur_date, to_clg=college_staff_duty_id_ex)
    path_wkhtmltopdf = "C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe"
    config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)

    pdf = pdfkit.from_string(html, False, configuration=config)
    response = make_response(pdf)
    response.headers["Content-Type"] = "application/pdf"
    response.headers["Content-Disposition"] = "inline; filename=output.pdf"
    return response


@app.route("/report_date_view")
def report_date_view():
    global main_lst_date, rep, date

    if request.method == "GET":
        if request.args.get('submit'):
            date = request.args.get('date')
            print("GIVEN DATE: ", date)
            main_lst_date = staff_data_ext_by_date(date)
            print(main_lst_date)
            rep = len(main_lst_date)
            print("REp: ", rep)
            if rep != 0:
                return render_template('date_wise_report_details.html', rep=rep, lst=main_lst_date)
            else:
                return "No staffs alloted on the date..."


main_lst_date_report_date_view_ext, rep_report_date_view_ext, cur_date_report_date_view_ext = [], 0, ""


@app.route("/report_date_view_ext")
def report_date_view_ext():
    global main_lst_date_report_date_view_ext, rep_report_date_view_ext, cur_date_report_date_view_ext
    if request.method == "GET":
        if request.args.get('submit'):
            date_report_date_view_ext = request.args.get('date')
            main_lst_date_report_date_view_ext = staff_data_ext_by_date_ext(date_report_date_view_ext,
                                                                            fetch_latest_clg())
            rep_report_date_view_ext = len(main_lst_date_report_date_view_ext)

            x = datetime.datetime.now()
            cur_date_report_date_view_ext = x.strftime('%x')

            if rep_report_date_view_ext != 0:
                return render_template('date_wise_report_app_order.html', rep=rep_report_date_view_ext,
                                       lst=main_lst_date_report_date_view_ext, Date=cur_date_report_date_view_ext)
            else:
                return "No staffs alloted on the date..."


rep_report_sess_view_ext, main_lst_date_report_sess_view_ext, cur_date_report_sess_view_ext = 0, [], ""


@app.route("/report_sess_view_ext")
def report_sess_view_ext():
    global rep_report_sess_view_ext, main_lst_date_report_sess_view_ext, cur_date_report_sess_view_ext
    if request.method == "GET":
        if request.args.get('submit'):
            sess_ = request.args.get('options')
            main_lst_date_report_sess_view_ext = staff_data_ext_by_session_ext(sess_, fetch_latest_clg())
            rep_report_sess_view_ext = len(main_lst_date_report_sess_view_ext)
            x = datetime.datetime.now()
            cur_date_report_sess_view_ext = x.strftime('%x')

            if rep_report_sess_view_ext != 0:
                return render_template('sess_wise_report_app_order.html', rep=rep_report_sess_view_ext,
                                       lst=main_lst_date_report_sess_view_ext, Date=cur_date_report_sess_view_ext)
            else:
                return "No staffs alloted on the date..."


@app.route("/report_pdf_staff_sess_ext")
def report_pdf_staff_sess_ext():
    global rep_report_sess_view_ext, main_lst_date_report_sess_view_ext, cur_date_report_sess_view_ext

    html = render_template('sess_wise_report_app_order_pdf.html', rep=rep_report_sess_view_ext,
                           lst=main_lst_date_report_sess_view_ext, Date=cur_date_report_sess_view_ext)

    path_wkhtmltopdf = "C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe"
    config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)

    pdf = pdfkit.from_string(html, False, configuration=config)
    response = make_response(pdf)
    response.headers["Content-Type"] = "application/pdf"
    response.headers["Content-Disposition"] = "inline; filename=output.pdf"
    return response


@app.route("/report_pdf_staff_date_ext")
def report_pdf_staff_date_ext():
    global main_lst_date_report_date_view_ext, rep_report_date_view_ext, cur_date_report_date_view_ext

    html = render_template('date_wise_report_app_order_pdf.html', rep=rep_report_date_view_ext,
                           lst=main_lst_date_report_date_view_ext, Date=cur_date_report_date_view_ext)

    path_wkhtmltopdf = "C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe"
    config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)

    pdf = pdfkit.from_string(html, False, configuration=config)
    response = make_response(pdf)
    response.headers["Content-Type"] = "application/pdf"
    response.headers["Content-Disposition"] = "inline; filename=output.pdf"
    return response


@app.route("/gen_report", methods=["POST", "GET"])
def gen_report():
    global date
    data, un = available_slots()
    if request.method == "GET":
        if request.args.get('op_dates'):

            return render_template('report_date_view.html')
        elif request.args.get('op_sess'):
            return render_template("report_sess_view.html", data=data, slots=un)

        elif request.args.get('op_staffs'):
            return render_template("staff_duty_id.html")

    return render_template("report_options.html")


dont_reset_op = ""


@app.route('/modify')
def modify():
    global dont_reset_op
    if request.method == "GET":
        if request.args.get('mod_date'):
            return render_template("mod_date_sel.html")

        elif request.args.get('del_date'):
            return render_template("del_date_sel.html")

        elif request.args.get('del_sess'):
            data, un = available_slots()
            print("Data: ", data)
            return render_template("mod_sess_sel.html", data=data, op=dont_reset_op, datas=un)
    return render_template("modify_options.html")


@app.route('/delete_session')
def delete_session():
    global dont_reset_op
    data, un = available_slots()

    print("Data: ", data)
    if request.args.get("options"):
        dont_reset_op = request.args.get("options")

        print("Selected option: ", dont_reset_op)

    return render_template("mod_sess_sel.html", data=data, op=dont_reset_op)


@app.route('/delete_session_ext')
def delete_session_ext():
    global dont_reset_op
    data, un = available_slots_ext(fetch_latest_clg())

    print("Data: ", data)
    if request.args.get("options"):
        dont_reset_op = request.args.get("options")

        print("Selected option: ", dont_reset_op)

    return render_template("mod_sess_sel_ext.html", data=data, op=dont_reset_op)


@app.route("/del_Sess_status")
def del_Sess_status():
    global dont_reset_op
    delete_entire_session(dont_reset_op)
    return render_template("mod_sess_status.html", slot_name=dont_reset_op)


@app.route("/del_Sess_status_ext")
def del_Sess_status_ext():
    global dont_reset_op
    print("CLICKED...", dont_reset_op)
    delete_entire_session_ext(dont_reset_op, fetch_latest_clg())
    return render_template("mod_sess_status_ext.html", slot_name=dont_reset_op)


@app.route("/del_date")
def del_date():
    if request.method == "GET":
        curr_date = request.args.get('date')

        if request.args.get('submit'):
            check = delete_exam_date(curr_date)
            if check == "no date":
                return "No duties are allloted in " + curr_date

            if check == "denied":
                return "Access denied, you should be Admin or Duty Superintend to delete a date"

            if check == "updated":
                return render_template("del_status.html", date=curr_date)
        return render_template("del_date_sel.html")


@app.route("/del_date_ext")
def del_date_ext():
    if request.method == "GET":
        curr_date = request.args.get('date')

        if request.args.get('submit'):
            check = delete_exam_date_ext(curr_date)
            if check == "no date":
                return "No duties are allocated in " + curr_date

            if check == "denied":
                return "Access denied, you should be Admin or Duty Superintend to delete a date"

            if check == "updated":
                return render_template("del_status_ext.html", date=curr_date)
        return render_template("del_date_sel_ext.html")


@app.route('/change_date')
def change_date():
    if request.method == "GET":
        before = request.args.get('before')
        after = request.args.get('after')

        if request.args.get('submit'):
            chk = change_date_db(before, after)
            if chk == "Granted":
                return render_template("mod_status.html", before=before, after=after)
            else:
                return "Cannot Override an existing date in which exam duty is alloted..."


@app.route('/change_date_ext')
def change_date_ext():
    if request.method == "GET":
        before = request.args.get('before')
        after = request.args.get('after')

        if request.args.get('submit'):
            chk = change_date_db_ext(before, after)
            if chk == "Granted":
                return render_template("mod_status_ext.html", before=before, after=after)
            else:
                return "Cannot Override an existing date in which exam duty is alloted..."


@app.route("/ext_duty")
def ext_duty():
    global auth_lst, all_files
    if request.args.get("ex_file_sel"):
        update_file_cookie(request.args.get("files"), "ins")
        return render_template("ext_duty_main.html", username=operate_user_cookie("fetch"),
                               file=update_file_cookie(request.args.get("files"), "fetch"),
                               files=all_files, sel_file=request.args.get("files"))

    return render_template("ext_duty_main.html", username=operate_user_cookie("fetch"),
                           file=update_file_cookie(request.args.get("files"), "fetch"), files=all_files)


@app.route("/Add_college")
def Add_college():
    if request.method == "GET":
        if request.args.get("confirm"):
            clg_name = request.args.get('clg_name')
            cs_name = request.args.get('cs_name')
            c_code = request.args.get('c_code')
            cs_phone = request.args.get('cs_phone')
            cs_ll = request.args.get('cs_ll')
            cs_email = request.args.get('cs_email')

            add_college_to_db(clg_name, c_code, cs_name, cs_phone, cs_ll, cs_email)
    main_, sub = extract_clg()
    return render_template("add_college.html", data=main_)


clg_name = extract_ext_clg_cookie()


@app.route("/slot_sel_ext")
def slot_sel_ext():
    global clg_name
    print("Im here")
    data, un = available_slots_ext(clg_name)
    print("data: ", data, un)
    op = ""

    if request.args.get("options"):
        print("COOKIE: ", request.args.get("options"), clg_name)
        cookie_update_ext(request.args.get("options"), clg_name)

    if request.args.get("duty"):
        print("You you")
        slot_details = ext_retrive_cookie(clg_name)
        print("Retrieved data: ", slot_details)
        return redirect(url_for("date_insert_ext", meta=clg_name, slot=slot_details))

    return render_template("phase1_slot.html", clg=clg_name, data=extract_ext_slots(clg_name), main=data)


@app.route("/ext_home", methods=["POST", "GET"])
def ext_home():
    global file, toggle, path, all_files, sel_file, clg_name

    dates = fetch_exam_dates()
    data = ext_retrive_cookie(clg_name)
    data_dict = initialise_dict_da(dates)
    print("DD before: ", data_dict)
    if request.method == "POST":
        dummy_sess_cnt("1", "del")

        if request.form.get("confirm"):
            print("You have clicked confirm..")
            for row in data_dict:
                get_fn = 'FN_' + row
                get_an = 'AN_' + row
                print("YOURS before: {} {}".format(get_fn, get_an))
                try:
                    FN = int(request.form.get(get_fn))
                    AN = int(request.form.get(get_an))
                except (ValueError, TypeError):
                    FN, AN = 0, 0

                print("YOURS: {} + {} = {}".format(FN, AN, FN + AN))
                session_sum = FN + AN
                dummy_sess_cnt(session_sum, "ins")
                data_dict[row] = [FN, AN, session_sum]

            """All the methods are failing, so the last option is to store the dictionary in data base and 
            then reconstruct it and display it using an iframe"""
            store_sess_sum_dict(data_dict)

            db_dict = extract_sess_sum_dict()
            delete_sess_sum_dict_ext(clg_name)
            all_duty = dummy_sess_cnt("1", "fetch")

            return render_template('ext_main.html', data=data, date=data_dict, db_dict=db_dict, total_duty=all_duty,
                                   files=all_files, sel_file=sel_file)
        if get_curr_file() is True:
            main_ob = process()

            if request.form.get('allot_duty'):  # == 'submit':
                main_ob.insert_meta(clg_name)
                main_ob.construct_dept_ext(clg_name)
                check, tot = main_ob.allot_dates_ext()

                if check == "success":
                    return redirect(url_for('success_ext'))
                else:
                    return render_template("staff_error.html", tot=str(tot))

        if request.form.get('ex_file_sel'):
            if request.form.get('files'):
                sel_file = request.form.get('files')
                print("Selected file here: ", sel_file)

                file_cookie(sel_file, toggle=1)
                db_dict = extract_sess_sum_dict()
                all_duty = dummy_sess_cnt("1", "fetch")

                if sel_file != "":
                    adv_config(path, sel_file, "ext")
                    a = process()
                    a.dept_table_creation()
                return render_template('ext_main.html', data=data, date=data_dict, db_dict=db_dict, total_duty=all_duty,
                                       files=all_files, sel_file=sel_file)

        if request.form.get('file_upload'):
            a = process()
            a.dept_table_creation()
            return redirect(url_for('ext_upload'))
        else:
            return redirect(url_for('fail'))

    all_duty = dummy_sess_cnt("1", "fetch")
    dummy_sess_cnt("1", "del")
    db_dict = extract_sess_sum_dict()
    return render_template('ext_main.html', data=data, date=data_dict, db_dict=db_dict, total_duty=all_duty,
                           files=all_files, sel_file=sel_file)


@app.route("/clg_sel")
def clg_sel():
    global clg_name
    main_, sub = extract_clg()
    if request.method == "GET":
        if request.args.get("submit"):
            clg_name = request.args.get('clg')
            return render_template("slot_creation_ext.html", clg=clg_name, data=extract_ext_slots(clg_name))
    return render_template("clg_sel.html", colleges=sub)


@app.route('/da_ext_phase1')
def da_ext_phase1():
    main_, sub = extract_clg()
    if request.method == "GET":
        if request.args.get("submit"):
            clg_name = request.args.get('clg')

            data, un = available_slots_ext(clg_name)
            print('Ext slots: ', data)
            return render_template("phase1_slot.html", clg=clg_name, data=extract_ext_slots(clg_name), main=data)

    return render_template("da_ext_phase1.html", colleges=sub)


@app.route("/get_college")
def get_college():
    main_, sub = extract_clg()
    if request.method == "GET":
        if request.args.get("submit"):
            clg_name = request.args.get('clg')

            data, un = available_slots_ext(clg_name)
            return redirect(url_for("view_options_ext"))

    return render_template("clg_for_display.html", colleges=sub)


@app.route("/get_college_report")
def get_college_report():
    main_, sub = extract_clg()
    if request.method == "GET":
        if request.args.get("submit"):
            clg_name = request.args.get('clg')

            data, un = available_slots_ext(clg_name)
            return redirect(url_for("gen_report_ext"))

    return render_template("clg_for_report.html", colleges=sub)


@app.route("/gen_report_ext", methods=["POST", "GET"])
def gen_report_ext():
    global date
    data, un = available_slots_ext(fetch_latest_clg())
    if request.method == "GET":
        if request.args.get('op_dates'):
            return render_template('report_date_view_ext.html')
        elif request.args.get('op_sess'):
            return render_template("report_sess_view_ext.html", data=data, slots=un)

        elif request.args.get('op_staffs'):
            return render_template("staff_duty_id_ext.html")

    return render_template("report_options_ext.html", clg=fetch_latest_clg())


@app.route("/view_options_ext", methods=['POST', 'GET'])
def view_options_ext():
    try:
        data, un = available_slots_ext(fetch_latest_clg())
        if request.method == "GET":
            if request.args.get('op_dates'):
                return render_template('sel_date_view_ext.html')
            elif request.args.get('op_sess'):
                print("Data: ", data, un)
                return render_template("sel_sess_view_ext.html", data=data, slots=un)

        return render_template("view_options_ext.html", clg=fetch_latest_clg())
    except TypeError:
        return "no duties is alloted..."


@app.route("/ext_slot", methods=["POST", "GET"])
def ext_slot():
    global clg_name
    start_Date = request.form.get('start')
    end_Date = request.form.get('end')
    session = request.form.get('session')

    d_lst = [start_Date, end_Date, session.upper(), clg_name]
    slot_num = web_input_slot_ext(d_lst, clg_name)

    return render_template('slot_status.html', output=slot_num)


@app.route("/date_insert_ext")
def date_insert_ext():
    global len_date_list, all_files, clg_name
    data = ext_retrive_cookie(clg_name)
    if request.args.get('date'):
        update_temp_dates(request.args.get('date'))
        return render_template("ext_duty_dates_input.html", data=fetch_temp_dates(), meta=clg_name, slot=data)

    if request.args.get('reset'):
        reset_dates()

    if request.args.get('confirm'):
        print("Now confirmed...")
        delete_old_dates()
        dates = fetch_exam_dates()
        print("Dates in DB: ", dates)
        len_date_list = len(dates)
        exam_dates_out(dates)

        # print("INI: ", initialise_dict_da(dates))
        # db_dict = initialise_dict_da(dates)
        # store_sess_sum_dict(initialise_dict_da(dates))

        db_dict = extract_sess_sum_dict()
        print("DB_dict: ", db_dict)
        delete_sess_sum_dict_ext(clg_name)
        return render_template('ext_main.html', data=data, date=dates, db_dict=db_dict, files=all_files, sel_file="")

    return render_template("ext_duty_dates_input.html", meta=clg_name, slot=data)


@app.route('/modify_ext')
def modify_ext():
    print("in modify ext")
    global dont_reset_op
    if request.method == "GET":
        if request.args.get('mod_date'):
            print("You have clicked mod date in external")
            return render_template("mod_date_sel_ext.html")

        elif request.args.get('del_date'):
            return render_template("del_date_sel_ext.html")

        elif request.args.get('del_sess'):
            data, un = available_slots_ext(fetch_latest_clg())
            print("Data: ", data)
            return render_template("mod_sess_sel_ext.html", data=data, op=dont_reset_op, datas=un)
    return render_template("modify_options_ext.html")


@app.route("/get_college_modify")
def get_college_modify():
    main_, sub = extract_clg()
    if request.method == "GET":
        if request.args.get("submit"):
            clg_name = request.args.get('clg')

            data, un = available_slots_ext(clg_name)
            return redirect(url_for("modify_ext"))

    return render_template("clg_for_modify.html", colleges=sub)


if __name__ == "__main__":
    app.run(debug=True)
