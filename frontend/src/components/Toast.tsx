/**
 * Toast Notification Component
 * ============================
 * Displays temporary notification messages with different types.
 */

import { useEffect } from 'react';

export type ToastType = 'success' | 'error' | 'warning' | 'info';

interface ToastProps {
  message: string;
  type: ToastType;
  duration?: number;
  onClose: () => void;
}

const Toast = ({ message, type, duration = 5000, onClose }: ToastProps) => {
  useEffect(() => {
    const timer = setTimeout(onClose, duration);
    return () => clearTimeout(timer);
  }, [duration, onClose]);

  const typeStyles = {
    success: 'bg-green-500 border-green-600',
    error: 'bg-red-500 border-red-600',
    warning: 'bg-yellow-500 border-yellow-600',
    info: 'bg-blue-500 border-blue-600',
  };

  const typeIcons = {
    success: '✓',
    error: '✕',
    warning: '⚠',
    info: 'ℹ',
  };

  return (
    <div
      className={`fixed bottom-4 right-4 z-50 flex items-center gap-3 px-4 py-3 rounded-lg shadow-lg border-l-4 text-white ${typeStyles[type]} animate-slide-in`}
      role="alert"
    >
      <span className="text-xl font-bold">{typeIcons[type]}</span>
      <p className="flex-1">{message}</p>
      <button
        onClick={onClose}
        className="ml-2 text-white hover:text-gray-200 font-bold"
        aria-label="Close"
      >
        ✕
      </button>
    </div>
  );
};

export default Toast;
