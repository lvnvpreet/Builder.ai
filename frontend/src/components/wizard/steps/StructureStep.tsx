import React from 'react';
import { UseFormReturn } from 'react-hook-form';
import { LayoutGrid, FileText } from 'lucide-react';
import { CardHeader, CardTitle, CardContent } from '@/components/ui/Card';
import type { WizardFormData } from '@/types/wizard';

interface StructureStepProps {
  form: UseFormReturn<WizardFormData>;
  formData: WizardFormData;
}

const commonPages = [
  { id: 'home', name: 'Home Page', default: true },
  { id: 'about', name: 'About Us', default: true },
  { id: 'services', name: 'Services/Products', default: true },
  { id: 'contact', name: 'Contact', default: true },
  { id: 'gallery', name: 'Gallery/Portfolio', default: false },
  { id: 'testimonials', name: 'Testimonials', default: false },
  { id: 'blog', name: 'Blog', default: false },
  { id: 'faq', name: 'FAQ', default: false },
  { id: 'pricing', name: 'Pricing', default: false },
  { id: 'team', name: 'Our Team', default: false }
];

const commonSections = [
  { id: 'hero', name: 'Hero/Banner', default: true },
  { id: 'features', name: 'Features/Services', default: true },
  { id: 'about', name: 'About Section', default: true },
  { id: 'testimonials', name: 'Testimonials', default: true },
  { id: 'cta', name: 'Call to Action', default: true },
  { id: 'stats', name: 'Statistics', default: false },
  { id: 'pricing', name: 'Pricing Table', default: false },
  { id: 'team', name: 'Team Members', default: false },
  { id: 'gallery', name: 'Image Gallery', default: false },
  { id: 'faq', name: 'FAQ Accordion', default: false },
  { id: 'contact', name: 'Contact Form', default: false },
  { id: 'blog', name: 'Blog Preview', default: false }
];

export const StructureStep: React.FC<StructureStepProps> = ({ form }) => {
  const { register, setValue, watch } = form;
  const selectedPages = watch('structure.pages') || [];
  const selectedSections = watch('structure.sections') || [];

  const handlePageToggle = (pageId: string) => {
    const currentPages = [...selectedPages];
    
    if (currentPages.includes(pageId)) {
      setValue('structure.pages', currentPages.filter(id => id !== pageId));
    } else {
      setValue('structure.pages', [...currentPages, pageId]);
    }
  };

  const handleSectionToggle = (sectionId: string) => {
    const currentSections = [...selectedSections];
    
    if (currentSections.includes(sectionId)) {
      setValue('structure.sections', currentSections.filter(id => id !== sectionId));
    } else {
      setValue('structure.sections', [...currentSections, sectionId]);
    }
  };

  return (
    <>
      <CardHeader>
        <CardTitle>Website Structure</CardTitle>
        <p className="text-gray-600 mt-1">
          Select the pages and sections you'd like to include in your website
        </p>
      </CardHeader>

      <CardContent>
        <div className="space-y-8">
          <div>
            <div className="flex items-center mb-4">
              <FileText className="h-5 w-5 text-blue-600 mr-2" />
              <h3 className="text-lg font-medium">Pages</h3>
            </div>
            
            <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-3">
              {commonPages.map((page) => {
                const isSelected = selectedPages.includes(page.id);
                
                return (
                  <div key={page.id}>
                    {/* Hidden checkbox for the form */}
                    <input
                      type="checkbox"
                      id={`page-${page.id}`}
                      value={page.id}
                      checked={isSelected}
                      className="sr-only"
                      {...register('structure.pages')}
                      onChange={() => handlePageToggle(page.id)}
                    />
                    <label
                      htmlFor={`page-${page.id}`}
                      className={`block p-3 border rounded-md cursor-pointer text-center transition-all ${
                        isSelected 
                          ? 'bg-blue-50 border-blue-500 text-blue-700' 
                          : 'border-gray-300 hover:bg-gray-50'
                      }`}
                    >
                      {page.name}
                    </label>
                  </div>
                );
              })}
            </div>
            <p className="text-xs text-gray-500 mt-2">
              Select at least one page for your website
            </p>
          </div>

          <div>
            <div className="flex items-center mb-4">
              <LayoutGrid className="h-5 w-5 text-blue-600 mr-2" />
              <h3 className="text-lg font-medium">Homepage Sections</h3>
            </div>
            
            <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-3">
              {commonSections.map((section) => {
                const isSelected = selectedSections.includes(section.id);
                
                return (
                  <div key={section.id}>
                    {/* Hidden checkbox for the form */}
                    <input
                      type="checkbox"
                      id={`section-${section.id}`}
                      value={section.id}
                      checked={isSelected}
                      className="sr-only"
                      {...register('structure.sections')}
                      onChange={() => handleSectionToggle(section.id)}
                    />
                    <label
                      htmlFor={`section-${section.id}`}
                      className={`block p-3 border rounded-md cursor-pointer text-center transition-all ${
                        isSelected 
                          ? 'bg-blue-50 border-blue-500 text-blue-700' 
                          : 'border-gray-300 hover:bg-gray-50'
                      }`}
                    >
                      {section.name}
                    </label>
                  </div>
                );
              })}
            </div>
            <p className="text-xs text-gray-500 mt-2">
              Select the sections you want to appear on your homepage
            </p>
          </div>
        </div>
      </CardContent>
    </>
  );
};
