from flask import Flask, render_template, request, redirect, url_for, flash ,session,Response
from flask_mysqldb import MySQL
from Mysql import MasterFlaskCode
import os
from werkzeug.utils import secure_filename
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Set a random secret key



mm = MasterFlaskCode()  # Ensure the class name is correct


@app.route("/")
def Home():
    return render_template("home.html")

@app.route("/About")
def About():
    return render_template("About.html")

@app.route("/Donar", methods=['GET', 'POST'])
def DonarLogin():
    error = None
    if request.method == 'POST':
        Donar_Email = request.form['email']
        password = request.form['password']

        # Query to fetch all donor details
        data = mm.select_direct_query(
            "SELECT donar_id,donar_name, donar_email, donar_image ,donar_address ,donar_password ,donar_aadhar ,donar_mobile ,gender ,donar_blood_group FROM donar WHERE donar_email = '{}' AND donar_password = '{}'".format(Donar_Email, password)
        )

        if data:
            donor_details = data[0]  # Get the first (and ideally, only) row of results
            session['donar_id'] = donor_details[0]  # Adjust according to your database structure
            session['donar_name'] = donor_details[1]  # Adjust according to your database structure
            session['donar_email'] = donor_details[2]
            session['donar_image'] = donor_details[3]
            session['donar_address'] = donor_details[4]
            session['donar_password'] = donor_details[5]
            session['donar_aadhar'] = donor_details[6]
            session['donar_mobile'] = donor_details[7]
            session['gender'] = donor_details[8]
            session['donar_blood_group'] = donor_details[9]



            return render_template('donar_dashboard.html', donor_details=donor_details)
        else:
            error = 'Invalid email or password. Please try again.'
            return render_template('DonarLogin.html', error=error)

    return render_template("DonarLogin.html")


import matplotlib.pyplot as plt
from flask import render_template, request

@app.route("/admin", methods=['GET', 'POST'])
def admin():
    error = 'Invalid Admin name and password'

    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password'].strip()

        if username == 'admin' and password == 'admin':
            data = mm.select_direct_query("SELECT * FROM admin")
            data1 = mm.select_direct_query("SELECT COUNT(*) AS total FROM donar")
            total_count = data1[0][0] if data1 else 0  
            data2 = mm.select_direct_query("SELECT COUNT(*) AS total FROM branches")
            total_count1 = data2[0][0] if data2 else 0 
            data3 = mm.select_direct_query("SELECT COUNT(*) AS total FROM recipient")
            total_count2 = data3[0][0] if data3 else 0
            data4 = mm.select_direct_query("SELECT COUNT(*) AS total FROM blood_donation_details")
            total_count3 = data4[0][0] if data4 else 0
            data5 = mm.select_direct_query("SELECT COUNT(*) AS total FROM nearby_location")
            total_count4 = data5[0][0] if data5 else 0

            # Data dictionary for charting
            data6 = {
                "Total Donors": total_count,
                "Total Branches": total_count1,
                "Total Recipients": total_count2,
                "Total Blood Donations": total_count3,
                "Total Locations": total_count4
            }

            # Create Pie Chart
            labels = list(data6.keys())
            sizes = list(data6.values())

            fig, ax = plt.subplots()
            ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
            ax.axis('equal')  # Equal aspect ratio ensures the pie chart is circular.

            # Save pie chart to a BytesIO object and convert it to base64
            img_pie = io.BytesIO()
            plt.savefig(img_pie, format='png')
            img_pie.seek(0)
            pie_chart_data = base64.b64encode(img_pie.getvalue()).decode()

            # Create Histogram
            fig, ax = plt.subplots()
            ax.bar(labels, sizes, color='green')
            ax.set_xlabel('Categories')
            ax.set_ylabel('Counts')
            ax.set_title('Distribution of Records')

            # Save histogram to a BytesIO object and convert it to base64
            img_hist = io.BytesIO()
            plt.savefig(img_hist, format='png')
            img_hist.seek(0)
            hist_chart_data = base64.b64encode(img_hist.getvalue()).decode()

            return render_template("adminHome.html", datas=data, total=total_count, total1=total_count1,
            total2=total_count2, total3=total_count3, total4=total_count4,
            data6=data6, pie_chart_data=pie_chart_data, hist_chart_data=hist_chart_data)
        else:
            return render_template("admin.html", error=error)

    return render_template("admin.html")


@app.route("/adminHome", methods=['GET', 'POST'])
def adminHome():
    # Fetch updated data to display
    data = mm.select_direct_query("SELECT * FROM admin")
    data1 = mm.select_direct_query("SELECT COUNT(*) AS total FROM donar")
    total_count = data1[0][0] if data1 else 0  
    data2 = mm.select_direct_query("SELECT COUNT(*) AS total FROM branches")
    total_count1 = data2[0][0] if data2 else 0 
    data3 = mm.select_direct_query("SELECT COUNT(*) AS total FROM recipient")
    total_count2 = data3[0][0] if data3 else 0
    data4 = mm.select_direct_query("SELECT COUNT(*) AS total FROM blood_donation_details")
    total_count3 = data4[0][0] if data4 else 0
    data5 = mm.select_direct_query("SELECT COUNT(*) AS total FROM nearby_location")
    total_count4 = data5[0][0] if data5 else 0

            # Data dictionary for charting
    data6 = {
            "Total Donors": total_count,
            "Total Branches": total_count1,
            "Total Recipients": total_count2,
            "Total Blood Donations": total_count3,
            "Total Locations": total_count4
            }

            # Create Pie Chart
    labels = list(data6.keys())
    sizes = list(data6.values())
    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
    ax.axis('equal')  # Equal aspect ratio ensures the pie chart is circular.

    # Save pie chart to a BytesIO object and convert it to base64
    img_pie = io.BytesIO()
    plt.savefig(img_pie, format='png')
    img_pie.seek(0)
    pie_chart_data = base64.b64encode(img_pie.getvalue()).decode()

            # Create Histogram
    fig, ax = plt.subplots()
    ax.bar(labels, sizes, color='green')
    ax.set_xlabel('Categories')
    ax.set_ylabel('Counts')
    ax.set_title('Distribution of Records')

            # Save histogram to a BytesIO object and convert it to base64
    img_hist = io.BytesIO()
    plt.savefig(img_hist, format='png')
    img_hist.seek(0)
    hist_chart_data = base64.b64encode(img_hist.getvalue()).decode()

    return render_template("adminHome.html",datas=data,total=total_count, total1=total_count1,
            total2=total_count2, total3=total_count3, total4=total_count4,
            data6=data6, pie_chart_data=pie_chart_data, hist_chart_data=hist_chart_data)
    
@app.route("/admin_view_donar", methods=['GET', 'POST'])
def admin_view_donar():
    # Fetch updated data to display
    data = mm.select_direct_query("SELECT * FROM donar")
    
    return render_template('admin_view_donar.html', datas=data)

@app.route('/delete_donor/<int:donor_id>', methods=['POST', 'GET'])
def delete_donor(donor_id):
    # Create the deletion query
    qry = "DELETE FROM donar WHERE donar_id = {}".format(donor_id)
    
    # Execute the deletion query
    mm.delete_direct_query(qry)  # Assuming mm.delete_direct_query handles the deletion
    
    # Redirect to the donor list page (or another relevant page)
    return redirect(url_for('admin_view_donar'))

@app.route("/admin_view_recipient", methods=['GET', 'POST'])
def admin_view_recipient():
    # Fetch updated data to display
    data = mm.select_direct_query("SELECT * FROM recipient")
    
    return render_template('admin_view_recipient.html', datas=data)



@app.route('/delete_recipient/<int:recipient_id>', methods=['POST', 'GET'])
def delete_recipient(recipient_id):
    # Create the deletion query
    qry = "DELETE FROM recipient WHERE recipient_id = {}".format(recipient_id)
    
    # Execute the deletion query
    mm.delete_direct_query(qry)  # Assuming mm.delete_direct_query handles the deletion
    
    # Redirect to the donor list page (or another relevant page)
    return redirect(url_for('admin_view_recipient'))

@app.route("/admin_view_staff", methods=['GET', 'POST'])
def admin_view_staff():
    # Fetch updated data to display
    data = mm.select_direct_query("SELECT * FROM branches")
    
    return render_template('admin_view_staff.html', datas=data)

@app.route('/delete_staff/<int:staff_id>', methods=['POST', 'GET'])
def delete_staff(staff_id):
    # Create the deletion query
    qry = "DELETE FROM branches WHERE branch_id = {}".format(staff_id)
    
    # Execute the deletion query
    mm.delete_direct_query(qry)  # Assuming mm.delete_direct_query handles the deletion
    
    # Redirect to the donor list page (or another relevant page)
    return redirect(url_for('admin_view_staff'))

@app.route("/admin_view_blood_donate", methods=['GET', 'POST'])
def admin_view_blood_donate():
    # Fetch updated data to display
    data = mm.select_direct_query("SELECT * FROM blood_donation_details")
    
    return render_template('admin_view_blood_donate.html', datas=data)

@app.route('/delete_donation/<int:donation_id>', methods=['POST', 'GET'])
def delete_donation(donation_id):
    # Create the deletion query
    qry = "DELETE FROM blood_donation_details WHERE donation_id = {}".format(donation_id)
    
    # Execute the deletion query
    mm.delete_direct_query(qry)  # Assuming mm.delete_direct_query handles the deletion
    
    # Redirect to the donor list page (or another relevant page)
    return redirect(url_for('admin_view_blood_donate'))


@app.route("/admin_view_nearby_location", methods=['GET', 'POST'])
def admin_view_nearby_location():
    # Fetch updated data to display
    data = mm.select_direct_query("SELECT * FROM nearby_location")
    
    return render_template('admin_view_nearby_location.html', datas=data)

@app.route('/delete_location/<int:Location_id>', methods=['POST', 'GET'])
def delete_location(Location_id):
    # Create the deletion query
    qry = "DELETE FROM nearby_location WHERE Location_id = {}".format(Location_id)
    
    # Execute the deletion query
    mm.delete_direct_query(qry)  # Assuming mm.delete_direct_query handles the deletion
    
    # Redirect to the donor list page (or another relevant page)
    return redirect(url_for('admin_view_nearby_location'))


@app.route("/update_location/<int:Location_id>", methods=['GET', 'POST'])
def update_location(Location_id):
    if request.method == 'POST':
        # Retrieve updated form data
        Location_name = request.form['Location_name']
        Hospital_Name = request.form['Hospital_Name']
        Hospital_contact = request.form['Hospital_contact']
        Hospital_Address = request.form['Hospital_Address']
        
        # Update the location information in the database
        qry = """
        UPDATE nearby_location 
        SET Location_name=%s, hospital_name=%s, hospital_contact=%s, location_address=%s
        WHERE Location_id=%s
        """
        values = (Location_name, Hospital_Name, Hospital_contact, Hospital_Address, Location_id)
        
        mm.Update_query(qry, values)  # Update database record
        flash("Location information updated successfully!")
        return redirect('/admin_view_nearby_location')
    
    # Fetch the current location details for display in the form
    query = "SELECT * FROM nearby_location WHERE Location_id = %s"
    location_details = mm.fetch_one(query, (Location_id,))
    
    return render_template('location_update.html', location_details=location_details)


@app.route("/add_location", methods=['GET', 'POST'])
def add_location():
    if request.method == 'POST':
        # Retrieve form data
        Location_name = request.form['Location_name']
        Hospital_Name = request.form['Hospital_Name']
        Hospital_contact = request.form['Hospital_contact']
        Hospital_Address = request.form['Hospital_Address']

        qry = """
        INSERT INTO nearby_location (Location_name, hospital_name, hospital_contact, location_address)
        VALUES (%s, %s, %s, %s)
        """
        values = (Location_name, Hospital_Name, Hospital_contact, Hospital_Address)
        
        
            # Insert the new donor
        result = mm.insert_query(qry, values)
        print(result)
        flash("Registration successful!")
        return redirect("/admin_view_nearby_location")  # Redirect to dashboard
    
    return render_template('add_location.html')


@app.route("/adminUpdate", methods=['GET', 'POST'])
def adminUpdate():
    if request.method == 'POST':
        Admin_Name = request.form['Admin_Name']
        Admin_Address = request.form['Admin_Address']
        Admin_Mobile = request.form['Admin_Mobile']
        Admin_Email = request.form['Admin_Email']
        Admin_password = request.form['Admin_password']
        f = request.files['file']
        file_path = os.path.join("static/uploads/", secure_filename(f.filename))
        f.save(file_path)
        
        maxin = mm.find_id("admin")
        qry = (
        "UPDATE admin SET "
        "Admin_Name = '{}', "
        "Admin_Address = '{}', "
        "Admin_Mobile = '{}', "
        "Admin_Email = '{}', "
        "Admin_password = '{}', "
        "Admin_File = '{}' "  # Add this line to include the filename
        "WHERE id = {}".format(
            Admin_Name,
            Admin_Address,
            Admin_Mobile,
            Admin_Email,
            Admin_password,
            secure_filename(f.filename),  # Save the filename in the database
            maxin
        )
    )

    # Execute the update query
    
        result = mm.Update_query(qry)
        print(result)

        return redirect("/adminHome")
    return render_template("AdminUpdate.html")


from pymysql.err import IntegrityError
from flask import flash, redirect, url_for, render_template

@app.route("/Donar_register", methods=['GET', 'POST'])
def Donar_register():
    if request.method == 'POST':
        # Retrieve form data
        donar_name = request.form['donar_name']
        donar_address = request.form['donar_address']
        donar_mobile = request.form['donar_mobile']
        donar_email = request.form['donar_email']
        donar_password = request.form['donar_password']
        donar_aadhar = request.form['donar_aadhar']
        donar_register_date = request.form['donar_register_date']  # Make sure this is in the correct format
        gender = request.form['gender']
        donar_blood_group = request.form['donar_blood_group']
        
        # Handle file upload
        f = request.files['file']
        file_path = os.path.join("static/uploads/", secure_filename(f.filename))
        f.save(file_path)

        # Query to check if the email already exists
        check_email_qry = "SELECT COUNT(*) FROM donar WHERE donar_email = %s"
        email_exists = mm.fetch_one(check_email_qry, (donar_email,))
        
        # If the email exists, flash an error message and redirect
        if email_exists[0] > 0:
            flash("Email already exists! Please use a different email.")
            return redirect(url_for('Donar_register'))
        
        # If the email doesn't exist, insert the new donor, including the image path
        qry = """
        INSERT INTO donar (donar_name, donar_address, donar_mobile, donar_email, donar_password, donar_aadhar, donar_register_date, gender, donar_blood_group, donar_image)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        values = (
            donar_name, donar_address, donar_mobile, donar_email, donar_password,
            donar_aadhar, donar_register_date, gender, donar_blood_group,
            secure_filename(f.filename) # Include the image path
        )
        
        try:
            # Insert the new donor
            result = mm.insert_query(qry, values)
            print(result)
            flash("Registration successful!")
            return redirect("/Donar")  # Redirect to dashboard
        
        except IntegrityError as e:
            if e.args[0] == 1062:  # Duplicate entry error code
                flash("Email already exists! Please use a different email.")
                return redirect(url_for('Donar_register'))
            else:
                flash("An error occurred during registration. Please try again.")
                return redirect(url_for('Donar_register'))
    
    return render_template('donar_register.html')


from flask import flash, redirect, render_template, request, session, url_for
from datetime import datetime

@app.route("/donar_dashboard", methods=['GET', 'POST'])
def donar_dashboard():
    qry = "SELECT * FROM donar"
    data = mm.select_direct_query(qry)
    
    return render_template('donar_dashboard.html', donors=data)



@app.route("/Blood_Donate", methods=['GET', 'POST'])
def Blood_Donate():
    usern = session.get('donar_name')
    
   
    datax = mm.select_query("SELECT * FROM donar WHERE donar_name = %s", (usern,))
    
    Donar_id = datax[0][0]
    Donar_Name = datax[0][1]
    Donar_Email = datax[0][4]
    if request.method == 'POST':
        Donar_Age = request.form['donar_age']
        Donate_Hospital = request.form['donate_hospital']
        Donate_City = request.form['donate_city']
        Donate_Date = request.form['donate_date']

        try:
            Donate_Date = datetime.strptime(Donate_Date, "%Y-%m-%d").date()
        except ValueError:
            flash("Invalid date format. Please use YYYY-MM-DD.")
            return redirect(url_for('Blood_Donate'))

        
        
        qry = """
        INSERT INTO Blood_donation_details (Donar_Id,Donar_Name, Donar_Email, Donar_Age, Donate_Hospital, Donate_City, Donate_Date)
        VALUES (%s, %s, %s, %s, %s, %s,%s)
        """
        values = (Donar_id,Donar_Name, Donar_Email, Donar_Age, Donate_Hospital, Donate_City, Donate_Date)
        
        try:
            result = mm.insert_query(qry, values)
            print(result)
            flash("Donation Information Sent Successfully!")
            return redirect(url_for('Blood_Donate_Success'))
        
        except IntegrityError:
            flash("An error occurred during registration. Please try again.")
            return redirect(url_for('Blood_Donate'))
    

    # Render the Blood Donation form template if request method is GET
    return render_template('Blood_Donate.html')



   

@app.route("/Blood_Donate_Success", methods=['GET', 'POST'])
def Blood_Donate_Success():
    
    return render_template('Blood_Donate_Success.html')
   

@app.route("/location_search", methods=['GET', 'POST'])
def location_search():
    data = None  # Initialize data to handle GET requests

    if request.method == 'POST':
        search = request.form['search']
        # Use a parameterized query to prevent SQL injection
        data = mm.select_query("SELECT * FROM Nearby_location WHERE Location_name = %s", (search,))
        
    return render_template('location_search.html', items=data)

@app.route("/donar_update/<int:donar_id>", methods=['GET', 'POST'])
def donar_update(donar_id):
    if request.method == 'POST':
        # Retrieve updated form data
        donar_name = request.form['donar_name']
        donar_address = request.form['donar_address']
        donar_mobile = request.form['donar_mobile']
        donar_email = request.form['donar_email']
        donar_password = request.form['donar_password']
        donar_aadhar = request.form['donar_aadhar']
        donar_register_date = request.form['donar_register_date']
        gender = request.form['gender']
        donar_blood_group = request.form['donar_blood_group']
        
        # Optional: handle updated file upload if needed
        f = request.files['file']
        file_path = os.path.join("static/uploads/", secure_filename(f.filename))
        f.save(file_path)
        
        # Update the donor information in the database
        qry = """
        UPDATE donar 
        SET donar_name=%s, donar_address=%s, donar_mobile=%s, donar_email=%s, 
            donar_password=%s, donar_aadhar=%s, donar_register_date=%s, 
            gender=%s, donar_blood_group=%s,donar_image=%s
        WHERE donar_id=%s
        """
        values = (
            donar_name, donar_address, donar_mobile, donar_email, donar_password,
            donar_aadhar, donar_register_date, gender, donar_blood_group,secure_filename(f.filename) ,donar_id
        )
        
        mm.Update_query(qry, values)  # Replace with actual database update function
        flash("Donor information updated successfully!")
        return redirect('/Donar')  # Redirect to the donor list page
    
    # Fetch the donor's current information for display in the update form
    query = "SELECT * FROM donar WHERE donar_id = %s"
    donor_details = mm.fetch_one(query, (donar_id,))
    
    return render_template('donar_update.html', donor_details=donor_details)



@app.route("/recipient", methods=['GET', 'POST'])
def recipient():
    data = None  # Initialize data to handle GET requests

    if request.method == 'POST':
        search = request.form['search']
        # Use a parameterized query to prevent SQL injection
        data = mm.select_query("SELECT * FROM Nearby_location WHERE Location_name = %s", (search,))
        
    return render_template('recipient.html', items=data)



@app.route("/Recipient_Register", methods=['GET', 'POST'])
def Recipient_Register():
    
    if request.method == 'POST':
        recipient_name = request.form['recipient_name']
        recipient_address = request.form['recipient_address']
        gender = request.form['gender']
        recipient_date_of_birth = request.form['recipient_date_of_birth']
        recipient_age = request.form['recipient_age']
        recipient_aadhar = request.form['recipient_aadhar']
        recipient_email = request.form['recipient_email']
        recipient_mobile = request.form['recipient_mobile']
        recipient_district = request.form['recipient_district']
        
        
        check_email_qry = "SELECT COUNT(*) FROM Recipient WHERE recipient_email = %s"
        email_exists = mm.fetch_one(check_email_qry, (recipient_email,))
        
        # If the email exists, flash an error message and redirect
        if email_exists[0] > 0:
            flash("Email already exists! Please use a different email.")
            return redirect(url_for('Recipient_Register'))
        
        # If the email doesn't exist, insert the new donor, including the image path
        qry = """
        INSERT INTO Recipient (recipient_name, recipient_address,gender,recipient_date_of_birth, recipient_age, recipient_aadhar, recipient_email, recipient_mobile, recipient_district)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        values = (
            recipient_name, recipient_address, gender, recipient_date_of_birth,recipient_age,
            recipient_aadhar, recipient_email, recipient_mobile, recipient_district
           
        )
        
        try:
            # Insert the new donor
            result = mm.insert_query(qry, values)
            print(result)
            flash("Registration successful!")
            return redirect("/recipient_success")  # Redirect to dashboard
        
        except IntegrityError as e:
            if e.args[0] == 1062:  # Duplicate entry error code
                flash("Email already exists! Please use a different email.")
                return redirect(url_for('Recipient_Register'))
            else:
                flash("An error occurred during registration. Please try again.")
                return redirect(url_for('Recipient_Register'))

    return render_template('Recipients_Register.html')


@app.route('/recipient_success')
def recipient_success():
    return render_template('recipient_success.html')



@app.route("/staff_register", methods=['GET', 'POST'])
def staff_register():
    if request.method == 'POST':
        # Retrieve form data
        branch_name = request.form['branch_name']
        staff_name = request.form['staff_name']
        staff_email = request.form['staff_email']
        staff_phone = request.form['staff_phone']
        city = request.form['city']
        password = request.form['password']
        # Handle file upload
        f = request.files['file']
        file_path = os.path.join("static/uploads/", secure_filename(f.filename))
        f.save(file_path)

        # Query to check if the email already exists
        check_email_qry = "SELECT COUNT(*) FROM branches WHERE staff_email = %s"
        email_exists = mm.fetch_one(check_email_qry, (staff_email,))
        
        # If the email exists, flash an error message and redirect
        if email_exists[0] > 0:
            flash("Email already exists! Please use a different email.")
            return redirect(url_for('staff_register'))
        
        # If the email doesn't exist, insert the new donor, including the image path
        qry = """
        INSERT INTO branches (branch_name, staff_name, staff_email, staff_phone, city, password, image)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        values = (
            branch_name,staff_name,staff_email,staff_phone,city,password,
            secure_filename(f.filename) # Include the image path
        )
        
        try:
            # Insert the new donor
            result = mm.insert_query(qry, values)
            print(result)
            flash("Registration successful!")
            return redirect("/staff_login")  # Redirect to dashboard
        
        except IntegrityError as e:
            if e.args[0] == 1062:  # Duplicate entry error code
                flash("Email already exists! Please use a different email.")
                return redirect(url_for('staff_register'))
            else:
                flash("An error occurred during registration. Please try again.")
                return redirect(url_for('staff_register'))
    
    return render_template('staff_register.html')


@app.route("/staff_login", methods=['GET', 'POST'])
def staff_login():
    error = None
    if request.method == 'POST':
        staff_Email = request.form['staff_email']
        password = request.form['password']

        # Query to fetch all donor details
        data = mm.select_direct_query(
            "SELECT branch_id,branch_name, staff_name,staff_email, staff_phone ,city , password , image  FROM branches WHERE staff_email = '{}' AND password = '{}'".format(staff_Email, password)
        )

        if data:
            staff_details = data[0]  # Get the first (and ideally, only) row of results
            session['branch_id'] = staff_details[0]  # Adjust according to your database structure
            session['branch_name'] = staff_details[1]  # Adjust according to your database structure
            session['staff_name'] = staff_details[2]
            session['staff_email'] = staff_details[3]
            session['staff_phone'] = staff_details[4]
            session['city'] = staff_details[5]
            session['password'] = staff_details[6]
            session['image'] = staff_details[7]

            return render_template('staff_dashboard.html', donor_details=staff_details)
        else:
            error = 'Invalid email or password. Please try again.'
            return render_template('staff_login.html', error=error)

    return render_template("staff_login.html")


@app.route("/recipient_information/<int:branch_id>", methods=['GET', 'POST'])
def recipient_information(branch_id):
    # Initialize data to handle both GET and POST requests
    data = []

    if request.method == 'POST':
        search = request.form['search']
        # Use a parameterized query to prevent SQL injection
        data = mm.select_query("SELECT * FROM recipient WHERE recipient_district = %s", (search,))
    else:
        # Optionally fetch all recipients for the branch if it's a GET request
        # Adjust the SQL query based on your schema
        data = mm.select_query("SELECT * FROM recipient WHERE branch_id = %s", (branch_id,))

    return render_template('recipient_information.html', donors=data)

@app.route("/Donar_information/<int:branch_id>", methods=['GET', 'POST'])
def Donar_information(branch_id):
    # Initialize data to handle both GET and POST requests
    donors = []

    if request.method == 'POST':
        search = request.form['search']
        # Use a parameterized query to prevent SQL injection
        donors = mm.select_query("SELECT * FROM donar WHERE donar_city = %s", (search,))
    else:
        # Fetch all donors for the specified branch
        donors = mm.select_query("SELECT * FROM donar WHERE branch_id = %s", (branch_id,))

    return render_template('donar_information.html', donors=donors)


@app.route("/staff_update/<int:branch_id>", methods=['GET', 'POST'])
def staff_update(branch_id):
    if request.method == 'POST':
        # Retrieve updated form data
        staff_name = request.form['staff_name']
        staff_email = request.form['staff_email']
        staff_phone = request.form['staff_phone']
        city = request.form['city']
        password = request.form['password']
        
        # Optional: handle updated file upload if needed
        f = request.files['file']
        file_path = os.path.join("static/uploads/", secure_filename(f.filename))
        f.save(file_path)
        
        # Update the donor information in the database
        qry = """
        UPDATE branches 
        SET staff_name=%s, staff_email=%s, staff_phone=%s, city=%s, 
            password=%s,image=%s
        WHERE branch_id=%s
        """
        values = (
            staff_name, staff_email, staff_phone, city, password,secure_filename(f.filename) ,branch_id
        )
        
        mm.Update_query(qry, values)  # Replace with actual database update function
        flash("staff information updated successfully!")
        return redirect('/staff_login')  # Redirect to the donor list page
    
    # Fetch the donor's current information for display in the update form
    query = "SELECT * FROM branches WHERE branch_id = %s"
    donor_details = mm.fetch_one(query, (branch_id,))
    
    return render_template('staff_update.html', donor_details=donor_details)




if __name__ == "__main__":
    app.run(debug=True, use_reloader=True)