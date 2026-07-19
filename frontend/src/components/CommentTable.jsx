import React, { useState } from 'react';
import { Search, Trash2, EyeOff, CheckCircle, AlertCircle, Sparkles } from 'lucide-react';
import ReplyModal from './ReplyModal';

export default function CommentTable({ comments = [], videoTitle }) {
  const [searchQuery, setSearchQuery] = useState('');
  const [actionFilter, setActionFilter] = useState('ALL');
  const [selectedComment, setSelectedComment] = useState(null);

  // Filter Logic
  const filteredComments = comments.filter((c) => {
    const textMatch =
      c.text.toLowerCase().includes(searchQuery.toLowerCase()) ||
      c.author.toLowerCase().includes(searchQuery.toLowerCase());

    const decision = c.moderation?.decision || 'Keep';
    const actionMatch = actionFilter === 'ALL' || decision === actionFilter;

    return textMatch && actionMatch;
  });

  const getDecisionBadge = (decision) => {
    switch (decision) {
      case 'Keep':
        return <span className="px-3 py-1 rounded-lg text-xs font-black bg-emerald-100 text-emerald-950 border border-emerald-400 flex items-center gap-1.5 shadow-sm"><CheckCircle className="w-4 h-4 text-emerald-700" /> Keep</span>;
      case 'Hide':
        return <span className="px-3 py-1 rounded-lg text-xs font-black bg-amber-100 text-amber-950 border border-amber-400 flex items-center gap-1.5 shadow-sm"><EyeOff className="w-4 h-4 text-amber-700" /> Hide</span>;
      case 'Delete':
        return <span className="px-3 py-1 rounded-lg text-xs font-black bg-rose-100 text-rose-950 border border-rose-400 flex items-center gap-1.5 shadow-sm"><Trash2 className="w-4 h-4 text-rose-700" /> Delete</span>;
      case 'Needs Human Review':
      default:
        return <span className="px-3 py-1 rounded-lg text-xs font-black bg-purple-100 text-purple-950 border border-purple-400 flex items-center gap-1.5 shadow-sm"><AlertCircle className="w-4 h-4 text-purple-700" /> Human Review</span>;
    }
  };

  const getSeverityBadge = (severity) => {
    switch (severity) {
      case 'Severe':
      case 'High':
        return <span className="text-rose-700 font-black text-xs">{severity}</span>;
      case 'Medium':
        return <span className="text-amber-800 font-black text-xs">{severity}</span>;
      default:
        return <span className="text-gray-700 font-bold text-xs">Low / None</span>;
    }
  };

  return (
    <div className="glass-panel rounded-2xl p-6 border-2 border-peach-200 bg-white shadow-md">
      {/* Header & Controls */}
      <div className="flex flex-col sm:flex-row items-center justify-between gap-4 mb-6">
        <div>
          <h3 className="text-xl font-black text-[#1a0f0b] flex items-center gap-2">
            Moderated Comments <span className="text-xs px-3 py-0.5 rounded-full bg-peach-200 text-peach-950 font-black">{filteredComments.length}</span>
          </h3>
          <p className="text-xs text-gray-800 font-bold">Detailed multi-agent classification matrix</p>
        </div>

        {/* Search & Action Filter Tabs */}
        <div className="flex flex-wrap items-center gap-3 w-full sm:w-auto">
          {/* Search Box */}
          <div className="relative flex-1 sm:w-64">
            <Search className="w-4 h-4 absolute left-3 top-3 text-peach-700" />
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder="Filter by keyword or author..."
              className="w-full bg-white border-2 border-peach-300 rounded-xl py-2 pl-9 pr-4 text-xs text-[#1a0f0b] placeholder-gray-500 font-bold shadow-inner"
            />
          </div>

          {/* Action Filter dropdown */}
          <div className="flex items-center gap-1 bg-peach-100 p-1 rounded-xl border border-peach-300 text-xs">
            {['ALL', 'Keep', 'Hide', 'Delete', 'Needs Human Review'].map((act) => (
              <button
                key={act}
                onClick={() => setActionFilter(act)}
                className={`px-3 py-1.5 rounded-lg text-xs font-black transition-all ${
                  actionFilter === act
                    ? 'bg-[#1a0f0b] text-white shadow-md'
                    : 'text-gray-800 hover:bg-peach-200 hover:text-[#1a0f0b]'
                }`}
              >
                {act === 'Needs Human Review' ? 'Review' : act}
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* Table */}
      <div className="overflow-x-auto">
        <table className="w-full text-left border-collapse text-xs">
          <thead>
            <tr className="border-b-2 border-peach-300 text-gray-900 uppercase tracking-wider text-[11px] bg-peach-100/90 font-black">
              <th className="py-3.5 px-4">Author & Comment</th>
              <th className="py-3.5 px-4">Category / Intent</th>
              <th className="py-3.5 px-4">Toxicity Severity</th>
              <th className="py-3.5 px-4">AI Confidence</th>
              <th className="py-3.5 px-4">Suggested Action</th>
              <th className="py-3.5 px-4 text-right">AI Reply</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-peach-200">
            {filteredComments.length > 0 ? (
              filteredComments.map((c) => {
                const confidencePct = Math.round(
                  ((c.spam?.confidence || 0.9) + (c.sentiment_intent?.confidence || 0.9)) * 50
                );

                return (
                  <tr key={c.comment_id} className="hover:bg-peach-50/80 transition-colors">
                    {/* Author & Comment */}
                    <td className="py-4 px-4 max-w-sm">
                      <div className="flex items-start gap-3">
                        <img
                          src={c.author_profile_image || 'https://i.pravatar.cc/150'}
                          alt={c.author}
                          className="w-9 h-9 rounded-full flex-shrink-0 object-cover border-2 border-peach-300 shadow-sm"
                        />
                        <div className="min-w-0">
                          <p className="font-black text-[#1a0f0b] text-sm truncate">{c.author}</p>
                          <p className="text-gray-900 mt-0.5 line-clamp-2 leading-relaxed font-semibold">{c.text}</p>
                          {c.moderation?.reason && (
                            <p className="text-[11px] text-gray-700 mt-1 italic line-clamp-1 font-bold">
                              Rationale: {c.moderation.reason}
                            </p>
                          )}
                        </div>
                      </div>
                    </td>

                    {/* Intent Category */}
                    <td className="py-4 px-4">
                      <span className="px-3 py-1 rounded-lg bg-peach-100 border border-peach-300 text-peach-950 font-black inline-block">
                        {c.sentiment_intent?.intent || 'General'}
                      </span>
                      <p className="text-[11px] text-gray-800 mt-1 font-bold">{c.sentiment_intent?.sentiment}</p>
                    </td>

                    {/* Toxicity Severity */}
                    <td className="py-4 px-4">
                      {getSeverityBadge(c.toxicity?.severity || 'None')}
                    </td>

                    {/* Confidence */}
                    <td className="py-4 px-4 font-mono font-black text-[#1a0f0b]">
                      {confidencePct}%
                    </td>

                    {/* Decision Badge */}
                    <td className="py-4 px-4">
                      {getDecisionBadge(c.moderation?.decision || 'Keep')}
                    </td>

                    {/* AI Reply Action */}
                    <td className="py-4 px-4 text-right">
                      {c.reply ? (
                        <button
                          onClick={() => setSelectedComment(c)}
                          className="px-4 py-2 rounded-lg bg-[#e64a19] hover:bg-[#d84315] text-white font-black text-xs transition-all flex items-center gap-1.5 ml-auto shadow-md cursor-pointer"
                        >
                          <Sparkles className="w-3.5 h-3.5 text-white" />
                          <span className="text-white">View Reply</span>
                        </button>
                      ) : (
                        <button
                          onClick={() => setSelectedComment(c)}
                          className="px-4 py-2 rounded-lg bg-peach-100 hover:bg-peach-200 text-[#1a0f0b] border-2 border-peach-300 text-xs font-black transition-all flex items-center gap-1 ml-auto shadow-sm cursor-pointer"
                        >
                          <span>Generate</span>
                        </button>
                      )}
                    </td>
                  </tr>
                );
              })
            ) : (
              <tr>
                <td colSpan={6} className="py-8 text-center text-gray-800 font-extrabold">
                  No comments match the selected filter query.
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>

      {/* Reply Modal */}
      {selectedComment && (
        <ReplyModal
          comment={selectedComment}
          videoTitle={videoTitle}
          onClose={() => setSelectedComment(null)}
        />
      )}
    </div>
  );
}
