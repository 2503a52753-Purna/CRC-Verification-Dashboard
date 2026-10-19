# How to Publish "Attendance CRC Dashboard" on PythonAnywhere

This guide provides the exact 3-minute steps to host your **Attendance CRC Dashboard** permanently on **PythonAnywhere**.

---

## ⚠️ Important Note on PythonAnywhere URLs
On PythonAnywhere, free tier websites take the URL:
`https://<your-username>.pythonanywhere.com`

Since web URLs cannot contain spaces, to name your site **"Attendance CRC Dashboard"**, choose a username like:
* `attendance-crc-dashboard` &rarr; gives URL: **`https://attendance-crc-dashboard.pythonanywhere.com`**
* `attendancecrc` &rarr; gives URL: **`https://attendancecrc.pythonanywhere.com`**

---

## 📦 Your Ready-to-Upload Package
The deployment package is already created and waiting on your Desktop:
📁 **`Attendance_CRC_Dashboard_PythonAnywhere.zip`**  
*(Contains `flask_app.py`, `wsgi.py`, `templates/`, `static/`, and sample CSV files)*

---

## 🚀 3-Minute Deployment Steps

### Step 1: Create a Free Account
1. Go to [https://www.pythonanywhere.com](https://www.pythonanywhere.com) and click **Pricing & Signup**.
2. Create a free **"Beginner"** account.
3. Choose your username as `attendance-crc-dashboard` (or `attendancecrc`).

---

### Step 2: Upload and Unzip Your Files
1. In your PythonAnywhere dashboard, click on the **Files** tab at the top.
2. Under **Upload a file**, click **Choose file** and select:
   `Attendance_CRC_Dashboard_PythonAnywhere.zip` from your Desktop.
3. Click the yellow **Upload** button.
4. Click the link that says **Open Bash console here** on the Files page.
5. In the black console window, type this command and press Enter:
   ```bash
   unzip Attendance_CRC_Dashboard_PythonAnywhere.zip
   ```
6. Type `exit` to close the console.

---

### Step 3: Create the Web App
1. Click on the **Web** tab at the top of PythonAnywhere.
2. Click the blue **Add a new web app** button.
3. Click **Next**, then choose **Flask**.
4. Choose **Python 3.10** (or 3.11).
5. For the path to Flask app, enter:
   `/home/<your-username>/flask_app.py`
   *(Replace `<your-username>` with your actual PythonAnywhere username)*.
6. Click **Next**.
7. Once created, look for the **WSGI configuration file** link on the Web tab (it looks like `/var/www/<username>_pythonanywhere_com_wsgi.py`).
8. Click on it, delete the contents, and paste this:
   ```python
   import sys
   import os

   path = '/home/<your-username>'
   if path not in sys.path:
       sys.path.insert(0, path)

   from flask_app import app as application
   ```
   *(Replace `<your-username>` with your actual username, e.g. `attendance-crc-dashboard`)*.
9. Click the green **Save** button in the top-right corner.
10. Go back to the **Web** tab and click the big green button: **Reload <your-username>.pythonanywhere.com**.

---

### 🎉 Result
Your website is now **permanently live 24/7/365** at:
👉 **`https://attendance-crc-dashboard.pythonanywhere.com`**!
