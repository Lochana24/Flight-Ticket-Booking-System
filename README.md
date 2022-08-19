# Flight-Ticket-Booking-System

## Status

Tech Stack:<br>
   Front-end : HTML, BootstrapCSS<br>
   Back-end  : Python Django<br>
   Database  : SQLite

Common Functionalities:
1. Register a new user.
2. Login for both user and administrator into the session.
3. Logout from the session. 

Admin Functionalities (has separate UI):
1. Add flight data with 60 seats by default.
2. View a list of avialable flights (ordered by soon to depart).
3. View comprehensive data on a single flight.<br>
   3.1. Update the flight data.<br>
   3.2. Delete the flight data (this would delete all tickets booked for that flight).
4. View all flights booked by users (ordered by recent bookings).
5. View each ticket data.<br>
   5.1. Cancel a ticket.

User Functionalities:
1. View a list of avialable flights (ordered by soon to depart).
2. View comprehensive data on a single flight.<br>
   2.1. Book tickets for a flight.
3. View a list of tickets booked (ordered by recent bookings).
4. View each ticket data.<br>
   4.1. Cancel a ticket.

Features yet to be implemented:
1. User searching for flights based on date and time.
2. Admin viewing all the bookings based on flight number and flights time.

## Instructions to Run

Pull the repository:
1. Copy the repository website link.
2. Create and open a folder in your computer.
3. Open command prompt and go to the folder directory.
4. Type the following commands:<br>
      git init<br>
      git remote add origin [url of the repository you just copied]<br>
      git pull origin main
5. Open the folder, and the contents would be there.

Install Requirements:
1. Navigate into the project folder in command prompt.
2. Execute the following:<br>
     pip3 install -r requirements.txt

Run Project:
1. Navigate into the project folder in command prompt.
2. Make migrations to create/update database:<br>
     python manage.py makemigrations<br>
     python manage.py migrate
3. View the website application by executing:<br>
     python manage.py runserver
4. Open http://127.0.0.1:8000/ in a web browser.

## Credentials

1. Admin:<br>
     username: admin<br>
     email: admin@email.com<br>
     password: admin#123

2. Test User 1<br>
     username: Test User A<br>
     password: atest#123
 
3. Test User 2<br>
     username: Test User B<br>
     password: btest#123
