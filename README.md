# 🎶 Silly Song Shop

A Django web application where users can order custom, silly songs for any occasion!

## Features

- 🎵 Custom song ordering with dynamic forms
- 💳 Stripe payment integration
- 📧 Email notifications
- 🎂 Multiple occasion types (Birthday, Anniversary, Roast, etc.)
- 📱 Mobile-responsive design
- 🔧 Admin order management

## Local Development

1. **Clone the repository:**
   ```bash
   git clone https://github.com/andrewtrentor1/sillysongshop.git
   cd sillysongshop
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   Create a `.env` file with:
   ```
   SECRET_KEY=your-secret-key-here
   EMAIL_HOST_USER=your-email@gmail.com
   EMAIL_HOST_PASSWORD=your-app-password
   STRIPE_PUBLISHABLE_KEY=pk_test_...
   STRIPE_SECRET_KEY=sk_test_...
   STRIPE_WEBHOOK_SECRET=whsec_...
   ```

5. **Run migrations:**
   ```bash
   python manage.py migrate
   ```

6. **Create superuser:**
   ```bash
   python manage.py createsuperuser
   ```

7. **Run development server:**
   ```bash
   python manage.py runserver
   ```

## Production Deployment

### For VPS/Server Deployment:

1. **Set up environment variables:**
   ```bash
   export SECRET_KEY="your-production-secret-key"
   export EMAIL_HOST_USER="your-email@gmail.com"
   export EMAIL_HOST_PASSWORD="your-app-password"
   export STRIPE_PUBLISHABLE_KEY="pk_live_..."
   export STRIPE_SECRET_KEY="sk_live_..."
   export STRIPE_WEBHOOK_SECRET="whsec_..."
   export DB_NAME="sillysongshop"
   export DB_USER="postgres"
   export DB_PASSWORD="your-db-password"
   export DB_HOST="localhost"
   export DB_PORT="5432"
   ```

2. **Install PostgreSQL:**
   ```bash
   sudo apt-get update
   sudo apt-get install postgresql postgresql-contrib
   ```

3. **Create database:**
   ```bash
   sudo -u postgres createdb sillysongshop
   ```

4. **Deploy:**
   ```bash
   chmod +x deploy.sh
   ./deploy.sh
   ```

5. **Set up web server (Nginx + Gunicorn):**
   ```bash
   pip install gunicorn
   gunicorn --bind 0.0.0.0:8000 weirdsongfactory.wsgi
   ```

### For Heroku Deployment:

1. **Install Heroku CLI**
2. **Login to Heroku:**
   ```bash
   heroku login
   ```

3. **Create Heroku app:**
   ```bash
   heroku create sillysongshop
   ```

4. **Set environment variables:**
   ```bash
   heroku config:set SECRET_KEY="your-secret-key"
   heroku config:set EMAIL_HOST_USER="your-email@gmail.com"
   heroku config:set EMAIL_HOST_PASSWORD="your-app-password"
   heroku config:set STRIPE_PUBLISHABLE_KEY="pk_live_..."
   heroku config:set STRIPE_SECRET_KEY="sk_live_..."
   heroku config:set STRIPE_WEBHOOK_SECRET="whsec_..."
   ```

5. **Deploy:**
   ```bash
   git push heroku main
   heroku run python manage.py migrate
   heroku run python manage.py createsuperuser
   ```

## Domain Setup

1. **Point your domain to your server:**
   - A record: `@` → your server IP
   - CNAME: `www` → your domain

2. **Set up SSL certificate:**
   ```bash
   sudo apt-get install certbot python3-certbot-nginx
   sudo certbot --nginx -d sillysongshop.com -d www.sillysongshop.com
   ```

## Admin Access

- URL: `https://sillysongshop.com/admin-login/`
- Password: `PickleKings1425`

## File Structure

```
sillysongshop/
├── orders/                 # Main app
│   ├── models.py          # Order model
│   ├── views.py           # Views
│   ├── forms.py           # Forms
│   ├── payment_views.py   # Stripe integration
│   └── templates/         # HTML templates
├── weirdsongfactory/      # Project settings
│   ├── settings.py        # Development settings
│   ├── settings_production.py  # Production settings
│   └── wsgi.py           # WSGI configuration
├── requirements.txt       # Python dependencies
├── Procfile             # Heroku deployment
├── deploy.sh            # Deployment script
└── README.md            # This file
```

## Support

For issues or questions, please contact the development team.