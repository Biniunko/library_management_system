# Library Management System API

This is a RESTful API built using Django and Django REST Framework to manage a library system. The API allows users to check out and return books, manage user subscriptions, and view available books. It also implements role-based access control for different types of users (Admin, Librarian, and Member).

## Features

- User registration and authentication (JWT-based login system).
- Role-based access control (Admin, Librarian, Member).
- Add, update, and delete books.
- Search books by title, author, genre, availability.
- Check out and return books.
- Subscription management for users.
- Overdue management (fines, overdue book tracking).

## Setup Instructions

Follow these steps to set up the project locally:

### 1. Clone the Repository

```bash
git clone https://github.com/Biniunko/library_management_system.git
cd library_management_system
