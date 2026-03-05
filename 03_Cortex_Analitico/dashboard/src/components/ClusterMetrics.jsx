import React from 'react';
import { motion } from 'framer-motion';
import { Target, Lightbulb, Wrench, Settings } from 'lucide-react';

const ClusterMetrics = () => {
    // Agrupamento Dinâmico baseado na Visão de Fev 2026
    const clusters = [
        {
            name: "Estratégico",
            icon: <Target className="w-4 h-4 text-amber-400" />,
            color: "amber",
            agents: [
                { name: "Arquiteta de Contexto", weight: 0.9, activations: 12 },
                { name: "Analista Estratégico", weight: 0.7, activations: 8 },
                { name: "Curador Arquitetura", weight: 0.6, activations: 24 },
            ]
        },
        {
            name: "Criativo",
            icon: <Lightbulb className="w-4 h-4 text-purple-400" />,
            color: "purple",
            agents: [
                { name: "Designer de Visão", weight: 0.7, activations: 4 },
                { name: "Dev Fullstack", weight: 0.8, activations: 19 },
                { name: "Provocador Criativo", weight: 0.5, activations: 6 },
            ]
        },
        {
            name: "Operacional",
            icon: <Wrench className="w-4 h-4 text-blue-400" />,
            color: "blue",
            agents: [
                { name: "Arquitetura Gameplay", weight: 0.9, activations: 15 },
                { name: "Arquiteto Sonoro", weight: 0.6, activations: 2 },
                { name: "Auditor Integridade", weight: 0.7, activations: 5 },
            ]
        },
        {
            name: "Meta-Cognitivo",
            icon: <Settings className="w-4 h-4 text-emerald-400" />,
            color: "emerald",
            agents: [
                { name: "Engenheiro Redes", weight: 0.8, activations: 32 },
                { name: "Especialista IA", weight: 0.7, activations: 21 },
                { name: "Filósofo de Loops", weight: 0.6, activations: 0 },
            ]
        }
    ];

    return (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            {clusters.map((cluster, i) => (
                <motion.div
                    key={cluster.name}
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: i * 0.1 }}
                    className="glass bg-white/[0.02] p-6 rounded-[32px] border border-white/5 hover:border-white/10 transition-all group overflow-hidden relative"
                >
                    {/* Glossy Overlay */}
                    <div className="absolute top-0 right-0 w-32 h-32 bg-white/5 blur-3xl rounded-full -mr-16 -mt-16 group-hover:bg-white/10 transition-colors" />

                    <div className="flex items-center gap-3 mb-5 relative z-10">
                        <div className={`p-2.5 rounded-2xl bg-${cluster.color}-400/10 border border-${cluster.color}-400/20`}>
                            {cluster.icon}
                        </div>
                        <h3 className="text-[10px] font-mono font-black uppercase tracking-widest text-white/50 group-hover:text-white/80 transition-colors">
                            {cluster.name}
                        </h3>
                    </div>

                    <div className="space-y-4 relative z-10">
                        {cluster.agents.map((agent, j) => (
                            <div key={agent.name} className="space-y-2">
                                <div className="flex justify-between items-end px-0.5">
                                    <span className="text-[10px] text-white/40 font-medium truncate pr-2 group-hover:text-white/60">
                                        {agent.name}
                                    </span>
                                    <span className="text-[8px] font-mono text-white/20 group-hover:text-white/40">
                                        {agent.activations} act.
                                    </span>
                                </div>
                                <div className="h-1 bg-white/5 rounded-full overflow-hidden border border-white/5">
                                    <motion.div
                                        initial={{ width: 0 }}
                                        animate={{ width: `${agent.weight * 100}%` }}
                                        className={`h-full bg-gradient-to-r from-${cluster.color}-400/40 to-${cluster.color}-400/10`}
                                    />
                                </div>
                            </div>
                        ))}
                    </div>
                </motion.div>
            ))}
        </div>
    );
};

export default ClusterMetrics;
