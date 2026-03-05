import React, { useState, useEffect } from 'react';
import { Database, TrendingUp, AlertTriangle, Network } from 'lucide-react';

const System2Panel = () => {
    const [data, setData] = useState(null);
    const [loading, setLoading] = useState(true);

    const fetchAnalytics = async () => {
        try {
            const res = await fetch('http://localhost:5000/api/neural/system2/analytics');
            const json = await res.json();
            if (json.status === 'OK') {
                setData(json);
            }
        } catch (e) {
            console.warn("System 2 Analytics offline");
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchAnalytics();
        const interval = setInterval(fetchAnalytics, 10000); // a cada 10s
        return () => clearInterval(interval);
    }, []);

    if (loading || !data) {
        return (
            <div className="glass p-6 rounded-[32px] animate-pulse">
                <h3 className="text-[9px] font-mono text-muted uppercase tracking-widest mb-4">Syst. 2: Analítico</h3>
                <div className="h-10 bg-white/5 rounded-lg w-full mb-2"></div>
            </div>
        );
    }

    const { metrics, insight } = data;
    const isHealthy = metrics.phi_status && metrics.phi_status.includes("Saudável");

    return (
        <div className="glass-premium p-6 rounded-[32px] border-r-4 border-r-blue-500/50">
            <div className="flex justify-between items-center mb-4">
                <h3 className="text-[9px] font-mono text-blue-400 uppercase tracking-widest flex items-center gap-2">
                    <Database className="w-4 h-4" />
                    Sistema 2 (Córtex Lento)
                </h3>
                <span className={`text-[9px] font-mono font-bold px-2 py-1 rounded-sm uppercase tracking-widest ${isHealthy ? 'bg-accent/20 text-accent' : 'bg-amber-500/20 text-amber-500'}`}>
                    {metrics.phi_status || "OFFLINE"}
                </span>
            </div>

            <div className="grid grid-cols-2 gap-4 mb-4">
                <div className="bg-white/5 p-4 rounded-2xl flex flex-col justify-center items-center">
                    <span className="text-[9px] font-mono text-muted uppercase tracking-widest">Densidade Sináptica</span>
                    <span className="text-xl font-bold text-white mt-1">{metrics.density || 0}</span>
                </div>
                <div className="bg-white/5 p-4 rounded-2xl flex flex-col justify-center items-center">
                    <span className="text-[9px] font-mono text-muted uppercase tracking-widest">Focos Isolados</span>
                    <span className={`text-xl font-bold mt-1 ${metrics.isolated_count > 0 ? 'text-amber-500' : 'text-accent'}`}>{metrics.isolated_count || 0}</span>
                </div>
            </div>

            <div className="border-t border-white/10 pt-4 mt-2">
                <p className="text-xs font-medium leading-relaxed" style={{ color: isHealthy ? '#e2e8f0' : '#fcd34d' }}>
                    {insight}
                </p>
            </div>
        </div>
    );
};

export default System2Panel;
