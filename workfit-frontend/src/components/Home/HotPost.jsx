export default function HotPost({ post, rank }) {
  const rankColors = ['#fbbf24', '#c4b5fd', '#93c5fd'];
  const rankIcons = ['🥇', '🥈', '🥉'];

  return (
    <div className="hot-post-item" style={{ borderLeftColor: rankColors[rank - 1] }}>
      <div className="post-rank">{rankIcons[rank - 1]}</div>
      <div className="post-content">
        <h4>{post.title}</h4>
        <p>ID: {post.id}</p>
      </div>
      <button className="post-btn">보기</button>
    </div>
  );
}
