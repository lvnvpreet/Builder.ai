import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { ChevronLeft, ChevronRight, Check } from 'lucide-react';
import { useForm } from 'react-hook-form';
import Button from '@/components/ui/Button';
import { Card } from '@/components/ui/Card';
import type { WizardFormData } from '@/types/wizard';
import toast from 'react-hot-toast';

// Import step components (we'll define them later)
import { BusinessInfoStep } from './steps/BusinessInfoStep.tsx';
import { DesignPreferencesStep } from './steps/DesignPreferencesStep.tsx';
import { StructureStep } from './steps/StructureStep.tsx';
import { FeaturesStep } from './steps/FeaturesStep.tsx';
import { ReviewStep } from './steps/ReviewStep.tsx';

const steps = [
  { id: 'business', title: 'Business Info', component: BusinessInfoStep },
  { id: 'design', title: 'Design', component: DesignPreferencesStep },
  { id: 'structure', title: 'Structure', component: StructureStep },
  { id: 'features', title: 'Features', component: FeaturesStep },
  { id: 'review', title: 'Review', component: ReviewStep },
];

interface GenerationWizardProps {
  onComplete: (data: WizardFormData) => void;
  onCancel: () => void;
}

export const GenerationWizard: React.FC<GenerationWizardProps> = ({
  onComplete,
  onCancel,
}) => {
  const [currentStep, setCurrentStep] = useState(0);
  const [completedSteps, setCompletedSteps] = useState<Set<number>>(new Set());
  
  const form = useForm<WizardFormData>({
    defaultValues: {
      businessInfo: {
        businessName: '',
        businessDescription: '',
        businessCategory: '',
        targetAudience: '',
        websitePurpose: '',
      },
      designPreferences: {
        colorScheme: 'blue',
        style: 'modern',
        mood: 'professional'
      },
      structure: {
        pages: ['home', 'about', 'services', 'contact'],
        sections: ['hero', 'features', 'testimonials']
      },
      features: {
        contactForm: true,
        gallery: false,
        blog: false,
        ecommerce: false,
        testimonials: true,
        socialMedia: true,
        newsletter: false
      }
    },
  });

  const { watch, trigger, getValues } = form;
  const formData = watch();

  const isStepValid = async (stepIndex: number): Promise<boolean> => {
    const stepValidationMap = {
      0: ['businessInfo.businessName', 'businessInfo.businessCategory', 'businessInfo.businessDescription'],
      1: ['designPreferences.colorScheme', 'designPreferences.style'],
      2: ['structure.pages'],
      3: [],
      4: [], // Review step is always valid
    };

    const fieldsToValidate = stepValidationMap[stepIndex as keyof typeof stepValidationMap] || [];
    
    if (fieldsToValidate.length === 0) return true;
    
    return await trigger(fieldsToValidate as any);
  };

  const handleNext = async () => {
    const isValid = await isStepValid(currentStep);
    
    if (isValid) {
      setCompletedSteps(prev => new Set([...prev, currentStep]));
      
      if (currentStep < steps.length - 1) {
        setCurrentStep(currentStep + 1);
      } else {
        // Submit the form
        try {
          onComplete(getValues());
          toast.success('Building your website...');
        } catch (error) {
          toast.error('Error submitting form');
          console.error(error);
        }
      }
    } else {
      toast.error('Please fill in all required fields');
    }
  };

  const handlePrevious = () => {
    if (currentStep > 0) {
      setCurrentStep(currentStep - 1);
    }
  };

  const handleStepClick = async (stepIndex: number) => {
    // Allow going to previous steps or next step if current is valid
    if (stepIndex < currentStep || (stepIndex === currentStep + 1 && await isStepValid(currentStep))) {
      setCurrentStep(stepIndex);
    }
  };

  const CurrentStepComponent = steps[currentStep].component;

  return (
    <div className="max-w-4xl mx-auto p-6">
      {/* Progress Steps */}
      <div className="mb-8">
        <div className="flex items-center justify-between">
          {steps.map((step, index) => (
            <div key={step.id} className="flex flex-col items-center">
              <button
                className={`flex items-center justify-center w-10 h-10 rounded-full ${
                  completedSteps.has(index)
                    ? 'bg-blue-600 text-white'
                    : index === currentStep
                    ? 'border-2 border-blue-600 text-blue-600'
                    : 'border border-gray-300 text-gray-400'
                } transition-colors duration-200`}
                onClick={() => handleStepClick(index)}
                disabled={index > currentStep && !completedSteps.has(currentStep)}
              >
                {completedSteps.has(index) ? (
                  <Check className="h-5 w-5" />
                ) : (
                  <span>{index + 1}</span>
                )}
              </button>
              <span className={`mt-2 text-sm font-medium ${
                index === currentStep ? 'text-blue-600' : 'text-gray-500'
              }`}>
                {step.title}
              </span>
            </div>
          ))}
        </div>
        <div className="relative mt-2">
          <div className="absolute top-0 left-0 w-full h-1 bg-gray-200 rounded"></div>
          <motion.div 
            className="absolute top-0 left-0 h-1 bg-blue-600 rounded"
            initial={{ width: '0%' }}
            animate={{ width: `${(currentStep / (steps.length - 1)) * 100}%` }}
            transition={{ duration: 0.3 }}
          />
        </div>
      </div>

      <Card variant="bordered" padding="lg">
        <AnimatePresence mode="wait">
          <motion.div
            key={currentStep}
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: -20 }}
            transition={{ duration: 0.3 }}
          >
            <CurrentStepComponent form={form} formData={formData} />
          </motion.div>
        </AnimatePresence>

        <div className="mt-8 flex justify-between">
          <Button 
            variant="outline" 
            onClick={currentStep === 0 ? onCancel : handlePrevious}
            leftIcon={currentStep > 0 ? <ChevronLeft className="h-4 w-4" /> : undefined}
          >
            {currentStep === 0 ? 'Cancel' : 'Previous'}
          </Button>
          <Button 
            variant="primary" 
            onClick={handleNext} 
            rightIcon={<ChevronRight className="h-4 w-4" />}
          >
            {currentStep === steps.length - 1 ? 'Create Website' : 'Next'}
          </Button>
        </div>
      </Card>
    </div>
  );
};
