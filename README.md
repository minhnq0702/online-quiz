# Real-Time Vocabulary Quiz System
![Real-Time Vocabulary Quiz System](./online-quiz.drawio.png)

## 📌 Overview
This project is a solution to the **Real-Time Quiz Coding Challenge**, designed for an English learning application. The system provides a real-time quiz experience where users can answer questions, compete with others, and see their scores updated live on a leaderboard.

### 🔑 Key Features
- **Real-Time Participation**: Users can join a quiz session using a unique quiz ID.
- **Real-Time Score Updates**: Scores are updated instantly as users submit their answers.
- **Real-Time Leaderboard**: Displays current rankings of all participants, with real-time updates.

---

## 🛠️ Architecture
The system follows a microservices-based architecture designed for scalability, performance, and real-time capabilities.

### **Components**
1. **Quiz Service**: Manages the creation and management of quizzes.
3. **Answer Service**: Processes user answers, calculates scores, and handles re-answered questions.
4. **Leaderboard Service (Implemented)**: 
   - Tracks users' scores and rankings in real-time.
   - Adjusts scores if users change their answers.
   - Provides live updates on the leaderboard.

---

## 📚 Technologies Used
- **Backend Framework**: FastAPI (Python)
- **Database**: 
    - PosgreSQl: quiz question management
    - MongoDB: storing user answers and scores
- **Message Broker**: Kafka (real-time communication between services)
- **WebSocket**: For real-time leaderboard updates

---

## 🔄 Data Flow
1. Users join a quiz session by providing a `quiz_id`.
2. Users submit answers via the **Answer Service**:
   - If a user re-answers, the previous score is adjusted before recalculating the new score.
3. The score of the answer will be produced to Kafka with format:
    ```json
    {
        "quiz_id": "quiz123",
        "user_id": "user1",
        "score": 10
    }
4. The **Leaderboard Service** consumes events from kafka and updates scores and broadcasts real-time updates.
5. The leaderboard displays the top participants and the user's current rank.

---

## 🚀 Implementation
I implemented the **Leaderboard Service**, which handles:
- Real-time score tracking.
- Score adjustments when users answer/re-answer questions.
- Providing users with their current ranking on the leaderboard.

### **1. Quiz Service Details**
#### Database Schema
    ```json
    {

    }
### **2. Answer Service Details**
#### Databaes Schema
- **Answer Collections**:
    ```json
    {
        "user_id": "user1",
        "quiz_id": "quiz123",
        "question_id": "1",
        "answer": "A",
        "is_correct": true,
        "score": 10,
        "update_ts": "2024-11-10T10:15:30Z"
    }
### **3. Leaderboard Service Details**
#### Database Schema
- **Leaderboard Collection**:
    ```json
    {
        "user_id": "user1",
        "quiz_id": "quiz123",
        "score": 50
    }
#### Real-time functionality
- Users receive updates via WebSocket periodically for:
    - Currenly leaderboard default top 10 users
    - The user's current rank
