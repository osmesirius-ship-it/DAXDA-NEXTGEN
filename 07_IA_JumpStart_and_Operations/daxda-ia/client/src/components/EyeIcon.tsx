/**
 * DAXDA.IA "Evil Eye" SVG icon component
 * Design: Mission Control aesthetic — precision SVG with cyan/blue palette
 */

interface EyeIconProps {
  size?: 'sm' | 'md' | 'lg';
  className?: string;
}

const sizes = {
  sm: 14,
  md: 20,
  lg: 32,
};

export function EyeIcon({ size = 'md', className = '' }: EyeIconProps) {
  const s = sizes[size];
  return (
    <svg
      className={className}
      width={s}
      height={s}
      viewBox="0 0 32 32"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
    >
      <ellipse cx="16" cy="16" rx="14" ry="9" stroke="#3b82f6" strokeWidth="1.5" />
      <circle cx="16" cy="16" r="6" fill="#0b1529" stroke="#60c8f5" strokeWidth="1.5" />
      <circle cx="16" cy="16" r="3" fill="#3b82f6" />
      <circle cx="17.5" cy="14.5" r="1" fill="#a8e6ff" opacity="0.8" />
      <ellipse cx="16" cy="16" rx="14" ry="9" stroke="#60c8f5" strokeWidth="0.5" strokeDasharray="2 3" />
      <line x1="2" y1="16" x2="4" y2="16" stroke="#60c8f5" strokeWidth="1" />
      <line x1="28" y1="16" x2="30" y2="16" stroke="#60c8f5" strokeWidth="1" />
    </svg>
  );
}

export function EyeIconDanger({ size = 'sm', className = '' }: EyeIconProps) {
  const s = sizes[size];
  return (
    <svg
      className={className}
      width={s}
      height={s}
      viewBox="0 0 14 14"
      fill="none"
    >
      <ellipse cx="7" cy="7" rx="6" ry="4" stroke="#f44" strokeWidth="1.2" />
      <circle cx="7" cy="7" r="2" fill="#f44" />
    </svg>
  );
}

export function PlayIcon({ className = '' }: { className?: string }) {
  return (
    <svg className={className} width="14" height="14" viewBox="0 0 14 14" fill="none">
      <polygon points="2,7 12,2 12,12" fill="#60c8f5" />
    </svg>
  );
}

export function ChevronIcon({ className = '' }: { className?: string }) {
  return (
    <svg className={className} width="10" height="10" viewBox="0 0 10 10" fill="none">
      <polyline points="2,3 5,7 8,3" stroke="#7bb3e0" strokeWidth="1.2" fill="none" />
    </svg>
  );
}

export function ViolationIcon({ className = '' }: { className?: string }) {
  return (
    <svg className={className} width="14" height="14" viewBox="0 0 14 14" fill="none">
      <ellipse cx="7" cy="7" rx="6" ry="4" stroke="#f44" strokeWidth="1.2" />
      <line x1="4" y1="4" x2="10" y2="10" stroke="#f44" strokeWidth="1" />
    </svg>
  );
}

export function LayerEyeIcon({ className = '' }: { className?: string }) {
  return (
    <svg className={className} width="12" height="12" viewBox="0 0 12 12" fill="none">
      <ellipse cx="6" cy="6" rx="5" ry="3" stroke="#60c8f5" strokeWidth="1" />
      <circle cx="6" cy="6" r="2" fill="#3b82f6" />
    </svg>
  );
}
