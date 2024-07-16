## AI Content Tools

The AI content tools experiments use an [Add-on for Google Docs](https://developers.google.com/workspace/add-ons/editors/docs) as part of the prototyping environment. This allows devs to focus on AI-related tinkering while incorporating a respresentative front-end content viewer / editor.

### Developer Environment setup

Google Doc Add-ons are implemented using Apps Scripts. To work with Apps Scripts, we use [clasp](https://developers.google.com/apps-script/guides/clasp). Accordingly, devs need to perform the following one-time actions to get the CLI working:

* Enable Google Apps Script API [here](https://script.google.com/home/usersettings) in your Google account
* Install and set up `clasp`:

```bash
$ npm install @google/clasp -g
$ clasp login
```

You can then create a project (you can use an alternate project name if desired):

```bash
$ clasp create --title "OpenStax (AI Spikes)" --rootDir add-on/. --type standalone
$ mv add-on/.clasp.json .
```

**NOTE:** The `mv` above is to work around [this issue](https://github.com/google/clasp/issues/869).

Once created, the project will appear in your Google Drive and can be opened / deleted there or via [https://script.google.com](https://script.google.com).

The code in `./add-on` can be pushed to the project whenever code changes are made:

```bash
$ clasp push
```

Alternatively, you can run the command in watch mode so it automatically pushes on local changes:

```bash
$ clasp push -w
```

The current code / tool functionality can then be tested from a fresh environment using the following steps:

1. Set environment variables:

```bash
$ export OPENAI_API_KEY=devkey
```

You may also optionally set environment variables for `LangSmith`:

```bash
$ export LANGCHAIN_TRACING_V2=true
$ export LANGCHAIN_API_KEY=<your-api-key>
```

2. Launch `docker compose` environment:

```bash
$ docker compose up --build -d
```

3. Download book content (replace book JSON URL as desired):

```bash
$ mkdir book-data/college-algebra-2e
$ docker compose exec contenttools-api python fetch_book.py https://openstax.org/apps/archive/20240603.181933/contents/35d7cce2-48dd-4403-b6a5-e828cb5a17da@8608bfb.json /book-data/college-algebra-2e/
```

4. Index book content:

```bash
$ docker compose exec contenttools-api python index_book.py /book-data/college-algebra-2e/
```

5. Expose your local Content Tools API on the Internet using [ngrok](https://ngrok.com/) or a similar service:

```bash
$ ngrok http http://localhost:8888
```

6. You will see a public URL displayed in your terminal after running the previous step. Modify `getApiEndpoint()` in `add-on/settings.js` to return the public URL where your API is exposed.

7. Push your code using `clasp` (skip if you enabled watch mode already):

```bash
$ clasp push
```

8. Open your Apps Script project and use [these steps](https://developers.google.com/workspace/add-ons/how-tos/testing-editor-addons) to run a test deployment with a Google doc of your choice

**NOTE:** When you navigate to `Extensions --> Apps Script name --> Open tools` the first time, you'll be asked to accept permissions. The tools should appear after you accept and attempt to open them again.
