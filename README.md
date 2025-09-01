TakeNotes – A Lightweight Note-Taking Application

This application allows users to create and store notes in a cache with a preconfigured TTL (time-to-live). Notes automatically expire, keeping your workspace clean and clutter-free – perfect for users who want a simple, disposable note-taking experience.

App demo:
![](example.gif)

Tech Stack 
* Backend: Flask (Python), Redis (for caching), PostgreSQL (for user credentials) \
* Frontend: HTML, CSS, JavaScript \
* Infrastructure: Docker, Nginx \
* Testing & API Interaction: Postman \
* Security: JWT Authentication \
* Other Integrations: CORS for cross-domain interaction


Features:

* JWT Authentication – Secure login and signup system.
* Temporary Notes – Notes are stored in Redis with TTL (expire automatically).
* User Credential Management – PostgreSQL database ensures secure storage.
* API-Driven – Fully RESTful API endpoints for frontend and external use. 
* Cross-Origin Support – CORS enabled for flexibility in client requests.
* Dockerized Setup – Seamless containerization using Docker & Docker Compose.


How to Run:

1) Clone the repository to your local machine
2) Change to the project directory
```bash
git clone https://github.com/getcerts1/TakeNote.git
cd repo
```

3) Make sure you have docker-compose installed 
4) Run the compose command to build the image and run in detached mode
```bash
docker-compose --version
docker-compose -f docker-compose.yaml up --build -d
```



Learning experience:

This has been my most challenging project yet as it required
the incorporation of many different skill sets and tools I have 
previously only worked with individually. I had to combine my flask web application
skills, psql command skills and more. This project took me a week to complete, but I 
spent most of it trying to get the nginx config file to work correctly and for the Javascript code
to correctly fetch the flask API endpoints. 

Some of the things I have learnt in this journey include

1) When using nginx as a reverse proxy to forward requests to your
flask API, you need to use the service name when compiling everything using
Docker compose. This is because nginx communicates with other services using the service name
specified in the Compose.

2) I found a neat way to initialize database tables in Postgres. You simply
create a Dockerfile pushing your init file whether it is a shell script or a
psql file to /docker-entrypoint-initdb.d. As long as your container runtime has an empty
folder at /usr/lib/postgresql/data, the initializing script will run

3) Lastly, having worked with FastAPI, the process of securing our endpoints with
jwt is so much easier using Flask in my opinion. This maybe due to me having to perform data manipulation, writing
functions to decode and encode and manually assigning secrets and algorithms for the checksum to pass.


What is next?

My goal is to now host this application on a production-grade managed cluster
such as Azure and to make this application accessible for all users. This will require me 
to leverage the tools necessary to host production-ready applications such as CI/CD, terraform, Docker registries, Kubernetes
and monitoring tools such as Prometheus and Grafana.
