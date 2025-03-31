# Code Dependencies and Relationships

## Frontend Dependencies

### Core Dependencies
- React (v18.x)
  - Status: ✅ Implemented
  - Usage: Core UI framework
  - Dependencies: None

- React Router (v6.x)
  - Status: ✅ Implemented
  - Usage: Navigation and routing
  - Dependencies: React

- TailwindCSS
  - Status: ✅ Implemented
  - Usage: Styling
  - Dependencies: PostCSS

### Component Dependencies

#### App.jsx
- Dependencies:
  - React Router
  - IntakeFlow component
- Status: ✅ Implemented
- Pending: Dashboard implementation

#### IntakeFlow.jsx
- Dependencies:
  - StageOneIntake
  - StageTwo5Ws
  - StageThreeSynopsis
- Status: ✅ Implemented
- State Management:
  - stage (number)
  - copilotData (object)
  - feedback (array)

#### Stage Components
- StageOneIntake
  - Status: ✅ Implemented
  - Dependencies: None
  - Props: onComplete, updateData

- StageTwo5Ws
  - Status: ✅ Implemented
  - Dependencies: None
  - Props: data, onBack, onComplete, updateData

- StageThreeSynopsis
  - Status: ✅ Implemented
  - Dependencies: None
  - Props: data, onBack, recordFeedback

## Backend Dependencies

### Core Dependencies
- FastAPI
  - Status: ✅ Implemented
  - Usage: API framework
  - Dependencies: Python 3.8+

- SQLAlchemy
  - Status: ⚠️ Partially Implemented
  - Usage: Database ORM
  - Dependencies: None

- Pydantic
  - Status: ✅ Implemented
  - Usage: Data validation
  - Dependencies: None

### Service Dependencies

#### AI Service
- OpenAI API
  - Status: ⚠️ Partially Implemented
  - Usage: AI analysis
  - Dependencies: OpenAI client

#### Database Service
- PostgreSQL
  - Status: ⚠️ Partially Implemented
  - Usage: Data storage
  - Dependencies: SQLAlchemy

### Route Dependencies

#### /copilot/intake
- Status: ✅ Implemented
- Dependencies:
  - IntakeData model
  - Business logic service
  - Database service

#### /copilot/analysis
- Status: ⚠️ Partially Implemented
- Dependencies:
  - AI service
  - Analysis models
  - Database service

#### /copilot/feedback
- Status: ⚠️ Partially Implemented
- Dependencies:
  - Feedback model
  - Database service

## Data Models

### Frontend Models
```typescript
interface CopilotData {
  trialName?: string;
  description?: string;
  stageOneData?: object;
  stageTwoData?: object;
  stageThreeData?: object;
}

interface FeedbackEntry {
  id: string;
  timestamp: Date;
  content: string;
  type: 'suggestion' | 'bug' | 'feature';
}
```

### Backend Models
```python
class IntakeData(BaseModel):
    trial_name: str
    description: str
    stage_one_data: Dict
    stage_two_data: Dict
    stage_three_data: Dict

class AnalysisResult(BaseModel):
    summary: str
    recommendations: List[str]
    risks: List[str]
    confidence: float
```

## API Dependencies

### Frontend → Backend
- POST /copilot/intake/submit
  - Status: ✅ Implemented
  - Dependencies: IntakeData model

- GET /copilot/intake/status
  - Status: ✅ Implemented
  - Dependencies: None

- POST /copilot/analysis/analyze
  - Status: ⚠️ Partially Implemented
  - Dependencies: AnalysisRequest model

- GET /copilot/analysis/results
  - Status: ⚠️ Partially Implemented
  - Dependencies: None

- POST /copilot/feedback/submit
  - Status: ⚠️ Partially Implemented
  - Dependencies: FeedbackEntry model

## Development Dependencies

### Frontend
- Vite
  - Status: ✅ Implemented
  - Usage: Build tool
  - Dependencies: Node.js

- ESLint
  - Status: ✅ Implemented
  - Usage: Code linting
  - Dependencies: None

- Prettier
  - Status: ✅ Implemented
  - Usage: Code formatting
  - Dependencies: None

### Backend
- pytest
  - Status: ❌ Not Implemented
  - Usage: Testing
  - Dependencies: Python

- black
  - Status: ✅ Implemented
  - Usage: Code formatting
  - Dependencies: Python

- mypy
  - Status: ❌ Not Implemented
  - Usage: Type checking
  - Dependencies: Python

## Legend
- ✅ Implemented: Feature is fully implemented and tested
- ⚠️ Partially Implemented: Feature is implemented but needs testing or refinement
- ❌ Not Implemented: Feature is planned but not yet implemented 