# Task Manager Frontend

Modern React frontend for the Task Management API.

## Features

- ✅ User authentication (Login/Register)
- ✅ Dashboard with statistics
- ✅ Project management (Create, view, delete)
- ✅ Task management (Create, view, update, delete)
- ✅ Task comments
- ✅ Responsive design
- ✅ Modern UI/UX

## Setup

1. **Install dependencies:**
   ```bash
   npm install
   ```

2. **Start development server:**
   ```bash
   npm run dev
   ```

3. **Build for production:**
   ```bash
   npm run build
   ```

4. **Preview production build:**
   ```bash
   npm run preview
   ```

## Configuration

The API base URL is configured in `src/services/api.js`. By default, it points to `http://127.0.0.1:8000/api`.

To change the API URL, update:
```javascript
const API_BASE_URL = 'http://your-api-url.com/api';
```

## Development

- **Frontend runs on:** http://localhost:5173 (Vite default)
- **Backend API:** http://127.0.0.1:8000/api
- **Hot Module Replacement:** Enabled
- **Fast Refresh:** Enabled

## Project Structure

```
frontend/
├── src/
│   ├── components/      # Reusable components
│   │   ├── Layout.jsx   # Main layout with navigation
│   │   └── Layout.css
│   ├── pages/          # Page components
│   │   ├── Login.jsx
│   │   ├── Register.jsx
│   │   ├── Dashboard.jsx
│   │   ├── Projects.jsx
│   │   ├── Tasks.jsx
│   │   └── ...
│   ├── context/        # React Context
│   │   └── AuthContext.jsx
│   ├── services/       # API services
│   │   └── api.js
│   ├── App.jsx         # Main app component
│   ├── App.css         # Global styles
│   └── main.jsx        # Entry point
├── public/             # Static assets
└── package.json
```

## Technologies

- **React 19** - UI library
- **Vite** - Build tool and dev server
- **React Router** - Routing
- **Axios** - HTTP client
- **CSS3** - Styling (no external CSS framework)

## Deployment

### Build for Production

```bash
npm run build
```

This creates an optimized build in the `dist/` directory.

### Deploy Options

1. **Static Hosting:**
   - Netlify
   - Vercel
   - GitHub Pages
   - AWS S3 + CloudFront

2. **With Backend:**
   - Serve `dist/` folder from Django (collectstatic)
   - Or use separate hosting with CORS configuration

3. **Docker:**
   - Use multi-stage build
   - Serve with nginx
