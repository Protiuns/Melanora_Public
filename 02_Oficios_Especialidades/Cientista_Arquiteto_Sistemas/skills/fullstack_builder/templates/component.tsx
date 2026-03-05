import React from 'react';

type Props = {
  // Defina as props aqui
  title?: string;
};

export const TemplateComponent: React.FC<Props> = ({ title = 'New Component' }) => {
  return (
    <div className="p-4 bg-white rounded-lg shadow-md">
      <h2 className="text-xl font-bold text-gray-800">{title}</h2>
      <div className="mt-2 text-gray-600">
        Conteúdo aqui...
      </div>
    </div>
  );
};
