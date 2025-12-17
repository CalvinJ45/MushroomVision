import React, { forwardRef } from 'react';
import { Camera, Book, Search, Info, MapPin } from 'lucide-react';
import './Hero.css';

interface HeroProps {
  scrollToSection: (section: string) => void;
}

const Hero = forwardRef<HTMLDivElement, HeroProps>(({ scrollToSection }, ref) => {
  return (
    <section ref={ref} className="hero-wrapper">
      
      <div className="hero-badge">
        <div className="dot"></div>
        AI-Powered Mushroom Identification
      </div>

      <h1 className="hero-title">
        Temukan Keajaiban <br />
        <span className="text-green">Dunia Fungi</span>
      </h1>

      <p className="hero-desc">
        Unggah foto jamur, identifikasi spesiesnya secara instan dengan AI, dan 
        bangun ensiklopedia jamur pribadimu di cloud.
      </p>

      <div className="hero-actions">
        <button onClick={() => scrollToSection('scanner')} className="btn-black">
          <Camera size={20} /> Mulai Scan
        </button>
        <button onClick={() => scrollToSection('collection')} className="btn-outline">
          <Book size={20} /> Lihat Koleksi
        </button>
      </div>

      <div className="features-container">
        {/* Kartu 1 */}
        <div className="feature-card">
          <div className="icon-box">
            <Search size={24} className="text-blue-600" color="#2563eb"/>
          </div>
          <div className="feature-info">
            <h3>Deteksi AI</h3>
            <p>Akurasi tinggi dalam mengenali spesies.</p>
          </div>
        </div>

        {/* Kartu 2 */}
        <div className="feature-card">
          <div className="icon-box">
            <Info size={24} color="#9333ea" />
          </div>
          <div className="feature-info">
            <h3>Info Lengkap</h3>
            <p>Habitat, toksisitas, dan fakta unik.</p>
          </div>
        </div>

        <div className="feature-card">
          <div className="icon-box">
            <MapPin size={24} color="#dc2626" />
          </div>
          <div className="feature-info">
            <h3>Pencatatan</h3>
            <p>Simpan lokasi dan tanggal temuanmu.</p>
          </div>
        </div>
      </div>

    </section>
  );
});

export default Hero;