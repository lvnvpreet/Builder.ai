import React from 'react';
import { UseFormReturn } from 'react-hook-form';
import { CheckCircle, AlertCircle, ChevronRight } from 'lucide-react';
import { CardHeader, CardTitle, CardContent } from '@/components/ui/Card';
import type { WizardFormData } from '@/types/wizard';

interface ReviewStepProps {
  form: UseFormReturn<WizardFormData>;
  formData: WizardFormData;
}

export const ReviewStep: React.FC<ReviewStepProps> = ({ formData }) => {
  const { 
    businessInfo, 
    designPreferences, 
    structure, 
    features 
  } = formData;

  return (
    <>
      <CardHeader>
        <CardTitle>Review Your Selections</CardTitle>
        <p className="text-gray-600 mt-1">
          Review the information you've provided before creating your website
        </p>
      </CardHeader>

      <CardContent>
        <div className="space-y-6">
          {/* Business Information */}
          <div className="border rounded-lg overflow-hidden">
            <div className="bg-blue-50 border-b border-blue-100 px-4 py-2 flex items-center justify-between">
              <h3 className="font-medium text-blue-800">Business Information</h3>
              <CheckCircle className="h-5 w-5 text-green-500" />
            </div>
            <div className="p-4 space-y-3">
              <div>
                <span className="text-sm font-medium text-gray-500">Business Name:</span>
                <p className="text-sm">{businessInfo.businessName}</p>
              </div>
              <div>
                <span className="text-sm font-medium text-gray-500">Category:</span>
                <p className="text-sm">{businessInfo.businessCategory}</p>
              </div>
              <div>
                <span className="text-sm font-medium text-gray-500">Description:</span>
                <p className="text-sm">{businessInfo.businessDescription}</p>
              </div>
              {businessInfo.targetAudience && (
                <div>
                  <span className="text-sm font-medium text-gray-500">Target Audience:</span>
                  <p className="text-sm">{businessInfo.targetAudience}</p>
                </div>
              )}
              {businessInfo.websitePurpose && (
                <div>
                  <span className="text-sm font-medium text-gray-500">Website Purpose:</span>
                  <p className="text-sm">{businessInfo.websitePurpose}</p>
                </div>
              )}
            </div>
          </div>

          {/* Design Preferences */}
          <div className="border rounded-lg overflow-hidden">
            <div className="bg-blue-50 border-b border-blue-100 px-4 py-2 flex items-center justify-between">
              <h3 className="font-medium text-blue-800">Design Preferences</h3>
              <CheckCircle className="h-5 w-5 text-green-500" />
            </div>
            <div className="p-4 grid grid-cols-1 sm:grid-cols-3 gap-4">
              <div>
                <span className="text-sm font-medium text-gray-500">Color Scheme:</span>
                <div className="flex items-center mt-1">
                  <div className={`w-4 h-4 rounded-full bg-${designPreferences.colorScheme}-500 mr-2`}></div>
                  <p className="text-sm capitalize">{designPreferences.colorScheme}</p>
                </div>
              </div>
              <div>
                <span className="text-sm font-medium text-gray-500">Style:</span>
                <p className="text-sm capitalize">{designPreferences.style}</p>
              </div>
              <div>
                <span className="text-sm font-medium text-gray-500">Mood:</span>
                <p className="text-sm capitalize">{designPreferences.mood}</p>
              </div>
            </div>
          </div>

          {/* Website Structure */}
          <div className="border rounded-lg overflow-hidden">
            <div className="bg-blue-50 border-b border-blue-100 px-4 py-2 flex items-center justify-between">
              <h3 className="font-medium text-blue-800">Website Structure</h3>
              <CheckCircle className="h-5 w-5 text-green-500" />
            </div>
            <div className="p-4 space-y-4">
              <div>
                <span className="text-sm font-medium text-gray-500">Pages:</span>
                <div className="mt-2 flex flex-wrap gap-2">
                  {structure.pages.map((page) => (
                    <span key={page} className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
                      {page}
                    </span>
                  ))}
                </div>
              </div>
              <div>
                <span className="text-sm font-medium text-gray-500">Homepage Sections:</span>
                <div className="mt-2 flex flex-wrap gap-2">
                  {structure.sections.map((section) => (
                    <span key={section} className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
                      {section}
                    </span>
                  ))}
                </div>
              </div>
            </div>
          </div>

          {/* Website Features */}
          <div className="border rounded-lg overflow-hidden">
            <div className="bg-blue-50 border-b border-blue-100 px-4 py-2 flex items-center justify-between">
              <h3 className="font-medium text-blue-800">Website Features</h3>
              <CheckCircle className="h-5 w-5 text-green-500" />
            </div>
            <div className="p-4">
              <ul className="space-y-1">
                {Object.entries(features).map(([key, value]) => {
                  if (key === 'other') return null;
                  if (!value) return null;
                  
                  return (
                    <li key={key} className="flex items-center">
                      <ChevronRight className="h-4 w-4 text-blue-500 mr-1" />
                      <span className="text-sm">{key.charAt(0).toUpperCase() + key.slice(1)}</span>
                    </li>
                  );
                })}
                
                {features.other && features.other.length > 0 && (
                  <>
                    <li className="pt-1 mt-1 border-t">
                      <span className="text-sm font-medium text-gray-500">Custom Features:</span>
                    </li>
                    {features.other.map((feature, index) => (
                      <li key={index} className="flex items-center">
                        <ChevronRight className="h-4 w-4 text-blue-500 mr-1" />
                        <span className="text-sm">{feature}</span>
                      </li>
                    ))}
                  </>
                )}
              </ul>
            </div>
          </div>
          
          {/* Final Notice */}
          <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
            <div className="flex">
              <div className="flex-shrink-0">
                <AlertCircle className="h-5 w-5 text-yellow-400" />
              </div>
              <div className="ml-3">
                <h3 className="text-sm font-medium text-yellow-800">
                  Ready to create your website
                </h3>
                <div className="mt-2 text-sm text-yellow-700">
                  <p>
                    Click "Create Website" to generate your website based on the information provided. 
                    The generation process may take a few minutes.
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </CardContent>
    </>
  );
};
