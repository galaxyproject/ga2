# ga2

## Setup

Using Node.js version `20.10.0`, run `npm install` in the root directory of the repository to install dependencies.

## Using the development server

The app can be run for development using `npm run dev`, and accessed at `http://localhost:3000`.

## Building the app locally

Run `npm run build:local` to build. The built app can be run using `npm start`, and accessed at `http://localhost:3000`.

# BRC Analytics Data Catalog

## Building the data source files

Create a Python virtual environment and install requirements:

```shell
python3 -m venv ./venv
source ./venv/bin/activate
pip install -r ./catalog-build/requirements.txt
```

Then run the script:

```shell
python3 ./catalog-build/build-files-from-ncbi.py
```

The environment can be deactivated by running `deactivate`, and re-activated by running `source ./venv/bin/activate`
again.
