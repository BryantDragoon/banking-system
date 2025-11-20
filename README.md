
# My Banking System App [Demo]

Demo of a functional CRUD application that simulates a banking system using an SQL database.

## 🎯 Problem Description

The use of databases is essential in the development of many applications, especially if they need to store or retain information in non-volatile memory, so they can later retrieve records or state after multiple uses.

## 🛠️ Proposed Solution

A fully functional, demonstrative application was developed to showcase my knowledge to create Python applications that integrate SQLite for data storage. The app was designed based on one of the most popular examples requiring the integration of the four fundamental database manipulation functions—create, read, update, and delete—the simulation of a banking system.

## ✨ Main Results

A fully functional application was developed, including app animations and functional basic operations like any real bank system has: users registration, a personal dashboard to deploy bank account balance and movements in the account, operations of deposits, withdraws and transferences.

- A single database containing the three tables: one for storing users, one for bank accounts, and one for all transactions.
- The app follows the minimum regulation like no repeated Login IDs, no withdrawals if not enought money, just valid amounts, etc.
- Every operations generates a transaction record with timestamp for reference
- The most important, the app was developed using a multi platform aproach, so is totally functional from pc as from a phone (asuming that the code is debidamente compilado)

## 📸 Visual Overview

### User Login Screen

- To access the dashboard and view balance and activity, the user must first log in by entering a password that matches a previously registered login ID. If the user is new and has not yet registered, they can easily do so by filling out a simple registration form with their information.

### Registration Screen

- The registration screen meets the minimum requirements of requiring all fields to be filled in, but more importantly, it checks that the chosen ID is not already in use, displaying a pop-up message that alerts the user and only allows them to proceed after entering a unique ID.

### Dashboard Screen

- Once logged in, the user can view their name, balance, and transaction history on the dashboard (from most recent to oldest). Negative balances (such as withdrawals or transfers to other users) are displayed in red, while positive balances (such as deposits or transfers) are shown in blue. Each transaction adheres to minimum requirements: deposits must be positive amounts, and withdrawals and transfers must be equal to or less than the available balance in the account. Transactions are updated and displayed on the screen immediately. Transfers are only possible if other users are registered, as they must be selected from a list (simulating and simplifying the tedious task of typing account numbers, acting instead as if they were your registered contacts).

### Database Records Screen
As an added feature, a discreet button in the lower left corner of the login screen provides access to a screen displaying the data stored in each table created in the database. This serves primarily as an aid for visualizing the records.





<img src="/images/main_page.jpeg" alt="Scheduling Main Page" width="20%">
<img src="/images/scheduled.jpeg" alt="Scheduling in a Specific Day" width="20%">
<img src="/images/scheduling form.jpeg" alt="Scheduling Form" width="20%">

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
