export const formatPrice = (price) => {
  if (!price && price !== 0) return '₹--';
  return `₹${Math.round(price).toLocaleString('en-IN')}`;
};

export const formatDate = (dateString) => {
  if (!dateString) return '';
  const date = new Date(dateString);
  return new Intl.DateTimeFormat('en-IN', {
    day: 'numeric',
    month: 'short',
    year: 'numeric'
  }).format(date);
};

export const formatPercentage = (value) => {
  if (!value && value !== 0) return '--%';
  return `${Math.round(value * 100)}%`;
};
