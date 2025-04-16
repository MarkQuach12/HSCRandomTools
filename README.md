# HSC Random Tools

## About The Project

HSC Random Tools is a personal project I built to help NSW HSC students better understand their performance and make more informed decisions. It includes tools like a scaled mark predictor, which estimates final HSC marks using past scaling data, and a Band 6 comparison tool that lets students explore how different schools have performed across subjects and years.

Current features:
* Scaled Mark Predictor
* Band 6 School List
* More Coming Soon!

## 🔧 Built With
* [![TypeScript](https://img.shields.io/badge/TypeScript-3178C6?style=for-the-badge&logo=typescript&logoColor=white)](https://www.typescriptlang.org/)
* [![React](https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB)](https://reactjs.org/)
* [![Shadcn/ui](https://img.shields.io/badge/Shadcn%2Fui-000000?style=for-the-badge&logo=tailwindcss&logoColor=white)](https://ui.shadcn.com/)
* [![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white)](https://tailwindcss.com/)
* [![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
* [![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
* [![Vercel](https://img.shields.io/badge/Vercel-000000?style=for-the-badge&logo=vercel&logoColor=white)](https://vercel.com/)
* [![Fly.io](https://img.shields.io/badge/Fly.io-000000?style=for-the-badge&logo=flydotio&logoColor=white)](https://fly.io/)

## 🚀 Get Started

Follow these steps to run **HSC Random Tools** locally.

### 📦 Prerequisites

Make sure you have the following installed:

- [Node.js](https://nodejs.org/) (v18+ recommended)  
- [Python](https://www.python.org/downloads/) (v3.9+)  
- [pip](https://pip.pypa.io/en/stable/installation/)  
- [virtualenv](https://virtualenv.pypa.io/en/latest/installation.html) *(optional but recommended)*

---

### 🧠 Backend Setup (Flask + Python)

```bash
# Navigate to the backend folder
cd backend

# Create and activate a virtual environment (optional)
python -m venv venv
source venv/bin/activate     # On Windows: venv\Scripts\activate

# Install Python dependencies
pip install -r requirements.txt

# Run the Flask backend
flask run

```
### 🌐 Frontend Setup (React + Vite)
```bash
# Navigate to the frontend folder
cd frontend

# Install dependencies
npm install

# Run the development server
npm run dev
```

### ⚙️ Environment Variables
Create a .env file inside the frontend directory with the following content:
```bash
VITE_REACT_APP_BACKEND_URL=http://127.0.0.1:5000
```
