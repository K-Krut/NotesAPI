
# Task

**Technical Assessment: AI-Enhanced Notes Management System** Your task is to develop a backend API service for a notes management system with AI capabilities. This system will allow users to create, manage, and analyze text notes while leveraging AI for enhanced functionality.

**Core Requirements**
For the Notes Management API, you should build a RESTful API using FastAPI that enables users to create, read, update, and delete notes. The system should maintain version history for each note and use SQLAlchemy for database operations. 

The AI Integration component requires you to implement note summarization functionality using either OpenAI API (please note there is no free tier) or Gemini API (which offers a free tier available at https://aistudio.google.com/).

You'll also need to create an Analytics feature with an endpoint that analyzes the notes database. This should calculate various statistics including total word count across all notes, average note length, most common words or phrases, and identify the top 3 longest and shortest notes. Use appropriate Python libraries such as NumPy, Pandas, or NLTK for this analysis.

For Testing, write comprehensive unit and integration tests using pytest. Make sure to include mocks for external API calls and achieve at least 80% test coverage for your code.

**Bonus Features (Optional)**
As optional enhancements, you may package your application using Docker for containerization, build a Vue.js frontend to visualize the analytics data, or deploy your application to a cloud platform.


**Submission Guidelines**
Please create a GitHub repository for your project and include a detailed README explaining your implementation decisions. Maintain a clean, meaningful commit history that shows your development process. Follow PEP 8 style guidelines. 

---

# Realization

## Features

- User auth with JWT tokens
- CRUD operations for notes with  version tracking
- AI summarization of notes (via OpenAI API)
- Note analytics
- Unit and integration tests

## Project Structure


```
.
├── app
│   ├── __init__.py
│   ├── auth/             # worrking with jwt (validation / generation / blacklisting) and passwords (hashing / validation)
│   ├── core/             # project configurtion 
│   ├── crud/             # users, tokens and notes models db operations
│   ├── database
│   │   ├── __init__.py   # db initialization
│   │   └── seeds/        # db seeding scripts
│   ├── main.py
│   ├── models/           # SQLAlchemy models
│   ├── routes/           # api routers
│   ├── schemas/          # pydantic schemas for request / response validation
│   ├── services/         # business logic for ai and analytics fucntional
│   └── utils/            # utils 
└── tests
    ├── __init__.py
    ├── conftest.py       # fixtures
    ├── crud/             # unit tests for crud operations
    ├── data/             # notes / users data for testing 
    ├── routes/           # integration tests for endpoints
    └── services/         # unit tests for business logic

```

---

## Implementation 

### Authentication

- Created registration / login / logout / refresh tokens functional 
- for secure used jwt tokens (it is required for all protected endpoints)
- passwords are saving in db in hashed form

### Notes & Versioning

- Only authenticated users have access for notes functional 
- Users can create / delete / list / get / update (fully / partially) notes
- Notes versions realized using parent_id and is_latest flags. While creation Note can be passed parent_id - that will mean current note is a new version of note with id = parent_id, created note will automatically be set as is_latest = True and note with id = parent_id will be updated is_latest = False
- Created also endpoint for listing note history, for it used recursive sql query
- In listing endpoint lists only user's notes and only notes where is_latest = True, bc we dont need to list previous note's versions as individual notes. also implemented pagination using offset and limit
- Notes also have summary field for saving summarized details. summary should be created with /api/ai/text/summarize endpoint. after creating suitable summary for db queries optimization note should be updated separately using one of update endpoints.
- 

### AI Integration

- Endpoint `/api/ai/text/summarize` uses OpenAI API for text summarization (can be passed any text)
- The implementation assumes that each user has a limited number of requests per month (50). and at each access to endpoints with ai integration the number of used requests is recorded. this is necessary to control the volume of requests used since the integration is paid. also in the future using this logic it is possible to connect plans for users. (it is important to note that at this stage the reset of usage counters is not implemented).

### Analytics

- All user notes are used for analysis (excluding versions, only those notes where is_latest = True). NLTK library is used for analysis. before analysis the text is processed and punctuation marks and stop words are removed. 
- Collected stats:
  - Total word count
  - Average note length
  - Most common words
  - 3 shortest and 3 longest notes

### Testing

- Integration tests for notes / auth  routes, with cases for auth, permissions, negative cases
- Unit tests for services and crud using pytest and MagicMock
- Fixtures in conftest.py for test users, notes, tokens

---

## Local Dev

1. ! Before launch please create .env file with this structure:
```
POSTGRES_DB=
POSTGRES_USER= 
POSTGRES_HOST= 
POSTGRES_PORT=
POSTGRES_PASSWORD=
  
ACCESS_TOKEN_EXPIRE=
REFRESH_TOKEN_EXPIRE=
SECRET_KEY=
  
OPENAI_API_KEY=
```
1. Install dependencies

```bash
pip install -r requirements.txt
```

2. Run the app

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

4. Run tests with coverage report

```bash
 pytest --cov=app --cov-config=.coverager --cov-report=term-missing
```

## API Endpoints

- `/docs`

- POST `/api/auth/register`
- POST `/api/auth/login`
- POST`/api/auth/logout`
- POST`/api/auth/token/refresh`

- GET `/api/notes/` 
- GET `/api/notes/stats` 
- GET `/api/notes/{id}` 
- GET `/api/notes/{id}/history` 
- POST `/api/notes/` 
- PUT `/api/notes/{id}`
- PATCH `/api/notes/{id}`
- DELETE `/api/notes/{id}`
  
- POST `/api/ai/text/summarize` 

