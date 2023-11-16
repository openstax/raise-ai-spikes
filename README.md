# RAISE AI Spikes

This repository contains spike code from AI related experimentation for the RAISE project. As such, everything here should be considered as quick and dirty prototypes created to better understand and / or demonstrate potential capabilities.

## AI Predictor

This spike entails adopting SageMaker to deploy and invoke AI models.

## Resource Match

This prototype is part of pilot work to help explore AI-enabled features for teachers.

## Development

The `docker` environment currently includes a local environment for Resource Match and can be launced as follows:

```bash
$ docker compose up -d
```

The development container launches uvicorn with --reload and volume mounts the code directory so file changes should get reflected without any additional steps. The API is accessible on port 8888 and docs available at [http://localhost:8888/docs](http://localhost:8888/docs).

The API does need a dev token to invoke OpenAI. Developers can set the environment variable `OPENAI_API_KEY` in their terminal with their token value, and it will get picked up by the docker environment.
