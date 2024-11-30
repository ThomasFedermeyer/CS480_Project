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
import { APIEducationLevelAPIResponse } from "../../api/interfaces";
import { getEducationLevel } from "../../api";
import { Box, Button } from "@mui/material";
import { useNavigate } from "react-router-dom";

const EducationLevel: React.FC = () => {
  const [data, setData] = useState<APIEducationLevelAPIResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const fetchData = async () => {
    setLoading(true);
    try {
      const response = await getEducationLevel();
      setData(response);
    } catch (error) {
      console.error("Error fetching data:", error);
    } finally {
      setLoading(false);
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

      {loading && <div>Loading...</div>}
      {!loading && !data && <div>No data available</div>}
      {!loading && data && (
        <BarChart
          width={600}
          height={300}
          data={data.data}
          margin={{
            top: 5,
            right: 30,
            left: 20,
            bottom: 5,
          }}
        >
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="EducationLevel" />
          <YAxis />
          <Tooltip />
          <Legend />
          <Bar dataKey="counts" fill="#8884d8" />
        </BarChart>
      )}
    </Box>
  );
};

export default EducationLevel;
