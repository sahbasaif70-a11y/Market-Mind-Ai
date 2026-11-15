import React, { useState, useEffect } from 'react';
import { BookOpen, Upload, FileText, CheckCircle2, RefreshCw, Database } from 'lucide-react';

const API_BASE_URL = import.meta.env.VITE_BACKEND_URL || 'https://market-mind-ai-yixa.onrender.com';


export default function KnowledgeBaseView() {
  const [corpusFiles, setCorpusFiles] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [uploadMessage, setUploadMessage] = useState('');

  const fetchCorpus = async () => {
    setIsLoading(true);
    try {
      const res = await fetch('http://localhost:8000/api/marketmind/corpus');
      if (res.ok) {
        const data = await res.json();
        setCorpusFiles(data.files || []);
      }
    } catch (e) {
      console.error(e);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchCorpus();
  }, []);

  const handleFileUpload = async (e) => {
    const file = e.target.files?.[0];
    if (!file) return;

    const formData = new FormData();
    formData.append('file', file);

    try {
      const res = await fetch('http://localhost:8000/api/marketmind/corpus/upload', {
        method: 'POST',
        body: formData,
      });
      if (res.ok) {
        setUploadMessage(`Document '${file.name}' added to Research Data Corpus!`);
        fetchCorpus();
      }
    } catch (err) {
      setUploadMessage(`Upload failed: ${err.message}`);
    }
  };

  return (
    <div className="space-y-6 max-w-5xl mx-auto pb-12">
      <div className="flex items-center justify-between border-b border-emerald-500/15 pb-4">
        <div>
          <h1 className="text-xl font-bold text-warm-ivory flex items-center gap-2">
            <BookOpen className="w-5 h-5 text-emerald-accent" />
            <span>Research Data Corpus (Knowledge Base)</span>
          </h1>
          <p className="text-xs text-muted-emerald">
            Approved text sources used by MarketMind AI agent to ground factual claims with verified provenance.
          </p>
        </div>

        <button
          onClick={fetchCorpus}
          className="p-2 rounded-xl bg-emerald-950 border border-emerald-500/20 text-emerald-accent hover:border-emerald-accent transition-all"
        >
          <RefreshCw className={`w-4 h-4 ${isLoading ? 'animate-spin' : ''}`} />
        </button>
      </div>

      {uploadMessage && (
        <div className="p-3 rounded-xl bg-emerald-950/80 border border-emerald-accent/40 text-xs text-emerald-accent flex items-center gap-2">
          <CheckCircle2 className="w-4 h-4" />
          <span>{uploadMessage}</span>
        </div>
      )}

      {/* Upload Box */}
      <div className="obsidian-panel rounded-3xl p-6 border border-emerald-500/30 text-center space-y-3">
        <div className="w-12 h-12 rounded-2xl bg-emerald-950 border border-emerald-accent/30 mx-auto flex items-center justify-center text-emerald-accent">
          <Upload className="w-6 h-6" />
        </div>
        <div>
          <h3 className="text-sm font-bold text-warm-ivory">Add New Research Document to Corpus</h3>
          <p className="text-xs text-muted-emerald">Upload .txt files containing vendor pricing, features, or market reports.</p>
        </div>

        <label className="inline-block px-5 py-2.5 rounded-xl bg-gradient-to-r from-champagne-gold via-[#E5C687] to-champagne-gold text-obsidian font-bold text-xs cursor-pointer shadow-lg shadow-champagne-gold/20 hover:scale-[1.02] transition-all">
          <span>Choose .txt Document</span>
          <input type="file" accept=".txt" onChange={handleFileUpload} className="hidden" />
        </label>
      </div>

      {/* Existing Files Grid */}
      <div className="space-y-3">
        <h3 className="text-xs font-bold text-warm-ivory flex items-center gap-2">
          <Database className="w-4 h-4 text-emerald-accent" />
          <span>Active Corpus Documents ({corpusFiles.length})</span>
        </h3>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {corpusFiles.map((file, idx) => (
            <div key={idx} className="obsidian-panel rounded-2xl p-4 border border-emerald-500/20 space-y-2 hover:border-emerald-accent/40 transition-all">
              <div className="w-8 h-8 rounded-xl bg-emerald-900/50 flex items-center justify-center text-emerald-accent">
                <FileText className="w-4 h-4" />
              </div>
              <h4 className="text-xs font-bold text-warm-ivory truncate">{file.name}</h4>
              <p className="text-[10px] text-muted-emerald font-mono">{file.size_bytes} bytes • Verified Source</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
