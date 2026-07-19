import React from 'react';
import {
  Chart as ChartJS,
  ArcElement,
  Tooltip,
  Legend,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
} from 'chart.js';
import { Doughnut, Bar } from 'react-chartjs-2';

ChartJS.register(
  ArcElement,
  Tooltip,
  Legend,
  CategoryScale,
  LinearScale,
  BarElement,
  Title
);

export default function ChartsSection({ analytics, comments = [] }) {
  if (!analytics) return null;

  // Sentiment Doughnut Data
  const sentimentData = {
    labels: ['Positive', 'Neutral', 'Negative'],
    datasets: [
      {
        data: [
          analytics.positive_pct || 0,
          analytics.neutral_pct || 0,
          analytics.negative_pct || 0,
        ],
        backgroundColor: ['#059669', '#6b7280', '#e11d48'],
        borderColor: '#ffffff',
        borderWidth: 3,
        hoverOffset: 6,
      },
    ],
  };

  // Moderation Actions Bar Chart Data
  const decisionCounts = {
    Keep: 0,
    Hide: 0,
    Delete: 0,
    'Needs Human Review': 0,
  };

  comments.forEach((c) => {
    const d = c.moderation?.decision || 'Keep';
    decisionCounts[d] = (decisionCounts[d] || 0) + 1;
  });

  const actionData = {
    labels: ['Keep', 'Hide', 'Delete', 'Human Review'],
    datasets: [
      {
        label: 'Comments',
        data: [
          decisionCounts['Keep'],
          decisionCounts['Hide'],
          decisionCounts['Delete'],
          decisionCounts['Needs Human Review'],
        ],
        backgroundColor: ['#059669', '#d97706', '#e11d48', '#7c3aed'],
        borderRadius: 8,
      },
    ],
  };

  const barOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: { display: false },
      tooltip: {
        backgroundColor: '#1a0f0b',
        titleColor: '#ffffff',
        bodyColor: '#ffffff',
        borderColor: '#ffcbab',
        borderWidth: 1,
        boxPadding: 6,
      },
    },
    scales: {
      x: {
        grid: { display: false },
        ticks: { color: '#1a0f0b', font: { size: 12, weight: 'bold' } },
      },
      y: {
        grid: { color: 'rgba(244, 81, 30, 0.12)' },
        ticks: { color: '#1a0f0b', precision: 0, font: { size: 12, weight: 'bold' } },
      },
    },
  };

  const doughnutOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: 'bottom',
        labels: { color: '#1a0f0b', font: { size: 13, weight: 'bold' }, padding: 16 },
      },
    },
  };

  return (
    <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
      {/* Sentiment Doughnut */}
      <div className="glass-panel rounded-2xl p-6 border-2 border-peach-200 bg-white flex flex-col justify-between shadow-sm">
        <div>
          <h3 className="text-lg font-black text-[#1a0f0b] mb-1">Sentiment Distribution</h3>
          <p className="text-xs text-gray-800 font-bold mb-4">Overall emotion analysis of community responses</p>
        </div>
        <div className="h-64 relative flex items-center justify-center">
          <Doughnut data={sentimentData} options={doughnutOptions} />
        </div>
      </div>

      {/* Moderation Actions Bar */}
      <div className="glass-panel rounded-2xl p-6 border-2 border-peach-200 bg-white flex flex-col justify-between shadow-sm">
        <div>
          <h3 className="text-lg font-black text-[#1a0f0b] mb-1">Moderation Action Matrix</h3>
          <p className="text-xs text-gray-800 font-bold mb-4">Breakdown of automated decision tags across all comments</p>
        </div>
        <div className="h-64 relative">
          <Bar data={actionData} options={barOptions} />
        </div>
      </div>
    </div>
  );
}
