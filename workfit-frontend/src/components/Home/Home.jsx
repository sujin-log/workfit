import { useEffect, useState } from 'react';
import client from '../../api/client';
import NewsTrendChart from './NewsTrendChart';
import RatioCharts from './RatioCharts';
import PolicyCard from './PolicyCard';
import HotPost from './HotPost';
import './Home.css';

export default function Home({ user, onLogout }) {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const fetchDashboardData = async () => {
    try {
      setLoading(true);
      const response = await client.get('/api/home/summary');
      setData(response.data);
      setError(null);
    } catch (err) {
      setError('대시보드 데이터를 불러올 수 없습니다.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <div className="home-container"><div className="loading">로딩 중...</div></div>;
  }

  if (error) {
    return <div className="home-container"><div className="error">{error}</div></div>;
  }

  if (!data) {
    return <div className="home-container"><div className="error">데이터가 없습니다.</div></div>;
  }

  return (
    <div className="home-container">
      <div className="home-navbar">
        <div className="navbar-left">
          <h2>🎯 청년워크핏</h2>
        </div>
        <div className="navbar-right">
          <span className="user-name">👤 {user?.name}님</span>
          <button className="logout-btn" onClick={onLogout}>로그아웃</button>
        </div>
      </div>

      <div className="home-content-wrapper">
        <div className="home-header">
          <h1>청년워크핏 대시보드</h1>
          <p>취업, 창업, 정책 정보를 한눈에</p>
        </div>

        <div className="home-grid">
        {/* 뉴스 트렌드 섹션 */}
        <div className="section news-section">
          <div className="section-header">
            <h2>📈 뉴스 트렌드</h2>
            <span className="keyword-badge">{data.news_trend.keyword}</span>
          </div>
          <NewsTrendChart data={data.news_trend.time_line} />
        </div>

        {/* 비율 섹션 */}
        <div className="section ratio-section">
          <RatioCharts
            categoryRatio={data.category_ratio}
            sentimentRatio={data.sentiment_ratio}
          />
        </div>
      </div>

      {/* 추천 정책 섹션 */}
      <div className="section policies-section">
        <div className="section-header">
          <h2>💼 추천 정책</h2>
        </div>
        <div className="policies-grid">
          {data.recommended_policies.map((policy) => (
            <PolicyCard key={policy.id} policy={policy} />
          ))}
        </div>
      </div>

        {/* 인기 게시물 섹션 */}
        <div className="section hot-posts-section">
          <div className="section-header">
            <h2>🔥 핫한 게시물</h2>
          </div>
          <div className="hot-posts-list">
            {data.hot_posts.map((post, idx) => (
              <HotPost key={post.id} post={post} rank={idx + 1} />
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
