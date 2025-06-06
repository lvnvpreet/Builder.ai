# 🤖 AI Website Builder

> **Multi-Agent AI System for Intelligent Website Generation**

An advanced AI-powered website builder that uses specialized agents and LangGraph orchestration to generate professional websites in under 90 seconds.

## 🌟 Key Features

- **🧠 Multi-Agent AI System**: 5 specialized agents working in parallel
- **⚡ Lightning Fast**: 75% faster than traditional builders
- **🎨 Professional Design**: AI-generated responsive layouts
- **📸 Smart Images**: Automatic Unsplash integration
- **🔄 Real-time Progress**: Live WebSocket updates
- **💰 Cost Effective**: Open-source LLMs via Ollama
- **🔒 Privacy First**: All processing on your infrastructure

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Node.js 18+
- MongoDB 7.0+
- Docker (optional)

### Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # macOS/Linux

# Install dependencies
pip install -r requirements.txt

# Copy environment file
copy .env.example .env  # Windows
# cp .env.example .env  # macOS/Linux

# Initialize database
python scripts/init_database.py

# Start server
python -m uvicorn main:app --reload
```

### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Copy environment file
copy .env.local.example .env.local  # Windows
# cp .env.local.example .env.local  # macOS/Linux

# Start development server
npm run dev
```

### Ollama Setup

```bash
# Install Ollama (follow instructions at https://ollama.ai)

# Download required models
ollama pull llama3.1:70b
ollama pull codellama:34b
ollama pull mistral:7b-instruct

# Start Ollama service
ollama serve
```

## 🏗️ Architecture

The system uses a multi-agent architecture orchestrated by LangGraph:

- **Content Agent** (Llama 3.1 70B): Generates business content and copy
- **Design Agent** (CodeLlama 34B): Creates CSS styles and responsive layouts
- **Structure Agent** (Mistral 7B): Builds HTML structure and navigation
- **Image Agent** (Unsplash API): Selects contextual professional images
- **Quality Agent**: Validates and optimizes all generated components

## 📁 Project Structure

```
ai-website-builder/
├── backend/                 # FastAPI backend
│   ├── agents/             # AI agent implementations
│   ├── api/                # API routes
│   ├── core/               # Core utilities
│   ├── database/           # MongoDB models
│   ├── langgraph/          # LangGraph workflows
│   ├── services/           # Business logic
│   └── main.py             # Application entry
├── frontend/               # Next.js frontend
│   ├── src/
│   │   ├── components/     # React components
│   │   ├── services/       # API services
│   │   └── types/          # TypeScript types
│   └── package.json
├── docker/                 # Container configurations
└── docs/                   # Documentation
```

## 🛠️ Tech Stack

**Backend:**
- Python 3.11+ with FastAPI
- LangGraph for agent orchestration
- Ollama for local LLM inference
- MongoDB for data storage
- WebSocket for real-time updates

**Frontend:**
- React 18 with TypeScript
- Next.js framework
- Tailwind CSS for styling
- Socket.io for real-time communication

**AI Models:**
- Llama 3.1 70B (Content)
- CodeLlama 34B (Design)
- Mistral 7B (Structure)
- Unsplash API (Images)

## 🐳 Docker Setup

```bash
# Clone the repository
git clone <repository-url>
cd ai-website-builder

# Start with Docker Compose
docker-compose -f docker/docker-compose.yml up --build

# Access the application
# Frontend: http://localhost:3000
# Backend API: http://localhost:8000
```

## 📊 API Endpoints

- `GET /health` - Health check
- `POST /api/v1/generate` - Start website generation
- `GET /api/v1/generate/{id}` - Get generation status
- `GET /api/v1/models/status` - Check AI models status
- `WS /ws/generation/{id}` - WebSocket for real-time updates

## 🔧 Configuration

### Backend Environment Variables

```bash
# Database
MONGODB_URL=mongodb://localhost:27017/ai_website_builder

# Ollama
OLLAMA_BASE_URL=http://localhost:11434
CONTENT_MODEL=llama3.1:70b
DESIGN_MODEL=codellama:34b
STRUCTURE_MODEL=mistral:7b-instruct

# Unsplash API
UNSPLASH_ACCESS_KEY=your_access_key
UNSPLASH_SECRET_KEY=your_secret_key

# Security
SECRET_KEY=your-secret-key
JWT_SECRET=your-jwt-secret
```

### Frontend Environment Variables

```bash
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_WS_URL=ws://localhost:8000/ws
```

## 🧪 Testing

```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
npm test
```

## 📚 Documentation

For detailed documentation, see the `docs/` directory:

- [Setup Guide](docs/setup_guide.md)
- [Architecture Guide](docs/architecture_guide.md)
- [API Documentation](docs/api_documentation.md)
- [Deployment Guide](docs/deployment_guide.md)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📜 License

This project is licensed under the MIT License.

## 🆘 Support

For support and troubleshooting, see [Troubleshooting Guide](docs/troubleshooting_guide.md) or open an issue.

---

**Made with ❤️ by the AI Website Builder Team**
