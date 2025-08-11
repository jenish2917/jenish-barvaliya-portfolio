import { useState, useEffect } from 'react';
import ApiService from '../services/api';

export const useApiData = (apiMethod, fallbackData = null) => {
  const [data, setData] = useState(fallbackData);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        setError(null);
        const result = await apiMethod();
        setData(result);
      } catch (err) {
        console.error('API fetch error:', err);
        setError(err);
        // Keep fallback data if API fails
        if (fallbackData) {
          setData(fallbackData);
        }
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  return { data, loading, error };
};

// Specific hooks for different data types
export const usePersonalInfo = (fallbackData) => {
  return useApiData(() => ApiService.getPersonalInfo(), fallbackData);
};

export const useAbout = (fallbackData) => {
  return useApiData(() => ApiService.getAbout(), fallbackData);
};

export const useSocialLinks = (fallbackData) => {
  return useApiData(() => ApiService.getSocialLinks(), fallbackData);
};

export const useProjects = (fallbackData) => {
  return useApiData(() => ApiService.getProjects(), fallbackData);
};

export const useSkills = (fallbackData) => {
  return useApiData(() => ApiService.getSkills(), fallbackData);
};

export const useExperience = (fallbackData) => {
  return useApiData(() => ApiService.getExperience(), fallbackData);
};

export const useEducation = (fallbackData) => {
  return useApiData(() => ApiService.getEducation(), fallbackData);
};

export const useCertifications = (fallbackData) => {
  return useApiData(() => ApiService.getCertifications(), fallbackData);
};
