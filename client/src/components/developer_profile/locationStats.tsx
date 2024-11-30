import React, { useEffect, useState } from "react";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  LabelList,
} from "recharts";
import { Box, Button, Typography } from "@mui/material";
import { useNavigate } from "react-router-dom";
import { getLocationStats } from "../../api";
import { APIAvgYearsCodingByLocationResponse } from "../../api/interfaces";

const LocationStats: React.FC = () => {
  const [data, setData] = useState<APIAvgYearsCodingByLocationResponse | null>(
    null
  );
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const fetchData = async () => {
    setLoading(true);
    try {
      const response = await getLocationStats();
      setLoading(false);
      setData(response);
    } catch (error) {
      setLoading(false);
      console.error("Error fetching data:", error);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  const customLabel = (props: {
    x: number;
    y: number;
    width: number;
    value: number;
    index: number;
  }) => {
    const { x, y, width, value, index } = props;
    const count = data?.data[index].counts;
    return (
      <text
        x={x + width / 2}
        y={y}
        fill="#000"
        textAnchor="middle"
        dy={-6}
      >{`Average:${value.toFixed(2)} Count:(${count})`}</text>
    );
  };

  return (
    <Box sx={{ p: 2 }}>
      <Button
        variant="contained"
        color="secondary"
        onClick={() => navigate("/developer_profile")}
        sx={{ mb: 4 }}
      >
        Back to Developer Profile
      </Button>
      <Typography variant="h4" gutterBottom>
        Location Stats
      </Typography>
      {loading && <Typography>Loading...</Typography>}
      {!loading && !data && <Typography>No data available</Typography>}
      {!loading && data && (
        <BarChart
          width={800}
          height={400}
          data={data.data}
          margin={{
            top: 20,
            right: 30,
            left: 20,
            bottom: 5,
          }}
        >
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="Location" />
          <YAxis />
          <Tooltip formatter={(value: number) => value.toFixed(2)} />
          <Legend />
          <Bar dataKey="AvgYearsCoding" fill="#8884d8" label={customLabel}>
            <LabelList dataKey="counts" position="outside" />
          </Bar>
        </BarChart>
      )}
    </Box>
  );
};

export default LocationStats;
