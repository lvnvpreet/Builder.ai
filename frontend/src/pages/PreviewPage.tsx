import React from 'react';
import { useParams } from 'react-router-dom';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/Card';
import Button from '@/components/ui/Button';
import { useAppStore } from '@/store';
import { ArrowLeft, ExternalLink } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import { getFullWebsiteUrl } from '@/utils/config';

const PreviewPage: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const { website } = useAppStore();
  const { currentWebsite, currentPreviewPage, setCurrentPreviewPage } = website;

  // In a real app, you would fetch the website data based on the ID if not available in the store
  // For now we'll use mock data
  
  const handleBack = () => {
    navigate('/');
  };
  
  const handlePageChange = (pageId: string) => {
    setCurrentPreviewPage(pageId);
  };

  if (!currentWebsite) {
    return (
      <div className="container py-12">
        <Card>
          <CardContent className="py-12">
            <div className="text-center">
              <h2 className="text-xl font-semibold mb-4">Website preview not available</h2>
              <p className="mb-6 text-gray-600">The website you're looking for could not be found.</p>
              <Button variant="primary" onClick={handleBack}>
                Back to Dashboard
              </Button>
            </div>
          </CardContent>
        </Card>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Preview Header */}
      <div className="bg-white shadow sticky top-0 z-10">
        <div className="container py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center">
              <Button
                variant="ghost"
                size="sm"
                leftIcon={<ArrowLeft className="h-4 w-4" />}
                onClick={handleBack}
              >
                Back to Dashboard
              </Button>
              <h1 className="text-lg font-medium ml-4">
                Previewing: {currentWebsite.websiteUrl}
              </h1>
            </div>
            
            <div>              <Button 
                variant="outline"
                size="sm"
                rightIcon={<ExternalLink className="h-4 w-4" />}
                onClick={() => window.open(getFullWebsiteUrl(currentWebsite.websiteUrl), '_blank')}
              >
                Open in New Tab
              </Button>
            </div>
          </div>
        </div>
      </div>

      {/* Preview Content */}
      <div className="container py-8">
        <div className="grid grid-cols-1 lg:grid-cols-4 gap-8">
          {/* Page Navigation Sidebar */}
          <div className="lg:col-span-1">
            <Card>
              <CardHeader>
                <CardTitle>Pages</CardTitle>
              </CardHeader>
              <CardContent>
                <nav className="space-y-1">
                  {currentWebsite.pages.map((page) => (
                    <button
                      key={page.id}
                      className={`block w-full text-left px-3 py-2 rounded-md transition-colors ${
                        currentPreviewPage === page.id
                          ? 'bg-blue-100 text-blue-800'
                          : 'hover:bg-gray-100'
                      }`}
                      onClick={() => handlePageChange(page.id)}
                    >
                      {page.name}
                    </button>
                  ))}
                </nav>
              </CardContent>
            </Card>
          </div>
          
          {/* Preview iframe */}
          <div className="lg:col-span-3">
            <Card padding="none">
              <div className="aspect-[16/9] w-full">                <iframe
                  src={getFullWebsiteUrl(currentWebsite.websiteUrl)}
                  className="w-full h-full border-0"
                  title="Website Preview"
                />
              </div>
            </Card>
          </div>
        </div>
      </div>
    </div>
  );
};

export default PreviewPage;
