# Deploying IdeaFlow Backend to Render

This guide provides step-by-step instructions to deploy your FastAPI backend and MySQL database on Render.

## 1. Prepare your Database

Since you are using MySQL with `aiomysql`, you need a managed MySQL instance.

### Option A: Render Managed MySQL (Paid)
Render offers managed PostgreSQL for free, but MySQL is usually a paid service or requires a Docker image.

### Option B: Aiven / PlanetScale (External Free MySQL)
1. Sign up for [Aiven](https://aiven.io/) or [PlanetScale](https://planetscale.com/).
2. Create a MySQL database.
3. Get the connection string. It should look like:
   `mysql+aiomysql://username:password@hostname:3306/databasename`

## 2. Deploy the Backend on Render

1. **Push your code to GitHub/GitLab.**
2. **Create a new Web Service on Render:**
   - Log in to [Render Dashboard](https://dashboard.render.com/).
   - Click **New** > **Web Service**.
   - Connect your repository.
3. **Configure the Service:**
   - **Name**: `ideaflow-backend`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
4. **Add Environment Variables:**
   Click on **Environment** tab and add:
   - `DATABASE_URL`: Your MySQL connection string.
   - `SECRET_KEY`: A long random string (e.g., `openssl rand -hex 32`).
   - `GROQ_API_KEY`: Your Groq API key.
   - `MAIL_USERNAME`: Your email address.
   - `MAIL_PASSWORD`: Your email app password.
   - `MAIL_FROM`: Your email address.
   - `PROJECT_NAME`: `IdeaFlow`
5. **Add a `runtime.txt` file (Optional but recommended):**
   Ensure your backend root has a `runtime.txt` specifying the Python version (e.g., `python-3.11.0`).

## 3. Database Migrations

Since you are using Alembic, you need to run migrations. You can add this to your Build Command or run it manually.

**Updated Build Command:**
```bash
pip install -r requirements.txt && alembic upgrade head
```

## 4. CORS Setup

Remember to update the CORS settings in `app/main.py` to allow your Render frontend URL once it's deployed.

```python
# app/main.py
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://your-frontend.onrender.com"], # Update this!
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## Troubleshooting

- **Check Logs**: If the service fails to start, check the **Logs** tab in Render.
- **Port**: Render automatically sets the `PORT` environment variable. Ensure your start command uses `--port $PORT`.
- **Async MySQL**: Ensure your `DATABASE_URL` starts with `mysql+aiomysql://`.
