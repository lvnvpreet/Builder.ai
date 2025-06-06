import React from 'react';
import { UseFormReturn } from 'react-hook-form';
import { Building2, Users, Target } from 'lucide-react';
import { CardHeader, CardTitle, CardContent } from '@/components/ui/Card';
import type { WizardFormData } from '@/types/wizard';

interface BusinessInfoStepProps {
  form: UseFormReturn<WizardFormData>;
  formData: WizardFormData;
}

const businessCategories = [
  'Technology', 'Healthcare', 'Finance', 'Education', 'E-commerce',
  'Real Estate', 'Legal', 'Consulting', 'Restaurant', 'Fitness',
  'Creative', 'Non-profit', 'Manufacturing', 'Other'
];

const websitePurposes = [
  'Lead Generation', 'Brand Awareness', 'E-commerce Sales', 
  'Information Sharing', 'Portfolio Showcase', 'Service Booking',
  'Community Building', 'Content Publishing'
];

export const BusinessInfoStep: React.FC<BusinessInfoStepProps> = ({ form }) => {
  const { register, formState: { errors } } = form;

  return (
    <>
      <CardHeader>
        <CardTitle>Business Information</CardTitle>
        <p className="text-gray-600 mt-1">
          Tell us about your business so we can create a perfect website for you
        </p>
      </CardHeader>

      <CardContent>
        <div className="space-y-6">
          <div>
            <label htmlFor="businessName" className="block text-sm font-medium text-gray-700 mb-1">
              Business Name*
            </label>
            <div className="relative">
              <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <Building2 className="h-5 w-5 text-gray-400" />
              </div>
              <input
                id="businessName"
                type="text"
                className={`pl-10 block w-full rounded-md border ${errors.businessInfo?.businessName ? 'border-red-500' : 'border-gray-300'} shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm`}
                placeholder="e.g. Acme Inc."
                {...register('businessInfo.businessName', { required: 'Business name is required' })}
              />
            </div>
            {errors.businessInfo?.businessName && (
              <p className="mt-1 text-sm text-red-600">{errors.businessInfo.businessName.message}</p>
            )}
          </div>

          <div>
            <label htmlFor="businessCategory" className="block text-sm font-medium text-gray-700 mb-1">
              Business Category*
            </label>
            <select
              id="businessCategory"
              className={`block w-full rounded-md border ${errors.businessInfo?.businessCategory ? 'border-red-500' : 'border-gray-300'} shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm`}
              {...register('businessInfo.businessCategory', { required: 'Business category is required' })}
            >
              <option value="">Select a category</option>
              {businessCategories.map((category) => (
                <option key={category} value={category}>{category}</option>
              ))}
            </select>
            {errors.businessInfo?.businessCategory && (
              <p className="mt-1 text-sm text-red-600">{errors.businessInfo.businessCategory.message}</p>
            )}
          </div>

          <div>
            <label htmlFor="businessDescription" className="block text-sm font-medium text-gray-700 mb-1">
              Business Description*
            </label>
            <textarea
              id="businessDescription"
              rows={4}
              className={`block w-full rounded-md border ${errors.businessInfo?.businessDescription ? 'border-red-500' : 'border-gray-300'} shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm`}
              placeholder="Describe what your business does, your products or services, and your unique value proposition."
              {...register('businessInfo.businessDescription', { 
                required: 'Business description is required',
                minLength: { value: 20, message: 'Description should be at least 20 characters' } 
              })}
            />
            {errors.businessInfo?.businessDescription && (
              <p className="mt-1 text-sm text-red-600">{errors.businessInfo.businessDescription.message}</p>
            )}
          </div>
          
          <div>
            <label htmlFor="targetAudience" className="block text-sm font-medium text-gray-700 mb-1">
              Target Audience
            </label>
            <div className="relative">
              <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <Users className="h-5 w-5 text-gray-400" />
              </div>
              <input
                id="targetAudience"
                type="text"
                className="pl-10 block w-full rounded-md border border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm"
                placeholder="e.g. Small business owners, young professionals, etc."
                {...register('businessInfo.targetAudience')}
              />
            </div>
          </div>

          <div>
            <label htmlFor="websitePurpose" className="block text-sm font-medium text-gray-700 mb-1">
              Website Purpose
            </label>
            <div className="relative">
              <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <Target className="h-5 w-5 text-gray-400" />
              </div>
              <select
                id="websitePurpose"
                className="pl-10 block w-full rounded-md border border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm"
                {...register('businessInfo.websitePurpose')}
              >
                <option value="">Select primary purpose</option>
                {websitePurposes.map((purpose) => (
                  <option key={purpose} value={purpose}>{purpose}</option>
                ))}
              </select>
            </div>
          </div>
          
          <div>
            <label htmlFor="additionalInfo" className="block text-sm font-medium text-gray-700 mb-1">
              Additional Information (Optional)
            </label>
            <textarea
              id="additionalInfo"
              rows={3}
              className="block w-full rounded-md border border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm"
              placeholder="Any additional details you'd like us to know about your business or website needs."
              {...register('businessInfo.additionalInfo')}
            />
          </div>
        </div>
      </CardContent>
    </>
  );
};
