import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from 'recharts';

export default function NewsTrendChart({ data }) {
  const formattedData = data.map((item) => ({
    ...item,
    date: item.label.slice(-2), // "20260901" -> "01"
  }));

  return (
    <ResponsiveContainer width="100%" height={300}>
      <LineChart data={formattedData} margin={{ top: 5, right: 30, left: 0, bottom: 5 }}>
        <CartesianGrid strokeDasharray="3 3" stroke="#e0e0e0" />
        <XAxis dataKey="date" stroke="#666" />
        <YAxis stroke="#666" />
        <Tooltip
          contentStyle={{
            backgroundColor: '#fff',
            border: '1px solid #ccc',
            borderRadius: '4px',
          }}
          formatter={(value) => [`${value} 검색`, 'hits']}
        />
        <Line
          type="monotone"
          dataKey="hits"
          stroke="#3b82f6"
          dot={{ fill: '#3b82f6', r: 4 }}
          activeDot={{ r: 6 }}
          strokeWidth={2}
        />
      </LineChart>
    </ResponsiveContainer>
  );
}
