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
      // Use environment variable if available, otherwise fall back to /api route
      const baseURL = import.meta.env.VITE_API_URL || '';
      const apiUrl = baseURL ? `${baseURL}/api/analyze` : '/api/analyze';
      
      console.log('Making API request to:', apiUrl); // Debug log
      
      const response = await axios.post<AnalyzeResponse>(
        apiUrl,
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
    } catch (error: any) {
      if (!axios.isCancel(error)) {
        console.error('Error analyzing bar:', error);
        console.error('Error details:', {
          message: error.message,
          response: error.response?.data,
          status: error.response?.status,
          url: error.config?.url
        });
        toast.error(`Failed to analyze rhymes: ${error.response?.status || error.message}`);
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