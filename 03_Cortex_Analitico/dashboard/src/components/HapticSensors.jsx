import React, { useEffect, useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { GitBranch, Activity, Zap, AlertTriangle } from 'lucide-react';

const HapticSensors = () => {
    const [hapticData, setHapticData] = useState(null);
    const [loading, setLoading] = useState(true);

    const fetchHapticData = async () => {
        try {
            const res = await fetch('http://localhost:5000/api/haptic');
            const data = await res.json();
            setHapticData(data);
        } catch (err) {
            console.warn("Haptic Engine Offline");
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchHapticData();
        const interval = setInterval(fetchHapticData, 5000); // Atualiza a cada 5 segundos
        return () => clearInterval(interval);
    }, []);

    if (loading || !hapticData) return null;

    const getStatusColor = (status) => {
        switch (status) {
            case 'STABLE': return 'text-accent';
            case 'DENSE': return 'text-amber-400';
            case 'CRITICAL': return 'text-red-500';
            default: return 'text-muted';
        }
    };

    const getHealthGlow = (health) => {
        if (health > 0.8) return 'shadow-[0_0_30px_rgba(252,163,17,0.15)]';
        if (health > 0.5) return 'shadow-[0_0_30px_rgba(251,191,36,0.15)]';
        return 'shadow-[0_0_30px_rgba(231,111,81,0.15)]';
    };

    return (
        <motion.div
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            className={`glass-premium p-8 rounded-[40px] border-white/5 relative overflow-hidden group transition-all duration-700 ${getHealthGlow(hapticData.overall_health)}`}
        >
            <div className="flex justify-between items-center mb-8">
                <div>
                    <h3 className="text-[10px] font-mono text-muted uppercase tracking-[0.4em] mb-1 text-left">Arquitetura Háptica</h3>
                    <p className="text-sm text-white font-bold tracking-tight text-left flex items-center gap-2">
                        CORTEX_HEALTH_MONITOR
                        <span className={`text-[9px] px-2 py-0.5 rounded-full bg-white/5 font-mono ${getStatusColor(hapticData.status)}`}>
                            {hapticData.status}
                        </span>
                    </p>
                </div>
                <GitBranch className={`w-5 h-5 ${getStatusColor(hapticData.status)}`} />
            </div>

            <div className="grid grid-cols-2 gap-8 mb-8">
                <div className="space-y-1">
                    <span className="text-[9px] font-mono text-muted uppercase tracking-widest block text-left">Entropia Total</span>
                    <div className="flex items-center gap-2">
                        <span className="text-2xl font-bold text-white leading-none">{hapticData.total_entropy}</span>
                        <Activity className="w-3 h-3 text-accent/40" />
                    </div>
                </div>
                <div className="space-y-1">
                    <span className="text-[9px] font-mono text-muted uppercase tracking-widest block text-left">Complexidade</span>
                    <div className="flex items-center gap-2">
                        <span className="text-2xl font-bold text-white leading-none">{(hapticData.overall_health * 100).toFixed(0)}%</span>
                        <div className="w-1.5 h-1.5 rounded-full bg-accent animate-pulse" />
                    </div>
                </div>
            </div>

            {/* Heatmap de Arquivos */}
            <div className="space-y-4">
                <h4 className="text-[9px] font-mono text-muted uppercase tracking-[0.2em] mb-3 text-left">Pontos de Calor (Hotspots)</h4>
                <div className="space-y-3">
                    {hapticData.hottest_files.map((file, idx) => (
                        <div key={idx} className="flex flex-col gap-1.5 p-3 rounded-2xl bg-white/[0.02] border border-white/5 hover:bg-white/[0.04] transition-colors group/item">
                            <div className="flex justify-between items-center">
                                <span className="text-[11px] text-text/90 font-medium truncate w-40 text-left">{file.name}</span>
                                <span className="text-[10px] font-mono text-accent/60">{(file.entropy).toFixed(2)}</span>
                            </div>
                            <div className="h-1 w-full bg-white/5 rounded-full overflow-hidden">
                                <motion.div
                                    initial={{ width: 0 }}
                                    animate={{ width: `${Math.min(100, file.entropy * 100)}%` }}
                                    className={`h-full ${file.entropy > 0.5 ? 'bg-amber-400' : 'bg-accent'}`}
                                />
                            </div>
                        </div>
                    ))}
                </div>
            </div>

            {/* Alerta de Saúde */}
            <AnimatePresence>
                {hapticData.overall_health < 0.6 && (
                    <motion.div
                        initial={{ height: 0, opacity: 0 }}
                        animate={{ height: 'auto', opacity: 1 }}
                        exit={{ height: 0, opacity: 0 }}
                        className="mt-6 pt-6 border-t border-white/5 overflow-hidden"
                    >
                        <div className="flex gap-4 p-4 rounded-2xl bg-red-500/10 border border-red-500/20 items-center">
                            <AlertTriangle className="w-5 h-5 text-red-500 shrink-0" />
                            <p className="text-[10px] text-red-400 font-medium leading-tight text-left">
                                Detectada alta densidade entrópica no Connectome. Sugerida cristalização de padrões.
                            </p>
                        </div>
                    </motion.div>
                )}
            </AnimatePresence>
        </motion.div>
    );
};

export default HapticSensors;
