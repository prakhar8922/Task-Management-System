# Task Management System

A full-stack Task and Project Management application with Django REST API backend and React frontend.

## 🚀 Features

### Backend (Django REST API)
- **User Authentication**: JWT-based authentication with user registration
- **Project Management**: Create, update, delete, and manage projects
- **Task Management**: Full CRUD operations for tasks with status, priority, and due dates
- **Task Assignments**: Assign tasks to multiple users
- **Tags**: Categorize tasks with tags
- **Comments**: Add comments to tasks
- **File Attachments**: Upload and manage file attachments for tasks
- **Filtering & Search**: Filter tasks by status, priority, assignee, and search by title/description
- **Permissions**: Role-based access control (project owners and members)
- **API Documentation**: Interactive API documentation with Swagger/ReDoc

### Frontend (React)
- **Modern UI**: Beautiful, responsive user interface
- **User Dashboard**: Statistics and overview
- **Project Management**: Visual project creation and management
- **Task Management**: Intuitive task creation and tracking
- **Real-time Updates**: Dynamic data fetching and updates
- **Mobile Responsive**: Works on all devices

## 🛠 Technology Stack

### Backend
- **Django 5.2+** - Web framework
- **Django REST Framework** - API framework
- **JWT Authentication** - Token-based authentication
- **PostgreSQL** - Production database
- **SQLite** - Development database
- **drf-spectacular** - API documentation

### Frontend
- **React 19.2+** - UI library
- **Vite** - Build tool
- **React Router** - Client-side routing
- **Axios** - HTTP client

### DevOps
- **Docker & Docker Compose** - Containerization
- **Python 3.8+** - Backend runtime
- **Node.js 18+** - Frontend runtime

## 📁 Project Structure

```
task_manager/
├── manage.py                 # Django management script
├── requirements.txt          # Python dependencies
├── Dockerfile               # Docker configuration
├── docker-compose.yml       # Docker Compose configuration
├── task_manager/            # Main project directory
│   ├── settings.py         # Django settings
│   ├── urls.py            # URL routing
│   └── ...
├── users/                  # User management app
├── projects/               # Projects app
├── tasks/                  # Tasks app
└── frontend/               # React frontend
    ├── package.json        # Node.js dependencies
    ├── src/               # React source code
    └── dist/              # Build output
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 18+
- PostgreSQL (for production) or SQLite (for development)

### Option 1: Full Stack Development

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd task_manager
   ```

2. **Backend Setup**
   ```bash
   # Create and activate virtual environment
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   
   # Install dependencies
   pip install -r requirements.txt
   
   # Run migrations
   python manage.py migrate
   
   # Create superuser (optional)
   python manage.py createsuperuser
   
   # Start backend server
   python manage.py runserver
   ```

3. **Frontend Setup** (in a new terminal)
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

4. **Access the Application**
   - **Frontend UI**: http://localhost:5173
   - **API Documentation**: http://127.0.0.1:8000/api/docs/
   - **Admin Panel**: http://127.0.0.1:8000/admin/

### Option 2: Docker Setup

1. **Build and run with Docker Compose**
   ```bash
   docker-compose up --build
   ```

2. **Run migrations** (first time only)
   ```bash
   docker-compose exec web python manage.py migrate
   ```

3. **Create superuser** (optional)
   ```bash
   docker-compose exec web python manage.py createsuperuser
   ```

4. **Access the application**
   - **Frontend**: http://localhost:3000
   - **API**: http://localhost:8000/api/
   - **API Documentation**: http://localhost:8000/api/docs/

## 📚 API Documentation

### Authentication Endpoints
- `POST /api/users/register/` - Register a new user
- `POST /api/users/token/` - Obtain JWT token (login)
- `POST /api/users/token/refresh/` - Refresh JWT token
- `GET /api/users/profile/` - Get user profile
- `PATCH /api/users/profile/` - Update user profile

### Project Endpoints
- `GET /api/projects/` - List projects
- `POST /api/projects/` - Create a project
- `GET /api/projects/{id}/` - Get project details
- `PATCH /api/projects/{id}/` - Update project
- `DELETE /api/projects/{id}/` - Delete project
- `POST /api/projects/{id}/add_member/` - Add member to project
- `POST /api/projects/{id}/remove_member/` - Remove member from project

### Task Endpoints
- `GET /api/tasks/` - List tasks (supports filtering)
- `POST /api/tasks/` - Create a task
- `GET /api/tasks/{id}/` - Get task details
- `PATCH /api/tasks/{id}/` - Update task
- `DELETE /api/tasks/{id}/` - Delete task

### Additional Endpoints
- `GET /api/tasks/tags/` - List tags
- `POST /api/tasks/tags/` - Create a tag
- `GET /api/tasks/comments/?task={id}` - List comments for a task
- `POST /api/tasks/comments/` - Create a comment
- `GET /api/tasks/attachments/?task={id}` - List attachments for a task
- `POST /api/tasks/attachments/` - Upload attachment

## 🔐 Authentication

The API uses JWT (JSON Web Token) authentication:

1. **Register/Login** to obtain tokens:
   ```bash
   POST /api/users/token/
   {
     "email": "user@example.com",
     "password": "yourpassword"
   }
   ```

2. **Use the access token** in subsequent requests:
   ```
   Authorization: Bearer <your_access_token>
   ```

## 🧪 Testing

```bash
# Run all tests
python manage.py test

# Run specific app tests
python manage.py test users.tests
python manage.py test projects.tests
python manage.py test tasks.tests
```

## ⚙️ Environment Variables

Create a `.env` file in the project root:

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=postgresql://user:password@localhost:5432/task_manager
```

## 📦 Deployment

For detailed deployment instructions, see `DEPLOYMENT.md`.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is for educational purposes.

## 🆘 Support

If you encounter any issues, please check the troubleshooting section in `DEPLOYMENT.md` or open an issue.
