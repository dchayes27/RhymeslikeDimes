import { } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { RhymeInfo, RhymeType } from '../types';
import { RhymeChip } from './RhymeChip';

interface SuggestionPanelProps {
  fragment: string;
  rhymeInfo: RhymeInfo;
  onWordClick: (word: string) => void;
  index: number;
}

export const SuggestionPanel: React.FC<SuggestionPanelProps> = ({ 
  fragment, 
  rhymeInfo, 
  onWordClick,
  index 
}) => {
  const hasRhymes = rhymeInfo.perfect.length > 0 || rhymeInfo.near.length > 0 || rhymeInfo.slant.length > 0;

  if (!hasRhymes) {
    return null;
  }

  const renderRhymeSection = (title: string, words: string[], type: RhymeType, color: string) => {
    if (words.length === 0) return null;

    return (
      <div className="mb-4">
        <h4 className={`text-xs font-semibold uppercase tracking-wider mb-2 ${color}`}>
          {title}
        </h4>
        <div className="flex flex-wrap gap-2">
          {words.map((word, idx) => (
            <RhymeChip
              key={`${type}-${word}-${idx}`}
              word={word}
              type={type}
              onClick={onWordClick}
              index={idx}
            />
          ))}
        </div>
      </div>
    );
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3, delay: index * 0.1 }}
      className="bg-white dark:bg-gray-800 rounded-lg p-4 shadow-sm border border-gray-200 dark:border-gray-700"
    >
      <h3 className="text-lg font-semibold mb-3 text-gray-900 dark:text-gray-100">
        "{fragment}"
        <span className="text-sm font-normal text-gray-500 dark:text-gray-400 ml-2">
          (words {rhymeInfo.span[0]}-{rhymeInfo.span[1] - 1})
        </span>
      </h3>
      
      <AnimatePresence>
        {renderRhymeSection('Perfect Rhymes', rhymeInfo.perfect, 'perfect', 'text-green-600 dark:text-green-400')}
        {renderRhymeSection('Near Rhymes', rhymeInfo.near, 'near', 'text-blue-600 dark:text-blue-400')}
        {renderRhymeSection('Slant Rhymes', rhymeInfo.slant, 'slant', 'text-purple-600 dark:text-purple-400')}
      </AnimatePresence>
    </motion.div>
  );
};