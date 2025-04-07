// Refactored Dashboard with Copilot Readiness Brief, Summary Cards, and Slide-Out Detail View
import React, { useState } from 'react';
import { Box, Grid, Paper, Typography, Drawer, Divider, LinearProgress, IconButton } from '@mui/material';
import CloseIcon from '@mui/icons-material/Close';
import InfoIcon from '@mui/icons-material/Info';

// Mock summary and detail data
const assessments = [
  {
    key: 'Five Ws',
    titleBold: 'Scientific Intent',
    titleLight: 'The 5 Ws of a definitive experiment',
    tagline: 'Clarify who, what, when, where, and why of your trial.',
    summaryScores: { completeness: 80, confidence: 70 },
    data: {
      who: { progress: 85, confidence: 'High', desc: 'Inclusion/exclusion criteria' },
      what: { progress: 90, confidence: 'High', desc: 'Intervention and endpoints' },
    }
  },
  {
    key: 'Five Rights',
    titleBold: 'Clinical Precision',
    titleLight: 'Targeted design for the right patients, endpoints, and timing',
    tagline: 'Align eligibility, intervention, and outcomes for mechanistic fit.',
    summaryScores: { completeness: 78, confidence: 65 },
    data: {
      'Right Patient': { progress: 50, confidence: 'High', desc: 'Eligibility criteria' },
      'Right Drug': { progress: 85, confidence: 'High', desc: 'Therapeutic match' },
    }
  },
  // ... add the rest of your assessment sections here
];

const CopilotReadinessBrief = () => (
  <Paper sx={{ p: 3, mb: 4 }}>
    <Typography variant="h6" fontWeight="bold">Copilot Readiness Brief</Typography>
    <Typography variant="subtitle2" color="text.secondary">Progress insights, next moves, and design sensitivities</Typography>
    <Divider sx={{ my: 2 }} />
    <Typography variant="body1" fontWeight={600}>Current Snapshot</Typography>
    <Typography variant="body2" mb={2}>
      Your trial synopsis is shaping into a clear and pragmatic design. Several components show growing clarity, while others remain adaptable — as expected at this stage.
    </Typography>
    <Typography variant="body1" fontWeight={600}>Recommended Next Moves</Typography>
    <ul>
      <li><Typography variant="body2">Refine eligibility criteria for target population</Typography></li>
      <li><Typography variant="body2">Align outcomes with stakeholder expectations</Typography></li>
      <li><Typography variant="body2">Map operational constraints into resource planning</Typography></li>
    </ul>
    <Typography variant="body1" fontWeight={600} mt={2}>Design Sensitivities to Explore</Typography>
    <ul>
      <li><Typography variant="body2">Validate endpoints against payer/regulator needs</Typography></li>
      <li><Typography variant="body2">Test recruitment assumptions across geographies</Typography></li>
    </ul>
  </Paper>
);

const AssessmentCard = ({ item, onOpen }) => (
  <Paper sx={{ p: 2, height: '100%', position: 'relative', cursor: 'pointer' }} onClick={() => onOpen(item)}>
    <Typography variant="h6" sx={{ fontWeight: 'bold', fontSize: '0.9rem' }}>
      {item.titleBold}{' '}
      <Typography component="span" sx={{ fontWeight: 'regular', color: 'text.secondary' }}>{item.titleLight}</Typography>
    </Typography>
    <Typography variant="body2" sx={{ color: 'text.secondary', fontStyle: 'italic', mt: 0.5 }}>{item.tagline}</Typography>
    <Divider sx={{ my: 2 }} />
    <Typography variant="body2" fontWeight={500}>Definition Completeness</Typography>
    <LinearProgress value={item.summaryScores.completeness} variant="determinate" sx={{ height: 8, borderRadius: 4, mb: 2 }} />
    <Typography variant="body2" fontWeight={500}>Confidence</Typography>
    <LinearProgress value={item.summaryScores.confidence} variant="determinate" sx={{ height: 8, borderRadius: 4 }} />
    <IconButton size="small" sx={{ position: 'absolute', top: 8, right: 8 }}><InfoIcon fontSize="small" /></IconButton>
  </Paper>
);

const AssessmentDetailDrawer = ({ item, onClose }) => (
  <Drawer anchor="right" open={!!item} onClose={onClose} PaperProps={{ sx: { width: '400px', p: 3 } }}>
    {item && (
      <>
        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <Typography variant="h6">{item.titleBold} <span style={{ fontWeight: 300, color: '#777' }}>{item.titleLight}</span></Typography>
          <IconButton onClick={onClose}><CloseIcon /></IconButton>
        </Box>
        <Typography variant="body2" sx={{ fontStyle: 'italic', color: 'text.secondary', mt: 1 }}>{item.tagline}</Typography>
        <Divider sx={{ my: 2 }} />
        {Object.entries(item.data).map(([key, value]) => (
          <Box key={key} mb={2}>
            <Typography variant="body2" fontWeight={500}>{key}</Typography>
            <Typography variant="caption" color="text.secondary">{value.desc}</Typography>
            <LinearProgress value={value.progress} variant="determinate" sx={{ height: 6, borderRadius: 3, my: 1 }} />
            <Typography variant="caption" color="text.secondary">Confidence: {value.confidence}</Typography>
          </Box>
        ))}
      </>
    )}
  </Drawer>
);

const Dashboard = () => {
  const [selectedItem, setSelectedItem] = useState(null);

  return (
    <Box sx={{ p: 4 }}>
      <CopilotReadinessBrief />
      <Grid container spacing={3}>
        {assessments.map(item => (
          <Grid item xs={12} sm={6} md={4} key={item.key}>
            <AssessmentCard item={item} onOpen={setSelectedItem} />
          </Grid>
        ))}
      </Grid>
      <AssessmentDetailDrawer item={selectedItem} onClose={() => setSelectedItem(null)} />
    </Box>
  );
};

export default Dashboard;
