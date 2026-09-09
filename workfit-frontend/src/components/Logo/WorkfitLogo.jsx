export default function WorkfitLogo({ size = 32 }) {
  return (
    <svg
      width={size}
      height={size}
      viewBox="0 0 100 100"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
    >
      {/* 상승하는 라인들 */}
      <line x1="30" y1="70" x2="40" y2="50" stroke="#ffd700" strokeWidth="3" strokeLinecap="round" />
      <line x1="50" y1="70" x2="50" y2="40" stroke="#ffed4e" strokeWidth="3" strokeLinecap="round" />
      <line x1="70" y1="70" x2="60" y2="50" stroke="#ffd700" strokeWidth="3" strokeLinecap="round" />

      {/* 연결선 (Y 모양) */}
      <path
        d="M 40 50 L 50 40 L 60 50"
        stroke="#ffed4e"
        strokeWidth="3"
        strokeLinecap="round"
        strokeLinejoin="round"
        fill="none"
      />

      {/* 꼭대기 별 */}
      <circle cx="50" cy="30" r="4" fill="#ffd700" />
      <circle cx="50" cy="30" r="2" fill="white" opacity="0.5" />

      {/* 효과: 주변 작은 별들 */}
      <circle cx="38" cy="35" r="2" fill="#ffd700" opacity="0.9" />
      <circle cx="62" cy="35" r="2" fill="#ffed4e" opacity="0.9" />
    </svg>
  );
}
