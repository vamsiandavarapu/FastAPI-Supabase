# AI vs Me — Week 04

As part of the Week 04 assignment, I asked an AI assistant to independently generate a FastAPI backend using Supabase Auth and PostgreSQL. I then compared the AI-generated approach with my own implementation.

## 1. Prompt Given to AI

The prompt asked the AI to build:

* Python + FastAPI backend
* Supabase Auth as the Identity Provider
* Signup, login, and logout endpoints
* Public and protected endpoints
* Bearer-token authentication
* Supabase access-token verification
* `401 Unauthorized` for missing or invalid tokens
* Reusable FastAPI authentication dependency
* Swagger Bearer authentication
* PostgreSQL Task CRUD endpoints
* Authentication protection for Task endpoints
* Environment variables for credentials
* `requirements.txt` and `.env.example`

## 2. AI vs My Implementation

| Area           | My Implementation                             | AI Implementation                                            |
| -------------- | --------------------------------------------- | ------------------------------------------------------------ |
| Architecture   | Simple `main.py` + `auth.py`                  | Multiple modules, routers, dependencies, models, and schemas |
| Database       | Direct SQL using `psycopg`                    | SQLAlchemy ORM                                               |
| Task ownership | Tasks are authenticated but not user-specific | Added `owner_id` for user-specific tasks                     |
| Token handling | FastAPI `HTTPBearer` + Supabase verification  | Explicit Bearer scheme and credential validation             |

I kept my implementation simple because SQLAlchemy and a larger modular architecture were not required for this assignment.

## 3. Token Extraction

My implementation uses FastAPI's `HTTPBearer` to extract:

```http
Authorization: Bearer <access_token>
```

The extracted token is then verified through Supabase.

The AI implementation also used `HTTPBearer` and performed more explicit checks for:

* Missing credentials
* Incorrect authentication scheme
* Empty token
* Invalid tokens

## 4. Security Review

The AI-generated code was reviewed instead of being accepted blindly.

The AI correctly used Supabase to verify the access token rather than simply decoding the JWT and trusting its contents.

The initial AI-generated logout implementation required correction because it did not properly handle the authorization information.

This showed that AI-generated authentication code must still be reviewed and tested for security.

## 5. What My Prompt Missed

The prompt did not explicitly specify:

* Exact project architecture
* Raw SQL vs ORM
* User-specific task ownership
* Exact internal organization of Python files

Because these details were not specified, the AI made its own design assumptions.

## 6. What I Learned

The comparison showed that AI can provide useful architectural ideas and accelerate backend development, but generated code should not be accepted without review.

For authentication systems, I need to verify:

* Bearer-token extraction
* Missing and invalid token handling
* Token verification
* Secret handling
* Authorization logic
* Status codes
* Actual API behavior through testing

The main lesson was that **clearer prompts produce more predictable implementations, while AI-generated security code still requires human validation.**
