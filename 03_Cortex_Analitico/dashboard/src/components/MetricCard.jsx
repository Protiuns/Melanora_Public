import React from 'react';

const MetricCard = ({ title, value, unit, icon: Icon, trend, simplified }) => {
    if (simplified) {
        return (
            <div className="flex items-baseline gap-2 border-l border-white/5 pl-6 group/simp">
                <span className="text-[8px] font-mono text-muted uppercase tracking-[0.2em] group-hover/simp:text-accent transition-colors">{title}</span>
                <span className="text-sm font-bold text-accent glow-text">{value}</span>
                <span className="text-[8px] font-mono text-muted">{unit}</span>
            </div>
        );
    }

    return (
        <div className="glass p-6 rounded-[32px] flex flex-col justify-between h-32 border border-white/5 hover:border-accent/40 hover:bg-white/[0.02] transition-all duration-500 group relative overflow-hidden">
            {/* Subtle Gradient Spot */}
            <div className="absolute -top-10 -right-10 w-24 h-24 bg-accent/5 blur-[40px] rounded-full group-hover:bg-accent/10 transition-colors" />

            <div className="flex justify-between items-start">
                <span className="text-[10px] font-mono text-muted uppercase tracking-[0.2em] group-hover:text-text/80 transition-colors">{title}</span>
                {Icon && (
                    <div className="p-2 rounded-xl bg-white/5 group-hover:bg-accent/10 transition-colors">
                        <Icon className="w-4 h-4 text-muted group-hover:text-accent transition-colors" />
                    </div>
                )}
            </div>

            <div className="flex items-baseline gap-1.5">
                <span className="text-2xl font-bold text-white tracking-tighter group-hover:scale-[1.02] transition-transform origin-left">{value}</span>
                <span className="text-[9px] text-muted font-mono uppercase tracking-widest">{unit}</span>
            </div>

            {trend && (
                <div className={`text-[8px] font-mono px-2 py-0.5 rounded-full w-fit ${trend > 0 ? 'bg-accent/10 text-accent' : 'bg-alert/10 text-alert'}`}>
                    {trend > 0 ? '↑' : '↓'} {Math.abs(trend)}% SYNC
                </div>
            )}
        </div>
    );
};

export default MetricCard;
