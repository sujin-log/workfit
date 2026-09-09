import { useState, useEffect } from 'react';
import axios from 'axios';
import './Community.css';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export default function Community() {
  const [posts, setPosts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [showModal, setShowModal] = useState(false);
  const [selectedPost, setSelectedPost] = useState(null);
  const [newPost, setNewPost] = useState({ title: '', content: '' });
  const [sortBy, setSortBy] = useState('latest');

  useEffect(() => {
    fetchPosts();
  }, [sortBy]);

  const fetchPosts = async () => {
    try {
      setLoading(true);
      const token = localStorage.getItem('token');
      const response = await axios.get(`${API_URL}/api/community/posts`, {
        params: { sort: sortBy },
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });

      setPosts(response.data.posts || response.data);
    } catch (err) {
      console.error('게시글 조회 실패:', err);
      // 더미 데이터
      const dummyPosts = [
        {
          id: 1,
          title: '청년정책 정보 공유합니다',
          content: '최근에 알게 된 유용한 정책들을 공유합니다. 많은 도움이 되길 바랍니다.',
          author: 'user1',
          created_at: '2026-09-10T10:30:00',
          likes: 15,
          comments: 3,
          liked: false
        },
        {
          id: 2,
          title: '주택청약 당첨되었어요!',
          content: '오랜 기다림 끝에 주택청약에 당첨되었습니다! 같은 처지의 분들 화이팅!',
          author: 'user2',
          created_at: '2026-09-09T15:20:00',
          likes: 42,
          comments: 8,
          liked: false
        }
      ];
      setPosts(dummyPosts);
    } finally {
      setLoading(false);
    }
  };

  const handleCreatePost = async () => {
    if (!newPost.title.trim() || !newPost.content.trim()) {
      alert('제목과 내용을 입력해주세요');
      return;
    }

    try {
      const token = localStorage.getItem('token');
      const response = await axios.post(
        `${API_URL}/api/community/posts`,
        newPost,
        {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        }
      );

      setPosts([response.data, ...posts]);
      setNewPost({ title: '', content: '' });
      setShowModal(false);
    } catch (err) {
      console.error('게시글 작성 실패:', err);
      alert('게시글 작성에 실패했습니다.');
    }
  };

  const handleDeletePost = async (postId) => {
    if (!window.confirm('게시글을 삭제하시겠습니까?')) return;

    try {
      const token = localStorage.getItem('token');
      await axios.delete(`${API_URL}/api/community/posts/${postId}`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });

      setPosts(posts.filter(p => p.id !== postId));
    } catch (err) {
      console.error('게시글 삭제 실패:', err);
      alert('게시글 삭제에 실패했습니다.');
    }
  };

  const handleLike = async (postId) => {
    try {
      const token = localStorage.getItem('token');
      await axios.post(`${API_URL}/api/community/posts/${postId}/like`, {}, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });

      setPosts(posts.map(p =>
        p.id === postId
          ? { ...p, liked: !p.liked, likes: p.liked ? p.likes - 1 : p.likes + 1 }
          : p
      ));
    } catch (err) {
      console.error('좋아요 실패:', err);
    }
  };

  if (loading) {
    return <div className="community-container"><p>로딩 중...</p></div>;
  }

  return (
    <div className="community-container">
      <div className="community-header">
        <h1>👥 커뮤니티</h1>
        <p>청년들과 정책 경험을 나누어보세요</p>
      </div>

      <div className="community-controls">
        <select value={sortBy} onChange={(e) => setSortBy(e.target.value)} className="sort-select">
          <option value="latest">최신순</option>
          <option value="popular">인기순</option>
        </select>
        <button className="btn-create" onClick={() => setShowModal(true)}>
          ✍️ 글쓰기
        </button>
      </div>

      {showModal && (
        <div className="modal-overlay" onClick={() => setShowModal(false)}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()}>
            <div className="modal-header">
              <h2>게시글 작성</h2>
              <button className="btn-close" onClick={() => setShowModal(false)}>✕</button>
            </div>
            <input
              type="text"
              placeholder="제목을 입력하세요"
              value={newPost.title}
              onChange={(e) => setNewPost({ ...newPost, title: e.target.value })}
              className="modal-input"
              maxLength="100"
            />
            <textarea
              placeholder="내용을 입력하세요"
              value={newPost.content}
              onChange={(e) => setNewPost({ ...newPost, content: e.target.value })}
              className="modal-textarea"
              rows="8"
            />
            <div className="modal-actions">
              <button className="btn-cancel" onClick={() => setShowModal(false)}>취소</button>
              <button className="btn-submit" onClick={handleCreatePost}>작성</button>
            </div>
          </div>
        </div>
      )}

      <div className="posts-list">
        {posts.length > 0 ? (
          posts.map(post => (
            <div key={post.id} className="post-card">
              <div className="post-header">
                <h3>{post.title}</h3>
                <span className="post-author">by {post.author}</span>
              </div>
              <p className="post-content">{post.content}</p>
              <div className="post-footer">
                <span className="post-date">
                  {new Date(post.created_at).toLocaleDateString('ko-KR')}
                </span>
                <div className="post-actions">
                  <button
                    className={`btn-like ${post.liked ? 'liked' : ''}`}
                    onClick={() => handleLike(post.id)}
                  >
                    ❤️ {post.likes}
                  </button>
                  <span className="comments-count">
                    💬 {post.comments || 0}
                  </span>
                  <button
                    className="btn-delete"
                    onClick={() => handleDeletePost(post.id)}
                  >
                    🗑️
                  </button>
                </div>
              </div>
            </div>
          ))
        ) : (
          <p className="no-posts">아직 게시글이 없습니다. 첫 번째로 작성해보세요!</p>
        )}
      </div>
    </div>
  );
}
