import { useState, useEffect } from 'react';

export const useLanguage = (defaultLang = 'en') => {
  const [language, setLanguage] = useState(() => {
    return localStorage.getItem('language') || defaultLang;
  });

  useEffect(() => {
    localStorage.setItem('language', language);
  }, [language]);

  const toggleLanguage = () => {
    setLanguage(prev => prev === 'en' ? 'hi' : 'en');
  };

  return { language, setLanguage, toggleLanguage };
};
