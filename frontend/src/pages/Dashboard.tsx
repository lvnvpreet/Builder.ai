import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/Card';
import Button from '@/components/ui/Button';
import { GenerationWizard } from '@/components/wizard/GenerationWizard';
import { ProgressDashboard } from '@/components/dashboard/ProgressDashboard';
import { useAppStore } from '@/store';
import type { WizardFormData } from '@/types/wizard';
import type { GenerationState } from '@/types/generation';
import toast from 'react-hot-toast';
import { Plus, Layers, Clock, CheckCircle } from 'lucide-react';
import useWebSocket from '@/hooks/useWebSocket';

const Dashboard: React.FC = () => {
  const [showWizard, setShowWizard] = useState(false);
  const navigate = useNavigate();
  
  const { 
    currentGeneration,
    generationHistory,
    startGeneration,
    isGenerating
  } = useAppStore();
  
  // Connect to WebSocket if there's an active generation
  useWebSocket(currentGeneration?.id || null);
  
  const handleNewWebsite = () => {
    setShowWizard(true);
  };  const handleWizardComplete = async (data: WizardFormData) => {
    try {
      // Start the generation process with just the business info
      // The backend API expects BusinessData type, not the full wizard data
      await startGeneration(data.businessInfo);
      setShowWizard(false);
    } catch (error: any) {
      console.error('Generation error:', error);
      // Display a more specific error message to the user
      const errorMessage = error?.message || 'Failed to start website generation';
      toast.error(errorMessage);
    }
  };
  
  const handleWizardCancel = () => {
    setShowWizard(false);
  };
  
  const handlePreviewWebsite = (id: string) => {
    navigate(`/preview/${id}`);
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="bg-white shadow">
        <div className="container py-6">
          <h1 className="text-2xl font-bold text-gray-900">AI Website Builder</h1>
        </div>
      </div>
      
      <div className="container py-8">
        {showWizard ? (
          <GenerationWizard 
            onComplete={handleWizardComplete} 
            onCancel={handleWizardCancel} 
          />
        ) : (
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
            <div className="lg:col-span-2">
              {currentGeneration ? (
                <ProgressDashboard />
              ) : (
                <Card variant="bordered" className="h-full flex flex-col justify-center items-center p-12">
                  <div className="text-center mb-6">
                    <div className="bg-blue-100 p-4 rounded-full inline-flex items-center justify-center mb-4">
                      <Layers className="h-8 w-8 text-blue-600" />
                    </div>
                    <h2 className="text-xl font-semibold text-gray-900 mb-2">Create Your AI Website</h2>
                    <p className="text-gray-600 max-w-md mx-auto">
                      Generate a professional website for your business in minutes using AI.
                    </p>
                  </div>
                  <Button 
                    variant="primary" 
                    size="lg" 
                    onClick={handleNewWebsite}
                    leftIcon={<Plus className="h-5 w-5" />}
                  >
                    Create New Website
                  </Button>
                </Card>
              )}
            </div>
            
            <div>
              <Card variant="bordered">
                <CardHeader>
                  <CardTitle>Recent Websites</CardTitle>
                </CardHeader>
                <CardContent>
                  {generationHistory.length === 0 ? (
                    <div className="text-center py-8 text-gray-500">
                      <Clock className="h-12 w-12 mx-auto mb-3 text-gray-400" />
                      <p>No website history yet</p>
                      <p className="text-sm mt-1">Your generated websites will appear here</p>
                    </div>
                  ) : (                    <div className="space-y-4">
                      {generationHistory.slice(0, 5).map((generation: GenerationState) => (
                        <div 
                          key={generation.id} 
                          className="p-4 border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors"
                        >
                          <div className="flex justify-between items-center mb-2">
                            <span className="font-medium">{generation.businessData.businessName}</span>
                            {generation.status === 'completed' && (
                              <CheckCircle className="h-4 w-4 text-green-500" />
                            )}
                          </div>
                          <p className="text-sm text-gray-600 mb-3 line-clamp-2">
                            {generation.businessData.businessDescription?.substring(0, 100)}
                          </p>
                          <div className="flex justify-end">
                            <Button 
                              variant="outline" 
                              size="sm" 
                              onClick={() => handlePreviewWebsite(generation.id)}
                              disabled={generation.status !== 'completed'}
                            >
                              Preview
                            </Button>
                          </div>
                        </div>
                      ))}
                    </div>
                  )}
                </CardContent>
              </Card>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default Dashboard;
