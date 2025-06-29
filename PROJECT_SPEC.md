# RhymeslikeDimes Project Specification

## Project Overview
RhymeslikeDimes is a sophisticated rhyme-finding web application inspired by MF DOOM's complex rhyming patterns. It helps rappers and creative writers discover perfect rhymes, near rhymes, slant rhymes, and multi-word rhyme combinations in real-time.

## Core Requirements

### Priority Features (In Order)
1. **Clean, Modern Web GUI** - Intuitive interface with real-time updates
2. **Near/Slant Rhyme Support** - Beyond perfect rhymes for creative flexibility
3. **Multi-word Rhyme Detection** - Match phrases like "cookie tear" → "rookie year"
4. **Real-time GUI Updates** - Instant feedback as users type
5. **Save Functionality** - Future feature for storing sessions/favorites

### Target Audience
- Rappers perfecting their craft
- Creative writers exploring wordplay
- Lyricists seeking complex rhyme patterns
- Anyone interested in advanced phonetic relationships

## Technical Architecture

### Frontend
- **Framework**: Modern React/Vue/Svelte (recommend React for ecosystem)
- **Styling**: Tailwind CSS for clean, responsive design
- **State Management**: React Context/Zustand for real-time updates
- **UI Components**:
  - Main textarea for bar input
  - Real-time suggestion panels (perfect/near/slant)
  - Click-to-insert functionality
  - Visual distinction between rhyme types
  - Mobile-responsive design

### Backend
- **Framework**: FastAPI (Python)
- **API Design**: RESTful endpoints with WebSocket support for real-time
- **Rhyme Engine**: 
  - Datamuse API integration (online mode)
  - CMU Pronouncing Dictionary (offline fallback)
  - Custom pronunciation overrides
- **Caching**: Redis for API response caching

### Data Sources
1. **Primary**: Datamuse API
   - Perfect rhymes (rel_rhy)
   - Near rhymes (rel_nry)
   - Sound-alike words (sl)
   - Multi-word phrase support
2. **Fallback**: CMU Dictionary via pronouncing library
3. **Custom**: User-defined pronunciation overrides

## Implementation Details

### API Endpoints
```
POST /api/analyze
  - Input: { "bar": "string", "options": {...} }
  - Output: { "fragments": { "word/phrase": { "perfect": [...], "near": [...], "slant": [...] }}}

GET /api/suggestions/:word
  - Real-time individual word lookup

WebSocket /ws/live
  - Live typing analysis
```

### Frontend Architecture
```
src/
├── components/
│   ├── BarInput.jsx        # Main text input
│   ├── SuggestionPanel.jsx # Rhyme suggestions display
│   ├── RhymeChip.jsx       # Clickable rhyme word
│   └── Layout.jsx          # App structure
├── hooks/
│   ├── useRhymes.js        # API integration
│   └── useDebounce.js      # Input throttling
├── utils/
│   └── rhymeHelpers.js     # Client-side utilities
└── styles/
    └── themes.js           # Design system
```

### Backend Structure
```
app/
├── main.py                 # FastAPI app
├── api/
│   ├── routes.py          # API endpoints
│   └── websocket.py       # Real-time handler
├── core/
│   ├── rhyme_engine.py    # Main logic
│   ├── datamuse.py        # API wrapper
│   └── phonemes.py        # CMU integration
├── models/
│   └── schemas.py         # Pydantic models
└── utils/
    ├── cache.py           # Redis caching
    └── config.py          # Settings
```

## Deployment Strategy

### Recommended: Vercel + Railway
1. **Frontend**: Vercel (optimal for React/Next.js)
   - Automatic deployments from GitHub
   - Edge caching for performance
   - Free tier sufficient for personal use

2. **Backend**: Railway or Render
   - Simple Python app deployment
   - Built-in Redis support
   - Environment variable management
   - Free tier available

### Alternative: Single VPS
- DigitalOcean Droplet or Linode
- Nginx reverse proxy
- PM2 for Node.js process management
- Systemd for Python services
- Let's Encrypt SSL

### Local Development
```bash
# Backend
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload

# Frontend
cd frontend
npm install
npm run dev
```

## UI/UX Design Principles

### Visual Design
- **Color Scheme**: Dark theme default with light mode option
- **Typography**: Clear distinction between input and suggestions
- **Rhyme Type Indicators**: 
  - Perfect: Bold/primary color
  - Near: Secondary color
  - Slant: Tertiary/muted color
- **Animations**: Subtle transitions for suggestion updates

### Interaction Design
- **Instant Feedback**: <200ms response time
- **Keyboard Shortcuts**: 
  - Tab to cycle through suggestions
  - Enter to insert selected
  - Cmd/Ctrl+Z for undo
- **Mobile Gestures**: Swipe to dismiss, tap to insert

## Development Roadmap

### Phase 1: MVP (Week 1-2)
- [ ] Basic FastAPI backend with Datamuse integration
- [ ] Simple React frontend with textarea and suggestion display
- [ ] Click-to-insert functionality
- [ ] Deploy to Vercel/Railway

### Phase 2: Enhanced UX (Week 3-4)
- [ ] Real-time WebSocket updates
- [ ] Keyboard navigation
- [ ] Mobile responsive design
- [ ] Loading states and error handling

### Phase 3: Advanced Features (Week 5-6)
- [ ] Redis caching layer
- [ ] CMU dictionary fallback
- [ ] Custom pronunciation overrides
- [ ] Basic session history

### Phase 4: Polish & Optimization (Week 7-8)
- [ ] Performance optimization
- [ ] PWA capabilities
- [ ] Analytics integration
- [ ] User feedback collection

## Future Enhancements
- User accounts with saved sessions
- Rhyme pattern analysis
- AI-powered suggestion ranking
- Collaborative sessions
- Export to various formats
- Integration with writing tools

## Success Metrics
- Response time <200ms for suggestions
- Mobile Lighthouse score >90
- Zero downtime deployment
- Positive user feedback on UX

## Development Principles
1. **Performance First**: Optimize for instant feedback
2. **Clean Code**: Modular, testable components
3. **User-Centric**: Every feature enhances the creative process
4. **Iterative**: Ship early, improve continuously