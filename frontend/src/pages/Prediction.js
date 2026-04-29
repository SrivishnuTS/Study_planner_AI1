import React, { useState } from 'react';
import api from '../utils/api';
import { 
  BrainCircuit, 
  ChevronRight, 
  Info, 
  AlertCircle,
  Save,
  CheckCircle2,
  SlidersHorizontal,
  Lightbulb,
  Sparkles,
  HelpCircle
} from 'lucide-react';
import { motion } from 'framer-motion';

export default function PredictPage() {
  const [form, setForm] = useState({
    study_hours: 4.0, break_time: 0.5, sleep_hours: 7.0, focus_score: 8.0, previous_score: 75,
    course: 'General', difficulty: 'medium', goal_type: 'revision',
    energy_level: 'medium', time_of_day: 'afternoon', distraction: 'low', day: 'monday'
  });

  const [prediction, setPrediction] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handlePredictAndSave = async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await api.post('/predict-and-save', form);
      setPrediction(res.data);
    } catch (e) {
      setError(e.response?.data?.message || "Connection failure to Intelligence Engine.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-6xl mx-auto p-4 md:p-8">
      <header className="mb-10 flex justify-between items-end">
        <div>
          <h1 className="text-4xl font-bold text-text tracking-tight font-serif mb-2 flex items-center gap-3">
            <BrainCircuit className="text-primary" size={32}/> Strategy Modeler
          </h1>
          <p className="text-text-secondary text-sm">Synchronize your behavioral profile with the AI Intelligence Engine.</p>
        </div>
        <button 
          onClick={handlePredictAndSave}
          disabled={loading}
          className="btn-primary px-8 py-3 flex items-center gap-2 shadow-xl shadow-primary/20 hover:scale-105 transition-all"
        >
          {loading ? (
            <div className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin"></div>
          ) : <Save size={18}/>}
          {loading ? "Syncing..." : "Save & Predict"}
        </button>
      </header>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-10 items-start">
        {/* Profile Inputs */}
        <div className="lg:col-span-5 space-y-8">
          <div className="classic-card">
            <h3 className="text-xs font-bold uppercase tracking-widest text-text-secondary border-b pb-3 mb-6 flex items-center gap-2">
              <SlidersHorizontal size={14}/> Behavioral Profile
            </h3>
            <div className="space-y-6">
              <div className="grid grid-cols-2 gap-6">
                <div>
                  <label className="text-xs font-bold text-text block mb-2">Focus: {form.focus_score}</label>
                  <input type="range" min="1" max="10" step="0.5" value={form.focus_score} onChange={e => setForm({...form, focus_score: parseFloat(e.target.value)})} className="w-full accent-primary h-1 bg-muted rounded-lg appearance-none cursor-pointer" />
                </div>
                <div>
                  <label className="text-xs font-bold text-text block mb-2">Prev Score: {form.previous_score}</label>
                  <input type="range" min="1" max="100" step="1" value={form.previous_score} onChange={e => setForm({...form, previous_score: parseFloat(e.target.value)})} className="w-full accent-primary h-1 bg-muted rounded-lg appearance-none cursor-pointer" />
                </div>
              </div>
              <div className="grid grid-cols-2 gap-4">
                {[
                  { label: 'Course', key: 'course', options: ['General', 'Data Structures', 'Algorithms', 'DBMS', 'Machine Learning', 'Mathematics'] },
                  { label: 'Difficulty', key: 'difficulty', options: ['low', 'medium', 'high'] },
                  { label: 'Goal Type', key: 'goal_type', options: ['concept', 'revision', 'exam'] },
                  { label: 'Energy Level', key: 'energy_level', options: ['low', 'medium', 'high'] },
                  { label: 'Time of Day', key: 'time_of_day', options: ['morning', 'afternoon', 'night'] },
                  { label: 'Distraction', key: 'distraction', options: ['low', 'medium', 'high'] },
                  { label: 'Day', key: 'day', options: ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'] }
                ].map(item => (
                  <div key={item.key}>
                    <label className="text-[10px] font-bold text-text-secondary uppercase mb-1.5 block">{item.label}</label>
                    <select value={form[item.key]} onChange={e => setForm({...form, [item.key]: e.target.value})} className="input-classic w-full text-sm">
                      {item.options.map(o => <option key={o} value={o}>{o}</option>)}
                    </select>
                  </div>
                ))}
                <div>
                  <label className="text-[10px] font-bold text-text-secondary uppercase mb-1.5 block">Sleep (h)</label>
                  <input type="number" step="0.5" value={form.sleep_hours} onChange={e => setForm({...form, sleep_hours: parseFloat(e.target.value)})} className="input-classic w-full text-sm" />
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Prediction Display */}
        <div className="lg:col-span-7 space-y-8">
          {error && (
            <div className="p-6 classic-card border-red-500/20 bg-red-500/5 text-center">
              <AlertCircle size={32} className="text-red-500 mx-auto mb-4"/>
              <h3 className="text-xl font-bold text-red-500 font-serif mb-2">Inference Error</h3>
              <p className="text-text-secondary text-sm">{error}</p>
            </div>
          )}

          {prediction && (
            <motion.div initial={{ opacity: 0, y: 15 }} animate={{ opacity: 1, y: 0 }} className="space-y-8">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div className="classic-card bg-primary/5 border-primary/20">
                  <p className="text-[10px] font-bold text-primary uppercase tracking-widest mb-2">Optimal Pattern</p>
                  <h2 className="text-3xl font-bold font-serif mb-4">{prediction.prediction}</h2>
                  <div className="flex items-center justify-between">
                    <span className="text-xs font-bold text-text-secondary uppercase">Confidence</span>
                    <span className="text-xl font-bold text-primary">{prediction.confidence}%</span>
                  </div>
                </div>
                <div className="classic-card flex flex-col justify-center">
                  <div className="flex items-center gap-2 mb-1">
                    <CheckCircle2 className="text-emerald-500" size={18}/>
                    <span className="text-xs font-bold text-emerald-500 uppercase tracking-widest">Strategy Logged</span>
                  </div>
                  <p className="text-[10px] text-text-secondary font-mono">ID: #{prediction.saved_id}</p>
                </div>
              </div>

              {prediction.recommendation && (
                <div className="classic-card border-primary/10 bg-primary/[0.02]">
                  <h4 className="text-xs font-bold text-primary uppercase tracking-widest mb-6 flex items-center gap-2">
                    <Sparkles size={14}/> Cognitive Strategy Map
                  </h4>
                  
                  <div className="space-y-8">
                    {/* Tier 1: Summary */}
                    <div className="bg-card p-5 rounded-2xl border border-border shadow-sm">
                      <p className="text-sm font-medium text-text leading-relaxed italic">
                        "{prediction.recommendation.summary}"
                      </p>
                    </div>

                    <div className="grid grid-cols-1 md:grid-cols-2 gap-10">
                      {/* Tier 2: Why it Works */}
                      <div>
                        <h5 className="text-[10px] font-bold text-text-secondary uppercase mb-4 flex items-center gap-2">
                          <HelpCircle size={12}/> Cognitive Reasoning
                        </h5>
                        <ul className="space-y-3">
                          {prediction.recommendation.explanation.map((item, i) => (
                            <li key={i} className="text-xs text-text-secondary flex gap-3">
                              <span className="w-1.5 h-1.5 rounded-full bg-primary mt-1.5 shrink-0"></span> {item}
                            </li>
                          ))}
                        </ul>
                      </div>

                      {/* Tier 3: Actions */}
                      <div>
                        <h5 className="text-[10px] font-bold text-text-secondary uppercase mb-4 flex items-center gap-2">
                          <Lightbulb size={12}/> Execution Actions
                        </h5>
                        <ul className="space-y-3">
                          {prediction.recommendation.key_actions.map((item, i) => (
                            <li key={i} className="text-xs text-text flex gap-3">
                              <ChevronRight size={14} className="text-primary shrink-0 mt-0.5"/> 
                              <span className="font-medium">{item}</span>
                            </li>
                          ))}
                        </ul>
                      </div>
                    </div>
                  </div>
                </div>
              )}
            </motion.div>
          )}
        </div>
      </div>
    </div>
  );
}
