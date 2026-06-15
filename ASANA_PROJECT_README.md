# Asana-like Project Management Tool

A full-featured project management tool built with Node.js, React, and PostgreSQL, designed to rival Asana with comprehensive task management, team collaboration, and advanced visualization features.

## Project Structure

```
bp/
├── backend/          # Node.js/Express API server
├── frontend/         # React/Vite client application
└── docs/            # Documentation (to be created)
```

## Getting Started

### Prerequisites

- Node.js 18+ 
- PostgreSQL 12+
- Redis (optional, for job queues)

### Backend Setup

```bash
cd backend

# Install dependencies
npm install

# Copy environment variables
cp .env.example .env

# Update .env with your PostgreSQL and JWT credentials
# DB_HOST=localhost
# DB_NAME=asana_db
# DB_USER=postgres
# DB_PASSWORD=postgres

# Run database migrations
npm run migrate

# Start development server
npm run dev
```

The backend will run on `http://localhost:3000`

### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Copy environment variables
cp .env.example .env

# Start development server
npm run dev
```

The frontend will run on `http://localhost:5173`

## Architecture Overview

### Backend

**Stack:** Express.js, TypeScript, PostgreSQL, Socket.io

**Key Directories:**
- `src/config/` - Configuration files (database, logger, environment)
- `src/middleware/` - Express middleware
- `src/routes/` - API route definitions
- `src/controllers/` - Request handlers
- `src/services/` - Business logic
- `src/repositories/` - Data access layer
- `src/models/` - Database models
- `src/types/` - TypeScript type definitions
- `src/socket/` - WebSocket event handling
- `src/jobs/` - Background job processing

### Frontend

**Stack:** React, TypeScript, Vite, Tailwind CSS

**Key Directories:**
- `src/components/` - Reusable React components
- `src/pages/` - Page components
- `src/hooks/` - Custom React hooks
- `src/context/` - React Context API
- `src/services/` - API client and socket services
- `src/store/` - State management (Zustand)
- `src/types/` - TypeScript type definitions
- `src/styles/` - CSS and Tailwind styling

## API Endpoints (Phase 1+)

### Authentication
- `POST /api/v1/auth/register` - Create new user
- `POST /api/v1/auth/login` - Login user
- `POST /api/v1/auth/refresh` - Refresh JWT token

### Tasks (Core MVP)
- `POST /api/v1/tasks` - Create task
- `GET /api/v1/tasks` - List tasks (with filters)
- `GET /api/v1/tasks/:id` - Get task details
- `PATCH /api/v1/tasks/:id` - Update task
- `DELETE /api/v1/tasks/:id` - Delete task

### Projects
- `POST /api/v1/projects` - Create project
- `GET /api/v1/projects` - List projects
- `GET /api/v1/projects/:id` - Get project details
- `PATCH /api/v1/projects/:id` - Update project

### Teams
- `POST /api/v1/teams` - Create team
- `GET /api/v1/teams` - List teams
- `GET /api/v1/teams/:id/members` - Get team members
- `POST /api/v1/teams/:id/members` - Add team member

See the comprehensive API documentation in the implementation plan for full endpoint details.

## Development Phases

### Phase 1: MVP Basics (4-5 weeks)
- Backend foundation and auth
- Core task management
- Basic frontend with task list

### Phase 2: Collaboration (3-4 weeks)
- Teams and multi-user projects
- Comments and activity feeds
- Advanced task features

### Phase 3: Advanced Views (3 weeks)
- Timeline/Gantt view
- Kanban board view
- Calendar view and analytics

### Phase 4: Real-time & Notifications (2-3 weeks)
- WebSocket integration
- Real-time task updates
- Email notifications

## Database Schema

The project uses PostgreSQL with the following core tables:
- `users` - User accounts
- `teams` - Team/workspace management
- `projects` - Projects within teams
- `tasks` - Individual tasks
- `comments` - Task comments
- `activities` - Audit log
- `notifications` - User notifications

See `backend/src/migrations/` for full schema definitions.

## Testing

### Backend
```bash
cd backend
npm run test              # Run all tests
npm run test:watch       # Watch mode
npm run test:coverage    # Coverage report
```

### Frontend
```bash
cd frontend
npm run test             # Run all tests
npm run test:ui          # UI mode
```

## Environment Variables

### Backend (.env)
```
NODE_ENV=development
PORT=3000
DB_HOST=localhost
DB_PORT=5432
DB_NAME=asana_db
DB_USER=postgres
DB_PASSWORD=postgres
JWT_SECRET=your_secret_key
JWT_REFRESH_SECRET=your_refresh_secret
FRONTEND_URL=http://localhost:5173
REDIS_HOST=localhost
REDIS_PORT=6379
```

### Frontend (.env)
```
VITE_API_URL=http://localhost:3000/api
VITE_SOCKET_URL=http://localhost:3000
VITE_APP_NAME=Asana Project Management
```

## Contributing

1. Create a feature branch (`git checkout -b feature/amazing-feature`)
2. Commit changes (`git commit -m 'Add amazing feature'`)
3. Push to branch (`git push origin feature/amazing-feature`)
4. Open a Pull Request

## Key Features (Planned)

✅ User authentication with JWT
✅ Task management (CRUD operations)
✅ Project organization
✅ Team collaboration
🔄 Timeline/Gantt views
🔄 Kanban board view
🔄 Real-time updates with WebSocket
🔄 Email notifications
🔄 Advanced search and filters
🔄 Activity feeds and audit logs

## Performance & Scalability

- Stateless backend for horizontal scaling
- Database indexing on frequently queried columns
- Redis caching for sessions and real-time data
- WebSocket rooms for efficient broadcasting
- Pagination and lazy loading on frontend
- Code splitting and bundle optimization

## Security

- JWT-based authentication
- Role-based access control (RBAC)
- Password hashing with bcrypt
- Environment variable management
- CORS configuration
- Rate limiting on API endpoints
- Input validation and sanitization
- SQL injection prevention via parameterized queries

## License

MIT License - see LICENSE file for details

## Notes

This is an active development project. The initial setup provides:
- Complete project structure for both backend and frontend
- Database configuration and models
- Authentication framework
- API route structure
- React component hierarchy
- Environment configuration

Phase 1 implementation will focus on core task management functionality.

For detailed implementation plans and architectural decisions, see the comprehensive plan document generated during project initialization.
