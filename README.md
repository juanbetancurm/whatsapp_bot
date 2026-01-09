# 🗿 WhatsApp AI Bot - Simple & Smart Assistant

A functional WhatsApp bot powered by local AI that responds intelligently to messages in real-time. Built with Django, MySQL, ngrok, and Twilio.

---

## 🤖 What is This?

This is a **fully working WhatsApp chatbot** that:
- ✅ Receives messages from WhatsApp users
- 🧠 Processes them with a local AI model (phi3:mini)
- 💬 Sends intelligent, context-aware responses
- 💾 Stores all conversations in a MySQL database
- 📊 Provides an admin dashboard to monitor chats

**Tech Stack:** Django | MySQL | Ollama AI | Twilio | ngrok

---
## 🎯 Current Features

- ✅ Real-time WhatsApp message processing
- ✅ AI-powered responses (Spanish/English)
- ✅ Conversation history storage
- ✅ Admin dashboard for monitoring
- ✅ Error handling and fallback messages
- ✅ Processing time tracking
- ✅ Multi-user support

---

## 🚀 Next Steps (Coming Soon!)

### Phase 1: Specialized AI Training
- Train custom models for specific business tasks
- Implement RAG (Retrieval Augmented Generation) for domain-specific knowledge

### Phase 2: Schedule Assistant 📅
- **Goal:** Create a WhatsApp appointment scheduler
- **Features:**
  - Book/cancel/reschedule appointments via chat
  - Check availability
  - Send reminders
  - Calendar integration
  - Multi-business support (SaaS model)

### Phase 3: Recruiter's Assistant 👔
- **Goal:** AI bot that answers questions about me (Juan Betancur) for recruiters
- **Features:**
  - Trained on my CV and resume
  - Integrated with my GitHub profile
  - Answers questions about skills, experience, projects
  - Provides portfolio links
  - Schedules interview calls
  - Available 24/7 even when I'm sleeping! 😴

---
## 🎮 Try It Out!

Want to chat with my bot? Here's how:

### Step 1: Join the Sandbox
1. Open WhatsApp on your phone
2. Send a message to: **+1 415 523 8886**
3. Message content: `join friend-book`
4. Wait for confirmation ✅

### Step 2: Start Chatting!
Just send any message and get an AI-powered response!

**Try these:**
- `Hola` - Get a greeting in Spanish
- `¿Quién te integró a este backend Django?` - Ask about me
---

## ⚠️ Important Note (Read This!)

> **🤪 Plot Twist:** This bot runs on **my personal computer** and I used to move every day with it in my bag.
> 
> That means:
> - ⚡ When it's on, it responds in ~5-10 seconds
> - 😴 When my PC is off, the bot is taking a siesta
> - 🔌 If you get no response, try again later.

## 📊 Stats & Performance

- **Average Response Time:** 5-10 seconds
- **AI Model:** phi3:mini
- **Database:** MySQL with indexed conversations
- **Uptime:** Whenever my laptop is on 😅

---

## 🤓 What I Learned Building This

- ✅ Twilio WhatsApp API integration
- ✅ Webhook handling and ngrok tunneling  
- ✅ Local LLM deployment with Ollama
- ✅ Real-time message processing architecture
- ✅ Database design for conversational AI
- ✅ Error handling in async messaging systems

---

## 📝 License

MIT License - Feel free to use this project as a learning resource!
---

## 🏗️ Project Architecture
```
User's WhatsApp
      ↓
Twilio API (receives message)
      ↓
ngrok Tunnel (exposes my local PC to internet)
      ↓
Django Backend (processes message)
      ↓
AI Model (generates response)
      ↓
MySQL Database (stores conversation)
      ↓
Django sends response back through Twilio
      ↓
User receives AI response in WhatsApp
```

---

## 📂 Project Structure
```
whatsapp_bot/
├── chatbot/
│   ├── models.py           # Database models (Message)
│   ├── views.py            # Webhook & endpoints
│   ├── ollama_utils.py     # AI integration
│   ├── twilio_utils.py     # WhatsApp messaging
│   └── admin.py            # Admin dashboard
├── bot_project/
│   └── settings.py         # Django configuration
├── .env                    # Credentials (secret!)
└── manage.py               # Django management
```

---

## 🔧 How to Run This Locally (For Developers)

### Prerequisites
- Python 3.9+
- MySQL 8.0+
- Phi3:mini model
- Twilio account (free trial)
- ngrok account (free)

### Quick Setup
```bash
# 1. Clone and setup environment
git clone [your-repo]
cd whatsapp_bot
python -m venv venv
# Windows 
venv\Scripts\activate
# Or Mac/Linux:
source venv/bin/activate

pip install -r requirements.txt

# 2. Configure environment
# Create .env file with your Twilio credentials

# 3. Setup database
mysql -u root -p
CREATE DATABASE whatsapp_bot_db;
python manage.py migrate

# 4. Start services (3 separate terminals)
# Terminal 1: Ollama
ollama serve
#If it gives you an error telling it is already working, just run the model:
ollama run phi3:mini 

# Terminal 2: Django
python manage.py runserver

# Terminal 3: ngrok
ngrok http 8000

# 5. Configure Twilio webhook
# Copy your ngrok URL: https://your-url.ngrok-free.dev/webhook/
# Paste it in Twilio Console → Sandbox Settings
```

---



---

## 👨‍💻 Author

**Juan José Betancur**  
Math Teacher and Developer  

- 📍 Medellín, Colombia
- 💼 https://www.linkedin.com/in/juanjbetancur852/
- 📧 juan.jbetancur852@gmail.com

---

*Built with coffee and lots of trial & error in Medellín, Colombia*