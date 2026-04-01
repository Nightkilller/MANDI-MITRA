import { useState } from 'react';
import { getPrediction } from '../services/api';

export const usePrediction = () => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const fetchPrediction = async (crop, mandi, horizonDays = 14) => {
    setLoading(true);
    setError(null);
    try {
      const response = await getPrediction(crop, mandi, horizonDays);
      setData(response.data);
    } catch (err) {
      setError(err.response?.data?.detail || err.message || 'Failed to fetch prediction');
    } finally {
      setLoading(false);
    }
  };

  return { data, loading, error, fetchPrediction };
};
