# Saanchari - Andhra Pradesh Tourism Chatbot

## Overview

This project is a Streamlit-based tourism chatbot for Andhra Pradesh that leverages Google's Gemini AI for conversational interactions. The application provides multilingual support and focuses on helping users explore tourism information about Andhra Pradesh.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

The application follows a simple web-based architecture:

- **Frontend**: Streamlit web framework for the user interface
- **AI Backend**: Google Generative AI (Gemini 1.5 Flash model) for natural language processing
- **Translation Service**: Google Translate API for multilingual support
- **Deployment**: Single Python application with web interface

## Key Components

### 1. User Interface Layer
- **Technology**: Streamlit framework
- **Features**: Wide layout configuration, custom CSS styling
- **Components**: Main header, language selector, chat interface
- **Styling**: Custom CSS for enhanced visual appeal with color scheme (#07546B primary color)

### 2. AI Processing Layer
- **Model**: Google Gemini 1.5 Flash
- **Purpose**: Natural language understanding and response generation
- **Configuration**: API key-based authentication via environment variables

### 3. Translation Layer
- **Service**: Google Translate (googletrans library)
- **Languages Supported**: English, Hindi, Telugu
- **Implementation**: Real-time translation of user inputs and bot responses

### 4. Configuration Management
- **Environment Variables**: GEMINI_API_KEY for secure API access
- **Fallback**: Default key handling for development environments

## Data Flow

1. **User Input**: User selects language and enters tourism-related queries
2. **Translation**: If non-English, input is translated to English for processing
3. **AI Processing**: Gemini model processes the query and generates contextual responses
4. **Response Translation**: AI response is translated back to user's selected language
5. **Display**: Final response is presented in the Streamlit interface

## External Dependencies

### Core Libraries
- `streamlit`: Web application framework
- `google-generativeai`: Google Gemini AI integration
- `googletrans`: Translation services
- `PIL (Pillow)`: Image processing capabilities
- `python-dotenv`: Environment variable management

### External Services
- **Google Generative AI**: Primary AI service for chatbot functionality
- **Google Translate**: Language translation services

## Deployment Strategy

### Current Setup
- **Platform**: Web-based Streamlit application
- **Configuration**: Single `app.py` file with embedded styling
- **Environment**: Requires GEMINI_API_KEY environment variable

### Recommended Deployment
- **Platform**: Streamlit Cloud, Heroku, or similar web platforms
- **Requirements**: Python environment with dependency management
- **Security**: Environment-based API key management
- **Scalability**: Stateless design allows for horizontal scaling

### Development Considerations
- Application uses default API key fallback for development
- Custom CSS is embedded for styling consistency
- Wide layout configuration optimizes screen real estate usage
- Collapsed sidebar configuration for cleaner interface

## Architecture Decisions

### Technology Choices

**Streamlit Framework**
- *Problem*: Need for rapid web application development
- *Solution*: Streamlit for quick UI creation with minimal code
- *Rationale*: Enables fast prototyping and deployment of ML/AI applications

**Gemini 1.5 Flash Model**
- *Problem*: Requirement for intelligent conversational AI
- *Solution*: Google's latest Gemini model for enhanced capabilities
- *Rationale*: Balance between performance and cost-effectiveness

**Google Translate Integration**
- *Problem*: Need for multilingual support in regional context
- *Solution*: Established translation service with good accuracy
- *Rationale*: Reliable translation quality for tourism domain

### Design Patterns
- **Single Page Application**: Simplified user experience
- **Environment-based Configuration**: Security and flexibility
- **Component-based Styling**: Maintainable CSS organization