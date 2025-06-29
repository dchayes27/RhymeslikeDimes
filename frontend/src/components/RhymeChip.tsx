import React from 'react';
import { motion } from 'framer-motion';
import clsx from 'clsx';
import { RhymeType } from '../types';

interface RhymeChipProps {
  word: string;
  type: RhymeType;
  onClick: (word: string) => void;
  index: number;
}

export const RhymeChip: React.FC<RhymeChipProps> = ({ word, type, onClick, index }) => {
  const chipClass = clsx('rhyme-chip', {
    'rhyme-chip-perfect': type === 'perfect',
    'rhyme-chip-near': type === 'near',
    'rhyme-chip-slant': type === 'slant',
  });

  return (
    <motion.button
      initial={{ opacity: 0, scale: 0.8 }}
      animate={{ opacity: 1, scale: 1 }}
      transition={{ duration: 0.2, delay: index * 0.03 }}
      whileHover={{ scale: 1.05 }}
      whileTap={{ scale: 0.95 }}
      onClick={() => onClick(word)}
      className={chipClass}
    >
      {word}
    </motion.button>
  );
};