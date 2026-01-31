/**
 * Skeleton Loader Component
 * ==========================
 * Displays animated loading placeholders.
 */

interface SkeletonProps {
  className?: string;
  variant?: 'text' | 'rect' | 'circle';
  width?: string;
  height?: string;
}

const Skeleton = ({ className = '', variant = 'text', width, height }: SkeletonProps) => {
  const baseClasses = 'animate-pulse bg-gray-200';

  const variantClasses = {
    text: 'h-4 rounded',
    rect: 'rounded',
    circle: 'rounded-full',
  };

  const style = {
    width: width || '100%',
    height: height || (variant === 'text' ? '1rem' : '100%'),
  };

  return (
    <div
      className={`${baseClasses} ${variantClasses[variant]} ${className}`}
      style={style}
    />
  );
};

export default Skeleton;

// Specialized skeleton loaders for specific components

export const VerseLoadingSkeleton = () => (
  <div className="space-y-4">
    <div className="flex items-center gap-3">
      <Skeleton variant="rect" width="60px" height="24px" />
      <Skeleton variant="text" width="200px" />
    </div>
    <div className="space-y-2">
      <Skeleton variant="text" width="100%" />
      <Skeleton variant="text" width="95%" />
      <Skeleton variant="text" width="98%" />
    </div>
    <div className="space-y-2 mt-4">
      <Skeleton variant="text" width="100%" />
      <Skeleton variant="text" width="92%" />
      <Skeleton variant="text" width="96%" />
    </div>
  </div>
);

export const LexiconLoadingSkeleton = () => (
  <div className="space-y-3">
    <div className="flex items-center gap-2">
      <Skeleton variant="rect" width="50px" height="20px" />
      <Skeleton variant="text" width="120px" />
    </div>
    <Skeleton variant="text" width="100%" />
    <Skeleton variant="text" width="95%" />
    <Skeleton variant="text" width="90%" />
    <div className="mt-4">
      <Skeleton variant="text" width="80px" height="14px" />
      <Skeleton variant="text" width="150px" height="14px" className="mt-1" />
    </div>
  </div>
);

export const ChatLoadingSkeleton = () => (
  <div className="space-y-4">
    {[1, 2, 3].map((i) => (
      <div key={i} className={`flex ${i % 2 === 0 ? 'justify-end' : 'justify-start'}`}>
        <div className={`max-w-[80%] rounded-lg p-3 space-y-2 ${i % 2 === 0 ? 'bg-blue-50' : 'bg-gray-50'}`}>
          <Skeleton variant="text" width="200px" />
          <Skeleton variant="text" width="180px" />
        </div>
      </div>
    ))}
  </div>
);
