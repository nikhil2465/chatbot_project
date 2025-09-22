# Ullas Incense Chatbot

A modern, AI-powered chatbot for Ullas Incense that helps customers with product inquiries, order tracking, and general support.

## Features

- **AI-Powered Responses**: Uses OpenAI's GPT-4 model for natural language understanding
- **Responsive Design**: Works on both desktop and mobile devices
- **Session Management**: Remembers conversation context during the session
- **Quick Replies**: Predefined quick reply buttons for common queries
- **Easy Integration**: Simple to integrate with any website

## Prerequisites

- Python 3.8+
- Node.js (for frontend development, optional)
- OpenAI API key

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd ullas-chatbot
   ```

2. Create and activate a virtual environment:
   ```bash
   # Windows
   python -m venv venv
   .\venv\Scripts\activate

   # macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the project root and add your OpenAI API key:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   FLASK_APP=app.py
   FLASK_ENV=development
   FLASK_RUN_PORT=5001
   ```

## Running the Application

1. Start the Flask development server:
   ```bash
   flask run --port 5001
   ```

2. Open your web browser and navigate to:
   ```
   http://localhost:5001
   ```

## Project Structure

```
ullas-chatbot/
├── app.py                 # Main Flask application
├── static/
│   ├── css/
│   │   └── chatbot.css    # Chat widget styles
│   └── js/
│       └── chatbot.js     # Frontend chat logic
├── templates/
│   └── index.html         # Main page with chat widget
├── .env                   # Environment variables
├── requirements.txt       # Python dependencies
└── README.md
```

## Configuration

### Environment Variables

- `OPENAI_API_KEY`: Your OpenAI API key (required)
- `FLASK_APP`: The name of the Flask application (default: `app.py`)
- `FLASK_ENV`: The environment to run the app in (development/production)
- `FLASK_RUN_PORT`: The port to run the Flask app on (default: 5001)

## Customization

### Adding Products

Edit the `PRODUCT_CATALOG` dictionary in `app.py` to add or modify products.

### Styling

Customize the chat widget's appearance by modifying the CSS in `static/css/chatbot.css`.

### Behavior

Modify the system prompt in the `get_llm_response` function in `app.py` to change the chatbot's behavior and tone.

## Deployment

For production deployment, consider using:

1. **WSGI Server**: Gunicorn or uWSGI
2. **Reverse Proxy**: Nginx or Apache
3. **Process Manager**: systemd or Supervisor

Example with Gunicorn:
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5001 app:app
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [Flask](https://flask.palletsprojects.com/)
- [OpenAI](https://openai.com/)
- [Tailwind CSS](https://tailwindcss.com/) (for inspiration)
