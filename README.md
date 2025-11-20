
# My Banking System App [Demo]

A functional CRUD application that simulates a simple banking system using an SQLite database.

## 🎯 Problem Description

Databases are essential in modern application development, especially for systems that require persistent storage to retrieve information or restore state across multiple sessions.

## 🛠️ Proposed Solution
To demonstrate my ability and knowledge to build Python applications integrated with SQLite, I developed a fully functional application based on one of the most common real-world scenarios requiring CRUD operations: a basic banking system.  
The app showcases the four fundamental database operations—create, read, update, and delete—through an intuitive interface and practical use cases.

## ✨ Main Results

A complete and fully functional application was developed, featuring smooth interface transitions, proper system validations, and the essential operations found in a real banking environment:

- User registration, personalized dashboards, and account overviews.
- Deposits, withdrawals, and transfers, each with proper validation.
- A single database containing three well-structured tables: users, bank accounts, and transaction history.
- Validation rules, such as preventing duplicate Login IDs, disallowing insufficient-balance withdrawals, and enforcing valid input amounts.
- Automatic transaction logging, including timestamps for each operation.
- Multi-platform approach: the application is fully operational on both desktop and mobile devices (assuming proper compilation for the target platform).

## 📸 Visual Overview

### User Login Screen

To access their account dashboard, users must enter a valid Login ID and password. New users may register quickly through a simple form that collects their essential information.

<div style="display: flex; justify-content: center; gap: 20px;">
  <img src="/docs/Screenshot_login_phone.jpg" alt="Login Screen" width="20%">
  <img src="/docs/Screenshot_credentials.jpg" alt="Login with credentials" width="20%">
</div>

### Registration Screen

The registration screen ensures all fields are completed and verifies that the chosen Login ID is unique. If the ID is already in use, the system displays a warning and prevents the user from proceeding until a valid, unused ID is provided.

<img src="/docs/Screenshot_registrationscreen_phone.jpg" alt="Registration Screen" width="20%">

### Dashboard Screen

Once logged in, users are presented with their name, account balance, and full transaction history, listed from most recent to oldest.  
Color coding provides clarity: red for negative amounts (withdrawals or outgoing transfers), blue for positive amounts (deposits or incoming transfers).  
All transactions follow the necessary rules: deposits must be positive, and withdrawals or transfers cannot exceed the available balance. Operations update the database and display immediately. Transfers require selecting a registered recipient from a list, simulating stored contacts and avoiding manual entry of account numbers (for greater ease).

<div style="display: flex; justify-content: center; gap: 20px;">
  <img src="/docs/Screenshot_dashboard.jpg" alt="Dashboard Screen" width="20%">
  <img src="/docs/Screenshot_dashboard_after_deposit.jpg" alt="Dashboard after deposit" width="20%">
  <img src="/docs/Screenshot_withdrw_panel.jpg" alt="Withdraw panel" width="20%">
</div>
<div style="display: flex; justify-content: center; gap: 20px;">
  <img src="/docs/Screenshot_transactionscreen_1.jpg" alt="Transaction Screen 1" width="20%">
  <img src="/docs/Screenshot_transactionscreen_2.jpg" alt="Transaction Screen 2" width="20%">
  <img src="/docs/Screenshot_dashboard_final.jpg" alt="Dashboard after a few operations" width="20%">
</div>

As expected, the other user sees a positive balance from from the transfer:
<img src="/docs/Screenshot_dashboard_other_user.jpg" alt="Dashboard from other user" width="20%">

### Database Records Screen

As an additional feature, a small, discreet button on the bottom left corner of the login screen provides access to a table viewer showing the contents of all database tables. This tool is primarily intended to help visualize the stored records during development or testing.

<img src="/docs/Screenshot_database.jpg" alt="Database Tables viewer" width="40%">




## 📁 Project Structure

```
main/
├── images/ # Images used in README.md
├── source/ # Source codes of the project
│ ├── admin/ # Administrators program code (extended capabilities with more functions)
│ └── user/ # End users program code
└── README.md # Project overview
```

## 🧰 Technologies Used

- Dart
  - Flutter
    - Firebase
    - Firebase_ui_auth
    - Firebase_ui_oauth_google
    - Cloud_firestore
    - Calendar

      
















my banking system app
En edición...

<img src="/docs/Captura de pantalla 2025-11-20 023959.png" alt="" width="25%">
<img src="/docs/Captura de pantalla 2025-11-20 024054.png" alt="" width="25%">
<img src="/docs/Captura de pantalla 2025-11-20 024113.png" alt="" width="25%">
<img src="/docs/Captura de pantalla 2025-11-20 024141.png" alt="" width="25%">
<img src="/docs/Captura de pantalla 2025-11-20 024206.png" alt="" width="25%">
