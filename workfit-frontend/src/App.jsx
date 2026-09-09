import { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Home from './components/Home/Home';
import Auth from './components/Auth/Auth';
import Policy from './components/Policy/Policy';
import Community from './components/Community/Community';
import Chat from './components/Chat/Chat';
import MyPage from './components/MyPage/MyPage';
import WorkfitLogo from './components/Logo/WorkfitLogo';
import './App.css';

function App() {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const token = localStorage.getItem('token');
    const savedUser = localStorage.getItem('user');

    if (token && savedUser) {
      try {
        setUser(JSON.parse(savedUser));
      } catch {
        localStorage.removeItem('token');
        localStorage.removeItem('user');
      }
    }

    setLoading(false);
  }, []);

  const handleLoginSuccess = (userData) => {
    setUser(userData);
  };

  const handleLogout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    setUser(null);
  };

  if (loading) {
    return <div className="app loading">로딩 중...</div>;
  }

  if (!user) {
    return <Auth onLoginSuccess={handleLoginSuccess} />;
  }

  return (
    <Router>
      <div className="app">
        <Routes>
          <Route path="/" element={<MainLayout user={user} onLogout={handleLogout} />}>
            <Route index element={<Home user={user} onLogout={handleLogout} />} />
            <Route path="policy" element={<Policy />} />
            <Route path="community" element={<Community />} />
            <Route path="chat" element={<Chat />} />
            <Route path="mypage" element={<MyPage />} />
          </Route>
        </Routes>
      </div>
    </Router>
  );
}

function MainLayout({ user, onLogout }) {
  return (
    <div className="main-layout">
      <nav className="main-navbar">
        <div className="navbar-left">
          <a href="/" className="logo">
            <WorkfitLogo size={36} />
            <span>청년워크핏</span>
          </a>
          <div className="nav-links">
            <a href="/">🏠 홈</a>
            <a href="/policy">🔍 정책</a>
            <a href="/community">👥 커뮤니티</a>
            <a href="/chat">💬 워크챗</a>
            <a href="/mypage">👤 마이페이지</a>
          </div>
        </div>
        <div className="navbar-right">
          <span className="user-name">{user?.name}님</span>
          <button className="logout-btn" onClick={onLogout}>로그아웃</button>
        </div>
      </nav>
      <Routes>
        <Route index element={<Home user={user} onLogout={onLogout} />} />
        <Route path="policy" element={<Policy />} />
        <Route path="community" element={<Community />} />
        <Route path="chat" element={<Chat />} />
        <Route path="mypage" element={<MyPage />} />
      </Routes>
    </div>
  );
}

export default App;
