import React, { useState, useEffect } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import {
  Box,
  TextField,
  Button,
  Typography,
  Paper,
  List,
  ListItem,
  ListItemText,
  CircularProgress,
} from '@mui/material';
import SendIcon from '@mui/icons-material/Send';
import { sendMessage, Message } from '../services/api';

const ChatPage: React.FC = () => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const location = useLocation();
  const navigate = useNavigate();

  useEffect(() => {
    const analysisResult = location.state?.analysisResult;
    if (analysisResult) {
      setMessages([
        {
          text: "Merhaba, test sonucunuz yüklendi. Bugün size nasıl yardımcı olabilirim?",
          isUser: false,
        },
      ]);
    } else {
      navigate('/');
    }
  }, [location, navigate]);

  const handleSend = async () => {
    if (!input.trim()) return;

    const userMessage: Message = { text: input, isUser: true };
    setMessages((prev) => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);

    try {
      const response = await sendMessage(input);
      setMessages((prev) => [
        ...prev,
        { text: response, isUser: false },
      ]);
    } catch (error) {
      console.error('Error sending message:', error);
      setMessages((prev) => [
        ...prev,
        {
          text: 'Mesaj gönderilirken bir hata oluştu. Lütfen tekrar deneyin.',
          isUser: false,
        },
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <Box
      sx={{
        display: 'flex',
        flexDirection: 'column',
        height: '100vh',
        p: 2,
      }}
    >
      <Typography variant="h4" gutterBottom>
        Kan Testi Analiz Sohbeti
      </Typography>
      <Paper
        sx={{
          flexGrow: 1,
          overflow: 'auto',
          mb: 2,
          p: 2,
        }}
      >
        <List>
          {messages.map((message, index) => (
            <ListItem
              key={index}
              sx={{
                justifyContent: message.isUser ? 'flex-end' : 'flex-start',
              }}
            >
              <Paper
                sx={{
                  p: 2,
                  backgroundColor: message.isUser ? 'primary.light' : 'grey.100',
                  maxWidth: '70%',
                }}
              >
                <ListItemText
                  sx={{
                    color: message.isUser ? 'white' : 'text.primary',
                  }}
                  primary={
                    <span
                      dangerouslySetInnerHTML={{ __html: message.text }}
                    />
                  }
                />
              </Paper>
            </ListItem>
          ))}
          {isLoading && (
            <ListItem sx={{ justifyContent: 'center' }}>
              <CircularProgress size={24} />
            </ListItem>
          )}
        </List>
      </Paper>
      <Box sx={{ display: 'flex', gap: 1 }}>
        <TextField
          fullWidth
          variant="outlined"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyPress={(e) => e.key === 'Enter' && handleSend()}
          disabled={isLoading}
        />
        <Button
          variant="contained"
          onClick={handleSend}
          disabled={isLoading || !input.trim()}
          endIcon={<SendIcon />}
        >
          Gönder
        </Button>
      </Box>
    </Box>
  );
};

export default ChatPage;
