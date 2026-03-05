import React, { useRef, useState, useEffect, useCallback } from 'react';
import ForceGraph2D from 'react-force-graph-2d';
import { motion, AnimatePresence } from 'framer-motion';
import { ZoomIn, ZoomOut, Maximize2, Tag, Activity } from 'lucide-react';

const ConnectomeGraph = ({ active, frequency, pulsing }) => {
    const fgRef = useRef();
    const containerRef = useRef();
    const [dimensions, setDimensions] = useState({ width: 800, height: 400 });
    const [graphData, setGraphData] = useState({ nodes: [], links: [], summary: {} });
    const [hoverNode, setHoverNode] = useState(null);
    const [selectedNode, setSelectedNode] = useState(null);

    // Ajustar dimensões ao container
    useEffect(() => {
        const updateDimensions = () => {
            if (containerRef.current) {
                const { width, height } = containerRef.current.getBoundingClientRect();
                setDimensions({ width, height: height || 400 });
            }
        };
        updateDimensions();
        window.addEventListener('resize', updateDimensions);
        // Delay extra para garantir que o layout renderizou
        setTimeout(updateDimensions, 100);
        return () => window.removeEventListener('resize', updateDimensions);
    }, []);

    // Gerar "Neurônios Espalhados na Mente"
    useEffect(() => {
        const numNodes = 60; // Cluster denso e visualmente rico
        const areas = ['Córtex Analítico', 'Motor Godot', 'Memória Vectorial', 'Ponte LLM', 'Sentinela Axiomático'];
        const nodes = Array.from({ length: numNodes }, (_, i) => ({
            id: i,
            label: `Neurônio-${Math.floor(Math.random() * 9000) + 1000}`,
            area: areas[Math.floor(Math.random() * areas.length)],
            val: Math.random() * 5 + 1, // Tamanho do nó
            tags: ['Ativo', 'Sinapse']
        }));

        const links = [];
        for (let i = 0; i < numNodes * 1.5; i++) {
            const source = Math.floor(Math.random() * numNodes);
            let target = Math.floor(Math.random() * numNodes);
            while (target === source) {
                target = Math.floor(Math.random() * numNodes);
            }
            links.push({
                source,
                target,
                value: Math.random() * 2 + 0.5
            });
        }

        setGraphData({
            nodes,
            links,
            summary: { phi: 3.14, total_links: links.length }
        });
    }, []);

    const particleCount = active ? (pulsing ? 8 : 2) : 0;
    const particleSpeed = pulsing ? 0.02 : 0.005;

    const paintNode = useCallback((node, ctx, globalScale) => {
        const isHovered = node === hoverNode;
        const isSelected = node === selectedNode;

        // Cores baseadas na área simulando clusters neurais
        const color = node.area === 'Sentinela Axiomático' ? '#FF5C8E' :
            node.area === 'Ponte LLM' ? '#8B5CF6' : '#00FFAB';

        const size = (node.val || 2) * (isHovered || isSelected ? 1.5 : 1);

        ctx.beginPath();
        ctx.arc(node.x, node.y, size, 0, 2 * Math.PI, false);
        ctx.fillStyle = color;
        ctx.fill();

        // Glow effect para o nó
        if (active) {
            ctx.shadowBlur = isHovered ? 20 : 10;
            ctx.shadowColor = color;
            ctx.fill();
            ctx.shadowBlur = 0; // Reset
        }

        if (globalScale >= 2 && (isHovered || isSelected)) {
            const fontSize = 12 / globalScale;
            ctx.font = `${fontSize}px monospace`;
            ctx.textAlign = 'center';
            ctx.textBaseline = 'middle';
            ctx.fillStyle = '#FFFFFF';
            ctx.fillText(node.label, node.x, node.y + size + 4);
        }
    }, [hoverNode, selectedNode, active]);

    const handleNodeClick = useCallback(node => {
        setSelectedNode(node);
        if (fgRef.current) {
            fgRef.current.centerAt(node.x, node.y, 1000);
            fgRef.current.zoom(4, 1000);
        }
    }, [fgRef]);

    const resetZoom = () => {
        setSelectedNode(null);
        if (fgRef.current) {
            fgRef.current.zoomToFit(800, 50);
        }
    };

    return (
        <div ref={containerRef} className="relative w-full h-full glass-premium rounded-[inherit] overflow-hidden group border border-accent/5 shadow-2xl bg-black/50">
            {/* Background Narrative Layers */}
            <div className="absolute inset-0 pointer-events-none transition-opacity duration-1000 opacity-20">
                <div className="absolute top-1/4 left-1/4 w-[500px] h-[500px] bg-accent/5 rounded-full blur-[100px] mix-blend-screen" />
                <div className="absolute bottom-1/4 right-1/4 w-[600px] h-[600px] bg-secondary/5 rounded-full blur-[120px] mix-blend-screen" />
            </div>

            {graphData.nodes.length > 0 && (
                <ForceGraph2D
                    ref={fgRef}
                    graphData={graphData}
                    width={dimensions.width}
                    height={dimensions.height}
                    backgroundColor="rgba(0,0,0,0)"
                    nodeCanvasObject={paintNode}
                    nodeRelSize={4}
                    linkColor={() => active || pulsing ? 'rgba(0, 255, 171, 0.15)' : 'rgba(255, 255, 255, 0.02)'}
                    linkWidth={link => (active || pulsing ? 2 : 1) * link.value}
                    linkDirectionalParticles={particleCount}
                    linkDirectionalParticleSpeed={d => d.value * particleSpeed}
                    linkDirectionalParticleWidth={pulsing ? 3 : 1.5}
                    linkDirectionalParticleColor={() => pulsing ? '#8B5CF6' : '#00FFAB'}
                    onNodeClick={handleNodeClick}
                    onNodeHover={setHoverNode}
                    cooldownTicks={200}
                    d3VelocityDecay={0.4}
                />
            )}

            {/* HUD Controls */}
            <div className="absolute bottom-6 right-8 flex gap-2 z-10">
                <button onClick={() => fgRef.current?.zoom(fgRef.current.zoom() * 1.2, 400)} className="p-3 bg-white/5 hover:bg-white/10 rounded-xl border border-white/5 text-muted transition-all">
                    <ZoomIn className="w-4 h-4" />
                </button>
                <button onClick={() => fgRef.current?.zoom(fgRef.current.zoom() * 0.8, 400)} className="p-3 bg-white/5 hover:bg-white/10 rounded-xl border border-white/5 text-muted transition-all">
                    <ZoomOut className="w-4 h-4" />
                </button>
                <button onClick={resetZoom} className="p-3 bg-white/5 hover:bg-white/10 rounded-xl border border-white/5 text-muted transition-all">
                    <Maximize2 className="w-4 h-4" />
                </button>
            </div>

            {/* Neural Meta Info */}
            <div className="absolute top-8 left-10 pointer-events-none z-10">
                <div className="flex items-center gap-3 mb-2">
                    <Activity className={`w-4 h-4 ${active ? 'text-accent animate-pulse' : 'text-red-500'}`} />
                    <h3 className="text-xs font-mono text-white uppercase tracking-[0.4em]">Connectome_Topography_v5</h3>
                </div>

                {/* Vitality Indicator */}
                <div className="flex flex-col gap-2 bg-black/40 backdrop-blur-md py-3 px-4 rounded-2xl border border-white/5 max-w-[250px]">
                    <div className="flex items-center justify-between">
                        <span className="text-[8px] font-mono text-muted uppercase tracking-tighter">Nós Analíticos:</span>
                        <span className="text-[10px] text-accent font-bold">{graphData.nodes.length}</span>
                    </div>
                    <div className="flex items-center justify-between">
                        <span className="text-[8px] font-mono text-muted uppercase tracking-tighter">Sinapses Livres:</span>
                        <span className="text-[10px] text-secondary font-bold">{graphData.links.length}</span>
                    </div>
                </div>
            </div>

            <AnimatePresence>
                {selectedNode && (
                    <motion.div
                        initial={{ opacity: 0, x: -20 }}
                        animate={{ opacity: 1, x: 0 }}
                        exit={{ opacity: 0, x: -20 }}
                        className="absolute bottom-8 left-10 glass-premium p-6 rounded-3xl border-white/10 max-w-xs shadow-2xl pointer-events-auto z-20"
                    >
                        <div className="flex items-center gap-2 mb-3">
                            <Tag className="w-3 h-3 text-accent" />
                            <span className="text-[10px] font-mono text-muted uppercase tracking-widest">Metadata_Focus</span>
                        </div>
                        <h2 className="text-lg font-bold text-white mb-1">{selectedNode.label}</h2>
                        <div className="flex flex-wrap gap-1.5 mb-4">
                            {selectedNode.tags.map(tag => (
                                <span key={tag} className="px-2 py-0.5 bg-white/5 border border-white/10 rounded-md text-[9px] text-accent/80 font-mono">
                                    #{tag}
                                </span>
                            ))}
                        </div>
                        <div className="flex items-center gap-4 text-[9px] font-mono text-muted/60 uppercase">
                            <span className="flex items-center gap-1"><Activity className="w-3 h-3" /> Area: {selectedNode.area}</span>
                        </div>
                    </motion.div>
                )}
            </AnimatePresence>

            {!active && (
                <div className="absolute inset-0 bg-black/60 backdrop-blur-sm flex items-center justify-center pointer-events-none transition-all z-30">
                    <div className="flex flex-col items-center gap-2 opacity-60">
                        <Activity className="w-8 h-8 text-accent animate-pulse" />
                        <span className="text-[10px] font-mono uppercase tracking-[0.5em] text-white">Neural_Dormancy_Active</span>
                    </div>
                </div>
            )}
        </div>
    );
};

export default ConnectomeGraph;
