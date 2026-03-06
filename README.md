# FundGrow Platform Setup Instructions

## Requirements

- **Python 3.8+**
- **XAMPP / MySQL**

## 1. Database Setup (XAMPP)

1. Start **XAMPP Control Panel** and start **Apache** and **MySQL**.
2. Open your browser and go to `http://localhost/phpmyadmin/`.
3. Create a new database named `fundgrow` OR you can import the `database.sql` provided in the project folder to structure the tables and seed default settings!
   - Alternatively, you can just create an empty database named `fundgrow` and the Flask app will automatically create the required tables on the first run.

## 2. Python Environment Setup

Open PowerShell or Command Prompt in the `d:\fundgrow` directory and run the following commands:

```bash
# 1. (Optional but recommended) Create and activate virtual environment
python -m venv venv
.\venv\Scripts\activate

# 2. Install required dependencies
pip install -r requirements.txt
```

## 3. Running the Application

Once the packages are installed and the MySQL database is running, you can start the robust Flask application via the console:

```bash
python app.py
```

The application will launch effectively at `http://localhost:5000`.

## Demo Credentials

An initial Admin account is automatically seeded within the schema whenever the application runs for the first time.

**Admin**
- **Email:** `admin@fundgrow.com`
- **Password:** `Admin@123`

You can seamlessly register as an **Investor** or a **Startup Owner** directly from the **Register** page on the platform to verify the corresponding role permissions and dashboard capabilities!
