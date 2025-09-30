import React from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { RhymeInfo, RhymeType } from '../types';
import { RhymeChip } from './RhymeChip';

interface SuggestionPanelProps {
  fragment: string;
  rhymeInfo: RhymeInfo;
  onWordClick: (word: string) => void;
  index: number;
}

interface RhymeCategoryConfig {
  key: RhymeType;
  label: string;
  accentClass: string;
}

interface RhymeGroupConfig {
  title: string;
  description: string;
  categories: RhymeCategoryConfig[];
}

const RHYME_GROUPS: RhymeGroupConfig[] = [
  {
    title: 'Word Rhymes',
    description: 'Single-word matches to keep your flow tight.',
    categories: [
      {
        key: 'perfect',
        label: 'Perfect Rhymes',
        accentClass: 'text-green-600 dark:text-green-400',
      },
      {
        key: 'near',
        label: 'Near Rhymes',
        accentClass: 'text-blue-600 dark:text-blue-400',
      },
      {
        key: 'slant',
        label: 'Slant Rhymes',
        accentClass: 'text-purple-600 dark:text-purple-400',
      },
    ],
  },
  {
    title: 'Phrase Rhymes',
    description: 'Multi-word echoes for DOOM-style endings.',
    categories: [
      {
        key: 'phrase_perfect',
        label: 'Perfect Phrase Rhymes',
        accentClass: 'text-emerald-600 dark:text-emerald-400',
      },
      {
        key: 'phrase_near',
        label: 'Near Phrase Rhymes',
        accentClass: 'text-sky-600 dark:text-sky-400',
      },
      {
        key: 'phrase_slant',
        label: 'Slant Phrase Rhymes',
        accentClass: 'text-fuchsia-600 dark:text-fuchsia-400',
      },
    ],
  },
];

export const SuggestionPanel: React.FC<SuggestionPanelProps> = ({
  fragment,
  rhymeInfo,
  onWordClick,
  index
}) => {
  const groupsWithResults = RHYME_GROUPS.map((group) => ({
    ...group,
    categories: group.categories.filter((category) => rhymeInfo[category.key].length > 0),
  })).filter((group) => group.categories.length > 0);

  if (groupsWithResults.length === 0) {
    return null;
  }

  const renderRhymeSection = (config: RhymeCategoryConfig) => {
    const words = rhymeInfo[config.key];

    if (words.length === 0) return null;

    return (
      <div className="mb-4">
        <h4 className={`text-xs font-semibold uppercase tracking-wider mb-2 ${config.accentClass}`}>
          {config.label}
        </h4>
        <div className="flex flex-wrap gap-2">
          {words.map((word, idx) => (
            <RhymeChip
              key={`${config.key}-${word}-${idx}`}
              word={word}
              type={config.key}
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
        {fragment}
        <span className="text-sm font-normal text-gray-500 dark:text-gray-400 ml-2">
          (words {rhymeInfo.span[0]}-{rhymeInfo.span[1] - 1})
        </span>
      </h3>

      <div className="space-y-6">
        {groupsWithResults.map((group) => (
          <div key={group.title}>
            <div className="mb-3">
              <h4 className="text-sm font-semibold uppercase tracking-wide text-gray-700 dark:text-gray-300">
                {group.title}
              </h4>
              <p className="text-xs text-gray-500 dark:text-gray-400">
                {group.description}
              </p>
            </div>
            <AnimatePresence>
              {group.categories.map((category) => (
                <motion.div
                  key={category.key}
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0, y: -10 }}
                  transition={{ duration: 0.2 }}
                >
                  {renderRhymeSection(category)}
                </motion.div>
              ))}
            </AnimatePresence>
          </div>
        ))}
      </div>
    </motion.div>
  );
};
