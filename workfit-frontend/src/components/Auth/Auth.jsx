import { useState } from 'react';
import client from '../../api/client';
import './Auth.css';

export default function Auth({ onLoginSuccess }) {
  const [isLogin, setIsLogin] = useState(true);
  const [isForgotPassword, setIsForgotPassword] = useState(false);
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [name, setName] = useState('');
  const [birthYear, setBirthYear] = useState('');
  const [termsAgreed, setTermsAgreed] = useState(false);
  const [resetToken, setResetToken] = useState('');
  const [newPassword, setNewPassword] = useState('');
  const [confirmNewPassword, setConfirmNewPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [successMessage, setSuccessMessage] = useState('');

  const currentYear = new Date().getFullYear();
  const birthYears = Array.from({ length: 40 }, (_, i) => currentYear - 18 - i);

  const isPasswordValid = password && password.length >= 6;
  const isPasswordMatching = password === confirmPassword && isPasswordValid;

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setSuccessMessage('');
    setLoading(true);

    try {
      if (isForgotPassword) {
        if (resetToken) {
          await handleResetPassword();
        } else {
          await handleForgotPassword();
        }
      } else if (isLogin) {
        await handleLogin();
      } else {
        await handleSignup();
      }
    } catch (err) {
      const errorMessage = err.response?.data?.detail || err.message || '요청 처리 중 오류가 발생했습니다.';
      setError(errorMessage);
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

  const handleForgotPassword = async () => {
    if (!email) {
      throw new Error('이메일을 입력해주세요.');
    }

    const response = await client.post('/api/auth/forgot-password', {
      email,
    });

    // 토큰을 localStorage에만 저장 (화면에 노출 X)
    localStorage.setItem('resetToken', response.data.reset_token);
    setResetToken(response.data.reset_token);
    setSuccessMessage('비밀번호 재설정 링크가 이메일로 전송되었습니다. 아래에서 새 비밀번호를 설정하세요.');
    setEmail('');
  };

  const handleEmailKeyDown = async (e) => {
    if (e.key === 'Enter') {
      e.preventDefault();
      if (!email) {
        setError('이메일을 입력해주세요.');
        return;
      }
      try {
        setError('');
        setLoading(true);
        await handleForgotPassword();
      } catch (err) {
        const errorMessage = err.response?.data?.detail || err.message || '요청 처리 중 오류가 발생했습니다.';
        setError(errorMessage);
      } finally {
        setLoading(false);
      }
    }
  };

  const handleResetPassword = async () => {
    if (!resetToken || !newPassword || !confirmNewPassword) {
      throw new Error('모든 필드를 입력해주세요.');
    }

    if (newPassword !== confirmNewPassword) {
      throw new Error('비밀번호가 일치하지 않습니다.');
    }

    if (newPassword.length < 6) {
      throw new Error('비밀번호는 최소 6자 이상이어야 합니다.');
    }

    await client.post('/api/auth/reset-password', {
      reset_token: resetToken,
      new_password: newPassword,
    });

    setSuccessMessage('비밀번호가 성공적으로 변경되었습니다. 로그인 페이지로 이동합니다.');
    setTimeout(() => {
      setIsForgotPassword(false);
      setIsLogin(true);
      setResetToken('');
      setNewPassword('');
      setConfirmNewPassword('');
    }, 2000);
  };

  const handleSignup = async () => {
    if (!email || !password || !confirmPassword || !name || !birthYear) {
      throw new Error('모든 필드를 입력해주세요.');
    }

    if (!termsAgreed) {
      throw new Error('이용약관에 동의해주세요.');
    }

    if (password !== confirmPassword) {
      throw new Error('비밀번호가 일치하지 않습니다.');
    }

    if (password.length < 6) {
      throw new Error('비밀번호는 최소 6자 이상이어야 합니다.');
    }

    const age = currentYear - parseInt(birthYear);

    const response = await client.post('/api/auth/register', {
      email,
      password,
      name,
      age: age,
    });

    const { access_token, user } = response.data;
    localStorage.setItem('token', access_token);
    localStorage.setItem('user', JSON.stringify(user));
    onLoginSuccess(user);
  };

  if (isForgotPassword) {
    return (
      <div className="auth-container">
        <div className="login-card">
          <div className="login-brand">
            <div className="opportunity-icon">
              <svg viewBox="0 0 120 120" xmlns="http://www.w3.org/2000/svg">
                <g>
                  <path d="M 35 70 L 35 50 Q 35 40 45 40"
                        fill="none" stroke="white" strokeWidth="2.5" strokeLinecap="round"/>
                  <path d="M 45 40 L 50 20"
                        fill="none" stroke="white" strokeWidth="2.5" strokeLinecap="round"/>
                  <path d="M 45 40 L 55 18"
                        fill="none" stroke="white" strokeWidth="2.5" strokeLinecap="round"/>
                  <path d="M 45 40 L 65 15"
                        fill="none" stroke="white" strokeWidth="2.5" strokeLinecap="round"/>
                  <path d="M 45 40 L 75 20"
                        fill="none" stroke="white" strokeWidth="2.5" strokeLinecap="round"/>
                  <path d="M 45 40 L 80 35"
                        fill="none" stroke="white" strokeWidth="2.5" strokeLinecap="round"/>
                  <circle cx="45" cy="50" r="8" fill="white" opacity="0.3"/>
                </g>
                <g>
                  <path d="M 60 50 L 62 55 L 67 56 L 63 60 L 64 65 L 60 62 L 56 65 L 57 60 L 53 56 L 58 55 Z"
                        fill="white" opacity="0.9"/>
                  <path d="M 75 35 L 76 38 L 79 39 L 77 41 L 77 44 L 75 42 L 73 44 L 73 41 L 71 39 L 74 38 Z"
                        fill="white" opacity="0.7"/>
                  <path d="M 85 55 L 86 57 L 88 58 L 86 59 L 87 61 L 85 60 L 83 61 L 84 59 L 82 58 L 84 57 Z"
                        fill="white" opacity="0.5"/>
                </g>
                <path d="M 35 70 Q 50 65 60 50 Q 70 40 80 35"
                      fill="none" stroke="white" strokeWidth="1.5" strokeDasharray="4,4" opacity="0.5" strokeLinecap="round"/>
              </svg>
            </div>

            <div className="brand-content">
              <h2>비밀번호 재설정</h2>
              <p>새로운 비밀번호를 설정해주세요</p>
            </div>
          </div>

          <div className="login-form-area">
            <form onSubmit={handleSubmit} className="login-form">
              {error && <div className="error-message">{error}</div>}
              {successMessage && <div className="success-message">{successMessage}</div>}

              {!resetToken ? (
                <>
                  <div className="underline-form-group">
                    <label htmlFor="forgot-email">EMAIL</label>
                    <input
                      id="forgot-email"
                      type="email"
                      placeholder="이메일을 입력하세요"
                      value={email}
                      onChange={(e) => setEmail(e.target.value)}
                      onKeyDown={handleEmailKeyDown}
                      required
                    />
                  </div>

                  <button type="submit" className="login-btn" disabled={loading}>
                    {loading ? '처리 중...' : '재설정 링크 받기'}
                  </button>
                </>
              ) : (
                <>
                  <div className="underline-form-group">
                    <label htmlFor="new-password">NEW PASSWORD</label>
                    <input
                      id="new-password"
                      type="password"
                      placeholder="새 비밀번호 (6자 이상)"
                      value={newPassword}
                      onChange={(e) => setNewPassword(e.target.value)}
                      required
                    />
                  </div>

                  <div className="underline-form-group">
                    <label htmlFor="confirm-new-password">CONFIRM PASSWORD</label>
                    <input
                      id="confirm-new-password"
                      type="password"
                      placeholder="비밀번호 확인"
                      value={confirmNewPassword}
                      onChange={(e) => setConfirmNewPassword(e.target.value)}
                      required
                    />
                  </div>

                  <button type="submit" className="login-btn" disabled={loading}>
                    {loading ? '처리 중...' : '비밀번호 변경'}
                  </button>
                </>
              )}

              <p className="login-link">
                <button
                  type="button"
                  onClick={() => {
                    setIsForgotPassword(false);
                    setIsLogin(true);
                    setResetToken('');
                    setEmail('');
                    setNewPassword('');
                    setConfirmNewPassword('');
                    setError('');
                    setSuccessMessage('');
                  }}
                  className="login-text-btn"
                >
                  로그인 페이지로 돌아가기
                </button>
              </p>
            </form>
          </div>
        </div>

        <div className="auth-footer">
          <p>© 2026 청년워크핏 - 청년 취업 정보 플랫폼</p>
        </div>
      </div>
    );
  }

  if (isLogin) {
    return (
      <div className="auth-container">
        <div className="login-card">
          {/* 좌측: 브랜드 영역 */}
          <div className="login-brand">
            <div className="brand-circle circle-1"></div>
            <div className="brand-circle circle-2"></div>
            <div className="brand-circle circle-3"></div>

            <div className="opportunity-icon">
              <svg viewBox="0 0 120 120" xmlns="http://www.w3.org/2000/svg">
                {/* 손 */}
                <g>
                  {/* 팔 */}
                  <path d="M 35 70 L 35 50 Q 35 40 45 40"
                        fill="none" stroke="white" strokeWidth="2.5" strokeLinecap="round"/>
                  {/* 손가락 1 */}
                  <path d="M 45 40 L 50 20"
                        fill="none" stroke="white" strokeWidth="2.5" strokeLinecap="round"/>
                  {/* 손가락 2 */}
                  <path d="M 45 40 L 55 18"
                        fill="none" stroke="white" strokeWidth="2.5" strokeLinecap="round"/>
                  {/* 손가락 3 */}
                  <path d="M 45 40 L 65 15"
                        fill="none" stroke="white" strokeWidth="2.5" strokeLinecap="round"/>
                  {/* 손가락 4 */}
                  <path d="M 45 40 L 75 20"
                        fill="none" stroke="white" strokeWidth="2.5" strokeLinecap="round"/>
                  {/* 손가락 5 */}
                  <path d="M 45 40 L 80 35"
                        fill="none" stroke="white" strokeWidth="2.5" strokeLinecap="round"/>
                  {/* 손바닥 */}
                  <circle cx="45" cy="50" r="8" fill="white" opacity="0.3"/>
                </g>

                {/* 위로 올라가는 별 */}
                <g>
                  {/* 별 1 */}
                  <path d="M 60 50 L 62 55 L 67 56 L 63 60 L 64 65 L 60 62 L 56 65 L 57 60 L 53 56 L 58 55 Z"
                        fill="white" opacity="0.9"/>
                  {/* 별 2 */}
                  <path d="M 75 35 L 76 38 L 79 39 L 77 41 L 77 44 L 75 42 L 73 44 L 73 41 L 71 39 L 74 38 Z"
                        fill="white" opacity="0.7"/>
                  {/* 별 3 */}
                  <path d="M 85 55 L 86 57 L 88 58 L 86 59 L 87 61 L 85 60 L 83 61 L 84 59 L 82 58 L 84 57 Z"
                        fill="white" opacity="0.5"/>
                </g>

                {/* 경로 선 */}
                <path d="M 35 70 Q 50 65 60 50 Q 70 40 80 35"
                      fill="none" stroke="white" strokeWidth="1.5" strokeDasharray="4,4" opacity="0.5" strokeLinecap="round"/>
              </svg>
            </div>

            <div className="brand-content">
              <h2>나에게 꼭 맞는 시작</h2>
              <p>워크핏이 당신에게 맞는 기회를 찾아드립니다</p>
            </div>

          </div>

          {/* 우측: 로그인 폼 영역 */}
          <div className="login-form-area">
            {/* 탭 */}
            <div className="login-tabs">
              <button className="login-tab active">로그인</button>
              <button
                className="login-tab"
                onClick={() => setIsLogin(false)}
              >
                회원가입
              </button>
            </div>

            <form onSubmit={handleSubmit} className="login-form">
              {error && <div className="error-message">{error}</div>}

              <div className="underline-form-group">
                <label htmlFor="login-email">EMAIL</label>
                <input
                  id="login-email"
                  type="email"
                  placeholder="이메일을 입력하세요"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  required
                />
              </div>

              <div className="underline-form-group">
                <label htmlFor="login-password">PASSWORD</label>
                <input
                  id="login-password"
                  type="password"
                  placeholder="비밀번호를 입력하세요"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  required
                />
              </div>

              <div className="login-links">
                <button
                  type="button"
                  onClick={() => {
                    setIsForgotPassword(true);
                    setEmail('');
                    setPassword('');
                    setError('');
                  }}
                  className="forgot-link"
                >
                  비밀번호 찾기
                </button>
                <button
                  type="button"
                  onClick={() => setIsLogin(false)}
                  className="signup-link"
                >
                  회원가입
                </button>
              </div>

              <button type="submit" className="login-btn" disabled={loading}>
                {loading ? '처리 중...' : '로그인'}
              </button>
            </form>

          </div>
        </div>

        <div className="auth-footer">
          <p>© 2026 청년워크핏 - 청년 취업 정보 플랫폼</p>
        </div>
      </div>
    );
  }

  if (!isLogin) {
    return (
      <div className="auth-container">
        <div className="signup-card">
          <button
            className="close-btn"
            onClick={() => setIsLogin(true)}
            aria-label="Close"
          >
            ✕
          </button>

          <div className="signup-wrapper">
            {/* 좌측: 브랜드 영역 */}
            <div className="signup-brand">
              <div className="brand-circle circle-1"></div>
              <div className="brand-circle circle-2"></div>
              <div className="brand-circle circle-3"></div>

              <div className="brand-content">
                <h2>회원가입</h2>
                <p>청년워크핏의 모든 기능을 이용해보세요</p>
              </div>

              <div className="brand-icon">
                <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <circle cx="12" cy="12" r="10" stroke="white" strokeWidth="2"/>
                  <path d="M8 12.5L11 15.5L16 9" stroke="white" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                </svg>
              </div>
            </div>

            {/* 우측: 폼 영역 */}
            <div className="signup-form-area">
              <form onSubmit={handleSubmit} className="signup-form">
                {error && <div className="error-message">{error}</div>}

                {/* 이름 */}
                <div className="underline-form-group">
                  <label htmlFor="signup-name">NAME</label>
                  <input
                    id="signup-name"
                    type="text"
                    placeholder="이름을 입력하세요"
                    value={name}
                    onChange={(e) => setName(e.target.value)}
                    required
                  />
                </div>

                {/* 출생연도 */}
                <div className="underline-form-group">
                  <label htmlFor="signup-birth">BIRTH YEAR</label>
                  <select
                    id="signup-birth"
                    value={birthYear}
                    onChange={(e) => setBirthYear(e.target.value)}
                    required
                  >
                    <option value="">출생연도를 선택해주세요</option>
                    {birthYears.map((year) => (
                      <option key={year} value={year}>
                        {year}년생
                      </option>
                    ))}
                  </select>
                </div>

                {/* 이메일 */}
                <div className="underline-form-group">
                  <label htmlFor="signup-email">EMAIL</label>
                  <input
                    id="signup-email"
                    type="email"
                    placeholder="이메일을 입력하세요"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    required
                  />
                </div>

                {/* 비밀번호 */}
                <div className="underline-form-group">
                  <label htmlFor="signup-password">PASSWORD</label>
                  <div className="password-input-wrapper">
                    <input
                      id="signup-password"
                      type="password"
                      placeholder="비밀번호 (6자 이상)"
                      value={password}
                      onChange={(e) => setPassword(e.target.value)}
                      required
                    />
                    {isPasswordValid && <span className="check-icon">✓</span>}
                  </div>
                </div>

                {/* 비밀번호 확인 */}
                <div className="underline-form-group">
                  <label htmlFor="signup-confirm">PASSWORD CONFIRM</label>
                  <div className="password-input-wrapper">
                    <input
                      id="signup-confirm"
                      type="password"
                      placeholder="비밀번호 확인"
                      value={confirmPassword}
                      onChange={(e) => setConfirmPassword(e.target.value)}
                      required
                    />
                    {confirmPassword && isPasswordMatching && <span className="check-icon">✓</span>}
                  </div>
                </div>

                {/* 약관 동의 */}
                <div className="terms-checkbox">
                  <input
                    id="terms"
                    type="checkbox"
                    checked={termsAgreed}
                    onChange={(e) => setTermsAgreed(e.target.checked)}
                  />
                  <label htmlFor="terms">
                    가입 시 <a href="#terms" className="terms-link">이용약관</a>에 동의합니다
                  </label>
                </div>

                {/* 회원가입 버튼 */}
                <button type="submit" className="signup-btn" disabled={loading}>
                  {loading ? '처리 중...' : '회원가입'}
                </button>

                {/* 로그인 링크 */}
                <p className="login-link">
                  또는 <button
                    type="button"
                    onClick={() => setIsLogin(true)}
                    className="login-text-btn"
                  >
                    로그인
                  </button>
                </p>
              </form>
            </div>
          </div>
        </div>

        <div className="auth-footer">
          <p>© 2026 청년워크핏 - 청년 취업 정보 플랫폼</p>
        </div>
      </div>
    );
  }

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

          <div className="form-group">
            <label htmlFor="login-email">이메일</label>
            <input
              id="login-email"
              type="email"
              placeholder="user@example.com"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
          </div>

          <div className="form-group">
            <label htmlFor="login-password">비밀번호</label>
            <input
              id="login-password"
              type="password"
              placeholder="••••••"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>

          <button type="submit" className="submit-btn" disabled={loading}>
            {loading ? '처리 중...' : '로그인'}
          </button>
        </form>

        <p className="demo-info">
          💡 테스트: 이메일: test@test.com / 비밀번호: password
        </p>
      </div>

      <div className="auth-footer">
        <p>© 2026 청년워크핏 - 청년 취업 정보 플랫폼</p>
      </div>
    </div>
  );
}
