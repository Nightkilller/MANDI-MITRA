import { useState } from 'react';
import { getExplanation } from '../services/api';

export const useExplanation = () => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const fetchExplanation = async (crop, mandi, horizonDays = 7) => {
    setLoading(true);
    setError(null);
    try {
      const response = await getExplanation(crop, mandi, horizonDays);
      setData(response.data);
    } catch (err) {
      setError(err.response?.data?.detail || err.message || 'Failed to fetch explanation');
    } finally {
      setLoading(false);
    }
  };

  return { data, loading, error, fetchExplanation };
};
