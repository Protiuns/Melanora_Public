import React, { useEffect, useState, useMemo } from 'react';
import { motion } from 'framer-motion';

const NeuralMap = ({ active, frequency, intensity }) => {
    const nodeCount = 50;

    // Estrutura da rede neural com pesos de energia
    const nodes = useMemo(() => {
        return Array.from({ length: nodeCount }).map((_, i) => {
            const connections = Array.from({ length: 2 }).map(() => ({
                id: Math.floor(Math.random() * nodeCount),
                energy: Math.random() // Peso de energia sináptica
            }));

            return {
                id: i,
                x: 10 + Math.random() * 80,
                y: 10 + Math.random() * 80,
                size: 2 + Math.random() * 4,
                delay: Math.random() * 2,
                connections
            };
        });
    }, []);

    const pulseDuration = active ? Math.max(0.05, 1.5 / (frequency || 100)) : 3;

    return (
        <div className="relative w-full h-[400px] glass-premium rounded-3xl overflow-hidden mb-6 flex items-center justify-center border-white/10 group">
            {/* Background Grid - Sophisticated */}
            <div className="absolute inset-0 opacity-[0.05] pointer-events-none transition-opacity group-hover:opacity-[0.08]"
                style={{
                    backgroundImage: 'linear-gradient(rgba(0, 255, 171, 0.1) 1px, transparent 1px), linear-gradient(90deg, rgba(139, 92, 246, 0.1) 1px, transparent 1px)',
                    backgroundSize: '40px 40px'
                }} />

            <svg width="100%" height="100%" viewBox="0 0 100 100" preserveAspectRatio="none" className="absolute inset-0 p-8">
                <defs>
                    <filter id="neural-glow" x="-50%" y="-50%" width="200%" height="200%">
                        <feGaussianBlur stdDeviation="0.6" result="blur" />
                        <feComposite in="SourceGraphic" in2="blur" operator="over" />
                    </filter>
                    <radialGradient id="nodeGradient">
                        <stop offset="0%" stopColor="var(--neural-accent)" />
                        <stop offset="100%" stopColor="rgba(0, 255, 171, 0)" />
                    </radialGradient>
                </defs>

                {/* Connections (The 'Fibras de Luz' effect) */}
                {nodes.map(node =>
                    node.connections.map(edge => {
                        const target = nodes[edge.id];
                        if (!target) return null;

                        const isHighEnergy = edge.energy > 0.8;
                        const strokeColor = isHighEnergy ? 'var(--neural-accent)' : 'rgba(100, 116, 139, 0.1)';
                        const strokeWidth = isHighEnergy ? '0.35' : '0.05';
                        const opacity = isHighEnergy ? 0.8 : 0.15;

                        return (
                            <React.Fragment key={`${node.id}-${edge.id}`}>
                                <line
                                    x1={node.x} y1={node.y}
                                    x2={target.x} y2={target.y}
                                    stroke={strokeColor}
                                    strokeWidth={strokeWidth}
                                    strokeDasharray="0.1 1.2"
                                    strokeLinecap="round"
                                    opacity={opacity}
                                    style={isHighEnergy ? { filter: 'url(#neural-glow)' } : {}}
                                    className="transition-all duration-1000"
                                />

                                {/* High Intensity Signal Propagation */}
                                {active && isHighEnergy && (
                                    <motion.circle
                                        r="0.25"
                                        fill="var(--neural-accent)"
                                        style={{ filter: 'url(#neural-glow)' }}
                                        animate={{
                                            cx: [node.x, target.x],
                                            cy: [node.y, target.y],
                                            opacity: [0, 1, 0]
                                        }}
                                        transition={{
                                            duration: pulseDuration * 2,
                                            repeat: Infinity,
                                            delay: node.delay + (edge.energy * 2),
                                            ease: "easeInOut"
                                        }}
                                    />
                                )}
                            </React.Fragment>
                        );
                    })
                )}

                {/* Neurons (Nodes) */}
                {nodes.map(node => (
                    <g key={node.id}>
                        <motion.circle
                            cx={node.x}
                            cy={node.y}
                            r={node.size / 15}
                            fill={active ? "var(--neural-accent)" : "rgba(148, 163, 184, 0.1)"}
                            initial={{ opacity: 0.2 }}
                            animate={active ? {
                                opacity: [0.3, 1, 0.3],
                                r: [node.size / 15, node.size / 12, node.size / 15],
                            } : {}}
                            transition={{
                                duration: pulseDuration * 2,
                                repeat: Infinity,
                                delay: node.delay,
                                ease: "easeInOut"
                            }}
                            style={active ? { filter: 'url(#neural-glow)' } : {}}
                        />
                    </g>
                ))}
            </svg>

            {/* Neural HUD Overlay */}
            <div className="absolute top-6 right-6 flex flex-col items-end">
                <span className="text-[7px] font-mono text-muted uppercase tracking-[0.4em]">Synaptic Density</span>
                <div className="h-0.5 w-24 bg-white/5 mt-1 overflow-hidden rounded-full">
                    <motion.div
                        className="h-full bg-accent"
                        animate={{ width: active ? '76%' : '10%' }}
                    />
                </div>
            </div>

            <div className="absolute bottom-6 left-6 flex flex-col">
                <span className="text-[9px] font-mono text-muted uppercase tracking-[0.3em] font-light">Neural Oscillator</span>
                <div className="flex items-center gap-3">
                    <div className={`w-1.5 h-1.5 rounded-full ${active ? 'bg-accent shadow-[0_0_10px_#00FFAB]' : 'bg-muted/20'}`} />
                    <span className="text-[14px] font-bold text-white font-mono tracking-tighter">
                        {active ? frequency.toLocaleString() : '---'} <span className="text-[10px] text-muted font-normal">Hz</span>
                    </span>
                </div>
            </div>

            {!active && (
                <div className="absolute inset-0 flex items-center justify-center bg-black/60 backdrop-blur-[4px]">
                    <div className="flex flex-col items-center gap-2">
                        <span className="text-[10px] font-mono text-accent/50 uppercase tracking-[0.5em] animate-pulse">Hibernating</span>
                        <div className="w-32 h-[1px] bg-gradient-to-r from-transparent via-accent/20 to-transparent" />
                    </div>
                </div>
            )}
        </div>
    );
};

export default NeuralMap;
