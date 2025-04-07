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
  const CustomTooltip = ({ active, payload, label }) => {
    if (active && payload && payload.length) {
      return (
        <>
          <Paper sx={{ p: 1, backgroundColor: 'rgba(255, 255, 255, 0.9)' }}>
            <Typography variant="body2">Month: {Math.round(label)}</Typography>
            <Typography variant="body2" sx={{ color: '#8884d8' }}>
              Revenue: ${payload[0].value.toFixed(2)}M
            </Typography>
            <Typography variant="body2" sx={{ color: '#82ca9d' }}>
              Cumulative Value: ${payload[1].value.toFixed(2)}M
            </Typography>
          </Paper>
        </>
      );
    }
    return null;
  };

  

  const [selectedItem, setSelectedItem] = useState(null);

  return (
    <Box sx={{ p: 4 }}>
      <Paper
    sx={{
      p: 2,
      height: '100%',
      boxShadow: 2,
      display: 'flex',
      flexDirection: 'column',
      minWidth: '280px',
      flex: 1,
    }}
  >
    {/* Title and tagline */}
    <Box mb={1}>
      <Typography variant="h6" component="div" sx={{ fontWeight: 'bold', fontSize: '0.9rem' }}>
        {titleBold}{' '}
        <Typography component="span" sx={{ fontWeight: 'regular', color: 'text.secondary' }}>
          {titleLight}
        </Typography>
      </Typography>
      {tagline && (
        <Typography variant="body2" sx={{ color: 'text.secondary', fontStyle: 'italic', mt: 1 }}>
          {tagline}
        </Typography>
      )}
    </Box>

    {/* Divider between title and progress bars */}
    <Divider sx={{ mb: 2 }} />

    {/* Progress bars and data */}
    <Box sx={{ flex: 1 }}>
      {Object.entries(data).map(([key, value]) => (
        <Box key={key} sx={{ mb: 1.5 }}>
          <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 0.5 }}>
            <Typography variant="body2" sx={{ fontWeight: 500, fontSize: '0.8rem' }}>
              {key}
              <Typography
                component="span"
                sx={{
                  display: 'block',
                  fontSize: '0.7rem',
                  color: 'text.secondary',
                  fontStyle: 'italic',
                }}
              >
                {value.desc}
              </Typography>
            </Typography>
            <Typography
              variant="body2"
              sx={{
                fontSize: '0.8rem',
                color:
                  value.confidence === 'High'
                    ? 'success.main'
                    : value.confidence === 'Medium'
                      ? 'warning.main'
                      : 'error.main',
              }}
            >
              {value.confidence}
            </Typography>
          </Box>

          {/* Progress bar */}
          <LinearProgress
            variant="determinate"
            value={value.progress}
            sx={{
              height: 6,
              borderRadius: 3,
              backgroundColor: '#e0e0e0',
              '& .MuiLinearProgress-bar': {
                backgroundColor:
                  value.confidence === 'High'
                    ? '#4caf50'
                    : value.confidence === 'Medium'
                      ? '#ff9800'
                      : '#f44336',
              },
            }}
          />
        </Box>
      ))}
    </Box>
  </Paper>
);

// In your chart component
const CustomTooltip = ({ active, payload, label }) => {
  if (active && payload && payload.length) {
    return (
      <Paper sx={{ p: 1, backgroundColor: 'rgba(255, 255, 255, 0.9)' }}>
        <Typography variant="body2">Month: {Math.round(label)}</Typography>
        <Typography variant="body2" sx={{ color: '#8884d8' }}>
          Revenue: ${payload[0].value.toFixed(2)}M
        </Typography>
        <Typography variant="body2" sx={{ color: '#82ca9d' }}>
          Cumulative Value: ${payload[1].value.toFixed(2)}M
        </Typography>
      </Paper>
    );
  }
  return null;
};

// Diamond marker component for milestones
const DiamondMarker = ({ cx, cy }) => (
  <polygon
    points={`${cx},${cy - 6} ${cx + 6},${cy} ${cx},${cy + 6} ${cx - 6},${cy}`}
    fill="#ff7300"
    stroke="#fff"
  />
);

export default function Dashboard() {
  return (
    <Box
      sx={{
        width: '100vw',
        minHeight: '100vh',
        backgroundColor: '#f5f5f5',
        margin: -3,
        padding: 3,
      }}
    >
      <Typography variant="h3" gutterBottom sx={{ fontWeight: 600, color: '#1a237e' }}>
        Clinical Development Dashboard
      </Typography>

      {/* Combined Timeline and Revenue Chart */}
      <Paper sx={{ p: 3, mb: 3, width: '100%', boxShadow: 2 }}>
        <Typography variant="h4" gutterBottom sx={{ fontWeight: 600, color: '#1a237e' }}>
          Development Forecast & Market Trajectory
        </Typography>
        <Typography variant="body1" sx={{ mb: 2, color: '#555' }}>
          This projection visualizes the estimated development timeline and potential revenue
          trajectory based on the current state of your trial synopsis. It reflects how clinical
          design decisions affect time-to-market and commercial outcomes. As the Copilot iteratively
          refines your design inputs, this projection dynamically updates to show the stakes,
          timing, and potential impact of strategic trial adjustments.
        </Typography>
        <Typography variant="h6" gutterBottom sx={{ fontWeight: 600 }}>
          Development Timeline, Revenue Projections and Cumulative Value Creation
        </Typography>
        <Box sx={{ width: '100%', height: 400, mb: 4 }}>
          <ResponsiveContainer width="100%" height="100%">
            <LineChart
              data={generateTimelineData()}
              margin={{ top: 40, right: 50, left: 50, bottom: 60 }}
            >
              <CartesianGrid strokeDasharray="3 3" stroke="#cccccc" />
              <XAxis
                dataKey="time"
                type="number"
                domain={['dataMin', 'dataMax']}
                tickFormatter={value => {
                  const actualTime = unscaleTime(value);
                  return Math.round(actualTime);
                }}
                label={{
                  value: 'Months from Start',
                  position: 'bottom',
                  offset: 0,
                  style: {
                    fontWeight: 500,
                    fontSize: '14px',
                    fill: '#333333',
                  },
                }}
                tick={{
                  fontSize: 12,
                  fontWeight: 500,
                  fill: '#333333',
                }}
                ticks={generateTimelineData()
                  .filter(point => point.milestone)
                  .map(point => point.time)}
              />
              <YAxis
                yAxisId="left"
                label={{
                  value: 'Revenue ($M)',
                  angle: -90,
                  position: 'insideLeft',
                  offset: -10,
                  style: {
                    fontWeight: 500,
                    fontSize: '14px',
                    fill: '#333333',
                  },
                }}
                tick={{
                  fontSize: 12,
                  fontWeight: 500,
                  fill: '#333333',
                }}
                tickFormatter={value => `$${value.toFixed(0)}M`}
              />
              <YAxis
                yAxisId="right"
                orientation="right"
                label={{
                  value: 'Cumulative Value ($M)',
                  angle: 90,
                  position: 'insideRight',
                  offset: 0,
                  style: {
                    fontWeight: 500,
                    fontSize: '14px',
                    fill: '#333333',
                  },
                }}
                tick={{
                  fontSize: 12,
                  fontWeight: 500,
                  fill: '#333333',
                }}
                tickFormatter={value => `$${(value / 1_000).toFixed(1)}T`}
              />
              <Tooltip
                content={<CustomTooltip />}
                labelFormatter={value => `Month ${Math.round(unscaleTime(value))}`}
              />
              <Legend
                verticalAlign="bottom"
                align="center"
                wrapperStyle={{
                  fontSize: '14px',
                  fontWeight: 500,
                  color: '#333333',
                  paddingTop: '20px',
                }}
              />
              <Line
                yAxisId="left"
                type="monotone"
                dataKey="revenue"
                stroke="#4051B5"
                strokeWidth={2.5}
                dot={false}
                name="Annual Revenue"
                key="revenue"
              />
              <Line
                yAxisId="right"
                type="monotone"
                dataKey="cumulativeValue"
                stroke="#2E7D32"
                strokeWidth={2.5}
                strokeDasharray="5 5"
                dot={false}
                name="Cumulative Value"
                key="cumulative"
              />
              {/* Milestone markers with labels */}
              <Line
                yAxisId="left"
                dataKey="revenue"
                stroke="none"
                key="milestones"
                dot={props => {
                  if (!props || !props.payload || !props.payload.milestone) {
                    return null;
                  }
                  const actualMonth = Math.round(unscaleTime(props.payload.time));
                  return (
                    <g>
                      <DiamondMarker cx={props.cx} cy={props.cy} />
                      <text
                        x={props.cx}
                        y={props.cy - 15}
                        textAnchor="middle"
                        fill="#333333"
                        fontSize={12}
                        fontWeight={500}
                      >
                        {props.payload.milestone}
                      </text>
                      <text
                        x={props.cx}
                        y={props.cy}
                        textAnchor="start"
                        fill="#666666"
                        fontSize={11}
                        transform={`rotate(45, ${props.cx}, ${props.cy})`}
                        dx="10"
                      >
                        {`Month ${actualMonth}`}
                      </text>
                    </g>
                  );
                }}
              />
            </LineChart>
          </ResponsiveContainer>
        </Box>
      </Paper>

      {/* Assessment Section Header */}
      <Paper sx={{ p: 3, mb: 3, width: '100%', boxShadow: 2 }}>
        <Typography variant="h4" gutterBottom sx={{ fontWeight: 600, color: '#1a237e' }}>
          Synopsis Maturity & Design Readiness
        </Typography>
        <Typography variant="body1" sx={{ mb: 2, color: '#555' }}>
          This section tracks how the Copilot guides the development of a definitive trial synopsis
          across six key frameworks. Each framework represents a critical lens—spanning scientific
          intent, executional feasibility, stakeholder alignment, and market realism. Progress bars
          reflect how well each element is defined (completion) and how confident we are in its
          current articulation (certainty). Together, they signal the maturity and readiness of your
          trial design for real-world execution.
        </Typography>
      </Paper>

      {/* Assessment Blocks */}
      <Box sx={{ width: '100%', overflowX: 'auto', mb: 3 }}>
        <Box
          sx={{
            display: 'flex',
            gap: 2,
            minWidth: 'fit-content',
            p: 1,
          }}
        >
          <AssessmentBlock
            titleBold="Scientific Intent"
            titleLight="The 5 Ws of a definitive experiment"
            tagline="Clarify the who, what, when, where, and why of your trial’s purpose and population."
            data={assessmentData['Five Ws']}
          />

          <AssessmentBlock
            titleBold="Clinical Precision"
            titleLight="Targeted design for the right patients, endpoints, and timing"
            tagline="Align eligibility, intervention, and outcomes for mechanistic fit and real-world value."
            data={assessmentData['Five Rights']}
          />

          <AssessmentBlock
            titleBold="Executional Resilience"
            titleLight="Coordination, communication, and control under uncertainty"
            tagline="Ensure your trial can adapt, align, and deliver under evolving conditions."
            data={assessmentData['Five Cs']}
          />

          <AssessmentBlock
            titleBold="Ethical & Efficacy Foundations"
            titleLight="Ensuring human protection and evidence integrity"
            tagline="Ground your design in ethics, robust evidence, and inclusive participation."
            data={assessmentData['Five Es']}
          />

          <AssessmentBlock
            titleBold="Traceability & Teaming"
            titleLight="Making your trial transparent, tech-enabled, and team-aligned"
            tagline="Integrate technology, training, and cross-functional workflows to streamline execution."
            data={assessmentData['Five Ts']}
          />

          <AssessmentBlock
            titleBold="Commercial Readiness"
            titleLight="Linking design to market access, pricing, and positioning"
            tagline="Ensure your trial supports reimbursement, access, and strategic differentiation."
            data={assessmentData['Market']}
          />
        </Box>
      </Box>
    </Box>
  );
}

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
