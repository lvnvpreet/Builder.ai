import React from 'react';
import { UseFormReturn } from 'react-hook-form';
import { Palette, Brush, Smile } from 'lucide-react';
import { CardHeader, CardTitle, CardContent } from '@/components/ui/Card';
import type { WizardFormData } from '@/types/wizard';

interface DesignPreferencesStepProps {
  form: UseFormReturn<WizardFormData>;
  formData: WizardFormData;
}

const colorSchemes = [
  { name: 'Blue', value: 'blue', preview: 'bg-blue-500' },
  { name: 'Green', value: 'green', preview: 'bg-green-500' },
  { name: 'Red', value: 'red', preview: 'bg-red-500' },
  { name: 'Purple', value: 'purple', preview: 'bg-purple-500' },
  { name: 'Teal', value: 'teal', preview: 'bg-teal-500' },
  { name: 'Orange', value: 'orange', preview: 'bg-orange-500' },
  { name: 'Gray', value: 'gray', preview: 'bg-gray-500' },
];

const designStyles = [
  'Modern',
  'Minimalist',
  'Corporate',
  'Creative',
  'Bold',
  'Elegant',
  'Playful',
  'Professional'
];

const designMoods = [
  'Professional',
  'Friendly',
  'Luxury',
  'Energetic',
  'Calm',
  'Innovative',
  'Trustworthy',
  'Fun'
];

export const DesignPreferencesStep: React.FC<DesignPreferencesStepProps> = ({ form }) => {
  const { register, formState: { errors }, watch } = form;
  const selectedScheme = watch('designPreferences.colorScheme');

  return (
    <>
      <CardHeader>
        <CardTitle>Design Preferences</CardTitle>
        <p className="text-gray-600 mt-1">
          Choose the visual style and feel for your website
        </p>
      </CardHeader>

      <CardContent>
        <div className="space-y-6">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Color Scheme
            </label>
            <div className="grid grid-cols-3 sm:grid-cols-4 md:grid-cols-7 gap-3">
              {colorSchemes.map((scheme) => (
                <label
                  key={scheme.value}
                  className={`flex flex-col items-center p-2 rounded-md cursor-pointer ${
                    selectedScheme === scheme.value ? 'ring-2 ring-blue-500 ring-offset-2' : 'hover:bg-gray-50'
                  }`}
                >
                  <div className={`w-10 h-10 rounded-full mb-2 ${scheme.preview}`}></div>
                  <div className="flex items-center">
                    <input
                      type="radio"
                      className="sr-only"
                      value={scheme.value}
                      {...register('designPreferences.colorScheme')}
                    />
                    <span className="text-sm">{scheme.name}</span>
                  </div>
                </label>
              ))}
            </div>
          </div>

          <div>
            <label htmlFor="designStyle" className="block text-sm font-medium text-gray-700 mb-1">
              Design Style
            </label>
            <div className="relative">
              <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <Brush className="h-5 w-5 text-gray-400" />
              </div>
              <select
                id="designStyle"
                className="pl-10 block w-full rounded-md border border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm"
                {...register('designPreferences.style')}
              >
                <option value="">Select a design style</option>
                {designStyles.map((style) => (
                  <option key={style} value={style.toLowerCase()}>{style}</option>
                ))}
              </select>
            </div>
          </div>

          <div>
            <label htmlFor="designMood" className="block text-sm font-medium text-gray-700 mb-1">
              Mood/Feel
            </label>
            <div className="relative">
              <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <Smile className="h-5 w-5 text-gray-400" />
              </div>
              <select
                id="designMood"
                className="pl-10 block w-full rounded-md border border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm"
                {...register('designPreferences.mood')}
              >
                <option value="">Select a mood</option>
                {designMoods.map((mood) => (
                  <option key={mood} value={mood.toLowerCase()}>{mood}</option>
                ))}
              </select>
            </div>
          </div>

          <div>
            <label htmlFor="designReferences" className="block text-sm font-medium text-gray-700 mb-1">
              References (Optional)
            </label>
            <textarea
              id="designReferences"
              rows={3}
              className="block w-full rounded-md border border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm"
              placeholder="Enter any website URLs that you like the style of, separated by commas."
              {...register('designPreferences.references')}
            />
            <p className="text-xs text-gray-500 mt-1">
              You can provide URLs of websites you like as design references.
            </p>
          </div>
        </div>
      </CardContent>
    </>
  );
};
