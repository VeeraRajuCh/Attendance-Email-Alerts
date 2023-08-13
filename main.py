from flask import Flask, jsonify
import pandas as pd
import yagmail
from flask_mail import Mail, Message
app = Flask(__name__)

# Initialize Flask-Mail
mail = Mail(app)


# Define the send_email function using Yagmail
def send_email(to, subject, body):
    yag = yagmail.SMTP('leavesystems@admin.com', 'leavesystemsadminpassword')
    yag.send(to=to, subject=subject, contents=body)


# Define a route to send absentee notification emails
@app.route('/send_emails', methods=['GET'])
def send_emails():
    # Read the Excel file containing employee data
    excel_file = 'C:\\Users\\innovius\\Downloads\\Employee.xlsx'
    df = pd.read_excel(excel_file)

    # Templates for candidate and employer emails
    candidate_template = """
       Hi {{name}},
       This email is to inform you that according to our attendance records, you are absent from your duties
       for {{absence_days}} days. Please apply for leave.
       Thanks,
       HR Team
       """

    employer_template = """
       Hi,
       This email is to inform you that according to attendance records, {{name}} did not attend to the duties for {{absence_days}} days.
       Thanks,
       HR Team
       """

    candidates_absent = df[df['Attendance'] == 'A']

    for index, row in candidates_absent.iterrows():
        # Calculate the number of absence days for each employee
        absence_days = sum(candidates_absent['E.name'] == row['E.name'])

        if absence_days <= 2:
            # Replace placeholders in the templates with actual values
            candidate_body = candidate_template.replace('{{name}}', row['E.name']).replace('{{absence_days}}',
                                                                                           str(absence_days))
            send_email('employeename@mantra.com', 'Absentee Notification', candidate_body)
            print(candidate_body)
            return jsonify({'message': 'Emails sent successfully'})

        else:

            employer_body = employer_template.replace('{{name}}', row['E.name']).replace('{{absence_days}}',
                                                                                             str(absence_days))
            candidate_body = candidate_template.replace('{{name}}', row['E.name']).replace('{{absence_days}}',
                                                                                               str(absence_days))
            send_email('employeename@mantra.com', 'Absentee Notification', candidate_body)
            print(candidate_body)

            send_email('humanresourcesname@mantra.com', 'Absentee Report', employer_body)
            print(employer_body)

        return jsonify({'message': 'Emails sent successfully'})


if __name__ == '__main__':
    app.run(debug=True)


