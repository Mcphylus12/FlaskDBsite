from flask import Flask, render_template, request
import psycopg2
from datetime import datetime, timedelta

app = Flask(__name__)

dbCreds = 'dbname= user= password= host= port=';

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/addcustomer', methods=['POST'])
def addCustomer():
    ID = int(request.form['ID'])
    name = request.form['name']
    email = request.form['email']
    insertCus(ID, name, email)
    return render_template('home.html')

@app.route('/addticket', methods=['POST'])
def addticket():
    ID = int(request.form['ID'])
    problem = request.form['problem']
    priority = int(request.form['priority'])
    cusID = int(request.form['cusID'])
    prodID = int(request.form['prodID'])
    insertTick(ID, problem, priority, cusID, prodID)
    return render_template('results.html', title='Added Ticket', headings=['ID', 'problem', 'priority', 'Customer ID', 'Product Id'], results=[[ID, problem, priority, cusID, prodID]])

@app.route('/addupdate', methods=['POST'])
def addupdate():
    ID = int(request.form['ID'])
    message = request.form['message']
    tikID = int(request.form['tikID'])
    StaffID = request.form['StaffID']
    if not StaffID.strip():
        StaffID=None
    else: StaffID = int(StaffID)
    insertTickUp(ID, message, tikID, StaffID)
    return render_template('home.html')

@app.route('/listopenticks', methods=['POST'])
def listopenticks():
    return render_template('results.html', title='Open Tickets', headings=['Ticket ID', 'Problem', 'Status', 'Priority', 'Logged Time', 'Customer ID', 'Product ID', 'Last Update'], results=viewOpenTicks())

@app.route('/closeTick', methods=['POST'])
def closeTick():
    ID = int(request.form['ID'])
    closeTic(ID)
    return render_template('home.html')

@app.route('/getmessages', methods=['POST'])
def viewmessages():
    ID = int(request.form['ID'])
    return render_template('results.html', title='Ticket Review ID=' + str(ID), headings=['Customer Name', 'Logged Time', 'Problem', 'Staff Name', 'Update Time', 'Message'], results=getMessages(ID))

@app.route('/getreport', methods=['POST'])
def getreport():
    return render_template('results.html', title='Closed Tickets', headings=['Ticket ID', '# of Updates', 'Time before First Response', 'Time before last respnse'],  results=getClosedReports())

@app.route('/closeOld', methods=['POST'])
def closeOld():
    closeOldTiks()
    return render_template('home.html')

@app.route('/delCus', methods=['POST'])
def delCus():
        ID = int(request.form['ID'])
        delCus(ID)
        return render_template('home.html')

def insertCus(ID, name, email):
    conn = psycopg2.connect(dbCreds);
    cur = conn.cursor();
    cur.execute('INSERT INTO Customer VALUES (%s, %s, %s)', [ID, name, email]);
    conn.commit();
    cur.close()
    conn.close();

def insertTick(TicketID, Problem, Priority, CustomerID, ProductID):
    conn = psycopg2.connect(dbCreds);
    cur = conn.cursor();
    cur.execute('INSERT INTO Ticket(TicketID, Problem, Priority, LoggedTime, CustomerID, ProductID) VALUES (%s, %s, %s, NOW(), %s, %s)', [TicketID, Problem, Priority, CustomerID, ProductID]);
    conn.commit();
    cur.close()
    conn.close();

def insertTickUp(ID, message, ticketID, staffID):
    conn = psycopg2.connect(dbCreds);
    cur = conn.cursor();
    cur.execute('INSERT INTO TicketUpdate VALUES(%s, %s, NOW(), %s, %s)', [ID, message, ticketID, staffID]);
    conn.commit();
    cur.close()
    conn.close();

def viewOpenTicks():
    conn = psycopg2.connect(dbCreds);
    cur = conn.cursor();
    cur.execute("""SELECT Ticket.*, MAX(TicketUpdate.UpdateTime)
    From Ticket LEFT JOIN TicketUpdate on Ticket.TicketID=TicketUpdate.TicketID
    WHERE Ticket.Status='OPEN'
    GROUP BY Ticket.TicketID""");
    result = cur.fetchall();
    conn.commit();
    cur.close()
    conn.close();
    return result;

def closeTic(ID):
    conn = psycopg2.connect(dbCreds);
    cur = conn.cursor();
    cur.execute("UPDATE Ticket SET Status='CLOSED' WHERE TicketID=%s", [ID]);
    conn.commit();
    cur.close()
    conn.close();

def getMessages(ID):
    conn = psycopg2.connect(dbCreds);
    cur = conn.cursor();
    cur.execute("SELECT Customer.Name, Ticket.LoggedTime, Ticket.Problem, Staff.Name, TicketUpdate.UpdateTime, TicketUpdate.Message From Customer, Ticket, Staff RIGHT JOIN TicketUpdate ON TicketUpdate.StaffID=Staff.StaffID Where Ticket.TicketID=%s AND  TicketUpdate.TicketID=Ticket.TicketID AND Ticket.CustomerID=Customer.CustomerID ORDER BY TicketUpdate.UpdateTime ASC", [ID]);
    result = cur.fetchall();
    conn.commit();
    cur.close()
    conn.close();
    return result;

def getClosedReports():
    conn = psycopg2.connect(dbCreds);
    cur = conn.cursor();
    cur.execute("SELECT Ticket.TicketID, COUNT(TicketUpdate.TIcketID), MIN(TicketUpdate.UpdateTime) - Ticket.LoggedTime, MAX(TicketUpdate.UpdateTime) - Ticket.LoggedTime FROM Ticket LEFT JOIN TicketUpdate on Ticket.TicketID=TicketUpdate.TicketID WHERE Ticket.Status='CLOSED' GROUP BY Ticket.TicketID");
    result = cur.fetchall();
    conn.commit();
    cur.close()
    conn.close();
    return result;

def closeOldTiks():
    conn = psycopg2.connect(dbCreds);
    cur = conn.cursor();
    cur.execute("""UPDATE Ticket
Set Status='CLOSED'
WHERE Ticket.TicketID IN (
SELECT tn.TicketID FROM(
  SELECT TicketUpdate.TicketID, (NOW() -  MAX(TicketUpdate.UpdateTime))
  FROM TicketUpdate
  GROUP BY TicketUpdate.TicketID
  HAVING (NOW() -  MAX(TicketUpdate.UpdateTime))>interval '1 day'
) tn
) AND Ticket.TicketID IN (
    SELECT TicketUpdate.TicketID
    FROM TicketUpdate
    WHERE TicketUpdate.StaffID IS NOT NULL
)""");
    conn.commit();
    cur.close()
    conn.close();

def delCus(ID):
    conn = psycopg2.connect(dbCreds);
    cur = conn.cursor();
    cur.execute("DELETE FROM Customer WHERE CustomerID=%s AND CustomerID NOT IN( SELECT DISTINCT Ticket.CustomerID FROM Ticket)", [ID]);
    conn.commit();
    cur.close()
    conn.close();


if __name__ == '__main__':
    app.run(debug=True)
