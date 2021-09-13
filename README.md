# Eve startup example

Starts a Eve's API for simple usage.

## Quick reference

- **Maintained by:** ziuloliveira@gmail.com
- **Where to learn more  about Eve:** [Eve's doc](https://docs.python-eve.org/en/stable/)


## How to use this image

`docker run --name  eve -e MONGO_URI=<mongo://uri> -e MONGO_DBNAME=<mydatabase> -p 5000:5000 eve-template`

### Enviroments Variables

- `MONGO_URI`,`MONGO_HOST`
Mongo URI. Default: `localhost`

- `MONGO_DBNAME`
Mongo database to be used. Default: `example`

- `PORT`
Port where the service will bind. Default: `5000`

- `DEBUG`
Enables debug mode. Default: `0`

- `OPLOG`
Enables oplog. Default: `1`

- `USE_AUTH`
Enables auth. Default: `0`

- `JWT_SECRET_KEY`
Secret used by JWT hash. Default: `YourSecretPassword`

-  `JWT_ALGORITHM`
Algorithm used to create JWT token. Default: `HS256`