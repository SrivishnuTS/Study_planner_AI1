import React, { useEffect, useState } from 'react';
import api from '../utils/api';
import { motion, AnimatePresence } from 'framer-motion';
import { ChevronDown, ChevronUp, Info, HelpCircle, Lightbulb, Clock, ChevronRight } from 'lucide-react';

export default function HistoryPage() {
  const [history, setHistory] = useState([]);
  const [expandedId, setExpandedId] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => { 
    api.get('/history')
      .then(res => { setHistory(res.data); setLoading(false); })
      .catch(() => setLoading(false)); 
  }, []);

  if (loading) return <div className="classic-card h-64 flex items-center justify-center text-text-secondary text-sm font-medium">Retrieving strategy logs...</div>;
  if (!history.length) return <div className="classic-card text-center p-12"><p className="text-xl font-bold text-text font-serif mb-2">No Strategies Logged</p><p className="text-text-secondary text-sm">Use the Strategy Modeler to sync your first AI prediction.</p></div>;

  return (
    <div className="max-w-6xl mx-auto">
      <header className="mb-8 border-b border-border pb-6 flex items-center justify-between">
        <h1 className="text-3xl font-bold text-text tracking-tight font-serif">Strategy Ledger</h1>
        <div className="flex items-center gap-2 text-text-secondary text-xs uppercase font-bold tracking-widest bg-muted px-4 py-2 rounded-full">
          <Clock size={14}/> Recent Activity First
        </div>
      </header>
      <div className="classic-card !p-0 overflow-hidden shadow-2xl">
        <table className="w-full text-left text-sm">
          <thead className="bg-muted text-xs uppercase tracking-widest text-text-secondary font-bold border-b border-border">
            <tr><th className="p-4">Timestamp</th><th className="p-4">Suggested Pattern</th><th className="p-4">AI Confidence</th><th className="p-4">Status</th><th className="p-4"></th></tr>
          </thead>
          <tbody className="divide-y divide-border">
            {history.map(r => {
              const isExpanded = expandedId === r.id;
              return (
                <React.Fragment key={r.id}>
                  <tr onClick={() => setExpandedId(isExpanded ? null : r.id)} className={`cursor-pointer transition-all ${isExpanded ? 'bg-primary/5' : 'hover:bg-muted/50'}`}>
                    <td className="p-4 text-text-secondary text-xs">{new Date(r.timestamp).toLocaleString()}</td>
                    <td className="p-4 font-bold text-text">{r.prediction}</td>
                    <td className="p-4">
                      <div className="flex items-center gap-2">
                        <div className="w-16 h-1 bg-muted rounded-full overflow-hidden">
                          <div className="h-full bg-primary" style={{width: `${r.confidence}%`}}></div>
                        </div>
                        <span className="font-bold text-primary">{r.confidence}%</span>
                      </div>
                    </td>
                    <td className="p-4">
                      <span className="px-2.5 py-1 rounded-md text-[10px] font-bold uppercase tracking-tight bg-emerald-500/10 text-emerald-600 border border-emerald-500/20">Synced</span>
                    </td>
                    <td className="p-4 text-right text-text-secondary">{isExpanded ? <ChevronUp size={16}/> : <ChevronDown size={16}/>}</td>
                  </tr>
                  <AnimatePresence>
                    {isExpanded && (
                      <tr>
                        <td colSpan={5} className="p-0">
                          <motion.div initial={{ height: 0, opacity: 0 }} animate={{ height: 'auto', opacity: 1 }} exit={{ height: 0, opacity: 0 }} className="bg-muted/30 border-b border-border overflow-hidden">
                            <div className="p-8 space-y-10">
                              <div className="grid grid-cols-1 lg:grid-cols-2 gap-10">
                                <div>
                                  <h4 className="text-[10px] font-bold uppercase tracking-widest text-text-secondary mb-4">Contextual Inputs</h4>
                                  <div className="grid grid-cols-2 gap-x-6 gap-y-3 text-xs bg-card p-5 rounded-2xl border border-border shadow-sm">
                                    <div className="flex justify-between border-b border-border pb-2"><span className="text-text-secondary">Study Duration:</span> <span className="font-bold">{r.inputs.study_hours}h</span></div>
                                    <div className="flex justify-between border-b border-border pb-2"><span className="text-text-secondary">Sleep Quality:</span> <span className="font-bold">{r.inputs.sleep_hours}h</span></div>
                                    <div className="flex justify-between border-b border-border pb-2"><span className="text-text-secondary">Focus Index:</span> <span className="font-bold">{r.inputs.focus_score}/10</span></div>
                                    <div className="flex justify-between border-b border-border pb-2"><span className="text-text-secondary">Distraction:</span> <span className="font-bold capitalize">{r.inputs.distraction}</span></div>
                                  </div>
                                </div>
                                <div>
                                  <h4 className="text-[10px] font-bold uppercase tracking-widest text-text-secondary mb-4">Strategy Summary</h4>
                                  <div className="bg-card p-5 rounded-2xl border border-primary/20 shadow-sm relative overflow-hidden">
                                    <p className="text-sm font-medium italic text-text leading-relaxed">"{r.recommendation.summary}"</p>
                                  </div>
                                </div>
                              </div>

                              <div className="grid grid-cols-1 lg:grid-cols-2 gap-10">
                                <div>
                                  <h5 className="text-[10px] font-bold text-text-secondary uppercase mb-4 flex items-center gap-2"><HelpCircle size={12}/> Cognitive Reasoning</h5>
                                  <ul className="space-y-2">
                                    {r.recommendation.explanation?.map((e,i)=><li key={i} className="text-xs flex items-start gap-2 text-text-secondary"><span className="w-1 h-1 rounded-full bg-primary mt-1.5 shrink-0"></span> {e}</li>)}
                                  </ul>
                                </div>
                                <div>
                                  <h5 className="text-[10px] font-bold text-text-secondary uppercase mb-4 flex items-center gap-2"><Lightbulb size={12}/> Execution Actions</h5>
                                  <ul className="space-y-2">
                                    {r.recommendation.key_actions.map((a,i)=><li key={i} className="text-xs flex items-start gap-2 text-text-secondary"><ChevronRight size={14} className="text-primary mt-0.5 shrink-0"/> {a}</li>)}
                                  </ul>
                                </div>
                              </div>
                            </div>
                          </motion.div>
                        </td>
                      </tr>
                    )}
                  </AnimatePresence>
                </React.Fragment>
              );
            })}
          </tbody>
        </table>
      </div>
    </div>
  );
}
