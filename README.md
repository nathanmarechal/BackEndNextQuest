🎮 NextQuest · Backend
Discover your next game.
The API behind NextQuest: game discovery, personalized recommendations, reviews, live streams, and a conversational assistant.

Python · FastAPI · SQLAlchemy · MariaDB · LightFM

Explore NextQuest · Getting started · API overview · Roadmap
</div>About
NextQuest helps players find video games that match their interests. Its backend connects a game catalog, a hybrid recommendation engine, player reviews, Twitch live streams, and a conversational assistant through a FastAPI application.

This repository covers the server side of the platform. The web interface is built separately with Vue.js and Vuetify.
Documentation status: This README is based on the project's documented implementation. Repository-specific configuration, request schemas, and startup details should be checked against the current source code before publishing.

Features
Feature	What it brings
🎯 Personalized recommendations	Game suggestions powered by a LightFM hybrid recommendation model.
🕹️ Game catalog	Game information used by the discovery interface and recommendation workflow.
💬 Reviews	API routes supporting the platform's review features.
📺 Twitch integration	Live-stream discovery for a selected game.
✨ NextQuest Assistant	A conversational endpoint used by the frontend assistant.
🔌 Web API	A FastAPI backend connecting the frontend, database, and recommendation components.


Technology
Layer	Technology	Role
Language	Python	Application logic and recommendation components
API framework	FastAPI	HTTP routing and request handling
Application server	Uvicorn	ASGI application server
Database access	SQLAlchemy + PyMySQL	Relational database access
Database	MariaDB / MySQL	Persistent application data
Recommendation	LightFM with WARP loss	Hybrid ranking model
Live content	Twitch integration	Game-related live streams
Deployment	Ubuntu, Nginx, systemd, Certbot	Process management, reverse proxy, and HTTPS


Recommendation engine
NextQuest uses LightFM with the WARP ranking objective to generate game recommendations. Its hybrid approach combines interaction information with game metadata.

The project's recommendation features include:
- Genres and themes
- Game modes and player perspectives
- Release year
- Game ratings
WARP stands for Weighted Approximate-Rank Pairwise. The model produces a ranking of candidate games; these ranking scores should not be interpreted as probabilities.

The API layer exposes recommendations to the frontend. Model artifacts and any required feature mappings must be available in the locations expected by the application.
Getting started
1. Prepare the environment
The project has previously used Python 3.10 and a Conda environment named nextquest. From the repository root, create the environment using the supplied environment definition:
conda env create -f environment.yml
conda activate nextquest
If environment.yml declares a different environment name, use that name when activating it.
LightFM includes compiled components. Use the project's dependency definition as the starting point, especially on Windows, where a direct pip installation may require additional build tools.

2. Configure the application
Before launching the API, check the current source code for the exact configuration names and loading mechanism.
Component	Configuration to check
Database	SQLAlchemy connection URL, database name, and credentials; previously configured in database.py
Recommendation engine	Model artifact locations, feature mappings, and any required local data
Twitch	Credentials and token configuration used by the integration
Assistant	Provider or service configuration used by the assistant route
Frontend access	CORS origins matching the frontend development or deployment URL


Provision the database and load any required catalog data using the workflow provided by the repository. This README does not assume that starting the API automatically creates the schema or imports data.

Keep credentials outside version control. If the application supports environment-based configuration, provide only placeholder values in an .env.example file.
3. Start the development server
The previously documented entry point is main.py, exposing an ASGI application named app:
python -m uvicorn main:app --reload
The local server is then available at:
http://127.0.0.1:8000
Confirm the entry point against the current repository if the application has since been reorganized.
4. Explore the API
With FastAPI's default documentation settings enabled:
Interface	Local URL
Swagger UI	http://127.0.0.1:8000/docs
ReDoc	http://127.0.0.1:8000/redoc
OpenAPI schema	http://127.0.0.1:8000/openapi.json


Use the generated API documentation to inspect the current HTTP methods, parameters, request bodies, and response schemas.
API overview
The following route paths have been documented for the project. Check the running API's OpenAPI schema for their current contracts.
Route	Purpose
/games	Access the game catalog
/recommendation	Request game recommendations
/review	Work with game reviews
/twitch/live/{game_name}	Find live streams associated with a game
/assistant/chat	Interact with the NextQuest assistant


The deployment uses an Nginx reverse proxy with an /api/ prefix. Local application paths and externally exposed paths may therefore differ depending on the proxy configuration.
Deployment
The documented production setup runs the API on an Ubuntu VPS:
- Uvicorn serves the FastAPI application.
- systemd manages the backend process.
- Nginx acts as the reverse proxy.
- Certbot manages HTTPS certificates.
- MariaDB stores relational application data.
The backend service has been registered as nextquest-api.service. On a server using that configuration:
# Inspect the service
sudo systemctl status nextquest-api --no-pager

# Restart after a deployment or configuration change
sudo systemctl restart nextquest-api

# Follow application logs
sudo journalctl -u nextquest-api -f
Use development auto-reload only for local work. Check the server's actual service definition, working directory, and proxy configuration when deploying.
Data and credentials
Game metadata used by the project comes from IGDB. The project has also explored review data from Kaggle.

External datasets, artwork, and API responses remain subject to their respective terms. A license covering this repository's code does not automatically cover those materials.

For a public repository:
- Exclude passwords, API keys, access tokens, private keys, and local credential files.
- Use synthetic examples when documenting user interactions or reviews.
- Check that any included datasets and model artifacts can be redistributed.
- If a credential was committed, revoke it and address its presence in Git history.
Proposed roadmap
The following items are suggested next steps, to be reviewed against the current implementation before becoming committed project plans.
- [ ] Document all route contracts with example requests and responses.
- [ ] Provide a reproducible local setup with safe configuration examples.
- [ ] Improve catalog search, filtering, and pagination.
- [ ] Add integration tests for the catalog, review, and recommendation routes.
- [ ] Improve error handling for unavailable external services.
- [ ] Document database initialization and schema changes.
- [ ] Add health checks and clearer operational logging.
- [ ] Automate dependency checks and application validation in CI.
Contributing
Before proposing a change, open an issue describing the problem or feature and the expected behavior.

Keep pull requests focused, document configuration changes, and explain how the change was verified. Use synthetic data in examples and tests.
License
The applicable code license must be stated in a root-level LICENSE file. Check that file for the terms governing use, modification, and redistribution.

Before publishing: replace this paragraph with the actual license name and a link to LICENSE once the repository's license has been confirmed.
<div align="center">NextQuest — Find your next adventure.
</div>
