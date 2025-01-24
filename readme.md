# ManyDaughters GitHub Pages Project

This project hosts the ManyDaughters website, which allows research teams to upload and analyze their hypothesis testing do-files. The website is built using Jekyll and deployed via GitHub Pages. The backend functionality is provided by a Python Flask application.

## Project Structure

- `.github/workflows/pages.yml`: GitHub Actions workflow for building and deploying the site.
- `backend/`: Contains the Flask application and related files.
  - `app.py`: The main Flask application file.
  - `requirements.txt`: Python dependencies for the Flask application.
  - `Readme_python.md`: Instructions for setting up and running the Flask application.
- `files/`: Directory where uploaded do-files are stored.
- `index.html`: The main landing page for the website.
- `upload.html`: The page where users can upload their do-files.
- `upload_confirmation.html`: The page that confirms successful file uploads.
- `Gemfile`: Ruby dependencies for the Jekyll site.

## Setting Up the Backend

To start the backend Flask application, follow these steps:

1. **Create Python Virtual Environment** (needed only once when the project is set up):
    ```sh
    python -m venv venv
    ```

2. **Activate Python Virtual Environment** (needed whenever a terminal session is started):
    ```sh
    cd backend
    venv\Scripts\activate
    ```

3. **Upgrade pip**:
    ```sh
    pip install --upgrade pip
    ```

4. **Install Requirements**:
    ```sh
    pip install -r requirements.txt
    ```

5. **Start the Flask Application**:
    ```sh
    python app.py
    ```

6. **Deactivate Python Virtual Environment**:
    ```sh
    deactivate
    ```

## GitHub Pages Deployment

The site is automatically built and deployed to GitHub Pages whenever changes are pushed to the `main` branch. The deployment process is defined in the [pages.yml] file.

## Uploading Files

1. Navigate to the [index.html] page.
2. Enter your Research Team ID and password to log in.
3. Upload your do-files on the [upload.html] page.
4. After successful upload, you will be redirected to the [upload_confirmation.html] page.

## Contributing

If you would like to contribute to this project, please fork the repository and submit a pull request.

## License

This project is licensed under the Creative Commons Attribution 4.0 International License. You are free to:

- Share: copy and redistribute the material in any medium or format
- Adapt: remix, transform, and build upon the material for any purpose, even commercially.

Under the following terms:

- Attribution: You must give appropriate credit, provide a link to the license, and indicate if changes were made. You may do so in any reasonable manner, but not in any way that suggests the licensor endorses you or your use.

For more details, see the [LICENSE] file.
