# RhymeslikeDimes

Advanced rhyme finder inspired by MF DOOM's complex rhyming patterns. Find perfect rhymes, near rhymes, slant rhymes, and multi-word combinations in real-time.

## Features

- **Multi-word rhyme detection** - Finds rhymes for phrases like "cookie tear" → "rookie year"
- **Three rhyme types**:
  - Perfect rhymes (exact phonetic match)
  - Near rhymes (similar sounds)
  - Slant rhymes (assonance/consonance)
- **Real-time analysis** - Instant feedback as you type
- **Click-to-insert** - Add suggestions directly into your text
- **Clean, modern UI** - Responsive design with dark mode support

## Quick Start

> Deployed version available on Vercel!

### Prerequisites
- Python 3.8+
- Node.js 16+
- npm or yarn

### Development

1. Clone the repository:
```bash
git clone https://github.com/yourusername/RhymeslikeDimes.git
cd RhymeslikeDimes
```

2. Run the development environment:
```bash
./start-dev.sh
```

This will:
- Install all dependencies
- Start the backend API on http://localhost:8001
- Start the frontend on http://localhost:3000
- Open API documentation at http://localhost:8001/docs

### Manual Setup

#### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python app/main.py
```

#### Frontend
```bash
cd frontend
npm install
npm run dev
```

## Tech Stack

### Backend
- **FastAPI** - Modern Python web framework
- **Datamuse API** - Comprehensive word-finding engine
- **Pronouncing** - CMU dictionary interface
- **WebSocket** - Real-time communication

### Frontend
- **React** - UI framework
- **TypeScript** - Type safety
- **Tailwind CSS** - Styling
- **Framer Motion** - Animations
- **Vite** - Build tool

## Deployment

### Vercel (Frontend)
1. Fork this repository
2. Import to Vercel
3. Set root directory to `frontend`
4. Deploy

### Railway (Backend)
1. Create new project on Railway
2. Deploy from GitHub
3. Set root directory to `backend`
4. Add environment variables from `.env.example`

### Environment Variables

Backend (`.env`):
```
PORT=8001
CORS_ORIGINS=http://localhost:3000,https://yourdomain.com
```

## API Documentation

Once running, visit http://localhost:8001/docs for interactive API documentation.

### Key Endpoints

- `POST /api/analyze` - Analyze a bar for rhymes
- `GET /api/health` - Health check
- `WS /ws` - WebSocket for real-time analysis

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

MIT License - see LICENSE file for details

## Acknowledgments

- Inspired by MF DOOM's intricate rhyme schemes
- Built with the Datamuse API
- Uses CMU Pronouncing Dictionary