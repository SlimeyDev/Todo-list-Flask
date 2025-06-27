# Flask Todo List App

A simple Todo web application built with **Flask** and **MongoDB** as the backend and **HTML**, **CSS** and **Java Script** for frontend.
Users can register, log in, create multiple lists, add tasks to each list, mark tasks as complete, and delete tasks or entire lists.

---

## Features

- **User Authentication:** Register and log in securely.
- **Multiple Lists:** Create, view, and delete multiple todo lists.
- **Task Management:** Add, complete, and delete tasks within each list.
- **Persistent Storage:** All data is stored in MongoDB.

---

## Getting Started

### Prerequisites

- Python 3.8+
- [MongoDB](https://www.mongodb.com/)

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/SlimeyDev/Todo-list-Flask.git
   cd Todo-list-Flask
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables:**

   Create a `.env` file in the project root with:
   ```
   MONGO_URI=your_mongodb_connection_string
   SECRETKEY=your_secret_key
   ```

4. **Run the app:**
   ```bash
   python app.py
   ```

---

## Usage

- **Register** for a new account.
- **Log In** for a existing account.
- **Create lists** in the sidebar.
- **Add tasks** to the selected list.
- **Mark tasks as complete** by checking the box.
- **Delete tasks** or **delete entire lists** (which deletes all tasks in that list).

---

## Project Structure

```
.
├── app.py
├── requirements.txt
├── templates/
│   └── todos.html
├── static/
│   └── css/
│       └── todos.css
└── ...
```