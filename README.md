# Mailer-Bot

**Mailer-Bot** is a Streamlit-based application that allows professors to securely send personalized exam marks to students via email. It supports multiple exams, Gmail authentication via App Passwords, and secure storage of sensitive credentials using encryption. The backend is powered by Firebase Firestore, and the app is fully deployable on Streamlit Cloud.

---

## Features

- Gmail integration using App Passwords  
- Send marks for multiple exams in a single email  
- Secure credentials storage using Fernet encryption
- Auto-login using encrypted cookies
- Firebase Firestore backend for user data  
- Streamlit Cloud deployment for instant hosting

---

## Demo

![Screenshot Placeholder](docs/screenshot.png)  

---

## Installation (Local Development)

1. **Clone the repository**
```bash
git clone https://github.com/Aryan-Bodhe/Mailer-Bot.git
cd Mailer-Bot
````

2. **Install dependencies**

```bash
pip install -r requirements.txt
```

3. **Configure secrets**

 **Getting a Gmail App Password**
1. Enable **2-Step Verification** for your Google account.
2. Go to **[Google App Passwords](https://myaccount.google.com/apppasswords)**.
3. Generate a new password for **Mail** (or custom name).
4. Copy the 16-character password and use it in Mailer-Bot.

 **Getting a Fernet Key**
```python
from cryptography.fernet import Fernet
print(Fernet.generate_key().decode())
```

Create a `secrets.toml` file for Streamlit or `.env` for local testing:

```toml
[firebase]
serviceAccountKey = """{
  "type": "service_account",
  "project_id": "your-project-id",
  "private_key_id": "abc123...",
  "private_key": "-----BEGIN PRIVATE KEY-----\\n...\\n-----END PRIVATE KEY-----\\n",
  "client_email": "...@your-project.iam.gserviceaccount.com",
  "client_id": "...",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/..."
}"""

[fernet]
fernetKey = "YOUR_FERNET_KEY_HERE"
```

> **Note:** The `private_key` must escape `\n` as `\\n` in TOML.

---

## Usage

1. Open the app on **Streamlit Cloud** or run locally:

```bash
streamlit run app.py
```

2. **Register** with your Gmail account using an App Password.

3. **Upload** an Excel sheet containing student names, emails, and marks.

4. **Select exams** and send personalized emails with marks.

5. Monitor success and failed deliveries in the app.

---

## Project Structure

```
Mailer-Bot/
├─ app.py                  # Main Streamlit app
├─ services/
│  ├─ mailer_service.py    # Handles email sending
│  ├─ encryption_service.py # Encryption utility
│  └─ firestore_service.py  # Firebase Firestore wrapper
├─ models/
│  └─ UserCredentials.py
├─ pages/                  # Streamlit multipage files
├─ requirements.txt
├─ .env            # (Not committed, contains keys for local testing)
└─ README.md
```

---

## Contributing

1. Fork the repository
2. Create a new branch for your feature or bugfix
3. Make your changes and test locally
4. Submit a Pull Request

> Please do not commit secrets or credentials. Use `.gitignore` for `.env` and `secrets.toml`.

---

## Notes / Best Practices

* **Security:** Never expose your Firebase service account key or Fernet key.
* **Email limits:** Gmail may restrict bulk sending; use App Passwords carefully.
* **Streamlit Cloud:** Auto-deploy works with GitHub pushes if enabled.
* **Excel format:** Ensure your sheet has `Name`, `Mail`, and exam columns with marks.

---

## Contact

For any issues or questions, reach out to the author: Aryan Bodhe


