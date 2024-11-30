import React, { useEffect, useState } from "react";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
} from "recharts";
import { Box, Button, Typography } from "@mui/material";
import { useNavigate } from "react-router-dom";
import { APIYearsCodingGroupResponse } from "../../api/interfaces";
import { getYearsCodingDistribution } from "../../api";

const CodingYear: React.FC = () => {
  const [data, setData] = useState<APIYearsCodingGroupResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const fetchData = async () => {
    setLoading(true);
    try {
      const response = await getYearsCodingDistribution();
      setData(response);
      setLoading(false);
    } catch (error) {
      setLoading(false);
      console.error("Error fetching data:", error);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

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
        Years Coding Distribution
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
          <XAxis dataKey="YearsCodingGroup" />
          <YAxis />
          <Tooltip formatter={(value: number) => value.toFixed(2)} />
          <Legend />
          <Bar dataKey="counts" fill="#8884d8"></Bar>
        </BarChart>
      )}
    </Box>
  );
};

export default CodingYear;
