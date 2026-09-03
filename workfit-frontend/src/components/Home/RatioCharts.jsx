import {
  PieChart,
  Pie,
  Cell,
  Legend,
  Tooltip,
  ResponsiveContainer,
} from 'recharts';

const CATEGORY_COLORS = ['#3b82f6', '#10b981', '#f59e0b', '#ef4444'];
const SENTIMENT_COLORS = {
  긍정: '#10b981',
  중립: '#6b7280',
  부정: '#ef4444',
};

export default function RatioCharts({ categoryRatio, sentimentRatio }) {
  return (
    <div className="ratio-charts-grid">
      <div className="chart-wrapper">
        <h3>📊 카테고리별 정책</h3>
        <ResponsiveContainer width="100%" height={250}>
          <PieChart>
            <Pie
              data={categoryRatio}
              cx="50%"
              cy="50%"
              labelLine={false}
              label={({ category, percent }) => `${category} ${percent}%`}
              outerRadius={80}
              fill="#8884d8"
              dataKey="percent"
            >
              {categoryRatio.map((entry, index) => (
                <Cell key={`cell-${index}`} fill={CATEGORY_COLORS[index % CATEGORY_COLORS.length]} />
              ))}
            </Pie>
            <Tooltip formatter={(value) => `${value}%`} />
          </PieChart>
        </ResponsiveContainer>
      </div>

      <div className="chart-wrapper">
        <h3>💭 뉴스 감정 분석</h3>
        <ResponsiveContainer width="100%" height={250}>
          <PieChart>
            <Pie
              data={sentimentRatio}
              cx="50%"
              cy="50%"
              labelLine={false}
              label={({ sentiment, percent }) => `${sentiment} ${percent}%`}
              outerRadius={80}
              fill="#8884d8"
              dataKey="percent"
            >
              {sentimentRatio.map((entry) => (
                <Cell key={`cell-${entry.sentiment}`} fill={SENTIMENT_COLORS[entry.sentiment]} />
              ))}
            </Pie>
            <Tooltip formatter={(value) => `${value}%`} />
          </PieChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
