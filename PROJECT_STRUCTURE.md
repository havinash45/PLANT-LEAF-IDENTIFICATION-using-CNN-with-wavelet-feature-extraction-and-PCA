# LeafAI Hub - Project Structure

```
LeafAI Hub/
│
├── backend-python/                   # Python FastAPI Backend
│   ├── app/
│   │   ├── auth/                     # Authentication & Authorization
│   │   │   ├── dependencies.py       # JWT verification & role security dependencies
│   │   │   ├── jwt_utils.py          # JWT token generation and validation (HS256)
│   │   │   └── __init__.py
│   │   ├── models/                   # Beanie ODM MongoDB Document Models
│   │   │   ├── user.py               # User accounts & roles (USER, ADMIN, RESEARCHER)
│   │   │   ├── prediction.py         # Prediction history & disease analysis
│   │   │   ├── plant.py              # Botanical metadata & plant information
│   │   │   ├── feedback.py           # Researcher feedback & corrections
│   │   │   └── __init__.py
│   │   ├── routes/                   # FastAPI APIRouters (REST Endpoints)
│   │   │   ├── auth.py               # /api/auth (register, login)
│   │   │   ├── prediction.py         # /api/predict (single & batch upload, history)
│   │   │   ├── admin.py              # /api/admin (stats, users, pagination, predictions)
│   │   │   ├── researcher.py         # /api/researcher (unverified predictions, verify)
│   │   │   └── __init__.py
│   │   ├── schemas/                  # Pydantic Schemas (Request/Response Models)
│   │   │   ├── auth.py               # Auth DTOs (LoginRequest, RegisterRequest, AuthResponse)
│   │   │   ├── prediction.py         # Prediction DTOs (PredictionResponse)
│   │   │   ├── admin.py              # Admin DTOs (AdminUserDto, UpdateRoleRequest)
│   │   │   └── __init__.py
│   │   ├── services/                 # Business Logic & Integrations
│   │   │   ├── auth_service.py       # User registration, password hashing (BCrypt), login
│   │   │   ├── prediction_service.py # Image handling, ML call, label parsing, history
│   │   │   ├── admin_service.py      # System statistics, user role updates, pagination
│   │   │   ├── file_storage.py       # UUID-based image upload storage
│   │   │   ├── ml_client.py          # Async HTTP client (httpx) for ML service inference
│   │   │   └── __init__.py
│   │   ├── config.py                 # Pydantic BaseSettings configuration (.env)
│   │   ├── database.py               # Motor async client & Beanie ODM initialization
│   │   └── __init__.py
│   ├── tests/                        # Backend Test Suite
│   │   ├── conftest.py               # Test database fixtures & async test client
│   │   ├── test_auth.py              # Authentication endpoint tests
│   │   └── __init__.py
│   ├── uploads/                      # Uploaded leaf images storage (served at /uploads)
│   ├── .env                          # Backend environment variables (PORT=8081, MongoDB, JWT)
│   ├── main.py                       # FastAPI application entry point, CORS, static files
│   └── requirements.txt              # FastAPI, Uvicorn, Motor, Beanie, PyJWT, BCrypt, etc.
│
├── frontend/                         # React Frontend (Vite + Tailwind CSS)
│   ├── src/
│   │   ├── components/               # Reusable UI components
│   │   │   ├── Navbar.jsx            # Responsive navigation bar with role-based links
│   │   │   └── ProtectedRoute.jsx    # Route guard with role-based authorization
│   │   ├── context/                  # React Context
│   │   │   └── AuthContext.jsx       # Global authentication state, login, and logout
│   │   ├── pages/                    # Application Pages
│   │   │   ├── Login.jsx             # User login page
│   │   │   ├── Register.jsx          # User registration page
│   │   │   ├── UserDashboard.jsx     # Plant identification (single & batch) & history
│   │   │   ├── AdminDashboard.jsx    # Admin statistics, user list, recent predictions
│   │   │   ├── AdminUsersPage.jsx    # Paginated user management and role editing
│   │   │   └── ResearcherDashboard.jsx # Prediction verification and disease correction
│   │   ├── services/                 # API client
│   │   │   └── api.js                # Axios instance (configured for http://localhost:8081)
│   │   ├── App.jsx                   # Application router and layout
│   │   ├── main.jsx                  # React DOM entry point
│   │   └── index.css                 # Tailwind CSS styles and theme definitions
│   ├── index.html                    # HTML template
│   ├── package.json                  # Frontend dependencies and npm scripts
│   ├── vite.config.js                # Vite build and dev server configuration
│   ├── tailwind.config.js            # Tailwind CSS configuration and theme colors
│   └── postcss.config.js             # PostCSS configuration
│
├── ml-service/                       # Python Machine Learning Inference Service
│   ├── app.py                        # Flask API application (runs on http://localhost:5000)
│   ├── model_loader.py               # Model loading (MobileNetV2 CNN) & image inference
│   ├── train_model.py                # Deep learning model training script
│   ├── dataset_config.py             # Dataset discovery and class name mapping
│   ├── create_test_images.py         # Utility to generate placeholder test leaf images
│   ├── download_sample_images.py     # Sample image downloader utility
│   ├── trust_score_analysis.py       # Reliability and confidence analysis
│   ├── verify_test_cases.py          # ML test verification script
│   ├── get_test_images.md            # Guide for sourcing and organizing test images
│   ├── README.md                     # ML service documentation
│   ├── requirements.txt              # Flask, TensorFlow, Keras, Pillow, OpenCV, NumPy
│   └── models/                       # Trained model weights and class labels
│       ├── plant_classifier.h5       # Trained CNN model file
│       └── class_names.txt           # Ordered class names list
│
├── dataset/                          # Training Datasets
│   ├── leaf_dataset/                 # Lab and field leaf images
│   └── plantvillage dataset/         # PlantVillage color, grayscale, and segmented images
│
├── .gitignore                        # Git ignore patterns for Python, Node, and environment
├── FEATURES.md                       # Comprehensive feature specifications
├── PROJECT_STRUCTURE.md              # Project structure and architecture overview
├── QUICKSTART.md                     # Quick 5-minute setup and execution guide
├── QUICK_IMAGE_GUIDE.md              # Guide for batch test image setup and execution
├── README.md                         # Main repository overview and documentation
├── SETUP.md                          # Detailed installation and configuration guide
└── trim_dataset_to_25.py             # Dataset trimming utility script
```

---

## Key Components

### Backend (Python / FastAPI)
- **Framework**: FastAPI with asynchronous ASGI execution powered by Uvicorn.
- **Port**: `8081` (configurable via `SERVER_PORT` in `.env`).
- **Database Access**: Asynchronous MongoDB integration via **Motor** and **Beanie ODM** (Document-Object Mapper built on Pydantic).
- **Authentication & Security**:
  - JWT generation and validation via `PyJWT` (algorithm `HS256`).
  - Password hashing and verification using `bcrypt` / `passlib`.
  - Reusable security dependencies with `HTTPBearer` and `require_role("ROLE")`.
  - CORS middleware supporting Vite frontend (`http://localhost:5173`).
- **API Routers**:
  - `auth`: User registration (`/api/auth/register`) and login (`/api/auth/login`).
  - `prediction`: Single image identification (`/api/predict`), batch identification (`/api/predict/batch`), and user prediction history (`/api/predict/history`).
  - `admin`: System analytics (`/api/admin/stats`), recent users (`/api/admin/users`), paginated users (`/api/admin/users/page`), role updates (`/api/admin/users/{id}/role`), recent predictions (`/api/admin/predictions`), and prediction verification (`/api/admin/predictions/{id}/verify`).
  - `researcher`: View unverified predictions (`/api/researcher/unverified`) and verify/correct predictions (`/api/researcher/verify/{predictionId}`).
- **Services**:
  - `auth_service`: Handles user account creation, credentials verification, and JWT issuance.
  - `prediction_service`: Coordinates file saving, ML inference forwarding, label parsing, disease status determination, pesticide recommendations, and persistence.
  - `admin_service`: Computes aggregate platform statistics, top identified plants, and paginated user management.
  - `ml_client`: Non-blocking HTTP client (`httpx.AsyncClient`) communicating with the Python ML inference service.
  - `file_storage`: Stores uploaded image files on the filesystem under `uploads/` with UUID prefixes and generates public asset URLs.
- **Models (Beanie ODM Documents)**:
  - `User`: Stored in `users` collection with email index, password hash, and role (`USER`, `ADMIN`, `RESEARCHER`).
  - `Prediction`: Stored in `predictions` collection with plant name, confidence score, image URL, disease classification, status (`Healthy`/`Unhealthy`), pesticides, and verification state.
  - `Plant`: Stored in `plants` collection with scientific name, leaf type, geographic region, description, and sample image metadata.
  - `Feedback`: Stored in `feedback` collection with researcher annotations, comments, and corrections.

### Frontend (React / Vite)
- **Framework**: React 18, Vite 5, Tailwind CSS 3, Axios, Chart.js / React-Chartjs-2.
- **Port**: `5173` (proxied or pointing to FastAPI on `http://localhost:8081`).
- **Pages**:
  - `Login` & `Register`: Authentication flows with role selection.
  - `UserDashboard`: Plant and leaf disease identification supporting single file upload, camera capture, and batch upload (up to 30 images). Displays botanical data, health status, and historical logs.
  - `AdminDashboard`: Graphical analytics (plant popularity charts, success rates, system health) and recent activity lists.
  - `AdminUsersPage`: Paginated table of platform users with real-time role reassignment.
  - `ResearcherDashboard`: Review queue for unverified predictions with disease correction tools.
- **State & Routing**:
  - `AuthContext`: Centralized JWT authentication state and localStorage synchronization.
  - `ProtectedRoute`: Route guard restricting access based on user roles (`ADMIN`, `RESEARCHER`, `USER`).

### ML Service (Python / Flask / TensorFlow)
- **Framework**: Python 3.8+ / 3.10+, Flask API server, TensorFlow/Keras, OpenCV, NumPy.
- **Port**: `5000` (configurable in `app.py`).
- **Core Modules**:
  - `app.py`: Flask HTTP server exposing `POST /predict` and `GET /health`.
  - `model_loader.py`: Preprocessing pipeline (224x224 RGB image normalization) and MobileNetV2 CNN inference.
  - `train_model.py`: Transfer learning training script with dynamic class discovery across dataset subdirectories.
  - `create_test_images.py`: Script to generate synthetic test leaf images for quick end-to-end testing.

---

## Data Flow

```
[User Browser / React Frontend] :5173
              │
              ▼  (HTTP REST / Multipart Upload / JWT Bearer)
[FastAPI Backend Service] :8081
       ├── Stores image ───────────► [Local Filesystem: backend-python/uploads/]
       ├── Forwards image ─────────► [Python ML Service] :5000 (TensorFlow / CNN)
       │                             └── Inferred plant/disease label + confidence
       ├── Parses label & fetches ──► [MongoDB Database] :27017
       │   botanical info & pesticides    (Collections: users, predictions, plants, feedback)
       ▼
[JSON Response Returned to Frontend with Prediction & Treatment Data]
```

1. **User Upload**: Frontend submits leaf image(s) to FastAPI (`POST /api/predict` or `POST /api/predict/batch`).
2. **File Storage**: FastAPI stores the file under `backend-python/uploads/` with a unique UUID.
3. **ML Inference**: FastAPI dispatches an asynchronous multipart request via `httpx` to the Python ML Service (`POST /predict` on port `5000`).
4. **Data Enrichment**: FastAPI parses the prediction label (e.g. `Tomato___Early_blight`), retrieves botanical info and pesticide recommendations, and persists the record to MongoDB.
5. **Prediction History**: Frontend queries `GET /api/predict/history` to view personal identification history.
6. **Researcher Verification**: Researchers review unverified records via `GET /api/researcher/unverified` and submit corrections via `POST /api/researcher/verify/{id}`.

---

## Security Architecture

- **Token Authentication**: Stateless JSON Web Tokens (JWT) signed with HMAC-SHA256 (`HS256`).
- **Role-Based Access Control (RBAC)**: Enforced through FastAPI dependency injection (`require_role("ADMIN")`, `require_role("RESEARCHER", "ADMIN")`).
- **Password Security**: Salted password hashing via BCrypt.
- **CORS Configuration**: Restricts access to authorized frontend origins (`http://localhost:5173`, `http://localhost:3000`).
- **File Upload Protection**: Validates file types and enforces a 10MB file size limit.

---

## Database Architecture (MongoDB)

- **`users`**: User profile information, encrypted passwords, assigned role, account creation date, and last login timestamp.
- **`predictions`**: Prediction history records containing user ID, plant name, scientific name, disease diagnosis, health status, confidence percentage, confidence level, recommended pesticides, image file paths/URLs, and verification status.
- **`plants`**: Botanical encyclopedia data including plant name, scientific name, leaf type, regional distribution, and botanical descriptions.
- **`feedback`**: Researcher annotations, corrections, and model audit records.
