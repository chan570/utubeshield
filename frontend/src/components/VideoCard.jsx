import React from 'react';
import { Eye, ThumbsUp, MessageSquare, MessageSquareOff, Calendar, ExternalLink, User } from 'lucide-react';

export default function VideoCard({ video }) {
  if (!video) return null;

  const formatNumber = (num) => {
    if (!num) return '0';
    if (num >= 1000000) return (num / 1000000).toFixed(1) + 'M';
    if (num >= 1000) return (num / 1000).toFixed(1) + 'K';
    return num.toLocaleString();
  };

  const formatDate = (dateStr) => {
    if (!dateStr) return 'Recently';
    try {
      return new Date(dateStr).toLocaleDateString(undefined, { year: 'numeric', month: 'short', day: 'numeric' });
    } catch {
      return dateStr;
    }
  };

  return (
    <div className="glass-panel rounded-2xl p-5 mb-8 flex flex-col md:flex-row items-center gap-6 border-2 border-peach-200 bg-white shadow-md">
      {/* Thumbnail */}
      <div className="relative w-full md:w-64 h-36 rounded-xl overflow-hidden flex-shrink-0 group shadow-md">
        <img
          src={video.thumbnail_url || 'https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?w=800'}
          alt={video.title}
          className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
        />
        <a
          href={video.url}
          target="_blank"
          rel="noopener noreferrer"
          className="absolute inset-0 bg-black/50 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity"
        >
          <span className="px-3.5 py-2 rounded-lg bg-red-600 text-white text-xs font-black flex items-center gap-1.5 shadow-lg">
            Watch on YouTube <ExternalLink className="w-3.5 h-3.5" />
          </span>
        </a>
      </div>

      {/* Details */}
      <div className="flex-1 min-w-0 w-full">
        <div className="flex items-center gap-2 text-xs text-peach-800 font-extrabold mb-1">
          <User className="w-4 h-4 text-peach-700" />
          <span>{video.channel_title || 'YouTube Creator'}</span>
        </div>

        <h3 className="text-xl md:text-2xl font-black text-[#1a0f0b] mb-3 line-clamp-2 leading-snug">
          {video.title}
        </h3>

        {/* Video Statistics Badges */}
        <div className="flex flex-wrap items-center gap-3 text-xs text-gray-900 font-bold">
          <div className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-peach-100/90 border border-peach-300 shadow-sm">
            <Eye className="w-4 h-4 text-peach-800" />
            <span><strong className="text-[#1a0f0b] font-black">{formatNumber(video.view_count)}</strong> Views</span>
          </div>

          <div className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-emerald-100/90 border border-emerald-300 shadow-sm">
            <ThumbsUp className="w-4 h-4 text-emerald-800" />
            <span><strong className="text-[#1a0f0b] font-black">{formatNumber(video.like_count)}</strong> Likes</span>
          </div>

          {video.comments_disabled ? (
            <div className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-rose-100 border-2 border-rose-400 text-rose-950 font-black shadow-sm">
              <MessageSquareOff className="w-4 h-4 text-rose-700" />
              <span>Comments Turned Off</span>
            </div>
          ) : (
            <div className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-amber-100/90 border border-amber-300 shadow-sm">
              <MessageSquare className="w-4 h-4 text-amber-900" />
              <span><strong className="text-[#1a0f0b] font-black">{formatNumber(video.comment_count)}</strong> Comments</span>
            </div>
          )}

          <div className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-gray-100 border border-gray-300 text-gray-900 font-bold shadow-sm">
            <Calendar className="w-4 h-4 text-gray-700" />
            <span>{formatDate(video.published_at)}</span>
          </div>
        </div>
      </div>
    </div>
  );
}
