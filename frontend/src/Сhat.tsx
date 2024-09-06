import React, { useEffect, useState } from 'react';
import axios from 'axios';


interface Message {
    id: number;
    text: string;
}

const Chat: React.FC = () => {
    const [messages, setMessages] = useState<Message[]>([]);
    const [newMessage, setNewMessage] = useState<string>('');

    const fetchMessages = async () => {
        try {
            const response = await axios.get('http://your-ip-address/api/messages');
            setMessages(response.data);
        } catch (error) {
            console.error('Error fetching messages:', error);
        }
    };

    const sendMessage = async () => {
        if (newMessage.trim() === '') return;

        try {
            const response = await axios.post('http://your-ip-address/api/messages', {
                text: newMessage,
            });
            setMessages((prevMessages) => [...prevMessages, response.data]);
            setNewMessage('');
        } catch (error) {
            console.error('Error sending message:', error);
        }
    };

    useEffect(() => {
        fetchMessages();
        const interval = setInterval(fetchMessages, 5000);
        return () => clearInterval(interval);
    }, []);

    return (
        <div>
            <div>
                {messages.map((message) => (
                    <div key={message.id}>{message.text}</div>
                ))}
            </div>
            <input
                type="text"
                value={newMessage}
                onChange={(e) => setNewMessage(e.target.value)}
                placeholder="Enter your message"
            />
            <button onClick={sendMessage}>Send</button>
        </div>
    );
};

export default Chat;
