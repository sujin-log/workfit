import { useState } from 'react';
import client from '../../api/client';
import './Auth.css';

export default function Auth({ onLoginSuccess }) {
  const [isLogin, setIsLogin] = useState(true);
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [name, setName] = useState('');
  const [age, setAge] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      if (isLogin) {
        await handleLogin();
      } else {
        await handleSignup();
      }
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleLogin = async () => {
    if (!email || !password) {
      throw new Error('이메일과 비밀번호를 입력해주세요.');
    }

    const response = await client.post('/api/auth/login', {
      email,
      password,
    });

    const { access_token, user } = response.data;
    localStorage.setItem('token', access_token);
    localStorage.setItem('user', JSON.stringify(user));
    onLoginSuccess(user);
  };

  const handleSignup = async () => {
    if (!email || !password || !confirmPassword || !name || !age) {
      throw new Error('모든 필드를 입력해주세요.');
    }

    if (password !== confirmPassword) {
      throw new Error('비밀번호가 일치하지 않습니다.');
    }

    if (password.length < 6) {
      throw new Error('비밀번호는 최소 6자 이상이어야 합니다.');
    }

    const response = await client.post('/api/auth/register', {
      email,
      password,
      name,
      age: parseInt(age),
    });

    const { access_token, user } = response.data;
    localStorage.setItem('token', access_token);
    localStorage.setItem('user', JSON.stringify(user));
    onLoginSuccess(user);
  };

  return (
    <div className="auth-container">
      <div className="auth-card">
        <div className="auth-header">
          <h1>🎯 청년워크핏</h1>
          <p>청년 취업 정책 종합 플랫폼</p>
        </div>

        <div className="auth-tabs">
          <button
            className={`tab ${isLogin ? 'active' : ''}`}
            onClick={() => setIsLogin(true)}
          >
            로그인
          </button>
          <button
            className={`tab ${!isLogin ? 'active' : ''}`}
            onClick={() => setIsLogin(false)}
          >
            회원가입
          </button>
        </div>

        <form onSubmit={handleSubmit} className="auth-form">
          {error && <div className="error-message">{error}</div>}

          {/* 회원가입 전용 필드 */}
          {!isLogin && (
            <>
              <div className="form-group">
                <label htmlFor="name">이름</label>
                <input
                  id="name"
                  type="text"
                  placeholder="홍길동"
                  value={name}
                  onChange={(e) => setName(e.target.value)}
                  required
                />
              </div>

              <div className="form-group">
                <label htmlFor="age">나이</label>
                <input
                  id="age"
                  type="number"
                  placeholder="25"
                  value={age}
                  onChange={(e) => setAge(e.target.value)}
                  min="18"
                  max="39"
                  required
                />
              </div>
            </>
          )}

          {/* 로그인/회원가입 공통 필드 */}
          <div className="form-group">
            <label htmlFor="email">이메일</label>
            <input
              id="email"
              type="email"
              placeholder="user@example.com"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
          </div>

          <div className="form-group">
            <label htmlFor="password">비밀번호</label>
            <input
              id="password"
              type="password"
              placeholder="••••••"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>

          {/* 회원가입 비밀번호 확인 */}
          {!isLogin && (
            <div className="form-group">
              <label htmlFor="confirmPassword">비밀번호 확인</label>
              <input
                id="confirmPassword"
                type="password"
                placeholder="••••••"
                value={confirmPassword}
                onChange={(e) => setConfirmPassword(e.target.value)}
                required
              />
            </div>
          )}

          <button type="submit" className="submit-btn" disabled={loading}>
            {loading ? '처리 중...' : isLogin ? '로그인' : '회원가입'}
          </button>
        </form>

        {isLogin && (
          <p className="demo-info">
            💡 테스트: 이메일: test@test.com / 비밀번호: password
          </p>
        )}
      </div>

      <div className="auth-footer">
        <p>© 2026 청년워크핏 - 청년 취업 정보 플랫폼</p>
      </div>
    </div>
  );
}
