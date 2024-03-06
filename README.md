# 🌱 EndangerEd Project

---

## 🗄️ Gameserver

### 🔍 Overview
Gameserver, as the name suggests, is the game server of the EndangerEd platform. It acts as the mediator between
the knowledge base and the game client, and works with the game client to manage scores and sessions. Moreover, 
the server is easily configurable through its web interface, providing a way for authorized users to edit its settings.

### 📟 Technical Details
The game server uses Django as its framework and PostgreSQL as its database.

The purpose of the server can be divided into two sections.
#### 🎲 Game Session and Score Management
Gameserver keeps track of players' session, which is a period where a game is currently ongoing. A session is created
when a player starts the game, and lasts until it is over. When the latter happens, the client submits the total
score to the server. The server then insert said score to the central scoreboard. In addition, the scoreboard data 
can be requested by the client to be displayed to the player.
#### 🙌 Mediator for the Client and the Knowledge Base 
The server provides a microgame metadata when the client requests one, so that it
can compose it into a playable experience. It does this by using of the knowledge base's API
and its own RESTful API. The process happens during a game session and can be described as follows:
1. The server receives a request for a new microgame, and starts assembling a metadata.
2. The server chooses an appropriate question.
3. The server requests data from the knowledge base based on the question.
4. The server fits the provided data into an appropriate pattern.
5. The server sends the metadata back to the client.

On top of the above features, the server also provides a web interface for managing its settings. An authorized user can add 
or edit patterns and questions using the corresponding forms.

### 📥 Installation
1. Clone the repository to your machine using the following command:
```commandline
git clone https://github.com/endangered-project/gameserver.git
```
2. Navigate to the project folder.
3. Create your own `.env` file based on the provided example.
3. Setup poetry on your machine by following the tutorial [here](https://python-poetry.org/docs/).
4. All poetry files are already provided, the only thing left is to properly setup poetry virtual environment.
5. Create a poetry virtual environment:
```commandline
poetry shell
```
6. Install dependencies:
```commandline
poetry install
```
7. The project can now be run using the following command:
```commandline
poetry run python manage.py runserver
```

### 📊 Progression
Jump to Shīdo [GitHub Project](https://github.com/orgs/endangered-project/projects/1/) ([or the old board](https://github.com/users/HelloYeew/projects/8/views/2)).

---

## 🧭 Navigation

#### &emsp;&emsp;&emsp; [📚 Shīdo - Platform's Knowledge Base](https://github.com/HelloYeew/shido)

#### &emsp;&nbsp;&nbsp; 👉 🗄️ Gameserver - Platform's Server

#### &emsp;&emsp;&nbsp;&nbsp;&nbsp; [🕹️ EndangerEd - Platform's Client](https://github.com/endangered-project/EndangerEd)



