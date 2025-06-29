import { useState, useCallback, useRef } from 'react';
import axios from 'axios';
import { AnalyzeResponse } from '../types';
import { toast } from 'react-hot-toast';

export const useRhymes = () => {
  const [loading, setLoading] = useState(false);
  const [rhymes, setRhymes] = useState<AnalyzeResponse | null>(null);
  const abortControllerRef = useRef<AbortController | null>(null);

  const analyzeBar = useCallback(async (bar: string) => {
    // Cancel previous request if still pending
    if (abortControllerRef.current) {
      abortControllerRef.current.abort();
    }

    if (!bar.trim()) {
      setRhymes(null);
      return;
    }

    setLoading(true);
    abortControllerRef.current = new AbortController();

    try {
      const response = await axios.post<AnalyzeResponse>(
        '/api/analyze',
        {
          bar,
          max_results: 7,
          ngram_max: 3,
        },
        {
          signal: abortControllerRef.current.signal,
        }
      );
      setRhymes(response.data);
    } catch (error) {
      if (!axios.isCancel(error)) {
        console.error('Error analyzing bar:', error);
        toast.error('Failed to analyze rhymes. Please try again.');
      }
    } finally {
      setLoading(false);
    }
  }, []);

  return {
    loading,
    rhymes,
    analyzeBar,
  };
};