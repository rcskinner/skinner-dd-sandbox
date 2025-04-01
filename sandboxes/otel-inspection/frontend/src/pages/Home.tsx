import React from 'react';
import { Typography, Paper, Box } from '@mui/material';
import RequestSender from '../components/RequestSender';

const Home: React.FC = () => {
  return (
    <Box sx={{ width: '100%' }}>
      <Paper sx={{ p: 3 }}>
        <Typography variant="h4" gutterBottom>
          Welcome to OTel Inspection
        </Typography>
        <Typography variant="body1">
          This tool helps you inspect and analyze OpenTelemetry traces in your system.
        </Typography>
      </Paper>
      <RequestSender />
    </Box>
  );
};

export default Home; 