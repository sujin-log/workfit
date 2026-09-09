import { useState, useEffect } from 'react';
import axios from 'axios';
import './Policy.css';
import PolicyCard from '../Home/PolicyCard';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export default function Policy() {
  const [policies, setPolicies] = useState([]);
  const [filteredPolicies, setFilteredPolicies] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const [filters, setFilters] = useState({
    region: '',
    age: '',
    category: '',
    sort: 'latest'
  });

  const regions = ['서울', '경기', '인천', '대전', '대구', '부산', '광주', '울산', '세종', '강원', '충청북도', '충청남도', '전라북도', '전라남도', '경상북도', '경상남도', '제주'];
  const categories = ['취업', '교육', '금융', '주택', '의료', '생활'];
  const ageGroups = ['20-25', '25-30', '30-35', '전체'];

  useEffect(() => {
    fetchPolicies();
  }, []);

  const fetchPolicies = async () => {
    try {
      setLoading(true);
      const token = localStorage.getItem('token');
      const response = await axios.get(`${API_URL}/api/policy/search`, {
        params: {
          region: filters.region || undefined,
          age: filters.age || undefined,
          category: filters.category || undefined,
          sort: filters.sort
        },
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });

      setPolicies(response.data.policies || response.data);
      setFilteredPolicies(response.data.policies || response.data);
    } catch (err) {
      console.error('정책 조회 실패:', err);
      setError('정책을 불러올 수 없습니다.');
      // 더미 데이터로 기본값 설정
      const dummyPolicies = [
        {
          id: 1,
          title: '청년창업지원금 2026',
          region: '서울',
          category: '취업',
          deadline: '2026-12-31',
          eligibility_age: '25-39',
          description: '청년 창업자를 위한 지원금 프로그램입니다.',
          support_amount: '최대 5000만원'
        },
        {
          id: 2,
          title: '청년주택특공',
          region: '경기',
          category: '주택',
          deadline: '2026-11-30',
          eligibility_age: '20-34',
          description: '청년을 위한 주택 특공 프로그램입니다.',
          support_amount: '최대 2억원'
        }
      ];
      setPolicies(dummyPolicies);
      setFilteredPolicies(dummyPolicies);
    } finally {
      setLoading(false);
    }
  };

  const handleFilterChange = (field, value) => {
    const newFilters = { ...filters, [field]: value };
    setFilters(newFilters);
  };

  const applyFilters = () => {
    fetchPolicies();
  };

  const resetFilters = () => {
    setFilters({
      region: '',
      age: '',
      category: '',
      sort: 'latest'
    });
  };

  if (loading) {
    return <div className="policy-container"><p>로딩 중...</p></div>;
  }

  return (
    <div className="policy-container">
      <div className="policy-header">
        <h1>🔍 정책 검색</h1>
        <p>자신에게 맞는 정책을 찾아보세요</p>
      </div>

      <div className="policy-wrapper">
        <div className="policy-filter-section">
          <div className="filter-row">
            <div className="filter-group">
              <label>지역</label>
              <select
                value={filters.region}
                onChange={(e) => handleFilterChange('region', e.target.value)}
              >
                <option value="">전체</option>
                {regions.map(region => (
                  <option key={region} value={region}>{region}</option>
                ))}
              </select>
            </div>

            <div className="filter-group">
              <label>나이</label>
              <select
                value={filters.age}
                onChange={(e) => handleFilterChange('age', e.target.value)}
              >
                <option value="">전체</option>
                {ageGroups.map(age => (
                  <option key={age} value={age}>{age}</option>
                ))}
              </select>
            </div>

            <div className="filter-group">
              <label>카테고리</label>
              <select
                value={filters.category}
                onChange={(e) => handleFilterChange('category', e.target.value)}
              >
                <option value="">전체</option>
                {categories.map(cat => (
                  <option key={cat} value={cat}>{cat}</option>
                ))}
              </select>
            </div>

            <div className="filter-group">
              <label>정렬</label>
              <select
                value={filters.sort}
                onChange={(e) => handleFilterChange('sort', e.target.value)}
              >
                <option value="latest">최신순</option>
                <option value="deadline">마감임박순</option>
              </select>
            </div>

            <div className="filter-buttons">
              <button className="btn-apply" onClick={applyFilters}>검색</button>
              <button className="btn-reset" onClick={resetFilters}>초기화</button>
            </div>
          </div>
        </div>

        <div className="policy-results">
          {error && <div className="error-message">{error}</div>}

          <div className="policy-list">
            {filteredPolicies.length > 0 ? (
              filteredPolicies.map(policy => (
                <PolicyCard key={policy.id} policy={policy} />
              ))
            ) : (
              <p className="no-results">검색 결과가 없습니다.</p>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
