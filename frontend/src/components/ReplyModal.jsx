import React, { useState } from 'react';
import { X, Sparkles, Copy, Check, RefreshCw, MessageSquare } from 'lucide-react';
import { generateReply } from '../services/api';

export default function ReplyModal({ comment, videoTitle, onClose }) {
  if (!comment) return null;

  const [replyText, setReplyText] = useState(comment.reply?.suggested_reply || '');
  const [tone, setTone] = useState(comment.reply?.tone || 'Professional');
  const [isGenerating, setIsGenerating] = useState(false);
  const [copied, setCopied] = useState(false);

  const handleRegenerate = async () => {
    setIsGenerating(true);
    try {
      const res = await generateReply({
        commentText: comment.text,
        author: comment.author,
        intent: comment.sentiment_intent?.intent || 'Question',
        context: videoTitle
      });
      setReplyText(res.suggested_reply);
      setTone(res.tone);
    } catch (e) {
      console.error("Failed to generate custom reply", e);
    } finally {
      setIsGenerating(false);
    }
  };

  const handleCopy = () => {
    navigator.clipboard.writeText(replyText);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60 backdrop-blur-sm">
      <div className="glass-panel w-full max-w-xl rounded-2xl p-6 border-2 border-peach-300 bg-white shadow-2xl relative animate-in fade-in zoom-in duration-200">
        {/* Header */}
        <div className="flex items-center justify-between pb-4 border-b border-peach-200">
          <div className="flex items-center gap-2">
            <div className="w-8 h-8 rounded-lg bg-peach-100 border border-peach-300 flex items-center justify-center text-peach-700">
              <Sparkles className="w-4 h-4" />
            </div>
            <h3 className="text-lg font-black text-[#1a0f0b]">AI Response Generator</h3>
          </div>
          <button
            onClick={onClose}
            className="p-1.5 rounded-lg text-gray-700 hover:text-black hover:bg-peach-100 transition-all font-bold"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Original Comment */}
        <div className="my-4 p-4 rounded-xl bg-peach-100/70 border border-peach-300">
          <div className="flex items-center justify-between mb-1">
            <span className="text-xs font-black text-peach-950">{comment.author}</span>
            <span className="text-[10px] font-extrabold px-2 py-0.5 rounded bg-white text-peach-950 border border-peach-300">
              {comment.sentiment_intent?.intent}
            </span>
          </div>
          <p className="text-xs text-gray-900 font-bold italic">"{comment.text}"</p>
        </div>

        {/* AI Reply Editor */}
        <div className="mb-6">
          <div className="flex items-center justify-between mb-2">
            <label className="text-xs font-black text-[#1a0f0b]">Generated AI Reply ({tone})</label>
            <button
              onClick={handleRegenerate}
              disabled={isGenerating}
              className="text-xs text-peach-700 hover:text-peach-900 flex items-center gap-1 font-black transition-all"
            >
              <RefreshCw className={`w-3.5 h-3.5 ${isGenerating ? 'animate-spin' : ''}`} />
              <span>Regenerate</span>
            </button>
          </div>

          <textarea
            value={replyText}
            onChange={(e) => setReplyText(e.target.value)}
            rows={4}
            className="w-full bg-white border-2 border-peach-300 rounded-xl p-3 text-xs text-[#1a0f0b] placeholder-gray-500 focus:outline-none focus:border-peach-600 focus:ring-2 focus:ring-peach-500/30 transition-all resize-none font-bold shadow-inner"
            placeholder="AI reply will appear here..."
          />
        </div>

        {/* Footer Actions */}
        <div className="flex items-center justify-between pt-3 border-t border-peach-200">
          <span className="text-[11px] text-gray-800 font-bold flex items-center gap-1">
            <MessageSquare className="w-3.5 h-3.5 text-peach-600" /> Ready to copy & post to YouTube
          </span>

          <div className="flex items-center gap-3">
            <button
              onClick={onClose}
              className="px-4 py-2 rounded-xl text-xs font-black text-gray-800 hover:bg-peach-100 transition-all"
            >
              Cancel
            </button>

            <button
              onClick={handleCopy}
              className="px-5 py-2.5 rounded-xl bg-[#e64a19] hover:bg-[#d84315] text-white font-black text-xs flex items-center gap-1.5 shadow-md transition-all cursor-pointer"
            >
              {copied ? (
                <>
                  <Check className="w-4 h-4 text-emerald-200" />
                  <span>Copied to Clipboard!</span>
                </>
              ) : (
                <>
                  <Copy className="w-4 h-4" />
                  <span>Copy AI Reply</span>
                </>
              )}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
