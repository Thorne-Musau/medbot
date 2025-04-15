import React, { useState } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { motion } from 'framer-motion';
import axios from 'axios';

interface Symptom {
  id: string;
  name: string;
  severity: 'mild' | 'moderate' | 'severe';
}

interface DiagnosisResult {
  primary_diagnosis: string;
  confidence: number;
  symptoms: string[];
  recommendations: string[];
}

const Diagnosis: React.FC = () => {
  const { user } = useAuth();
  const [symptoms, setSymptoms] = useState<Symptom[]>([]);
  const [newSymptom, setNewSymptom] = useState('');
  const [severity, setSeverity] = useState<'mild' | 'moderate' | 'severe'>('moderate');
  const [diagnosis, setDiagnosis] = useState<DiagnosisResult | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  const handleAddSymptom = () => {
    if (!newSymptom.trim()) return;

    const symptom: Symptom = {
      id: Date.now().toString(),
      name: newSymptom.trim(),
      severity,
    };

    setSymptoms((prev) => [...prev, symptom]);
    setNewSymptom('');
  };

  const handleRemoveSymptom = (id: string) => {
    setSymptoms((prev) => prev.filter((s) => s.id !== id));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (symptoms.length === 0) return;

    setIsLoading(true);
    try {
      const response = await axios.post('/api/diagnosis/predict', {
        symptoms: symptoms.map((s) => ({
          name: s.name,
          severity: s.severity,
        })),
      });

      setDiagnosis(response.data);
    } catch (error) {
      console.error('Error getting diagnosis:', error);
      // Handle error appropriately
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="bg-white rounded-lg shadow-lg overflow-hidden"
      >
        {/* Header */}
        <div className="bg-indigo-600 px-4 py-3">
          <h2 className="text-xl font-semibold text-white">Medical Diagnosis</h2>
        </div>

        <div className="p-6">
          {/* Symptoms Input */}
          <div className="mb-6">
            <h3 className="text-lg font-medium text-gray-900 mb-4">Add Symptoms</h3>
            <div className="flex space-x-4">
              <input
                type="text"
                value={newSymptom}
                onChange={(e) => setNewSymptom(e.target.value)}
                placeholder="Enter symptom..."
                className="flex-1 rounded-lg border border-gray-300 px-4 py-2 focus:outline-none focus:ring-2 focus:ring-indigo-500"
              />
              <select
                value={severity}
                onChange={(e) => setSeverity(e.target.value as 'mild' | 'moderate' | 'severe')}
                className="rounded-lg border border-gray-300 px-4 py-2 focus:outline-none focus:ring-2 focus:ring-indigo-500"
              >
                <option value="mild">Mild</option>
                <option value="moderate">Moderate</option>
                <option value="severe">Severe</option>
              </select>
              <button
                onClick={handleAddSymptom}
                className="bg-indigo-600 text-white px-4 py-2 rounded-lg font-medium hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500"
              >
                Add
              </button>
            </div>
          </div>

          {/* Symptoms List */}
          <div className="mb-6">
            <h3 className="text-lg font-medium text-gray-900 mb-4">Current Symptoms</h3>
            <div className="space-y-2">
              {symptoms.map((symptom) => (
                <motion.div
                  key={symptom.id}
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  exit={{ opacity: 0, x: 20 }}
                  className="flex items-center justify-between bg-gray-50 rounded-lg px-4 py-2"
                >
                  <div>
                    <span className="font-medium">{symptom.name}</span>
                    <span className="ml-2 text-sm text-gray-500">
                      ({symptom.severity})
                    </span>
                  </div>
                  <button
                    onClick={() => handleRemoveSymptom(symptom.id)}
                    className="text-red-500 hover:text-red-700"
                  >
                    Remove
                  </button>
                </motion.div>
              ))}
            </div>
          </div>

          {/* Submit Button */}
          <button
            onClick={handleSubmit}
            disabled={symptoms.length === 0 || isLoading}
            className="w-full bg-indigo-600 text-white px-6 py-3 rounded-lg font-medium hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {isLoading ? 'Analyzing...' : 'Get Diagnosis'}
          </button>

          {/* Diagnosis Result */}
          {diagnosis && (
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              className="mt-6 bg-gray-50 rounded-lg p-6"
            >
              <h3 className="text-lg font-medium text-gray-900 mb-4">Diagnosis Result</h3>
              <div className="space-y-4">
                <div>
                  <h4 className="font-medium text-gray-700">Primary Diagnosis</h4>
                  <p className="text-indigo-600 font-semibold">
                    {diagnosis.primary_diagnosis}
                  </p>
                  <p className="text-sm text-gray-500">
                    Confidence: {(diagnosis.confidence * 100).toFixed(1)}%
                  </p>
                </div>
                <div>
                  <h4 className="font-medium text-gray-700">Symptoms Analyzed</h4>
                  <ul className="list-disc list-inside text-gray-600">
                    {diagnosis.symptoms.map((symptom, index) => (
                      <li key={index}>{symptom}</li>
                    ))}
                  </ul>
                </div>
                <div>
                  <h4 className="font-medium text-gray-700">Recommendations</h4>
                  <ul className="list-disc list-inside text-gray-600">
                    {diagnosis.recommendations.map((recommendation, index) => (
                      <li key={index}>{recommendation}</li>
                    ))}
                  </ul>
                </div>
              </div>
            </motion.div>
          )}
        </div>
      </motion.div>
    </div>
  );
};

export default Diagnosis; 