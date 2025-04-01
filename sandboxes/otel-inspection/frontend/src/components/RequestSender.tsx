import React, { useState, ReactElement } from 'react';
import { 
  Paper, 
  Button, 
  Box, 
  Typography,
  Alert,
  Snackbar,
  Stack,
  Divider,
  IconButton,
  Grid
} from '@mui/material';
import KeyboardArrowDownIcon from '@mui/icons-material/KeyboardArrowDown';
import KeyboardArrowRightIcon from '@mui/icons-material/KeyboardArrowRight';
import { getTraces, triggerError } from '../services/api';

interface RequestMetadata {
  timestamp: string;
  endpoint: string;
  method: string;
  status: number | null;
  duration: number | null;
}

const RequestMetadataDisplay: React.FC<{ metadata: RequestMetadata }> = ({ metadata }) => (
  <Box sx={{ mt: 2, mb: 2 }}>
    <Typography variant="subtitle2" color="text.secondary" gutterBottom>
      Request Metadata
    </Typography>
    <Paper variant="outlined" sx={{ p: 2, bgcolor: '#1e1e1e' }}>
      <Stack spacing={1}>
        <Typography variant="body2" fontFamily="monospace">
          Timestamp: {metadata.timestamp}
        </Typography>
        <Typography variant="body2" fontFamily="monospace">
          Endpoint: {metadata.endpoint}
        </Typography>
        <Typography variant="body2" fontFamily="monospace">
          Method: {metadata.method}
        </Typography>
        <Typography variant="body2" fontFamily="monospace">
          Status: {metadata.status !== null ? metadata.status : 'N/A'}
        </Typography>
        <Typography variant="body2" fontFamily="monospace">
          Duration: {metadata.duration !== null ? `${metadata.duration.toFixed(2)}ms` : 'N/A'}
        </Typography>
      </Stack>
    </Paper>
  </Box>
);

const JSONDisplay: React.FC<{ data: any }> = ({ data }) => {
  // Only track top-level keys for collapsing
  const [expandedTopLevelKeys, setExpandedTopLevelKeys] = useState<Set<string>>(new Set());

  const formatValue = (value: any): string => {
    if (typeof value === 'string') {
      return `"${value}"`;
    }
    return JSON.stringify(value);
  };

  const toggleExpand = (key: string) => {
    setExpandedTopLevelKeys(prev => {
      const next = new Set(prev);
      if (next.has(key)) {
        next.delete(key);
      } else {
        next.add(key);
      }
      return next;
    });
  };

  const renderCollapsibleButton = (key: string, isExpanded: boolean) => (
    <IconButton
      size="small"
      onClick={() => toggleExpand(key)}
      sx={{ 
        padding: '0px',
        marginRight: '4px',
        color: '#D4D4D4',
        '&:hover': {
          backgroundColor: 'rgba(255, 255, 255, 0.08)'
        }
      }}
    >
      {isExpanded ? <KeyboardArrowDownIcon /> : <KeyboardArrowRightIcon />}
    </IconButton>
  );

  const renderJSON = (obj: any, indent: number = 0, path: string = ''): ReactElement[] => {
    return Object.entries(obj).map(([key, value], index) => {
      const isLast = index === Object.entries(obj).length - 1;
      const comma = isLast ? '' : ',';
      const isTopLevel = path === '';
      const isExpanded = isTopLevel ? expandedTopLevelKeys.has(key) : true;
      
      if (value === null) {
        return (
          <Box key={key} sx={{ marginLeft: `${indent * 20}px` }}>
            <span style={{ color: '#9CDCFE' }}>{`"${key}"`}</span>
            <span style={{ color: '#D4D4D4' }}>: </span>
            <span style={{ color: '#569CD6' }}>null</span>
            {comma}
          </Box>
        );
      }
      
      if (typeof value === 'object' && !Array.isArray(value)) {
        const preview = isExpanded ? null : (
          <Typography component="span" sx={{ color: '#D4D4D4' }}>
            {' {'} ... {`}${comma}`}
          </Typography>
        );

        return (
          <Box key={key}>
            <Box sx={{ marginLeft: `${indent * 20}px`, display: 'flex', alignItems: 'center' }}>
              {isTopLevel && renderCollapsibleButton(key, isExpanded)}
              <Typography component="span" sx={{ color: '#9CDCFE' }}>{`"${key}"`}</Typography>
              <Typography component="span" sx={{ color: '#D4D4D4' }}>: {'{'}</Typography>
              {preview}
            </Box>
            {isExpanded && (
              <>
                {renderJSON(value, indent + 1, path + key + '.')}
                <Box sx={{ marginLeft: `${indent * 20}px` }}>
                  {`}${comma}`}
                </Box>
              </>
            )}
          </Box>
        );
      }

      if (Array.isArray(value)) {
        const preview = isExpanded ? null : (
          <Typography component="span" sx={{ color: '#D4D4D4' }}>
            {' ['} ... {`]${comma}`}
          </Typography>
        );

        return (
          <Box key={key}>
            <Box sx={{ marginLeft: `${indent * 20}px`, display: 'flex', alignItems: 'center' }}>
              {isTopLevel && renderCollapsibleButton(key, isExpanded)}
              <Typography component="span" sx={{ color: '#9CDCFE' }}>{`"${key}"`}</Typography>
              <Typography component="span" sx={{ color: '#D4D4D4' }}>: [</Typography>
              {preview}
            </Box>
            {isExpanded && (
              <>
                {value.map((item, i) => (
                  <Box key={i} sx={{ marginLeft: `${(indent + 1) * 20}px` }}>
                    {typeof item === 'object' ? (
                      <>
                        <Box>{`{`}</Box>
                        {renderJSON(item, indent + 2, path + key + '.' + i)}
                        <Box>{`}${i === value.length - 1 ? '' : ','}`}</Box>
                      </>
                    ) : (
                      <Typography component="span" sx={{ color: '#CE9178' }}>
                        {formatValue(item)}{i === value.length - 1 ? '' : ','}
                      </Typography>
                    )}
                  </Box>
                ))}
                <Box sx={{ marginLeft: `${indent * 20}px` }}>
                  {`]${comma}`}
                </Box>
              </>
            )}
          </Box>
        );
      }

      return (
        <Box key={key} sx={{ marginLeft: `${indent * 20}px` }}>
          <Typography component="span" sx={{ color: '#9CDCFE' }}>{`"${key}"`}</Typography>
          <Typography component="span" sx={{ color: '#D4D4D4' }}>: </Typography>
          <Typography component="span" sx={{ color: typeof value === 'string' ? '#CE9178' : '#B5CEA8' }}>
            {formatValue(value)}
          </Typography>
          {comma}
        </Box>
      );
    });
  };

  return (
    <Box sx={{ 
      fontFamily: 'Consolas, monospace',
      fontSize: '14px',
      lineHeight: '1.5'
    }}>
      {`{`}
      {renderJSON(data)}
      {`}`}
    </Box>
  );
};

const RequestSender: React.FC = () => {
  const [status, setStatus] = useState<'idle' | 'loading' | 'success' | 'error'>('idle');
  const [errorMessage, setErrorMessage] = useState('');
  const [response, setResponse] = useState<any>(null);
  const [requestMetadata, setRequestMetadata] = useState<RequestMetadata | null>(null);

  const updateRequestMetadata = (endpoint: string, method: string, startTime: number, statusCode: number) => {
    const endTime = performance.now();
    setRequestMetadata({
      timestamp: new Date().toISOString(),
      endpoint,
      method,
      status: statusCode,
      duration: endTime - startTime
    });
  };

  const handleFetchTraces = async (e: React.FormEvent) => {
    e.preventDefault();
    setStatus('loading');
    const startTime = performance.now();
    
    try {
      const result = await getTraces();
      setStatus('success');
      setResponse(result);
      updateRequestMetadata('/', 'GET', startTime, 200);
    } catch (error: any) {
      setStatus('error');
      setErrorMessage('Failed to fetch traces. Please try again.');
      setResponse(null);
      updateRequestMetadata('/', 'GET', startTime, error.response?.status || 500);
    }
  };

  const handleTriggerError = async (e: React.FormEvent) => {
    e.preventDefault();
    setStatus('loading');
    const startTime = performance.now();
    
    try {
      await triggerError();
    } catch (error: any) {
      setStatus('error');
      setResponse(error.response?.data || { message: 'An error occurred' });
      updateRequestMetadata('/error', 'GET', startTime, error.response?.status || 500);
    }
  };

  return (
    <Paper sx={{ p: 3, mt: 3, minHeight: '80vh' }}>
      <Box sx={{ display: 'grid', gap: 3, gridTemplateColumns: { xs: '1fr', md: '4fr 8fr', lg: '3fr 9fr' } }}>
        {/* Left sidebar with controls */}
        <Box>
          <Typography variant="h6" gutterBottom>
            API Endpoints
          </Typography>
          <Stack spacing={2}>
            <Button 
              variant="contained" 
              onClick={handleFetchTraces}
              disabled={status === 'loading'}
              fullWidth
            >
              {status === 'loading' ? 'Loading...' : 'Fetch Traces'}
            </Button>
            <Button 
              variant="contained" 
              color="error"
              onClick={handleTriggerError}
              disabled={status === 'loading'}
              fullWidth
            >
              {status === 'loading' ? 'Loading...' : 'Trigger Error'}
            </Button>
            
            {requestMetadata && <RequestMetadataDisplay metadata={requestMetadata} />}

            {status === 'error' && (
              <Alert severity="error">
                {errorMessage}
              </Alert>
            )}
          </Stack>
        </Box>

        {/* Main content area with JSON display */}
        <Box>
          {response ? (
            <Paper 
              variant="outlined" 
              sx={{ 
                p: 2, 
                bgcolor: '#1e1e1e',
                height: { xs: '50vh', md: '75vh' },
                overflow: 'auto'
              }}
            >
              <JSONDisplay data={response} />
            </Paper>
          ) : (
            <Box 
              sx={{ 
                height: { xs: '50vh', md: '75vh' },
                display: 'flex', 
                alignItems: 'center', 
                justifyContent: 'center',
                bgcolor: '#1e1e1e',
                borderRadius: 1,
                border: '1px solid rgba(255, 255, 255, 0.12)'
              }}
            >
              <Typography variant="body1" color="text.secondary">
                No trace data to display. Click "Fetch Traces" to begin.
              </Typography>
            </Box>
          )}
        </Box>
      </Box>

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