from flask import Flask, render_template, request
import psycopg2
from datetime import datetime, timedelta

app = Flask(__name__)

dbCreds = 'dbname=postgres user=test password=Mandatory1 host=localhost';

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/addcustomer', methods=['POST'])
def addCustomer():
    ID = request.form['ID']
    name = request.form['name']
    email = request.form['email']

@app.route('/addticket', methods=['POST'])
def addticket():
    ID = request.form['ID']
    problem = request.form['problem']
    priority = request.form['priority']
    cusID = request.form['cusID']
    prodID = request.form['prodID']

@app.route('/addupdate', methods=['POST'])
def addupdate():
    ID = request.form['ID']
    message = request.form['message']
    tikID = request.form['tikID']
    StaffID = request.form['StaffID']

@app.route('/listopenticks', methods=['POST'])
def listopenticks():

@app.route('/closeTick', methods=['POST'])
def closeTick():
    ID = request.form['ID']

@app.route('/getmessages', methods=['POST'])
def getmessages():
    ID = request.form['ID']

@app.route('/getreport', methods=['POST'])
def getreport():

@app.route('/closeOld', methods=['POST'])
def closeOld():

@app.route('/delCus', methods=['POST'])
def delCus():
        ID = request.form['ID']


def insertCus(ID, name, email):
    conn = psycopg2.connect(dbCreds);
    cur = conn.cursor();
    cur.execute('INSERT INTO Customer VALUES (%s, %s, %s)', (ID, name, email));
    conn.commit();
    cur.close()
    conn.close();

def insertTick(TicketID, Problem, Priority, CustomerID, ProductID):
    conn = psycopg2.connect(dbCreds);
    cur = conn.cursor();
    cur.execute('INSERT INTO Ticket(TicketID, Problem, Priority, LoggedTime, CustomerID, ProductID) VALUES (%s, %s, %s, NOW(), %s, %s)', (TicketID, Problem, Priority, CustomerID, ProductID));
    conn.commit();
    cur.close()
    conn.close();

def insertTickUp(ID, message, updateTime, ticketID, staffID):
    conn = psycopg2.connect(dbCreds);
    cur = conn.cursor();
    cur.execute('INSERT INTO TicketUpdate VALUES(%s, %s, %s, %s, %s)', (ID, message, updateTime, ticketID, staffID));
    conn.commit();
    cur.close()
    conn.close();

def viewOpenTicks():
    conn = psycopg2.connect(dbCreds);
    cur = conn.cursor();
    cur.execute("SELECT Ticket.*, MAX(TicketUpdate.UpdateTime) AS 'Last Update' From Ticket, TicketUpdate WHERE Ticket.Status='OPEN' and Ticket.TicketID=TicketUpdate.TicketID GROUP BY Ticket.TicketID");
    result = cur.fetchall();
    conn.commit();
    cur.close()
    conn.close();
    return result;

def closeTic(ID):
    conn = psycopg2.connect(dbCreds);
    cur = conn.cursor();
    cur.execute("UPDATE Ticket SET Status='CLOSED' WHERE TicketID=%s", (ID));
    conn.commit();
    cur.close()
    conn.close();

def getMessages(ID):
    conn = psycopg2.connect(dbCreds);
    cur = conn.cursor();
    cur.execute("SELECT Customer.Name AS 'Customer Name', Ticket.LoggedTime, Ticket.Problem, Staff.Name AS 'Staff Name', TicketUpdate.UpdateTime, TicketUpdate.Message From Customer, Ticket, Staff, TicketUpdate Where Ticket.TicketID=%s AND  TicketUpdate.TicketID=Ticket.TicketID AND Ticket.CustomerID=Customer.CustomerID AND TicketUpdate.StaffID=Staff.StaffID ORDER BY TicketUpdate.UpdateTime ASC", (ID));
    result = cur.fetchall();
    conn.commit();
    cur.close()
    conn.close();
    return result;

def getClosedReports():
    conn = psycopg2.connect(dbCreds);
    cur = conn.cursor();
    cur.execute("SELECT Ticket.TicketID, COUNT(TicketUpdate.TIcketID) AS 'Updates', DATEDIFF(MIN(TicketUpdate.UpdateTime), Ticket.LoggedTime) AS 'Time Before First Response', DATEDIFF(MAX(TicketUpdate.UpdateTime), Ticket.LoggedTime) AS 'Time Before Last Response' FROM Ticket, TicketUpdate WHERE Ticket.Status='CLOSED' AND Ticket.TicketID=TicketUpdate.TicketID GROUP BY Ticket.TicketID");
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
  SELECT TicketUpdate.TicketID, DATEDIFF(NOW(), MAX(TicketUpdate.UpdateTime)) AS 'AGE'
  FROM TicketUpdate
  GROUP BY TicketUpdate.TicketID
  HAVING DATEDIFF(NOW(), MAX(TicketUpdate.UpdateTime))>1
) tn
) AND Ticket.TicketID IN (
  SELECT tm.TicketID FROM(
    SELECT TicketUpdate.TicketID, TicketUpdate.StaffID, TicketUpdate.UpdateTime
    FROM TicketUpdate
    INNER JOIN(
      SELECT TicketUpdate.TicketID, MAX(TicketUpdate.UpdateTime) AS 'lastDate'
      FROM TicketUpdate
      GROUP BY TicketUpdate.TicketID
    ) t ON t.TicketID = TicketUpdate.TicketID AND t.lastDate=TicketUpdate.UpdateTime
    WHERE TicketUpdate.StaffID IS NOT NULL
  ) tm
)""");
    conn.commit();
    cur.close()
    conn.close();

def delCus(ID):
    conn = psycopg2.connect(dbCreds);
    cur = conn.cursor();
    cur.execute("DELETE FROM Customer WHERE CustomerID=%s AND CustomerID NOT IN( SELECT DISTINCT Ticket.CustomerID FROM Ticket)", (ID));
    conn.commit();
    cur.close()
    conn.close();


if __name__ == '__main__':
    app.run(debug=True)
