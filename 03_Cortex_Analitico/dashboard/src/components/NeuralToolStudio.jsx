import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Beaker, Plus, Trash2, Play, Activity, Tag, Cpu, ShieldCheck, X } from 'lucide-react';

const NeuralToolStudio = ({ onScanTrigger }) => {
    const [tools, setTools] = useState([]);
    const [loading, setLoading] = useState(true);
    const [isCreating, setIsCreating] = useState(false);
    const [scanResult, setScanResult] = useState(null);
    const [newTool, setNewTool] = useState({
        id: '',
        name: '',
        class: 'RelationalSymmetryTool',
        axiom_hooks: [],
        type: 'STATIC'
    });

    const fetchTools = async () => {
        try {
            const res = await fetch('http://localhost:5000/api/neural/tools');
            const data = await res.json();
            setTools(data.tools || []);
        } catch (err) {
            console.error("Studio Offline");
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchTools();
    }, []);

    const handleCreate = async () => {
        if (!newTool.id || !newTool.name) return;
        try {
            await fetch('http://localhost:5000/api/neural/tools', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(newTool)
            });
            setIsCreating(false);
            setNewTool({ id: '', name: '', class: 'RelationalSymmetryTool', axiom_hooks: [], type: 'STATIC' });
            fetchTools();
        } catch (err) {
            console.error(err);
        }
    };

    const handleDelete = async (id) => {
        try {
            await fetch(`http://localhost:5000/api/neural/tools/${id}`, { method: 'DELETE' });
            fetchTools();
        } catch (err) {
            console.error(err);
        }
    };

    const handleScan = async (toolId) => {
        setScanResult({ toolId, status: 'RUNNING' });
        if (onScanTrigger) onScanTrigger();
        try {
            const res = await fetch('http://localhost:5000/api/neural/tools/scan', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ tool_id: toolId })
            });
            const data = await res.json();
            setScanResult(data);
        } catch (err) {
            setScanResult({ status: 'ERROR', message: "Falha na varredura." });
        }
    };

    return (
        <div className="space-y-8 min-h-[600px]">
            {/* Header / Workbench Action */}
            <div className="flex justify-between items-center px-4">
                <div className="flex items-center gap-4">
                    <div className="p-3 rounded-2xl bg-accent/10 border border-accent/20">
                        <Beaker className="text-accent w-6 h-6" />
                    </div>
                    <div>
                        <h2 className="text-xl font-bold text-white tracking-tight">Neural Tool Studio</h2>
                        <p className="text-[10px] font-mono text-muted uppercase tracking-[0.2em]">Cognitive Engineering Workbench</p>
                    </div>
                </div>
                <button
                    onClick={() => setIsCreating(true)}
                    className="flex items-center gap-2 px-6 py-3 bg-accent text-background rounded-2xl font-bold text-xs uppercase tracking-widest hover:shadow-[0_0_20px_#00FFAB66] transition-all"
                >
                    <Plus className="w-4 h-4" /> Instanciar Ferramenta
                </button>
            </div>

            {/* Main Laboratory Grid */}
            {loading ? (
                <div className="flex justify-center items-center h-48">
                    <Activity className="animate-spin text-accent w-10 h-10" />
                </div>
            ) : (
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                    <AnimatePresence>
                        {tools.map((tool) => (
                            <motion.div
                                key={tool.id}
                                layout
                                initial={{ opacity: 0, scale: 0.9 }}
                                animate={{ opacity: 1, scale: 1 }}
                                exit={{ opacity: 0, scale: 0.9 }}
                                className="glass-premium p-6 rounded-[32px] border-white/10 flex flex-col justify-between group h-full relative overflow-hidden"
                            >
                                <div className="space-y-4 relative z-10">
                                    <div className="flex justify-between items-start">
                                        <div className="p-2 rounded-xl bg-white/5">
                                            {tool.type === 'DYNAMIC' ? <Cpu className="w-4 h-4 text-purple-400" /> : <ShieldCheck className="w-4 h-4 text-accent" />}
                                        </div>
                                        <button
                                            onClick={() => handleDelete(tool.id)}
                                            className="p-2 opacity-0 group-hover:opacity-100 text-alert/50 hover:text-alert transition-all"
                                        >
                                            <Trash2 className="w-4 h-4" />
                                        </button>
                                    </div>

                                    <div>
                                        <h3 className="text-lg font-bold text-white mb-1">{tool.name}</h3>
                                        <p className="text-[9px] font-mono text-muted uppercase tracking-widest">{tool.id}</p>
                                    </div>

                                    <div className="flex flex-wrap gap-2">
                                        {tool.axiom_hooks && tool.axiom_hooks.map(axiom => (
                                            <span key={axiom} className="px-2 py-1 rounded-md bg-accent/5 border border-accent/10 text-[9px] font-mono text-accent/80">
                                                <Tag className="w-2 h-2 inline mr-1" /> {axiom}
                                            </span>
                                        ))}
                                    </div>
                                </div>

                                <div className="mt-6 flex items-center gap-3">
                                    <button
                                        onClick={() => handleScan(tool.id)}
                                        className="flex-1 flex items-center justify-center gap-2 py-3 bg-white/5 border border-white/10 rounded-2xl text-[10px] font-mono font-bold uppercase tracking-widest hover:bg-accent/10 hover:border-accent/30 transition-all"
                                    >
                                        <Play className="w-3 h-3" /> Run Scan
                                    </button>
                                </div>

                                {/* Background Glow Effect on hover */}
                                <div className="absolute inset-0 bg-accent/5 opacity-0 group-hover:opacity-100 transition-opacity pointer-events-none" />
                            </motion.div>
                        ))}
                    </AnimatePresence>
                </div>
            )}

            {/* Scan Results Panel */}
            {scanResult && (
                <motion.div
                    initial={{ opacity: 0, y: 30 }}
                    animate={{ opacity: 1, y: 0 }}
                    className="glass-premium p-8 rounded-[40px] border-accent/30 bg-accent/5"
                >
                    <div className="flex justify-between items-center mb-6">
                        <h3 className="text-xs font-mono font-bold text-accent uppercase tracking-[0.4em]">Scan Output :: {scanResult.toolId || 'LIVE'}</h3>
                        <button onClick={() => setScanResult(null)} className="text-muted hover:text-white transition-all"><X className="w-4 h-4" /></button>
                    </div>

                    {scanResult.status === 'RUNNING' ? (
                        <div className="flex items-center gap-4 text-accent animate-pulse">
                            <Activity className="w-5 h-5" />
                            <span className="text-xs font-mono uppercase tracking-widest">Processando Padrões...</span>
                        </div>
                    ) : (
                        <div className="bg-black/40 rounded-2xl p-6 font-mono text-[11px] text-slate-300 max-h-[300px] overflow-auto border border-white/5">
                            <pre>{JSON.stringify(scanResult, null, 2)}</pre>
                        </div>
                    )}
                </motion.div>
            )}

            {/* Modal de Criação */}
            <AnimatePresence>
                {isCreating && (
                    <div className="fixed inset-0 z-[100] flex items-center justify-center p-6 backdrop-blur-xl bg-black/60">
                        <motion.div
                            initial={{ opacity: 0, scale: 0.9, y: 20 }}
                            animate={{ opacity: 1, scale: 1, y: 0 }}
                            exit={{ opacity: 0, scale: 0.9, y: 20 }}
                            className="glass-premium p-10 rounded-[48px] border-white/20 w-full max-w-xl shadow-2xl relative"
                        >
                            <button onClick={() => setIsCreating(false)} className="absolute top-8 right-8 text-muted hover:text-white"><X className="w-6 h-6" /></button>

                            <h2 className="text-2xl font-bold text-white mb-2">Novo Axioma de Ferrramenta</h2>
                            <p className="text-xs text-muted mb-8">Defina uma nova estrutura cognitiva para rastreio de padrões.</p>

                            <div className="space-y-6">
                                <div className="space-y-2">
                                    <label className="text-[10px] font-mono text-muted uppercase tracking-widest">Identificador Neural (ID)</label>
                                    <input
                                        type="text"
                                        placeholder="nt_pattern_detector"
                                        value={newTool.id}
                                        onChange={(e) => setNewTool({ ...newTool, id: e.target.value })}
                                        className="w-full bg-white/5 border border-white/10 rounded-2xl p-4 text-sm text-white focus:border-accent/40 focus:outline-none transition-all"
                                    />
                                </div>
                                <div className="space-y-2">
                                    <label className="text-[10px] font-mono text-muted uppercase tracking-widest">Nome da Ferramenta</label>
                                    <input
                                        type="text"
                                        placeholder="Detector de Padrões"
                                        value={newTool.name}
                                        onChange={(e) => setNewTool({ ...newTool, name: e.target.value })}
                                        className="w-full bg-white/5 border border-white/10 rounded-2xl p-4 text-sm text-white focus:border-accent/40 focus:outline-none transition-all"
                                    />
                                </div>
                                <div className="grid grid-cols-2 gap-6">
                                    <div className="space-y-2">
                                        <label className="text-[10px] font-mono text-muted uppercase tracking-widest">Classe Logic</label>
                                        <select
                                            value={newTool.class}
                                            onChange={(e) => setNewTool({ ...newTool, class: e.target.value })}
                                            className="w-full bg-white/5 border border-white/10 rounded-2xl p-4 text-sm text-white focus:border-accent/40 focus:outline-none transition-all"
                                        >
                                            <option value="RelationalSymmetryTool">RelationalSymmetry</option>
                                            <option value="DynamicPredictiveTool">DynamicPredictive</option>
                                        </select>
                                    </div>
                                    <div className="space-y-2">
                                        <label className="text-[10px] font-mono text-muted uppercase tracking-widest">Tipo</label>
                                        <select
                                            value={newTool.type}
                                            onChange={(e) => setNewTool({ ...newTool, type: e.target.value })}
                                            className="w-full bg-white/5 border border-white/10 rounded-2xl p-4 text-sm text-white focus:border-accent/40 focus:outline-none transition-all"
                                        >
                                            <option value="STATIC">Static</option>
                                            <option value="DYNAMIC">Dynamic</option>
                                        </select>
                                    </div>
                                </div>

                                <div className="pt-6">
                                    <button
                                        onClick={handleCreate}
                                        className="w-full py-4 bg-accent text-background rounded-3xl font-bold text-sm uppercase tracking-[0.2em] shadow-[0_0_30px_#00FFAB44]"
                                    >
                                        Materializar Ferramenta
                                    </button>
                                </div>
                            </div>
                        </motion.div>
                    </div>
                )}
            </AnimatePresence>
        </div>
    );
};

export default NeuralToolStudio;
