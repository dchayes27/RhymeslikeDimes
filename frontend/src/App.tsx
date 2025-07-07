import { useState, useEffect, useRef } from 'react';
import { Toaster } from 'react-hot-toast';
import { motion } from 'framer-motion';
import { BarInput, BarInputHandle } from './components/BarInput';
import { SuggestionPanel } from './components/SuggestionPanel';
import { LoadingSpinner } from './components/LoadingSpinner';
import { useRhymes } from './hooks/useRhymes';
import { useDebounce } from './hooks/useDebounce';

function App() {
  const [barText, setBarText] = useState('');
  const debouncedBar = useDebounce(barText, 300);
  const { loading, rhymes, analyzeBar } = useRhymes();
  const barInputRef = useRef<BarInputHandle>(null);

  useEffect(() => {
    if (debouncedBar) {
      analyzeBar(debouncedBar);
    }
  }, [debouncedBar, analyzeBar]);

  const handleWordInsert = (word: string) => {
    barInputRef.current?.insertAtCursor(word);
  };

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900 transition-colors duration-200">
      <Toaster position="top-right" />
      
      <div className="container mx-auto px-4 py-8 max-w-6xl">
        <motion.header
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-center mb-12"
        >
          <h1 className="text-5xl font-black text-gray-900 dark:text-gray-100 mb-2 tracking-wider" 
              style={{ fontFamily: '"Bungee", "Fredoka One", "Permanent Marker", cursive', textShadow: '2px 2px 4px rgba(0,0,0,0.3)' }}>
            <span className="text-red-600 dark:text-red-400">RHYMES</span>
            <span className="text-2xl font-normal text-blue-600 dark:text-blue-400">like</span>
            <span className="text-yellow-600 dark:text-yellow-400">DIMES</span>
          </h1>
          <p className="text-lg text-gray-600 dark:text-gray-400 font-medium" style={{ fontFamily: '"Comic Neue", "Kalam", cursive' }}>
            Advanced Rhyme Finder
          </p>
        </motion.header>

        <div className="mb-8">
          <BarInput
            ref={barInputRef}
            value={barText}
            onChange={setBarText}
          />
        </div>

        {loading && <LoadingSpinner />}

        {rhymes && !loading && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 0.3 }}
          >
            <h2 className="text-2xl font-semibold mb-6 text-gray-900 dark:text-gray-100">
              Rhyme Suggestions
            </h2>
            
            <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
              {Object.entries(rhymes.fragments).map(([fragment, rhymeInfo], index) => (
                <SuggestionPanel
                  key={fragment}
                  fragment={fragment}
                  rhymeInfo={rhymeInfo}
                  onWordClick={handleWordInsert}
                  index={index}
                />
              ))}
            </div>
          </motion.div>
        )}

        {!loading && rhymes && Object.keys(rhymes.fragments).length === 0 && (
          <div className="text-center py-8 text-gray-500 dark:text-gray-400">
            No rhymes found. Try a different phrase!
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
