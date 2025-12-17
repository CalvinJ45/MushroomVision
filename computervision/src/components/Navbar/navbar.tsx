import React from 'react';
import { Leaf } from 'lucide-react';
import './Navbar.css';

interface NavbarProps {
  scrollToSection: (section: string) => void;
}

export default function Navbar({ scrollToSection }: NavbarProps) {
  return (
    <nav className="navbar">
      <div className="nav-container">

        <div className="nav-logo" onClick={() => scrollToSection('home')}>
          <div className="logo-icon"><Leaf size={20} fill="white" /></div>
          <span>MushroomVision</span>
        </div>

        <div className="nav-menu">
          <button onClick={() => scrollToSection('home')} className="nav-link">Home</button>
          <button onClick={() => scrollToSection('scanner')} className="nav-link">Scanner</button>
        </div>

      </div>
    </nav>
  );
}