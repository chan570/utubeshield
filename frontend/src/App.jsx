import React, { useState, useEffect } from 'react';
import Header from './components/Header';
import UrlInputForm from './components/UrlInputForm';
import VideoCard from './components/VideoCard';
import AnalyticsCards from './components/AnalyticsCards';
import HealthScoreMeter from './components/HealthScoreMeter';
import ChartsSection from './components/ChartsSection';
import KeywordCloud from './components/KeywordCloud';
import CommentTable from './components/CommentTable';
import { analyzeVideo } from './services/api';

export default function App() {
  const [video, setVideo] = useState(null);
  const [analytics, setAnalytics] = useState(null);
  const [comments, setComments] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  // Auto-analyze initial demo video on first load if empty
  useEffect(() => {
    handleAnalyze('https://www.youtube.com/watch?v=dQw4w9WgXcQ');
  }, []);

  const handleAnalyze = async (url) => {
    setIsLoading(true);
    setError(null);
    try {
      const data = await analyzeVideo(url);
      setVideo(data.video);
      setAnalytics(data.analytics);
      setComments(data.comments || []);
    } catch (err) {
      console.error("Analysis Error:", err);
      setError(err.response?.data?.detail || "Failed to analyze video. Ensure backend server is running.");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-[#fff7f4] text-[#2d1f1a] flex flex-col selection:bg-rose-400 selection:text-white">
      {/* Header */}
      <Header />

      {/* Main Content Container */}
      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 mb-16">
        {/* Input Bar */}
        <UrlInputForm onAnalyze={handleAnalyze} isLoading={isLoading} />

        {/* Global Error Banner */}
        {error && (
          <div className="mb-6 p-4 rounded-xl bg-rose-100 border border-rose-300 text-rose-800 text-sm text-center font-bold">
            {error}
          </div>
        )}

        {/* Dashboard Content */}
        {video && (
          <div className="space-y-8 animate-in fade-in duration-500">
            {/* Video Metadata Banner */}
            <VideoCard video={video} />

            {/* Community Health Score Gauge & AI Recommendations */}
            <HealthScoreMeter analytics={analytics} />

            {/* Analytics Metric Cards */}
            <AnalyticsCards analytics={analytics} commentsCount={comments.length} />

            {/* Visual Analytics Charts */}
            <ChartsSection analytics={analytics} comments={comments} />

            {/* Keywords & Feature Requests */}
            <KeywordCloud analytics={analytics} />

            {/* Filterable Comment Table */}
            <CommentTable comments={comments} videoTitle={video?.title} commentsDisabled={video?.comments_disabled} />
          </div>
        )}
      </main>

      {/* Footer */}
      <footer className="border-t border-peach-200 py-6 text-center text-xs text-gray-500 bg-white/70 font-medium">
        <p>TubeShield AI — Built with LangGraph, LangChain, FastAPI & React</p>
      </footer>
    </div>
  );
}
