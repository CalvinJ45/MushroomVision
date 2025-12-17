import React, { useRef } from 'react';
import Navbar from './components/Navbar/navbar';
import Hero from './components/Hero/Hero';
import Scanner from './components/Scanner/Scanner';

export default function App() {
  // Refs untuk Scroll
  const homeRef = useRef<HTMLDivElement>(null);
  const scannerRef = useRef<HTMLDivElement>(null);

  // Fungsi Scroll
  const scrollToSection = (section: string) => {
    if (section === 'home') homeRef.current?.scrollIntoView({ behavior: 'smooth' });
    if (section === 'scanner') scannerRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  return (
    <>
      <Navbar 
        scrollToSection={scrollToSection} 
      />
      
      {/* Wrapper Ref */}
      <div ref={homeRef}>
        <Hero scrollToSection={scrollToSection} />
      </div>

      <div ref={scannerRef}>
        <Scanner />
      </div>

      {/* Footer Simple */}
      <footer style={{textAlign: 'center', padding: '40px', background: 'white', color: '#9ca3af', fontSize: '0.85rem'}}>
        &copy; 2025 MushroomVision Project.
      </footer>
    </>
  );
}