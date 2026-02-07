import React from 'react';

const Footer = () => {
  return (
    <footer className="bg-gray-100 border-t mt-auto">
      <div className="container mx-auto px-4 py-6 max-w-4xl">
        <div className="text-center text-gray-600">
          <p>&copy; {new Date().getFullYear()} Todo App. All rights reserved.</p>
        </div>
      </div>
    </footer>
  );
};

export default Footer;