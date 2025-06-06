export interface GenerationState {
  id: string;
  status: 'pending' | 'in_progress' | 'completed' | 'failed';
  progress: number;
  startedAt: Date;
  completedAt?: Date;
  businessData: BusinessData;
  steps: GenerationStep[];
  result?: GenerationResult;
  error?: GenerationError;
}

export interface GenerationStep {
  id: string;
  name: string;
  status: 'pending' | 'in_progress' | 'completed' | 'failed';
  progress: number;
  startedAt?: Date;
  completedAt?: Date;
  error?: string;
}

export interface BusinessData {
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
}

export interface GenerationProgress {
  generationId: string;
  progress: number;
  step: string;
  stepProgress: number;
  message?: string;
  timestamp: Date;
}

export interface GenerationResult {
  websiteUrl: string;
  htmlContent: string;
  cssContent: string;
  jsContent: string;
  images: ImageAsset[];
  pages: WebsitePage[];
  designSystem: DesignSystem;
}

export interface ImageAsset {
  id: string;
  url: string;
  alt: string;
  type: 'hero' | 'background' | 'product' | 'team' | 'icon' | 'logo' | 'other';
}

export interface WebsitePage {
  id: string;
  name: string;
  path: string;
  sections: WebsiteSection[];
}

export interface WebsiteSection {
  id: string;
  type: string;
  content: any;
}

export interface DesignSystem {
  colors: {
    primary: string;
    secondary: string;
    accent: string;
    background: string;
    text: string;
  };
  typography: {
    headingFont: string;
    bodyFont: string;
  };
  spacing: {
    base: number;
  };
}

export interface GenerationError {
  message: string;
  code: string;
  details?: string;
}
