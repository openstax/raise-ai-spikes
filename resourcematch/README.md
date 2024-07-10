## Resource Match

A local environment for Resource Match and can be launced as follows:

```bash
$ docker compose up -d
```

The Resource Match API development container launches uvicorn with --reload and volume mounts the code directory so file changes should get reflected without any additional steps. The API is accessible on port 8888 and docs available at [http://localhost:8888/docs](http://localhost:8888/docs).

The Resource Match API does need a dev token to invoke OpenAI. Developers can set the environment variable `OPENAI_API_KEY` in their terminal with their token value, and it will get picked up by the docker environment.

Devs can also test the deployment build of the Resource Match app / frontend by running the following:

```bash
$ RESOURCEMATCH_APP_TARGET=deploy docker compose up --build -d