import React from 'react';
import { motion } from 'framer-motion';
import { Database, BookOpen, Layers, Microscope, CheckCircle2 } from 'lucide-react';

const KnowledgeSubnets = () => {
    // Dados extraídos do relatório de Fev 2026
    const subnets = [
        { id: "theoretical", name: "Mente Teórica", docs: 38, icon: <Database className="w-3 h-3 text-accent" />, status: "stable" },
        { id: "articles", name: "Ateliê Artigos", docs: 21, icon: <BookOpen className="w-3 h-3 text-secondary" />, status: "stable" },
        { id: "nexus", name: "Studio Nexus", docs: "120+", icon: <Layers className="w-3 h-3 text-emotion" />, status: "stable" },
        { id: "research", name: "Central Pesquisa", docs: 23, icon: <Microscope className="w-3 h-3 text-amber-400" />, status: "stable" }
    ];

    return (
        <div className="space-y-4">
            <h2 className="text-[10px] font-black text-white/40 tracking-[0.2em] uppercase flex items-center gap-2 px-1">
                <Database className="w-3 h-3" /> Knowledge_Subnets_v2.0
            </h2>
            <div className="grid grid-cols-1 gap-2">
                {subnets.map((subnet, i) => (
                    <motion.div
                        key={subnet.id}
                        initial={{ opacity: 0, x: -10 }}
                        animate={{ opacity: 1, x: 0 }}
                        transition={{ delay: i * 0.1 }}
                        className="glass bg-white/[0.02] hover:bg-white/[0.05] border border-white/5 hover:border-white/10 p-3 rounded-2xl flex items-center justify-between group transition-all"
                    >
                        <div className="flex items-center gap-3">
                            <div className="p-2 rounded-xl bg-white/5 group-hover:bg-white/10 transition-colors">
                                {subnet.icon}
                            </div>
                            <div>
                                <h3 className="text-[11px] font-bold text-white/80">{subnet.name}</h3>
                                <p className="text-[9px] text-muted font-mono">{subnet.docs} Objects Indexed</p>
                            </div>
                        </div>
                        <div className="flex items-center gap-2">
                            <CheckCircle2 className="w-3.5 h-3.5 text-accent opacity-50 group-hover:opacity-100 transition-opacity" />
                        </div>
                    </motion.div>
                ))}
            </div>
        </div>
    );
};

export default KnowledgeSubnets;
