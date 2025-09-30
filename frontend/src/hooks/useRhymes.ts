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
      // Use environment variable if available; default to proxy-relative URL in dev
      const defaultBaseURL = import.meta.env.DEV
        ? ''
        : 'https://rhymeslikedimes-production.up.railway.app';
      const baseURL = (import.meta.env.VITE_API_URL as string | undefined) || defaultBaseURL;
      const normalizedBaseURL = baseURL.replace(/\/+$/, '');
      const hasApiSuffix = /\/api$/i.test(normalizedBaseURL);
      const apiPath = hasApiSuffix ? 'analyze' : 'api/analyze';
      const apiUrl = normalizedBaseURL
        ? `${normalizedBaseURL}/${apiPath}`
        : `/${apiPath}`;
      
      if (import.meta.env.DEV) {
        console.debug('Making API request to:', apiUrl);
      }
      
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
        if (import.meta.env.DEV) {
          console.error('Error analyzing bar:', error);
        }
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