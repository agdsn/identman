# Identmen

This is a Software used for validating AG DSN membership IDs via a given Backend.
Its intended deployment used pycroft in order to validate the Data, but it can also use a csv as data source to compare the encrypted data to the data in the data source.

## Dev Setup requirements

- npm >= 10.9.3
- uv >= 0.8.22

## Components

Its composed out of a frontend and an api to have maximum flexibility and enable in future iot devices to validate to.

### Frontend

The frontend was written in TS with react which can be found in `frontend/`.
To run the dev deployment:

- go into `frontend/`
- `npm install`
-  if needed and just the frontend should be used set `REACT_APP_API=INSTANCE_OF_IDENTMAN_API`
- `npm run`


### API 
The API was implemented in python using FastApi webserver. Its main purpose is to send a challenge to the client before validating the data and verifying the result and decrypting the payload afterword.

To run dev deployment:

- `uv sync`
- `uv run uvicorn identman.main:app --host 0.0.0.0 --port 5000`

#### Endpoints

- GET: `/api?query=str`  -> sets a cookie and returns a challenge for the for the given query 
- POST: `/api/challenge` -> returns decrypted data