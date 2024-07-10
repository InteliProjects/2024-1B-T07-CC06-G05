import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Dashboard from './pages/dashboard';
import Header from './components/header';
import Comparison from './pages/comparison';
import Comercial from './pages/comercial';

import './reset.css';
import './styles.css';

/**
 * Componente que define as rotas da aplicação.
 *
 * @returns {JSX.Element} O elemento JSX que representa as rotas da aplicação.
 */
export default function AppRoutes() {
  return (
    <BrowserRouter>
      <Header />
      <Routes>
        <Route index element={<Comercial />} />
        <Route path="/technical" element={<Dashboard />} />
        <Route path="/compare" element={<Comparison />} />
      </Routes>
    </BrowserRouter>
  );
}
