import React from 'react';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  ReferenceLine,
} from 'recharts';
import { Paper, Typography, Box, Divider, LinearProgress, Grid } from '@mui/material';

// Gamma function implementation
function gamma(z) {
  // Lanczos Approximation
  const p = [
    676.5203681218851, -1259.1392167224028, 771.32342877765313, -176.61502916214059,
    12.507343278686905, -0.13857109526572012, 9.9843695780195716e-6, 1.5056327351493116e-7,
  ];

  if (z < 0.5) {
    return Math.PI / (Math.sin(Math.PI * z) * gamma(1 - z));
  }

  z -= 1;
  let x = 0.99999999999980993;
  for (let i = 0; i < p.length; i++) {
    x += p[i] / (z + i + 1);
  }

  const t = z + p.length - 0.5;
  return Math.sqrt(2 * Math.PI) * Math.pow(t, z + 0.5) * Math.exp(-t) * x;
}

// Revenue model function using gamma distribution
function drugRevenueModel(t, a, b, scale) {
  if (t === 0) return 0;
  return (100 * scale * Math.pow(t / b, a - 1) * Math.exp(-t / b)) / (b * gamma(a));
}

// Custom scale function to compress later time periods
function scaleTime(month) {
  if (month <= 60) {
    // Pre-launch: linear scale
    return month;
  }
  // Post-launch: logarithmic compression
  const monthsSinceLaunch = month - 60;
  return 60 + (Math.log(monthsSinceLaunch + 1) / Math.log(240)) * 180;
}

// Inverse scale function for tooltip display
function unscaleTime(scaled) {
  if (scaled <= 60) {
    return scaled;
  }
  return 60 + (Math.exp(((scaled - 60) * Math.log(240)) / 180) - 1);
}

// Generate timeline data with both curves
function generateTimelineData() {
  const a = 2; // Shape parameter
  const b = 6.5; // Scale parameter
  const scale = 100; // Scale factor
  const numPoints = 250;
  const maxYears = 25;

  // Pre-milestone data points with scaled time
  const preMilestones = [
    { month: 0, label: 'Current', revenue: 0, milestone: 'Current' },
    { month: 3, label: 'IND', revenue: 0, milestone: 'IND' },
    { month: 9, label: 'Phase 1', revenue: 0, milestone: 'Phase 1' },
    { month: 21, label: 'Phase 2', revenue: 0, milestone: 'Phase 2' },
    { month: 48, label: 'Phase 3', revenue: 0, milestone: 'Phase 3' },
    { month: 54, label: 'NDA', revenue: 0, milestone: 'NDA' },
  ];

  const data = [];
  let cumulativeValue = 0;

  // Add pre-milestone points with scaled time
  preMilestones.forEach(point => {
    data.push({
      actualTime: point.month,
      time: scaleTime(point.month),
      revenue: 0,
      cumulativeValue: 0,
      milestone: point.milestone,
    });
  });

  // Start revenue calculation from NDA approval with scaled time
  for (let i = 0; i < numPoints; i++) {
    const actualMonth = 60 + (i * (maxYears * 12 - 54)) / numPoints;
    const year = (actualMonth - 60) / 12; // Years since NDA
    const revenue = year >= 0 ? drugRevenueModel(year, a, b, scale) : 0;
    cumulativeValue += (revenue * 0.15 * ((maxYears * 12 - 54) / numPoints)) / 12;

    data.push({
      actualTime: actualMonth,
      time: scaleTime(actualMonth),
      revenue: revenue,
      cumulativeValue: cumulativeValue,
      milestone: null,
    });
  }

  // Add post-launch milestones
  const postMilestones = [
    { month: 60, label: 'Launch' },
    { month: 72, label: 'Year 1' },
    { month: 96, label: 'Year 2' },
    { month: 120, label: 'Year 3' },
    { month: 180, label: 'Year 5' },
  ];

  // Merge milestones into data with scaled time
  postMilestones.forEach(milestone => {
    const index = data.findIndex(point => Math.round(point.actualTime) === milestone.month);
    if (index !== -1) {
      data[index].milestone = milestone.label;
    }
  });

  return data;
}

// Assessment data
const assessmentData = {
  'Five Ws': {
    who: {
      progress: 85,
      confidence: 'High',
      desc: 'Patient demographics, inclusion/exclusion criteria, and subgroup stratification',
    },
    what: {
      progress: 90,
      confidence: 'High',
      desc: 'Intervention details, control groups, and outcome measurements',
    },
    where: {
      progress: 75,
      confidence: 'Medium',
      desc: 'Site selection criteria, geographical distribution, and facility requirements',
    },
    when: {
      progress: 80,
      confidence: 'High',
      desc: 'Timeline planning, visit schedules, and follow-up periods',
    },
    why: {
      progress: 85,
      confidence: 'High',
      desc: 'Study rationale, unmet needs, and expected clinical impact',
    },
  },
  'Five Rights': {
    'Right Patient': {
      progress: 50,
      confidence: 'High',
      desc: 'Precise targeting of patient population with verified eligibility criteria',
    },
    'Right Drug': {
      progress: 85,
      confidence: 'High',
      desc: 'Optimal therapeutic choice based on mechanism and patient needs',
    },
    'Right Dose': {
      progress: 75,
      confidence: 'Medium',
      desc: 'Evidence-based dosing strategy with adjustment protocols',
    },
    'Right Time': {
      progress: 70,
      confidence: 'Medium',
      desc: 'Optimal timing of intervention and outcome assessments',
    },
    'Right Documentation': {
      progress: 90,
      confidence: 'High',
      desc: 'Comprehensive documentation system with quality controls',
    },
  },
  'Five Cs': {
    Coordination: {
      progress: 75,
      confidence: 'Medium',
      desc: 'Cross-functional alignment and resource synchronization',
    },
    Collaboration: {
      progress: 80,
      confidence: 'High',
      desc: 'Integrated partnerships across sites, sponsors, and CROs',
    },
    Communication: {
      progress: 85,
      confidence: 'High',
      desc: 'Clear protocols for information sharing and reporting',
    },
    Control: {
      progress: 90,
      confidence: 'High',
      desc: 'Risk monitoring and mitigation strategies with defined triggers',
    },
    Compliance: {
      progress: 85,
      confidence: 'High',
      desc: 'Adherence to regulatory requirements and ethical standards',
    },
  },
  'Five Es': {
    Ethics: {
      progress: 95,
      confidence: 'High',
      desc: 'Human subject protection and informed consent processes',
    },
    Efficacy: {
      progress: 80,
      confidence: 'High',
      desc: 'Primary/secondary endpoint selection and effect size estimation',
    },
    Efficiency: {
      progress: 75,
      confidence: 'Medium',
      desc: 'Streamlined processes and resource optimization plans',
    },
    Equality: {
      progress: 85,
      confidence: 'High',
      desc: 'Diversity, equity, and inclusion in trial participation',
    },
    Evidence: {
      progress: 90,
      confidence: 'High',
      desc: 'Robust data collection and statistical analysis methods',
    },
  },
  'Five Ts': {
    Transparency: {
      progress: 85,
      confidence: 'High',
      desc: 'Clear documentation and reporting of all trial aspects',
    },
    Traceability: {
      progress: 80,
      confidence: 'High',
      desc: 'Complete audit trail and data provenance systems',
    },
    Training: {
      progress: 75,
      confidence: 'Medium',
      desc: 'Comprehensive site and personnel qualification programs',
    },
    Technology: {
      progress: 90,
      confidence: 'High',
      desc: 'Integrated eClinical and data management platforms',
    },
    Teamwork: {
      progress: 85,
      confidence: 'High',
      desc: 'Cross-functional collaboration and role definition',
    },
  },
  Market: {
    Size: {
      progress: 75,
      confidence: 'Medium',
      desc: 'Target population size and market opportunity analysis',
    },
    Competition: {
      progress: 85,
      confidence: 'High',
      desc: 'Current/future competitive landscape assessment',
    },
    Pricing: {
      progress: 70,
      confidence: 'Medium',
      desc: 'Value-based pricing strategy and reimbursement planning',
    },
    Access: {
      progress: 65,
      confidence: 'Medium',
      desc: 'Market access barriers and distribution strategy',
    },
    ROI: {
      progress: 80,
      confidence: 'High',
      desc: 'Investment return projections and value proposition',
    },
  },
};

const AssessmentBlock = ({ titleBold, titleLight, tagline, data }) => (
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
