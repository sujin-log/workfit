import { useState, useEffect } from 'react';
import axios from 'axios';
import './MyPage.css';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export default function MyPage() {
  const [user, setUser] = useState(null);
  const [activeTab, setActiveTab] = useState('bookmarks');
  const [bookmarks, setBookmarks] = useState([]);
  const [chatHistory, setChatHistory] = useState([]);
  const [myPosts, setMyPosts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [isEditMode, setIsEditMode] = useState(false);
  const [editName, setEditName] = useState('');
  const [editAge, setEditAge] = useState('');
  const [isSaving, setIsSaving] = useState(false);

  useEffect(() => {
    const token = localStorage.getItem('token');
    if (!token) {
      // 로그인 페이지로 리다이렉트
      window.location.href = '/';
      return;
    }
    fetchUserData();
  }, []);

  useEffect(() => {
    if (activeTab === 'bookmarks') {
      fetchBookmarks();
    } else if (activeTab === 'chat') {
      fetchChatHistory();
    } else if (activeTab === 'posts') {
      fetchMyPosts();
    }
  }, [activeTab]);

  const fetchUserData = async () => {
    try {
      const token = localStorage.getItem('token');
      const response = await axios.get(`${API_URL}/api/auth/me`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      setUser(response.data);
      setEditName(response.data.name);
      setEditAge(response.data.age);
    } catch (err) {
      console.error('사용자 정보 조회 실패:', err);
      setError('사용자 정보를 불러올 수 없습니다.');
      // 더미 유저
      const dummyUser = {
        id: 1,
        email: 'user@example.com',
        name: '테스트유저',
        age: 25
      };
      setUser(dummyUser);
      setEditName(dummyUser.name);
      setEditAge(dummyUser.age);
    } finally {
      setLoading(false);
    }
  };

  const fetchBookmarks = async () => {
    try {
      const token = localStorage.getItem('token');
      const response = await axios.get(`${API_URL}/api/mypage/bookmarks`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      setBookmarks(response.data.bookmarks || response.data);
    } catch (err) {
      console.error('북마크 조회 실패:', err);
      // 더미 데이터
      setBookmarks([
        {
          id: 1,
          title: '청년창업지원금 2026',
          category: '취업',
          region: '서울'
        }
      ]);
    }
  };

  const fetchChatHistory = async () => {
    try {
      const token = localStorage.getItem('token');
      const response = await axios.get(`${API_URL}/api/mypage/chat-history`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      setChatHistory(response.data.history || response.data);
    } catch (err) {
      console.error('채팅 이력 조회 실패:', err);
      setChatHistory([]);
    }
  };

  const fetchMyPosts = async () => {
    try {
      const token = localStorage.getItem('token');
      const response = await axios.get(`${API_URL}/api/mypage/posts`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      setMyPosts(response.data.posts || response.data);
    } catch (err) {
      console.error('내 게시글 조회 실패:', err);
      setMyPosts([]);
    }
  };

  const handleLogout = () => {
    localStorage.removeItem('token');
    window.location.href = '/';
  };

  const handleEditClick = () => {
    setIsEditMode(true);
  };

  const handleCancelEdit = () => {
    setIsEditMode(false);
    setEditName(user.name);
    setEditAge(user.age);
  };

  const handleSaveProfile = async () => {
    if (!editName.trim()) {
      setError('이름을 입력해주세요.');
      return;
    }
    if (editAge < 18 || editAge > 100) {
      setError('나이는 18세 이상 100세 이하여야 합니다.');
      return;
    }

    try {
      setError('');
      setIsSaving(true);
      const token = localStorage.getItem('token');
      const response = await axios.put(`${API_URL}/api/auth/me`,
        {
          name: editName,
          age: parseInt(editAge)
        },
        {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        }
      );

      setUser(response.data.user);
      setIsEditMode(false);
      setError('');
    } catch (err) {
      const errorMessage = err.response?.data?.detail || err.message || '프로필 업데이트 실패';
      setError(errorMessage);
    } finally {
      setIsSaving(false);
    }
  };

  const removeBookmark = async (bookmarkId) => {
    try {
      const token = localStorage.getItem('token');
      await axios.delete(`${API_URL}/api/policy/${bookmarkId}/bookmark`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      setBookmarks(bookmarks.filter(b => b.id !== bookmarkId));
    } catch (err) {
      console.error('북마크 삭제 실패:', err);
    }
  };

  const deletePost = async (postId) => {
    if (!window.confirm('게시글을 삭제하시겠습니까?')) return;

    try {
      const token = localStorage.getItem('token');
      await axios.delete(`${API_URL}/api/community/posts/${postId}`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      setMyPosts(myPosts.filter(p => p.id !== postId));
    } catch (err) {
      console.error('게시글 삭제 실패:', err);
    }
  };

  if (loading) {
    return <div className="mypage-container"><p>로딩 중...</p></div>;
  }

  return (
    <div className="mypage-container">
      <div className="mypage-header">
        <div className="profile-section">
          <div className="profile-avatar">👤</div>
          {isEditMode ? (
            <div className="profile-edit">
              <div className="edit-form-group">
                <label>이름</label>
                <input
                  type="text"
                  value={editName}
                  onChange={(e) => setEditName(e.target.value)}
                  placeholder="이름 입력"
                />
              </div>
              <div className="edit-form-group">
                <label>나이</label>
                <input
                  type="number"
                  value={editAge}
                  onChange={(e) => setEditAge(e.target.value)}
                  placeholder="나이 입력"
                  min="18"
                  max="100"
                />
              </div>
              <div className="edit-buttons">
                <button
                  className="btn-save"
                  onClick={handleSaveProfile}
                  disabled={isSaving}
                >
                  {isSaving ? '저장 중...' : '저장'}
                </button>
                <button
                  className="btn-cancel"
                  onClick={handleCancelEdit}
                  disabled={isSaving}
                >
                  취소
                </button>
              </div>
            </div>
          ) : (
            <div className="profile-info">
              <h1>{user?.name || '사용자'}</h1>
              <p>{user?.email}</p>
              <p className="profile-age">만 {user?.age || '?'}세</p>
            </div>
          )}
        </div>
        <div className="header-buttons">
          {!isEditMode && (
            <button className="btn-edit" onClick={handleEditClick}>✏️ 프로필 편집</button>
          )}
          <button className="btn-logout" onClick={handleLogout}>로그아웃</button>
        </div>
      </div>

      <div className="mypage-tabs">
        <button
          className={`tab-btn ${activeTab === 'bookmarks' ? 'active' : ''}`}
          onClick={() => setActiveTab('bookmarks')}
        >
          🔖 북마크 ({bookmarks.length})
        </button>
        <button
          className={`tab-btn ${activeTab === 'chat' ? 'active' : ''}`}
          onClick={() => setActiveTab('chat')}
        >
          💬 채팅 이력 ({chatHistory.length})
        </button>
        <button
          className={`tab-btn ${activeTab === 'posts' ? 'active' : ''}`}
          onClick={() => setActiveTab('posts')}
        >
          📝 내 게시글 ({myPosts.length})
        </button>
      </div>

      <div className="mypage-content">
        {error && <div className="error-message">{error}</div>}

        {activeTab === 'bookmarks' && (
          <div className="tab-content">
            <h2>저장된 정책</h2>
            {bookmarks.length > 0 ? (
              <div className="items-list">
                {bookmarks.map(bookmark => (
                  <div key={bookmark.id} className="bookmark-item">
                    <div className="item-info">
                      <h3>{bookmark.title}</h3>
                      <div className="item-tags">
                        <span className="tag category">{bookmark.category}</span>
                        <span className="tag region">{bookmark.region}</span>
                      </div>
                    </div>
                    <button
                      className="btn-delete"
                      onClick={() => removeBookmark(bookmark.id)}
                    >
                      🗑️
                    </button>
                  </div>
                ))}
              </div>
            ) : (
              <p className="empty-message">저장된 정책이 없습니다.</p>
            )}
          </div>
        )}

        {activeTab === 'chat' && (
          <div className="tab-content">
            <h2>채팅 이력</h2>
            {chatHistory.length > 0 ? (
              <div className="items-list">
                {chatHistory.map((chat, idx) => (
                  <div key={idx} className="chat-history-item">
                    <div className="chat-header-info">
                      <h4>{chat.title || `대화 ${idx + 1}`}</h4>
                      <span className="chat-date">
                        {new Date(chat.created_at).toLocaleDateString('ko-KR')}
                      </span>
                    </div>
                    <p className="chat-preview">
                      {chat.messages?.[0]?.content?.substring(0, 100) || '내용 없음'}...
                    </p>
                  </div>
                ))}
              </div>
            ) : (
              <p className="empty-message">채팅 이력이 없습니다.</p>
            )}
          </div>
        )}

        {activeTab === 'posts' && (
          <div className="tab-content">
            <h2>내 게시글</h2>
            {myPosts.length > 0 ? (
              <div className="items-list">
                {myPosts.map(post => (
                  <div key={post.id} className="post-item">
                    <div className="post-info">
                      <h3>{post.title}</h3>
                      <p className="post-content">{post.content}</p>
                      <div className="post-meta">
                        <span className="post-date">
                          {new Date(post.created_at).toLocaleDateString('ko-KR')}
                        </span>
                        <span className="post-stats">
                          ❤️ {post.likes || 0} • 💬 {post.comments || 0}
                        </span>
                      </div>
                    </div>
                    <button
                      className="btn-delete"
                      onClick={() => deletePost(post.id)}
                    >
                      🗑️
                    </button>
                  </div>
                ))}
              </div>
            ) : (
              <p className="empty-message">작성한 게시글이 없습니다.</p>
            )}
          </div>
        )}
      </div>
    </div>
  );
}
