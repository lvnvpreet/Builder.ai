import React from 'react';
import { useNavigate } from 'react-router-dom';
import { GenerationWizard } from '@/components/wizard/GenerationWizard';
import { useAppStore } from '@/store';
import { WizardFormData } from '@/types/wizard';
import toast from 'react-hot-toast';
import useWebSocket from '@/hooks/useWebSocket';
import { ProgressDashboard } from '@/components/dashboard/ProgressDashboard';

const GenerationPage: React.FC = () => {
  const navigate = useNavigate();
  const { startGeneration, currentGeneration } = useAppStore();
  
  // Connect to WebSocket if there's an active generation
  useWebSocket(currentGeneration?.id || null);
    const handleWizardComplete = async (data: WizardFormData) => {
    try {
      // Start the generation process with the form data
      await startGeneration(data.businessInfo);
      toast.success('Website generation started! Please wait while we process your request.');
    } catch (error) {
      console.error('Generation error:', error);
      toast.error('Failed to start website generation');
    }
  };
  
  const handleWizardCancel = () => {
    navigate('/');
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="bg-white shadow">
        <div className="container py-6">
          <h1 className="text-2xl font-bold text-gray-900">Generate Website</h1>
        </div>
      </div>
      
      <div className="container py-8">
        {currentGeneration ? (
          <ProgressDashboard />
        ) : (
          <GenerationWizard
            onComplete={handleWizardComplete}
            onCancel={handleWizardCancel}
          />
        )}
      </div>
    </div>
  );
};

export default GenerationPage;
