import React, { useEffect, useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { AlertTriangle, ShieldCheck, Activity, Terminal } from 'lucide-react';

const HomeostasisPanel = () => {
    const [alerts, setAlerts] = useState([
        { id: 1, type: 'warning', message: '7 agents with 0 activations detected', time: 'SYSTEM_START' },
        { id: 2, type: 'success', message: 'All specialists in healthy range (0.4-1.1)', time: 'STABLE' },
        { id: 3, type: 'success', message: 'Sync Pulse Integrity: 100%', time: 'NOMINAL' }
    ]);

    return (
        <div className="flex flex-col gap-4 h-full">
            <h2 className="text-[10px] font-black text-white/40 tracking-[0.2em] uppercase flex items-center gap-2 px-1">
                <ShieldCheck className="w-3 h-3" /> Homeostatic_Sentinel
            </h2>

            <div className="flex-1 space-y-3 overflow-y-auto pr-2 custom-scrollbar">
                <AnimatePresence>
                    {alerts.map((alert) => (
                        <motion.div
                            key={alert.id}
                            initial={{ opacity: 0, scale: 0.95 }}
                            animate={{ opacity: 1, scale: 1 }}
                            exit={{ opacity: 0, scale: 0.95 }}
                            className={`p-4 rounded-2xl border flex gap-3 ${alert.type === 'warning'
                                    ? 'bg-amber-400/5 border-amber-400/20 text-amber-200/80 shadow-[0_0_15px_rgba(251,191,36,0.05)]'
                                    : 'bg-accent/5 border-accent/20 text-accent/80 shadow-[0_0_15px_rgba(0,255,171,0.05)]'
                                }`}
                        >
                            {alert.type === 'warning' ? <AlertTriangle className="w-4 h-4 shrink-0" /> : <Activity className="w-4 h-4 shrink-0" />}
                            <div className="flex flex-col gap-1">
                                <span className="text-[10px] font-medium leading-tight">{alert.message}</span>
                                <span className="text-[8px] font-mono opacity-50 uppercase tracking-tighter">{alert.time}</span>
                            </div>
                        </motion.div>
                    ))}
                </AnimatePresence>
            </div>

            <div className="mt-auto glass bg-black/40 border border-white/5 rounded-2xl p-3 flex items-center justify-between">
                <div className="flex items-center gap-2">
                    <Terminal className="w-3 h-3 text-muted" />
                    <span className="text-[9px] font-mono text-muted uppercase">Entropy_Status</span>
                </div>
                <div className="flex gap-1">
                    {[1, 2, 3, 4, 5, 6, 7].map(i => (
                        <div key={i} className={`h-1 w-2 rounded-full ${i < 3 ? 'bg-accent/40' : 'bg-white/5'}`} />
                    ))}
                </div>
            </div>
        </div>
    );
};

export default HomeostasisPanel;
