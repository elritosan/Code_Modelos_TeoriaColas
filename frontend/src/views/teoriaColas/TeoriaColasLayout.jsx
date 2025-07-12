// frontend\src\views\teoriaColas\TeoriaColasLayout.jsx
import React from 'react';
import { Outlet } from 'react-router-dom';
import Sidebar from '../../components/teoriaColas/Sidebar';

const TeoriaColasLayout = () => {
  return (
    <div className="teoria-colas-layout d-flex">
      <Sidebar />
      <main className="teoria-content flex-grow-1 p-4">
        <Outlet />
      </main>
    </div>
  );
};

export default TeoriaColasLayout;