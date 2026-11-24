import React, { useEffect, useRef } from 'react';

interface TorusProps {
  valence: number;
  arousal: number;
  helicity: number;
  verdict: 'PASS' | 'RELEASE/CAUTION' | 'BLOCK';
}

export const ToroidalVisualizer: React.FC<TorusProps> = ({ valence, arousal, helicity, verdict }) => {
  const canvasRef = useRef<HTMLCanvasElement | null>(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    let animId = 0;
    let angle = 0;

    const color =
      verdict === 'PASS' ? '#34d399' : verdict === 'RELEASE/CAUTION' ? '#fbbf24' : '#f87171';

    const render = () => {
      angle += 0.008 + arousal * 0.014;
      const w = canvas.clientWidth || 320;
      const h = canvas.clientHeight || 220;
      if (canvas.width !== w || canvas.height !== h) {
        canvas.width = w;
        canvas.height = h;
      }

      ctx.fillStyle = '#040812';
      ctx.fillRect(0, 0, w, h);

      const cx = w / 2;
      const cy = h / 2;
      const R = Math.min(w, h) * 0.28;
      const r = Math.min(w, h) * 0.11;

      const uSteps = 28;
      const vSteps = 14;
      const cosA = Math.cos(angle);
      const sinA = Math.sin(angle);
      const tilt = 0.55 + valence * 0.25;
      const cosT = Math.cos(tilt);
      const sinT = Math.sin(tilt);

      ctx.strokeStyle = color;
      ctx.lineWidth = 1;

      for (let i = 0; i < uSteps; i++) {
        const u = (i / uSteps) * Math.PI * 2;
        ctx.beginPath();
        for (let j = 0; j <= vSteps; j++) {
          const v = (j / vSteps) * Math.PI * 2;
          const x0 = (R + r * Math.cos(v)) * Math.cos(u);
          const y0 = (R + r * Math.cos(v)) * Math.sin(u);
          const z0 = r * Math.sin(v);

          const x1 = x0 * cosA - y0 * sinA;
          const y1 = x0 * sinA + y0 * cosA;
          const y2 = y1 * cosT - z0 * sinT;
          const z2 = y1 * sinT + z0 * cosT;

          const p = 260 / (260 + z2);
          const px = cx + x1 * p;
          const py = cy + y2 * p;
          if (j === 0) ctx.moveTo(px, py);
          else ctx.lineTo(px, py);
        }
        ctx.globalAlpha = 0.35;
        ctx.stroke();
      }

      // Helical Beltramian streamline
      ctx.beginPath();
      const turns = 120;
      for (let k = 0; k <= turns; k++) {
        const t = (k / turns) * Math.PI * 2;
        const u = t * 2 + angle * 1.4;
        const v = t * (3 + Math.round(Math.abs(helicity) * 4));
        const x0 = (R + (r + 3) * Math.cos(v)) * Math.cos(u);
        const y0 = (R + (r + 3) * Math.cos(v)) * Math.sin(u);
        const z0 = (r + 3) * Math.sin(v);

        const x1 = x0 * cosA - y0 * sinA;
        const y1 = x0 * sinA + y0 * cosA;
        const y2 = y1 * cosT - z0 * sinT;
        const z2 = y1 * sinT + z0 * cosT;
        const p = 260 / (260 + z2);
        const px = cx + x1 * p;
        const py = cy + y2 * p;
        if (k === 0) ctx.moveTo(px, py);
        else ctx.lineTo(px, py);
      }
      ctx.globalAlpha = 0.95;
      ctx.strokeStyle = '#38bdf8';
      ctx.lineWidth = 1.6;
      ctx.stroke();
      ctx.globalAlpha = 1.0;

      animId = requestAnimationFrame(render);
    };

    animId = requestAnimationFrame(render);
    return () => cancelAnimationFrame(animId);
  }, [valence, arousal, helicity, verdict]);

  return (
    <canvas
      ref={canvasRef}
      className="w-full h-52 rounded-lg border border-slate-800 block bg-slate-950"
    />
  );
};
