export default function PolicyCard({ policy }) {
  return (
    <div className="policy-card">
      <div className="policy-header">
        <span className="category-badge">{policy.category}</span>
        <span className="region-badge">{policy.region}</span>
      </div>
      <h3>{policy.title}</h3>
      <p className="policy-summary">{policy.summary}</p>
      <div className="policy-footer">
        <div className="age-range">
          👥 {policy.min_age}~{policy.max_age}세
        </div>
        <div className="deadline">
          📅 {new Date(policy.deadline).toLocaleDateString('ko-KR')}
        </div>
      </div>
      <button className="policy-btn">자세히 보기</button>
    </div>
  );
}
