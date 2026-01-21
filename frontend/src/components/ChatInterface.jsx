import { useState, useRef, useEffect } from "react";
import api from "../services/api";
import "../styles/dashboard.css";

const ChatInterface = () => {
    const [messages, setMessages] = useState([
        { id: 1, sender: "bot", text: "Hello! I'm here to listen. How are you feeling today?", emotion: "neutral" }
    ]);
    const [input, setInput] = useState("");
    const [loading, setLoading] = useState(false);
    const messagesEndRef = useRef(null);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    };

    useEffect(() => {
        scrollToBottom();
    }, [messages]);

    const handleSend = async (e) => {
        e.preventDefault();
        if (!input.trim()) return;

        const userMessage = {
            id: Date.now(),
            sender: "user",
            text: input
        };

        setMessages((prev) => [...prev, userMessage]);
        setInput("");
        setLoading(true);

        try {
            const response = await api.post("/api/chat/analyze", { message: userMessage.text });

            const botMessage = {
                id: Date.now() + 1,
                sender: "bot",
                text: response.data.reply,
                emotion: response.data.emotion
            };

            setMessages((prev) => [...prev, botMessage]);
        } catch (error) {
            console.error("Chat Error:", error);
            const errorMessage = {
                id: Date.now() + 1,
                sender: "bot",
                text: "I'm having a little trouble connecting right now. Please try again.",
                emotion: "neutral"
            };
            setMessages((prev) => [...prev, errorMessage]);
        } finally {
            setLoading(false);
        }
    };

    const getEmotionEmoji = (emotion) => {
        const map = {
            happy: "😊",
            sad: "💙",
            fear: "🌱",
            angry: "😤",
            neutral: "🙂",
            crisis: "🆘"
        };
        return map[emotion] || "";
    };

    return (
        <div className="chat-interface">
            <div className="chat-header">
                <h3>AI Companion</h3>
                <span className="status-indicator">Online</span>
            </div>

            <div className="messages-list">
                {messages.map((msg) => (
                    <div key={msg.id} className={`message ${msg.sender}`}>
                        {msg.sender === "bot" && (
                            <div className="bot-avatar">
                                {getEmotionEmoji(msg.emotion)}
                            </div>
                        )}
                        <div className="message-content">
                            <p>{msg.text}</p>
                        </div>
                    </div>
                ))}
                {loading && (
                    <div className="message bot">
                        <div className="bot-avatar">⏳</div>
                        <div className="message-content typing">
                            <span>.</span><span>.</span><span>.</span>
                        </div>
                    </div>
                )}
                <div ref={messagesEndRef} />
            </div>

            <form className="chat-input-area" onSubmit={handleSend}>
                <input
                    type="text"
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    placeholder="Type your message..."
                    disabled={loading}
                />
                <button type="submit" disabled={loading || !input.trim()}>
                    Send
                </button>
            </form>
        </div>
    );
};

export default ChatInterface;
