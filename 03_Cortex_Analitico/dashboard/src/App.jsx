import React, { useState, useEffect } from 'react';
import {
  Activity,
  BrainCircuit,
  Cpu,
  Power,
  Zap,
  Network,
  Info,
  Keyboard
} from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

// Componentes do Córtex
import ConnectomeGraph from './components/ConnectomeGraph';
import CommunicationCenter from './components/CommunicationCenter';
import VisionFeed from './components/VisionFeed';
import System2Panel from './components/System2Panel';
import MemoryMap from './components/MemoryMap';
import ClusterMetrics from './components/ClusterMetrics';
import HapticSensors from './components/HapticSensors';
import KnowledgeSubnets from './components/KnowledgeSubnets';
import HomeostasisPanel from './components/HomeostasisPanel';
import NeuralTags from './components/NeuralTags';

const API_BASE = "http://localhost:5000/api";

function App() {
  const [state, setState] = useState({
    active: false,
    intensity: 'MEDIUM',
    symbiotic_mode: 'NORMAL',
    processed: 0,
    latency: 0,
    cpu_load: 0,
    frequency: 0,
    cognitive_status: 'STABLE'
  });
  const [loading, setLoading] = useState(false);
  const [pulsing, setPulsing] = useState(false);

  // Polling de Estado Global
  const fetchState = async () => {
    try {
      const res = await fetch(`${API_BASE}/state`);
      const data = await res.json();
      setState(prev => ({ ...prev, ...data }));
    } catch (e) {
      console.warn("Melanora API Connection Failure");
    }
  };

  useEffect(() => {
    fetchState();
    const interval = setInterval(fetchState, 2500);
    return () => clearInterval(interval);
  }, []);

  const togglePower = async () => {
    setLoading(true);
    try {
      const res = await fetch(`${API_BASE}/toggle`, { method: 'POST' });
      const data = await res.json();
      setState(prev => ({ ...prev, active: data.active }));
      if (data.active) {
        setPulsing(true);
        setTimeout(() => setPulsing(false), 3000);
      }
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-background p-4 lg:p-8 flex flex-col gap-8 select-none overflow-x-hidden text-text">
      {/* Background Organic Pulse */}
      <div className="pulse-organic top-[-10%] left-[-10%]" />
      <div className="pulse-organic bottom-[-20%] right-[-10%] opacity-40 scale-75" style={{ animationDelay: '5s' }} />

      {/* --- Tier 1: Header Neural (Nível Executivo) --- */}
      <header className="flex justify-between items-center glass-premium px-8 py-5 rounded-[32px] z-50 border-accent/10 shadow-2xl">
        <div className="flex items-center gap-6">
          <div className="flex items-center gap-4">
            <div className={`w-12 h-12 rounded-[22px] flex items-center justify-center relative overflow-hidden transition-all duration-700 ${state.active ? 'bg-accent shadow-[0_0_30px_rgba(0,255,171,0.4)]' : 'bg-white/5 opacity-50'}`}>
              <BrainCircuit className={`w-7 h-7 ${state.active ? 'text-background' : 'text-muted'}`} />
            </div>
            <div>
              <h1 className="text-xl font-bold tracking-tighter text-glow flex items-center gap-2">
                MELANORA <span className="text-[10px] bg-accent/10 text-accent px-2 py-0.5 rounded-full border border-accent/20">V5.2</span>
              </h1>
              <p className="text-[9px] text-muted font-mono uppercase tracking-[0.3em]">Córtex Ativado :: Integridade_{state.cognitive_status}</p>
            </div>
          </div>
          <div className="flex items-center gap-3 pl-6 border-l border-white/5">
            <span className="text-[10px] font-mono text-accent uppercase tracking-widest">{state.active ? 'Mind_Active' : 'Mind_Dormant'}</span>
            <NeuralTags />
          </div>
        </div>

        <div className="flex items-center gap-4">
          <div className="hidden xl:flex items-center gap-4 px-4 py-2 bg-white/5 rounded-2xl border border-white/5">
            <div className="flex flex-col items-center px-3 border-r border-white/10">
              <span className="text-[7px] text-muted uppercase">Latency</span>
              <span className="text-[10px] font-mono font-bold text-accent">{state.latency}ms</span>
            </div>
            <div className="flex flex-col items-center px-3">
              <span className="text-[7px] text-muted uppercase">Pulsos</span>
              <span className="text-[10px] font-mono font-bold text-secondary">{state.processed}</span>
            </div>
          </div>
          <button
            onClick={togglePower}
            disabled={loading}
            className={`px-8 py-3 rounded-2xl font-bold text-[10px] tracking-widest transition-all uppercase flex items-center gap-3 border shadow-lg ${state.active
              ? 'bg-alert/10 text-alert border-alert/20 hover:bg-alert/20'
              : 'bg-accent text-background border-accent/30 hover:shadow-[0_0_25px_rgba(0,255,171,0.4)]'
              }`}
          >
            {loading ? <Activity className="w-4 h-4 animate-spin" /> : <Power className="w-4 h-4" />}
            {state.active ? 'Terminate' : 'Ignition'}
          </button>
        </div>
      </header>

      <div className="flex flex-col gap-8">
        {/* --- Tier 2: Loop Cognitivo & Homeostase --- */}
        <section className="grid grid-cols-12 gap-8 h-[500px]">
          {/* Percepção (Visão) */}
          <div className="col-span-12 lg:col-span-4 h-full">
            <VisionFeed />
          </div>
          {/* Comunicação Central */}
          <div className="col-span-12 lg:col-span-5 h-full">
            <CommunicationCenter symbioticMode={state.symbiotic_mode} />
          </div>
          {/* Sentinela Homeostático */}
          <div className="col-span-12 lg:col-span-3 h-full glass-premium rounded-[32px] p-6 border-white/5 shadow-xl">
            <HomeostasisPanel />
          </div>
        </section>

        {/* --- Tier 3: Estrutura Neural & Clusters --- */}
        <section className="grid grid-cols-12 gap-8 min-h-[400px]">
          {/* Conectoma & Sub-redes */}
          <div className="col-span-12 lg:col-span-9 flex flex-col gap-8">
            <div className="grid grid-cols-12 gap-8 h-full">
              {/* Grafo do Conectoma */}
              <div className="col-span-12 lg:col-span-8 glass-premium rounded-[40px] overflow-hidden relative border-accent/10 shadow-inner h-full min-h-[400px]">
                <ConnectomeGraph active={state.active} frequency={state.frequency} pulsing={pulsing} />
                <div className="absolute top-6 left-6 flex items-center gap-2 glass px-3 py-1.5 rounded-full border-white/10">
                  <Network className="w-3 h-3 text-accent" />
                  <span className="text-[9px] font-mono uppercase tracking-widest">Connectome_Mapping</span>
                </div>
              </div>
              {/* Hub de Conhecimento */}
              <div className="col-span-12 lg:col-span-4 glass-premium rounded-[32px] p-6 border-white/5">
                <KnowledgeSubnets />
              </div>
            </div>
            {/* Cluster Metrics (Ocupa a largura toda desse tier abaixo do grafo) */}
            <div className="w-full">
              <ClusterMetrics />
            </div>
          </div>

          {/* Haptic & Hardware Monitor */}
          <div className="col-span-12 lg:col-span-3 flex flex-col gap-8">
            <section className="glass-premium rounded-[32px] p-6 flex-1 border-white/5">
              <HapticSensors />
              <div className="mt-8 space-y-6">
                <StatBar label="System Load" value={state.cpu_load} color="accent" />
                <StatBar label="Neural Entropy" value={15} color="secondary" />
                <StatBar label="Sync Health" value={98} color="emotion" />
              </div>
            </section>
          </div>
        </section>

        {/* --- Tier 4: Análise Profunda (Sistema 2) --- */}
        <section className="grid grid-cols-1 gap-8">
          <System2Panel />
        </section>
      </div>

      {/* Bio-Footer */}
      <footer className="glass-premium px-10 py-4 rounded-[28px] flex justify-between items-center text-[9px] font-mono text-muted tracking-[0.4em] border-white/5">
        <div className="flex items-center gap-10">
          <span className="flex items-center gap-2">MELANORA_MIND_RESONANCE_OK</span>
          <span className="opacity-20">|</span>
          <span className="flex items-center gap-2"><Cpu className="w-3 h-3" /> {state.hardware?.slice(0, 30) || 'Unknown CPU'}</span>
        </div>
        <div className="opacity-40 uppercase tracking-widest">Single Source of Truth :: 2026</div>
      </footer>
    </div>
  );
}

// Utility Components
function StatBar({ label, value, color, suffix = '%' }) {
  const colors = {
    accent: 'bg-accent shadow-[0_0_10px_rgba(0,255,171,0.4)]',
    secondary: 'bg-secondary shadow-[0_0_10px_rgba(139,92,246,0.4)]',
    emotion: 'bg-emotion shadow-[0_0_10px_rgba(255,92,142,0.4)]'
  };

  return (
    <div className="space-y-2">
      <div className="flex justify-between text-[10px] font-bold text-muted">
        <span>{label}</span>
        <span className="font-mono">{Math.round(value)}{suffix}</span>
      </div>
      <div className="h-1 bg-white/5 rounded-full overflow-hidden">
        <motion.div
          initial={{ width: 0 }}
          animate={{ width: `${value}%` }}
          className={`h-full ${colors[color]}`}
        />
      </div>
    </div>
  );
}

export default App;
