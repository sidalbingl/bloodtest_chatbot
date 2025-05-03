import React, { useState, useEffect } from 'react';
import {
  Box,
  Card,
  CardContent,
  Typography,
  List,
  ListItem,
  ListItemText,
  ListItemSecondaryAction,
  IconButton,
  Divider,
  CircularProgress,
  Alert,
} from '@mui/material';
import DownloadIcon from '@mui/icons-material/Download';
import DeleteIcon from '@mui/icons-material/Delete';
import { AnalysisResult, getHistory } from '../services/api';

const HistoryPage: React.FC = () => {
  const [history, setHistory] = useState<AnalysisResult[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchHistory = async () => {
      try {
        const data = await getHistory();
        setHistory(data);
      } catch (error) {
        console.error('History fetch error:', error);
        setError('Geçmiş verileri yüklenirken bir hata oluştu.');
      } finally {
        setIsLoading(false);
      }
    };

    fetchHistory();
  }, []);

  const handleDownload = (id: string) => {
    // TODO: Implement download functionality
    console.log('Downloading analysis:', id);
  };

  const handleDelete = (id: string) => {
    // TODO: Implement delete functionality
    console.log('Deleting analysis:', id);
  };

  if (isLoading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="200px">
        <CircularProgress />
      </Box>
    );
  }

  if (error) {
    return (
      <Alert severity="error" onClose={() => setError(null)}>
        {error}
      </Alert>
    );
  }

  return (
    <Box>
      <Typography variant="h5" gutterBottom>
        Analiz Geçmişi
      </Typography>
      <Card>
        <CardContent>
          <List>
            {history.map((item, index) => (
              <React.Fragment key={item.id}>
                <ListItem>
                  <ListItemText
                    primary={item.fileName}
                    secondary={
                      <>
                        <Typography component="span" variant="body2" color="text.primary">
                          {item.date}
                        </Typography>
                        {` — ${item.summary}`}
                      </>
                    }
                  />
                  <ListItemSecondaryAction>
                    <IconButton
                      edge="end"
                      aria-label="download"
                      onClick={() => handleDownload(item.id)}
                    >
                      <DownloadIcon />
                    </IconButton>
                    <IconButton
                      edge="end"
                      aria-label="delete"
                      onClick={() => handleDelete(item.id)}
                    >
                      <DeleteIcon />
                    </IconButton>
                  </ListItemSecondaryAction>
                </ListItem>
                {index < history.length - 1 && <Divider />}
              </React.Fragment>
            ))}
          </List>
        </CardContent>
      </Card>
    </Box>
  );
};

export default HistoryPage; 