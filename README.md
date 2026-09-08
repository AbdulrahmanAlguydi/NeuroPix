# NeuroPix

NeuroPix is a web-based image editing application for standard and AI-assisted image edits.

Users can create an account, upload JPG or PNG images, apply standard edits, or use the OpenAI image-editing API. Processed images can be compared, downloaded, and managed from the Gallery.

The project uses:

- Flask for the backend and web server
- MySQL for users and image metadata
- Amazon S3 for original and processed image files
- OpenAI image editing for AI edits

## Project layout

```text
app.py                         Flask routes and application setup
database/                      MySQL connection, queries, and schema
services/                      Standard editing, AI editing, and image storage logic
utils/                         Shared security and S3 helpers
frontend/                      HTML pages, CSS, JavaScript, and image assets
tests/                         Automated API and security checks
tests/integration/             Real database, S3, and workflow checks
docs/                          Project documents such as the SRS and HLD
.github/workflows/deploy.yml   Automatic EC2 deployment workflow
```

## Requirements

- Python 3.9 or newer
- MySQL database
- Amazon S3 bucket
- OpenAI API key for AI editing

## Local setup

1. Install the Python packages:

   ```powershell
   pip install -r requirements.txt
   ```

2. Copy `.env.example` to `.env` and fill in the database, S3, Flask, and OpenAI values. The `.env` file is ignored by Git and must not be committed.

   On PowerShell:

   ```powershell
   Copy-Item .env.example .env
   ```

3. Start the application:

   ```powershell
   python app.py
   ```

4. Open [http://127.0.0.1:5000](http://127.0.0.1:5000) in a browser.

For detailed local error messages and automatic reloads, use Flask's development option instead:

```powershell
python -m flask --app app run --debug
```

## Demo account

The deployed demo includes a shared account for testing:

- Username: `123`
- Password: `12345678`

This is a normal user account with test data.

## Database setup

Run `database/schema.sql` against MySQL to create the database and tables. The integration scripts can be used when test records are needed.

## Basic checks

Run the automated checks with:

```powershell
python -m pytest -q
```

To check that the Python files compile:

```powershell
python -m compileall -q app.py database services utils
```

The database, S3, and full workflow checks are separate integration scripts because they use the real services. They create temporary test data and clean it up when they finish. Run them from the project root only when those services are available:

```powershell
python tests/integration/test_db.py
python tests/integration/test_s3.py
python tests/integration/test_workflow.py
```

## Deployment

The demo is hosted on an Amazon Linux 2023 EC2 instance. Nginx receives web traffic and forwards it to the Flask service on port 5000. Certbot provides HTTPS for `neuropix.me`.

Open the deployed website at [https://neuropix.me/](https://neuropix.me/).

The EC2 instance runs the app through the `neuropix` systemd service. A self-hosted GitHub Actions runner is also installed on the instance.

After the deployment workflow has been set up, pushing to `main` deploys the latest version automatically:

```powershell
git push origin main
```

The workflow pulls the latest code, installs the requirements, restarts the service, and checks:

```text
https://neuropix.me/health
```

If a manual deployment is needed, run these commands on EC2:

```bash
cd /home/ec2-user/NeuroPix
git pull --ff-only origin main
python3 -m pip install --user -r requirements.txt
sudo systemctl restart neuropix
curl https://neuropix.me/health
```

The EC2 `.env` file and GitHub runner credentials stay on the server and must never be added to the repository.

## Current project limits

- AI editing is handled through the OpenAI API.
- Images are limited to 1920 × 1080 landscape or 1080 × 1920 portrait dimensions.
