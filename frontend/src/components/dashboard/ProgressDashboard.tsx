import React from 'react';
import { motion } from 'framer-motion';
import { Clock, Zap, CheckCircle2, AlertCircle, X } from 'lucide-react';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/Card';
import ProgressBar from '@/components/ui/ProgressBar';
import Button from '@/components/ui/Button';
import { useAppStore } from '@/store';
import { formatDistanceToNow } from 'date-fns';

export const ProgressDashboard: React.FC = () => {
  const { currentGeneration, cancelGeneration, wsConnected } = useAppStore();

  if (!currentGeneration) {
    return null;
  }

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'completed':
        return <CheckCircle2 className="h-5 w-5 text-green-500" />;
      case 'in_progress':
        return <Zap className="h-5 w-5 text-blue-500 animate-pulse" />;
      case 'pending':
        return <Clock className="h-5 w-5 text-gray-400" />;
      case 'failed':
        return <AlertCircle className="h-5 w-5 text-red-500" />;
      default:
        return null;
    }
  };

  const getProgressColor = (progress: number) => {
    if (progress === 100) return 'green';
    if (progress > 0) return 'blue';
    return 'gray';
  };

  const agents = [
    { key: 'content', name: 'Content Generation', icon: '📝' },
    { key: 'design', name: 'Design System', icon: '🎨' },
    { key: 'structure', name: 'Website Structure', icon: '🏗️' },
    { key: 'quality', name: 'Quality Validation', icon: '✅' },
  ];

  return (
    <div className="space-y-6">
      {/* Status Header */}
      <Card variant="bordered">
        <CardHeader>
          <div className="flex justify-between items-center">
            <div>
              <CardTitle>Generation Status</CardTitle>
              <p className="text-sm text-gray-500 mt-1">
                Started {formatDistanceToNow(new Date(currentGeneration.startedAt), { addSuffix: true })}
              </p>
            </div>
            
            <div className="flex items-center">
              <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                currentGeneration.status === 'completed' ? 'bg-green-100 text-green-800' :
                currentGeneration.status === 'in_progress' ? 'bg-blue-100 text-blue-800' :
                currentGeneration.status === 'failed' ? 'bg-red-100 text-red-800' :
                'bg-gray-100 text-gray-800'
              }`}>
                {currentGeneration.status === 'in_progress' ? 'In Progress' : 
                 currentGeneration.status === 'completed' ? 'Completed' :
                 currentGeneration.status === 'failed' ? 'Failed' : 'Pending'}
              </span>
              
              {currentGeneration.status === 'in_progress' && (
                <Button 
                  variant="outline" 
                  size="sm"
                  className="ml-2" 
                  onClick={() => cancelGeneration()}
                >
                  <X className="h-4 w-4 mr-1" /> Cancel
                </Button>
              )}
            </div>
          </div>
        </CardHeader>
        <CardContent>
          {/* Overall Progress */}
          <div className="mb-6">
            <ProgressBar 
              value={currentGeneration.progress} 
              label="Overall Progress"
              color={getProgressColor(currentGeneration.progress)}
              size="lg"
            />
          </div>
            {/* WebSocket Status */}
          <div className="flex items-center mb-6">
            <div className={`w-3 h-3 rounded-full mr-2 ${wsConnected ? 'bg-green-500' : 'bg-red-500'}`}></div>
            <span className="text-sm text-gray-600">
              {wsConnected ? 'Connected - Receiving real-time updates' : 'Disconnected - Reconnecting...'}
            </span>
            {!wsConnected && currentGeneration.progress > 0 && (
              <span className="text-xs bg-amber-100 text-amber-800 px-2 py-1 rounded ml-2">
                Progress data might be delayed
              </span>
            )}
          </div>
          
          {/* Steps Progress */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {currentGeneration.steps.map((step) => (
              <Card key={step.id} variant="bordered" className="flex flex-col" padding="sm">
                <div className="flex items-center justify-between p-4 border-b border-gray-100">
                  <div className="flex items-center">
                    <span className="text-xl mr-2">
                      {agents.find(a => a.key === step.id)?.icon || '🔄'}
                    </span>
                    <h4 className="text-sm font-medium text-gray-900">
                      {step.name}
                    </h4>
                  </div>
                  <div>
                    {getStatusIcon(step.status)}
                  </div>
                </div>
                <div className="p-4">
                  <ProgressBar 
                    value={step.progress} 
                    color={getProgressColor(step.progress)}
                    size="sm"
                  />
                </div>
              </Card>
            ))}
          </div>
        </CardContent>
      </Card>
      
      {/* Error Message */}
      {currentGeneration.error && (
        <Card variant="bordered" className="bg-red-50 border-red-100">
          <CardContent className="p-4">
            <div className="flex items-start">
              <AlertCircle className="h-5 w-5 text-red-500 mt-0.5 mr-2" />
              <div>
                <h4 className="text-sm font-medium text-red-800">
                  {currentGeneration.error.message}
                </h4>
                {currentGeneration.error.details && (
                  <p className="text-xs text-red-700 mt-1">
                    {currentGeneration.error.details}
                  </p>
                )}
              </div>
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  );
};
