# Travel Chat Assistant UI

A modern React-based chat interface for the Enhanced Conversational Travel Assistant, featuring authentication, real-time messaging, and comprehensive travel planning capabilities.

## 🚀 Quick Start

### Prerequisites
- Node.js 16+ (recommended 18+)
- npm 8+
- Backend API running on 127.0.0.1:5000

### Installation & Setup

```powershell
# Navigate to UI directory
cd "c:\Users\reyes\OneDrive\Documentos\AI_Challenge-main\app\UI"

# Install dependencies
npm install

# Start development server
npm start
```

The application will open at `http://localhost:3000`

### Default Login
- **Username**: `admin` (or any username)
- **Password**: `password` (or any password)

## 📱 Features

### Core Functionality
- **Secure Login**: Authentication with protected routes
- **Real-time Chat**: Interactive messaging with AI travel assistant
- **Travel Planning**: Intelligent travel recommendations and booking suggestions
- **Responsive Design**: Works on desktop, tablet, and mobile devices
- **Modern UI**: Clean, professional interface with smooth animations

### Technical Features
- **React 18.3.1**: Latest React with concurrent features
- **React Router 6.26.2**: Modern routing with protected routes
- **styled-components 6.1.13**: CSS-in-JS styling
- **framer-motion 11.5.4**: Smooth animations and transitions
- **axios 1.7.7**: Secure API communication
- **Comprehensive Testing**: Jest + React Testing Library (5 test suites)
- **Docker Support**: Multi-stage containerization for Azure deployment
- **CI/CD Pipeline**: GitHub Actions for automated deployment

## 🛡️ Security

All dependencies are up-to-date with latest security patches. Production builds contain 0 vulnerabilities. Development dependencies contain 3 moderate vulnerabilities that do not affect production builds.

## 🏗️ Project Structure

```
UI/
├── src/
│   ├── components/          # Reusable components
│   │   ├── ChatMessage.js   # Individual message display
│   │   └── TypingIndicator.js # AI typing animation
│   ├── pages/               # Main application pages
│   │   ├── Login.js         # Authentication page
│   │   └── Chat.js          # Main chat interface
│   ├── styles/              # Styled components
│   │   ├── GlobalStyles.js  # Global CSS styles
│   │   ├── LoginStyles.js   # Login page styling
│   │   └── MessageStyles.js # Chat message styling
│   ├── utils/               # Utilities and contexts
│   │   ├── AuthContext.js   # Authentication state management
│   │   └── api.js           # API communication layer
│   ├── tests/               # Test files (Jest + React Testing Library)
│   │   ├── App.test.js      # App component tests
│   │   ├── api.test.js      # API utility tests
│   │   ├── ChatMessage.test.js # Chat message component tests
│   │   ├── Login.test.js    # Login page tests
│   │   └── TypingIndicator.test.js # Typing indicator component tests
│   ├── App.js               # Main application component
│   ├── index.js             # Application entry point
│   └── setupTests.js        # Test configuration
├── .github/workflows/       # GitHub Actions for CI/CD
├── public/                  # Static assets
├── Dockerfile              # Container configuration for Azure deployment
├── .dockerignore           # Docker build optimization
├── package.json             # Dependencies and scripts
└── README.md               # This file
```

## 🔧 Development

### Available Scripts

```powershell
npm start          # Start development server (localhost:3000)
npm test           # Run test suite
npm run build      # Create production build
npm audit          # Check for security vulnerabilities
```

### Building for Production
```powershell
# Create optimized production build
npm run build

# Preview production build locally
npx serve -s build
```

### Docker Deployment
The UI includes Docker support for containerized deployment:

```powershell
# Build Docker image
docker build -t travel-chat-ui .

# Run container locally
docker run -p 8080:8080 travel-chat-ui
```

### Azure Container Apps Deployment
Automated deployment to Azure Container Apps is configured via GitHub Actions:
- **Automatic deployment** on commits to main/production branches
- **Multi-stage Docker build** optimized for production
- **Health checks** and validation included
- See `AZURE_DEPLOYMENT_SETUP.md` for detailed setup instructions

## 🌐 API Integration

The UI communicates with the Flask backend API running on `http://127.0.0.1:5000`.

### Development Proxy
To avoid CORS issues during development, the React app uses a proxy configured in `package.json`:
- All API requests are forwarded from `http://localhost:3000/api/*` to `http://127.0.0.1:5000/api/*`
- This eliminates the need for CORS headers from the backend during development

### API Configuration
For production deployments, configure the API URL via environment variables:
```bash
# .env file
REACT_APP_API_URL=http://your-production-api.com
```

## 🎨 Styling & Theming

### Design System
- **Color Palette**: Red-based theme with gradient backgrounds
- **Typography**: Modern, readable fonts with proper hierarchy
- **Layout**: Responsive design with mobile-first approach
- **Animations**: Smooth transitions with framer-motion

### Message Styling
- **User Messages**: Red gradient background with white text
- **AI Messages**: Dark gradient background with white text for optimal readability
- **Timestamps**: White text with transparency for subtle appearance

### Responsive Breakpoints
- **Mobile**: < 768px
- **Tablet**: 768px - 1024px
- **Desktop**: > 1024px

## 📊 Performance

- **Bundle Size**: Optimized for fast loading
- **Build Time**: ~8 seconds
- **Hot Reload**: < 1 second
- **Modern Features**: Code splitting, tree shaking, ES2020+ syntax

## 🔄 State Management

### Authentication Flow
1. User enters credentials on login page
2. AuthContext validates and stores authentication state
3. Protected routes check authentication status
4. Automatic redirection based on auth state

### Chat State
- Message history stored in component state
- Real-time updates with typing indicators
- Error handling with user-friendly messages
- Auto-scroll to latest messages

## 🚨 Troubleshooting

### Common Issues

**Backend Connection:**
```powershell
# Verify backend is running
curl http://127.0.0.1:5000/api/health

# Start backend if needed
cd "c:\Users\reyes\OneDrive\Documentos\AI_Challenge-main\app"
.\.venv\Scripts\Activate.ps1
python app.py
```

**Port 3000 in use:**
```powershell
# Kill process using port 3000
netstat -ano | findstr :3000
taskkill /F /PID <PID_NUMBER>
```

**Build issues:**
```powershell
# Clear cache and reinstall
npm cache clean --force
rm -rf node_modules package-lock.json
npm install
```

### Browser Compatibility
- **Chrome**: 90+
- **Firefox**: 90+
- **Safari**: 14+
- **Edge**: 90+

## 📚 Additional Documentation

For detailed information about specific aspects of the UI:

- **`AZURE_DEPLOYMENT_SETUP.md`** - Complete Azure Container Apps deployment guide
- **`DEPLOYMENT_SUMMARY.md`** - Overview of Docker and GitHub Actions configuration  
- **`DOCKERFILE`** - Multi-stage container configuration for production deployment
- **`.github/workflows/deploy-ui.yml`** - Automated CI/CD pipeline configuration

## 🤝 Contributing

### Development Workflow
1. Create feature branch from main
2. Make changes with comprehensive tests
3. Add tests to `src/tests/` folder following existing naming patterns
4. Run security audit: `npm audit`
5. Ensure build passes: `npm run build`
6. Submit pull request with detailed description

### Code Standards
- ESLint configuration for consistent formatting
- Prettier for code formatting
- Component-based architecture
- Comprehensive test coverage
- Security-first development practices

---

**Version**: 1.0.0  
**Last Updated**: August 1, 2025  
**Status**: Production Ready ✅

### Recent Updates
- ✅ **Azure Container Apps deployment** configured with GitHub Actions
- ✅ **Docker containerization** with multi-stage optimization
- ✅ **Test structure cleanup** - organized all tests in `/src` following React conventions
- ✅ **Production-ready** Dockerfile with health checks and security optimizations
