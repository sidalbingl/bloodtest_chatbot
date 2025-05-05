import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Box,
  Button,
  Card,
  CardContent,
  Typography,
  CircularProgress,
  Alert,
} from '@mui/material';
import CloudUploadIcon from '@mui/icons-material/CloudUpload';
import { uploadFile } from '../services/api';

const UploadPage: React.FC = () => {
  const [isUploading, setIsUploading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const navigate = useNavigate();

  const handleFileUpload = async (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (!file) return;

    setIsUploading(true);
    setError(null);

    try {
      const result = await uploadFile(file);
      navigate('/chat', { state: { analysisResult: result } });
    } catch (error) {
      console.error('Upload error:', error);
      setError(error instanceof Error ? error.message : 'Dosya yüklenirken bir hata oluştu. Lütfen tekrar deneyin.');
    } finally {
      setIsUploading(false);
    }
  };

  return (
    <Box
      sx={{
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        minHeight: '100vh',
        backgroundColor: '#f5f5f5',
        p: 3,
      }}
    >
      {error && (
        <Alert severity="error" onClose={() => setError(null)} sx={{ mb: 2 }}>
          {error}
        </Alert>
      )}
      <Card sx={{ maxWidth: 600, width: '100%', boxShadow: 3 }}>
        <CardContent>
          <Typography
            variant="h4"
            component="h2"
            gutterBottom
            align="center"
            sx={{ color: '#B22222' }}
          >
            Kan Testi sonuçlarınızı PDF formatında yükleyiniz
          </Typography>
          <Box
            sx={{
              display: 'flex',
              flexDirection: 'column',
              alignItems: 'center',
              gap: 2,
              mt: 2,
            }}
          >
            <input
              accept=".pdf"
              style={{ display: 'none' }}
              id="raised-button-file"
              type="file"
              onChange={handleFileUpload}
            />
            <label htmlFor="raised-button-file">
              <Button
                variant="contained"
                component="span"
                startIcon={<CloudUploadIcon />}
                disabled={isUploading}
                sx={{
                  backgroundColor: '#B22222',
                  '&:hover': { backgroundColor: '#A52A2A' },
                }}
              >
                {isUploading ? (
                  <CircularProgress size={24} color="inherit" />
                ) : (
                  'Dosya Seç'
                )}
              </Button>
            </label>
          </Box>
        </CardContent>
      </Card>
    </Box>
  );
};

export default UploadPage;