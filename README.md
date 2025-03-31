# Clinical Trials Expert User Copilot UI/UX

A modern web application for managing clinical trial intake and analysis, featuring a multi-stage workflow and AI-powered assistance.

## Project Structure

```
.
├── frontend/                 # React frontend application
│   ├── src/
│   │   ├── components/      # Reusable UI components
│   │   ├── pages/          # Page-level components
│   │   ├── assets/         # Static assets
│   │   └── App.jsx         # Main application component
│   └── package.json         # Frontend dependencies
│
├── backend/                 # FastAPI backend application
│   ├── ai/                 # AI/ML related code
│   ├── db/                 # Database models and migrations
│   ├── etl/                # Data extraction/transformation
│   ├── logic/              # Business logic
│   ├── models/             # Data models
│   ├── routes/             # API endpoints
│   ├── utils/              # Utility functions
│   └── main.py             # Application entry point
│
└── .specstory/             # Project documentation and specs
```

## Architecture

### Frontend
- Built with React and React Router
- Uses a multi-stage form workflow
- Components are organized by feature and reusability
- State management using React hooks

### Backend
- FastAPI-based REST API
- Modular architecture with separate concerns
- AI-powered analysis capabilities
- Database integration for data persistence

## Setup

### Frontend
```bash
cd frontend
npm install
npm run dev
```

### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows
pip install -r requirements.txt
uvicorn main:app --reload
```

## Development Status

### Completed Features
- Basic application structure
- Multi-stage intake flow
- Frontend routing
- Basic backend API setup

### In Progress
- AI integration
- Data persistence
- User feedback system

### Pending
- Dashboard implementation
- Advanced analytics
- User authentication
- Test coverage

## Dependencies

### Frontend
- React
- React Router
- TailwindCSS
- Axios (for API calls)

### Backend
- FastAPI
- SQLAlchemy
- Pydantic
- Python-dotenv
- OpenAI (for AI features)

## API Documentation

The API documentation is available at `/docs` when running the backend server.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

[Add License Information] 