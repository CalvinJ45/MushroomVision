import React, { useState, forwardRef } from 'react';
import { Upload, Search, X, Loader2, RefreshCcw, MapPin, AlertTriangle } from 'lucide-react';
import './Scanner.css';

interface ScannerProps {}

const Scanner = forwardRef<HTMLDivElement, ScannerProps>((_, ref) => {
  const [image, setImage] = useState<string | null>(null);
  const [imageFile, setImageFile] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);

  const handleUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files?.[0]) {
      const file = e.target.files[0];
      setImage(URL.createObjectURL(file));
      setImageFile(file);
      setResult(null);
      setError(null);
    }
  };

  const onAnalyze = async () => {
    if (!imageFile) return;

    setLoading(true);
    setError(null);

    const formData = new FormData();
    formData.append('image', imageFile);

    try {
      const response = await fetch('http://localhost:5000/predict', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error('Gagal menganalisa gambar. Pastikan server backend berjalan.');
      }

      const data = await response.json();
      setResult(data);
    } catch (err: any) {
      console.error(err);
      setError(err.message || "Terjadi kesalahan saat memproses gambar.");
    } finally {
      setLoading(false);
    }
  };

  const handleReset = () => {
    setImage(null);
    setImageFile(null);
    setResult(null);
    setError(null);
  };

  return (
    <section ref={ref} className="scanner-section">
      <div className="scanner-container">
        
        {/* Header */}
        <div className="scanner-header">
          <span className="sub-label">SCANNER</span>
          <h2 className="section-title">Identifikasi Spesimen</h2>
        </div>

        <div className="scanner-grid">
          
          {/* KIRI: Upload */}
          <div>
            <div className="upload-card" onClick={() => !image && document.getElementById('fileInput')?.click()}>
              {image ? (
                <>
                  <img src={image} alt="Preview" className="img-preview" />
                  <button onClick={(e) => {e.stopPropagation(); handleReset();}} className="btn-reset">
                    <X size={20} />
                  </button>
                </>
              ) : (
                <>
                  <div className="icon-upload-bg"><Upload size={24} color="#16a34a"/></div>
                  <h3 className="upload-title">Upload Foto Jamur</h3>
                  <p className="upload-desc">Drag & drop atau klik untuk memilih</p>
                  <span className="btn-file">Pilih File</span>
                  <input id="fileInput" type="file" hidden onChange={handleUpload} accept="image/*" />
                </>
              )}
            </div>

            {image && !result && !loading && (
              <button onClick={onAnalyze} className="btn-analyze">
                <Search size={20} /> Analisa Sekarang
              </button>
            )}

            {loading && (
               <button className="btn-analyze" disabled>
                 <Loader2 className="animate-spin" /> Menganalisa...
               </button>
            )}

            {error && (
              <div style={{marginTop: '1rem', color: 'red', fontSize: '0.9rem', textAlign: 'center'}}>
                {error}
              </div>
            )}
          </div>

          {/* KANAN: Hasil / Placeholder */}
          <div className="result-card" style={{background: result ? 'white' : '#fafaf9', borderStyle: result ? 'solid' : 'dashed'}}>
            {result ? (
              <div className="result-content">
                <span className="confidence-tag">Akurasi {(result.confidence * 100).toFixed(0)}%</span>
                <h2 className="mushroom-name">{result.name}</h2>
                <p className="mushroom-desc">{result.desc}</p>
                
                <div className="info-grid">
                  <div className="info-box">
                    <span className="info-label"><MapPin size={12}/> Region</span>
                    <span className="info-val">{result.region}</span>
                  </div>
                  <div className="info-box" style={{background: '#fef2f2', borderColor: '#fee2e2'}}>
                    <span className="info-label" style={{color:'#ef4444'}}><AlertTriangle size={12}/> Safety</span>
                    <span className="info-val" style={{color:'#991b1b'}}>{result.edibility}</span>
                  </div>
                </div>

                <button className="btn-save" onClick={handleReset}>
                  <RefreshCcw size={18}/> Upload/Scan Lainnya
                </button>
              </div>
            ) : (
              <div className="empty-state">
                <div className="icon-search-bg"><Search size={40} /></div>
                <h3 className="upload-title" style={{color: '#9ca3af'}}>Menunggu Data</h3>
                <p className="upload-desc" style={{maxWidth: '250px', margin: '0 auto'}}>
                  Upload foto di panel sebelah kiri untuk melihat hasil identifikasi detil disini.
                </p>
              </div>
            )}
          </div>

        </div>
      </div>
    </section>
  );
});

export default Scanner;