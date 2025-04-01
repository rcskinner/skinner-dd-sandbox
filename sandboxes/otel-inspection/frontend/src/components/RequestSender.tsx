import React, { useState } from 'react';
import { 
  Paper, 
  Button, 
  Box, 
  Typography,
  Alert,
  Snackbar,
  Stack
} from '@mui/material';
import { getTraces, triggerError } from '../services/api';

const RequestSender: React.FC = () => {
  const [status, setStatus] = useState<'idle' | 'loading' | 'success' | 'error'>('idle');
  const [errorMessage, setErrorMessage] = useState('');
  const [response, setResponse] = useState<any>(null);

  const handleFetchTraces = async (e: React.FormEvent) => {
    e.preventDefault();
    setStatus('loading');
    
    try {
      const result = await getTraces();
      setStatus('success');
      setResponse(result);
    } catch (error) {
      setStatus('error');
      setErrorMessage('Failed to fetch traces. Please try again.');
      setResponse(null);
    }
  };

  const handleTriggerError = async (e: React.FormEvent) => {
    e.preventDefault();
    setStatus('loading');
    
    try {
      await triggerError();
    } catch (error: any) {
      setStatus('error');
      setResponse(error.response?.data || { message: 'An error occurred' });
    }
  };

  return (
    <Paper sx={{ p: 3, mt: 3 }}>
      <Typography variant="h6" gutterBottom>
        API Endpoints
      </Typography>
      <Stack direction="row" spacing={2} sx={{ mb: 3 }}>
        <Button 
          variant="contained" 
          onClick={handleFetchTraces}
          disabled={status === 'loading'}
        >
          {status === 'loading' ? 'Loading...' : 'Fetch Traces'}
        </Button>
        <Button 
          variant="contained" 
          color="error"
          onClick={handleTriggerError}
          disabled={status === 'loading'}
        >
          {status === 'loading' ? 'Loading...' : 'Trigger Error'}
        </Button>
      </Stack>

      {status === 'error' && (
        <Alert severity="error" sx={{ mb: 2 }}>
          {errorMessage}
        </Alert>
      )}

      {response && (
        <Paper 
          variant="outlined" 
          sx={{ 
            p: 2, 
            bgcolor: '#1e1e1e',  // Dark background like VS Code
            maxHeight: '500px',
            overflow: 'auto'
          }}
        >
          <pre style={{ margin: 0, color: '#d4d4d4', fontFamily: 'monospace' }}>
            {JSON.stringify(response, null, 2)}
          </pre>
        </Paper>
      )}

      <Snackbar 
        open={status === 'success'} 
        autoHideDuration={6000} 
        onClose={() => setStatus('idle')}
      >
        <Alert severity="success" onClose={() => setStatus('idle')}>
          Traces fetched successfully
        </Alert>
      </Snackbar>
    </Paper>
  );
};

export default RequestSender; 