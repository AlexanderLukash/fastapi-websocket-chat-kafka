# Chat Support Service

<div align="center">
<img src="https://i.postimg.cc/D0MBgjj0/Community-Cover.png">

![Python](https://img.shields.io/badge/-Python-070404?style=for-the-badge&logo=python)
![FastAPI](https://img.shields.io/badge/-Fastapi-070404?style=for-the-badge&logo=fastapi)
![Kafka](https://img.shields.io/badge/-Apachekafka-070404?style=for-the-badge&logo=apachekafka)
![MongoDB](https://img.shields.io/badge/-MongoDB-070404?style=for-the-badge&logo=mongodb)
![Docker](https://img.shields.io/badge/-Docker-070404?style=for-the-badge&logo=docker)
</div>
Chat Support Service is a service that provides an API for creating chats and real-time messaging using websockets. It allows users to interact with technical support via a web interface, and support staff to respond to requests via a Telegram bot.

## Requirements

Before using this project, make sure you have the following components installed:

- Docker
- Docker Compose
- GNU Make

## Installation and launch

1. Clone the repository:

```bush
git clone https://github.com/your_username/chat-support-api.git
```

2. Create a `.env` file based on `.env.example` and specify the necessary environment variables. 
3. Open a terminal and navigate to the project's root directory.
4. Use the command `make all` to build all Docker containers and start the project.
5. Open your browser and go to `http://localhost:8000/api/docs` to view the project.

## Implemented Commands

- `make all`: Start the project.
- `make app-logs`: Follow the logs in API container.
- `make test`: Run the test.
- `make storages`: Start MongoDB with UI on `28081` port.
- `messaging-logs`: See Kafka logs.

### The project provides UI for Apache Kafka and MongoDB:
- `http://localhost:8090/`: - UI for Apache Kafka
- `http://localhost:28081/`: - UI for MongoDB


## Contribute

If you would like to contribute to this project, please open a new Pull Request or Issue on GitHub.

## Licence

This project is distributed under the MIT license. See the LICENSE file for details.