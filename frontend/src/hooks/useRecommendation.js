import { useState } from 'react';
import { getRecommendation } from '../services/api';

export const useRecommendation = () => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const fetchRecommendation = async (payload) => {
    setLoading(true);
    setError(null);
    try {
      const response = await getRecommendation(payload);
      setData(response.data);
    } catch (err) {
      setError(err.response?.data?.detail || err.message || 'Failed to fetch recommendation');
    } finally {
      setLoading(false);
    }
  };

  return { data, loading, error, fetchRecommendation };
};
