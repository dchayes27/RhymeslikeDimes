import React, { useEffect, useRef, useImperativeHandle, forwardRef } from 'react';
import { motion } from 'framer-motion';

export interface BarInputHandle {
  insertAtCursor: (text: string) => void;
}

interface BarInputProps {
  value: string;
  onChange: (value: string) => void;
}

export const BarInput = forwardRef<BarInputHandle, BarInputProps>(
  ({ value, onChange }, ref) => {
  const textareaRef = useRef<HTMLTextAreaElement>(null);
  const cursorPositionRef = useRef<number>(0);

  useEffect(() => {
    // Restore cursor position after value change
    if (textareaRef.current) {
      textareaRef.current.setSelectionRange(cursorPositionRef.current, cursorPositionRef.current);
    }
  }, [value]);

  const handleChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    cursorPositionRef.current = e.target.selectionStart || 0;
    onChange(e.target.value);
  };

  const insertAtCursor = (text: string) => {
    if (textareaRef.current) {
      const start = textareaRef.current.selectionStart || value.length;
      const end = textareaRef.current.selectionEnd || value.length;
      const newValue = value.substring(0, start) + ' ' + text + value.substring(end);
      onChange(newValue);

      // Set cursor position after inserted text
      setTimeout(() => {
        const newPosition = start + text.length + 1;
        cursorPositionRef.current = newPosition;
        textareaRef.current?.focus();
        textareaRef.current?.setSelectionRange(newPosition, newPosition);
      }, 0);
    }
  };

  useImperativeHandle(ref, () => ({ insertAtCursor }), [insertAtCursor]);

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
      className="w-full"
    >
      <label htmlFor="bar-input" className="block text-sm font-medium mb-2">
        Enter Bar
      </label>
      <textarea
        ref={textareaRef}
        id="bar-input"
        value={value}
        onChange={handleChange}
        placeholder="Type a line here to find rhymes..."
        className="w-full px-4 py-3 border border-gray-300 dark:border-gray-700 rounded-lg 
                   bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100
                   focus:ring-2 focus:ring-blue-500 focus:border-transparent
                   resize-none transition-all duration-200"
        rows={3}
      />
      <div className="mt-2 text-sm text-gray-500 dark:text-gray-400">
        Click any suggestion to insert it at your cursor position
      </div>
    </motion.div>
  );
});

BarInput.displayName = 'BarInput';
