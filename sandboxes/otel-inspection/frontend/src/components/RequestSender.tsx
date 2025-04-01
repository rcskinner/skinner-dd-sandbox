import React, { useState } from 'react';
import { 
  Paper, 
  TextField, 
  Button, 
  Box, 
  Typography,
  Alert,
  Snackbar,
  Divider
} from '@mui/material';
import axios from 'axios';

// Function to add syntax highlighting
const formatJSON = (obj: any): React.ReactElement => {
  const json = JSON.stringify(obj, null, 2);
  return (
    <>
      {json.split('\n').map((line, i) => {
        // Handle key-value pairs
        const keyMatch = line.match(/^(\s*)"(.+)":/);
        if (keyMatch) {
          const [full, spaces, key] = keyMatch;
          const value = line.slice(full.length).trim();
          return (
            <div key={i} style={{ fontFamily: 'monospace' }}>
              {spaces}
              <span style={{ color: '#9cdcfe' }}>"{key}"</span>
              <span style={{ color: '#d4d4d4' }}>:</span>
              {value && (
                <>
                  {' '}
                  <span style={{ color: '#ce9178' }}>{value}</span>
                </>
              )}
            </div>
          );
        }
        // Handle braces and other lines
        return (
          <div key={i} style={{ fontFamily: 'monospace', color: '#d4d4d4' }}>
            {line}
          </div>
        );
      })}
    </>
  );
};

const RequestSender: React.FC = () => {
  const [message, setMessage] = useState('');
  const [status, setStatus] = useState<'idle' | 'success' | 'error'>('idle');
  const [errorMessage, setErrorMessage] = useState('');
  const [response, setResponse] = useState<any>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    // Temporary mock response for demonstration
    const mockResponse = {
      status: "success",
      message: message,
      timestamp: new Date().toISOString(),
      traceId: "mock-trace-" + Math.random().toString(36).substr(2, 9)
    };
    setStatus('success');
    setResponse(mockResponse);
    setMessage('');
    
    // Commented out until we have a backend
    /*try {
      const result = await axios.post('/api/traces', { message });
      setStatus('success');
      setMessage('');
      setResponse(result.data);
    } catch (error) {
      setStatus('error');
      setErrorMessage('Failed to send request. Please try again.');
      setResponse(null);
    }*/
  };

  return (
    <Paper sx={{ p: 3, mt: 3 }}>
      <Typography variant="h6" gutterBottom>
        Send Test Request
      </Typography>
      <Box component="form" onSubmit={handleSubmit} sx={{ display: 'flex', gap: 2 }}>
        <TextField
          fullWidth
          label="Request Message"
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          placeholder="Enter a message to generate a request"
        />
        <Button 
          variant="contained" 
          type="submit"
          disabled={!message}
        >
          Send
        </Button>
      </Box>

      {response && (
        <>
          <Divider sx={{ my: 2 }} />
          <Typography variant="subtitle1" gutterBottom>
            Response:
          </Typography>
          <Paper 
            variant="outlined" 
            sx={{ 
              p: 2, 
              bgcolor: '#1e1e1e',  // Dark background like VS Code
              maxHeight: '200px',
              overflow: 'auto'
            }}
          >
            {formatJSON(response)}
          </Paper>
        </>
      )}

      <Snackbar 
        open={status === 'success'} 
        autoHideDuration={3000} 
        onClose={() => setStatus('idle')}
      >
        <Alert severity="success" sx={{ width: '100%' }}>
          Request sent successfully!
        </Alert>
      </Snackbar>
      <Snackbar 
        open={status === 'error'} 
        autoHideDuration={3000} 
        onClose={() => setStatus('idle')}
      >
        <Alert severity="error" sx={{ width: '100%' }}>
          {errorMessage}
        </Alert>
      </Snackbar>
    </Paper>
  );
};

export default RequestSender; 