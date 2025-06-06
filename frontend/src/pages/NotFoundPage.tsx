import React from 'react';
import { useNavigate } from 'react-router-dom';
import Button from '@/components/ui/Button';
import { Card, CardContent } from '@/components/ui/Card';
import { Home } from 'lucide-react';

const NotFoundPage: React.FC = () => {
  const navigate = useNavigate();
  
  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50">
      <div className="w-full max-w-md p-6">
        <Card>
          <CardContent className="flex flex-col items-center p-8 text-center">
            <div className="w-24 h-24 bg-gray-100 rounded-full flex items-center justify-center mb-6">
              <span className="text-4xl">404</span>
            </div>
            <h1 className="text-2xl font-bold mb-2">Page Not Found</h1>
            <p className="text-gray-600 mb-6">
              The page you are looking for doesn't exist or has been moved.
            </p>
            <Button 
              variant="primary" 
              leftIcon={<Home className="h-5 w-5" />}
              onClick={() => navigate('/')}
            >
              Back to Dashboard
            </Button>
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export default NotFoundPage;
