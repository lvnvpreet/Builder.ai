import React from 'react';
import { UseFormReturn } from 'react-hook-form';
import { MessageSquare, ShoppingCart, Image, Star, Share2, Mail, Plus, Minus } from 'lucide-react';
import { CardHeader, CardTitle, CardContent } from '@/components/ui/Card';
import type { WizardFormData } from '@/types/wizard';

interface FeaturesStepProps {
  form: UseFormReturn<WizardFormData>;
  formData: WizardFormData;
}

const featuresList = [
  { 
    id: 'contactForm', 
    name: 'Contact Form', 
    description: 'Allow visitors to contact you directly from your website',
    icon: <MessageSquare className="h-5 w-5 text-blue-500" />
  },
  { 
    id: 'gallery', 
    name: 'Image Gallery', 
    description: 'Showcase your work, products, or portfolio with an image gallery',
    icon: <Image className="h-5 w-5 text-blue-500" />
  },
  { 
    id: 'blog', 
    name: 'Blog Section', 
    description: 'Share news, updates, and articles with your audience',
    icon: <MessageSquare className="h-5 w-5 text-blue-500" />
  },
  { 
    id: 'ecommerce', 
    name: 'E-commerce Features', 
    description: 'Add basic product listings and shopping capabilities',
    icon: <ShoppingCart className="h-5 w-5 text-blue-500" />
  },
  { 
    id: 'testimonials', 
    name: 'Testimonials', 
    description: 'Display customer reviews and testimonials',
    icon: <Star className="h-5 w-5 text-blue-500" />
  },
  { 
    id: 'socialMedia', 
    name: 'Social Media Integration', 
    description: 'Add links to your social media profiles',
    icon: <Share2 className="h-5 w-5 text-blue-500" />
  },
  { 
    id: 'newsletter', 
    name: 'Newsletter Signup', 
    description: 'Collect email addresses for your mailing list',
    icon: <Mail className="h-5 w-5 text-blue-500" />
  }
];

export const FeaturesStep: React.FC<FeaturesStepProps> = ({ form }) => {
  const { register, watch, setValue } = form;
  const features = watch('features');
  const customFeatures = watch('features.other') || [];

  const [newFeature, setNewFeature] = React.useState('');

  const handleAddCustomFeature = () => {
    if (newFeature && !customFeatures.includes(newFeature)) {
      setValue('features.other', [...customFeatures, newFeature]);
      setNewFeature('');
    }
  };

  const handleRemoveCustomFeature = (feature: string) => {
    setValue('features.other', customFeatures.filter(f => f !== feature));
  };

  return (
    <>
      <CardHeader>
        <CardTitle>Website Features</CardTitle>
        <p className="text-gray-600 mt-1">
          Select the functionality you'd like to include in your website
        </p>
      </CardHeader>

      <CardContent>
        <div className="space-y-6">
          <p className="text-sm text-gray-600">
            Choose the features that will help you achieve your website goals. You can always add more features later.
          </p>

          <div className="space-y-4">
            {featuresList.map(feature => (
              <div key={feature.id} className="flex items-start">
                <div className="flex items-center h-5 mt-1">
                  <input
                    id={feature.id}
                    type="checkbox"
                    className="h-4 w-4 rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                    {...register(`features.${feature.id}` as any)}
                  />
                </div>
                <div className="ml-3">
                  <label htmlFor={feature.id} className="flex items-center cursor-pointer">
                    {feature.icon}
                    <span className="ml-2 font-medium">{feature.name}</span>
                  </label>
                  <p className="text-sm text-gray-500 mt-1">
                    {feature.description}
                  </p>
                </div>
              </div>
            ))}
          </div>

          <div className="pt-4 border-t border-gray-200">
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Custom Features (Optional)
            </label>
            
            <div className="flex mb-2">
              <input
                type="text"
                value={newFeature}
                onChange={(e) => setNewFeature(e.target.value)}
                className="flex-1 rounded-l-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm"
                placeholder="Enter a custom feature"
              />
              <button
                type="button"
                onClick={handleAddCustomFeature}
                className="inline-flex items-center px-4 py-2 border border-l-0 border-gray-300 rounded-r-md bg-gray-50 text-gray-700 hover:bg-gray-100"
              >
                <Plus className="h-4 w-4" />
              </button>
            </div>

            {customFeatures.length > 0 && (
              <div className="space-y-2 mt-3">
                {customFeatures.map((feature, index) => (
                  <div key={index} className="flex items-center justify-between p-2 bg-gray-50 rounded border border-gray-200">
                    <span className="text-sm">{feature}</span>
                    <button
                      type="button"
                      onClick={() => handleRemoveCustomFeature(feature)}
                      className="text-gray-500 hover:text-red-500"
                    >
                      <Minus className="h-4 w-4" />
                    </button>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      </CardContent>
    </>
  );
};
