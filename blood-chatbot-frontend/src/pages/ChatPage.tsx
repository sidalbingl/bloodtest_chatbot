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
        alignItems: 'center',
        height: '100vh',
        backgroundColor: '#ffffff',
        p: 2,
      }}
    >
      <Box
        component="img"
        src={require('../kantest.jpeg')} // Correctly reference the image
        alt="Kan Testi Analiz"
        sx={{
          width: '120px', // Adjust the width
          height: '120px', // Adjust the height
          marginBottom: 2, // Add spacing below the image
        }}
      />
      <Paper
        sx={{
          flexGrow: 1,
          overflow: 'auto',
          p: 2,
          boxShadow: 3,
          backgroundColor: '#ffffff',
          maxHeight: '70vh',
          width: '70%',
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
                  backgroundColor: message.isUser ? '#F08080' : 'grey.100', // Change user message background to light red
                  maxWidth: '70%',
                  color: 'text.primary', // Revert text color to black
                  boxShadow: 2,
                }}
              >
                <ListItemText
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
      <Box
        sx={{
          display: 'flex',
          justifyContent: 'center',
          alignItems: 'center',
          gap: 1,
          mt: 3,
          width: '70%',
        }}
      >
        <TextField
          fullWidth
          variant="outlined"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyPress={(e) => e.key === 'Enter' && handleSend()}
          disabled={isLoading}
          sx={{
            backgroundColor: '#ffffff',
            borderRadius: 2,
            boxShadow: 1,
            height: '56px',
            '&:hover .MuiOutlinedInput-root': {
              borderColor: 'black', // Border turns black on hover
            },
            '& .MuiOutlinedInput-root.Mui-focused': {
              borderColor: 'blue', // Border turns blue when clicked
            },
          }}
        />
        <Button
          variant="contained"
          onClick={handleSend}
          disabled={isLoading || !input.trim()}
          endIcon={<SendIcon />}
          sx={{
            backgroundColor: input.trim() ? '#B22222' : 'grey.500', // Change to red when text is entered
            borderRadius: 2,
            fontSize: '1.2rem',
            padding: '12px 24px',
            height: '56px',
            '&:hover': {
              backgroundColor: input.trim() ? '#A52A2A' : 'grey.500', // Slightly darker red on hover
            },
            '&:focus': { borderColor: '#B22222', borderWidth: '2px' }, // Change focus border color to red
          }}
        >
          Gönder
        </Button>
      </Box>
    </Box>
  );
};

export default ChatPage;
