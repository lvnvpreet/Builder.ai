import React from 'react';
import { Routes, Route } from 'react-router-dom';
import { Toaster } from 'react-hot-toast';

// Pages
import Dashboard from './pages/Dashboard';
import GenerationPage from './pages/GenerationPage';
import PreviewPage from './pages/PreviewPage';
import NotFoundPage from './pages/NotFoundPage';

function App() {
  return (
    <>
      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/generate" element={<GenerationPage />} />
        <Route path="/preview/:id" element={<PreviewPage />} />
        <Route path="*" element={<NotFoundPage />} />
      </Routes>
      <Toaster 
        position="bottom-right" 
        toastOptions={{
          duration: 3000,
          style: {
            background: '#363636',
            color: '#fff',
          },
        }} 
      />
    </>
  );
}

export default App;
