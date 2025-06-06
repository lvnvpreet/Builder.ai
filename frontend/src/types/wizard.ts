import { BusinessData } from './generation';

export interface WizardFormData {
  businessInfo: {
    businessName: string;
    businessDescription: string;
    businessCategory: string;
    targetAudience: string;
    websitePurpose: string;
    contactInfo?: {
      email?: string;
      phone?: string;
      address?: string;
    };
    additionalInfo?: string;
  };
  designPreferences: {
    colorScheme: string;
    style: string;
    mood: string;
    references?: string[];
  };
  structure: {
    pages: string[];
    sections: string[];
  };
  features: {
    contactForm: boolean;
    gallery: boolean;
    blog: boolean;
    ecommerce: boolean;
    testimonials: boolean;
    socialMedia: boolean;
    newsletter: boolean;
    other?: string[];
  };
}

export interface StepComponentProps {
  form: any; // react-hook-form type
  formData: WizardFormData;
}
