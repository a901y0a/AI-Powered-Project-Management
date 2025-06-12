import axios from 'axios';
import { useState } from 'react';
import { useAuth } from '../context/AuthContext';
import '../styles/chatbot.css';

const Chatbot = () => {
  const { auth } = useAuth();
  const [input, setInput] = useState('');
  const [messages, setMessages] = useState([
    { role: 'system', text: '🔍 Ask a question about your database (or type "exit" to quit):' }
  ]);

  const sendMessage = async () => {
    if (!input.trim()) return;

    setMessages(prev => [...prev, { role: 'user', text: input }]);
    const userInput = input;
    setInput('');

    try {
      const res = await axios.post(
        'http://127.0.0.1:8000/api/run',
        { query: userInput },
        {
          headers: {
            Authorization: `Bearer ${auth.token}`
          }
        }
      );

      setMessages(prev => [
        ...prev,
        { role: 'bot', text: res.data.response }
      ]);
    } catch {
      setMessages(prev => [
        ...prev,
        { role: 'bot', text: '❌ Error occurred while processing your request.' }
      ]);
    }
  };

  return (
    <div className="chatbot">
      <h2 className="chat-title">ProjectAI Chatbot</h2>
      <div className="chat-window">
        {messages.map((msg, i) => (
          <div key={i} className={`message ${msg.role}`}>{msg.text}</div>
        ))}
      </div>
      <div className="input-area">
        <input
          value={input}
          onChange={e => setInput(e.target.value)}
          onKeyDown={e => e.key === 'Enter' && !e.shiftKey && sendMessage()}
          placeholder="Ask me anything..."
        />
        <button onClick={sendMessage}>Send</button>
      </div>
    </div>
  );
};

export default Chatbot;
