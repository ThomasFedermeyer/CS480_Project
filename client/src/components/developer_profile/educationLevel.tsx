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
import { CHART_HEIGHT, CHART_WIDTH } from "../../utils/globals";

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

  const customTooltip = ({ active, payload, label }: any) => {
    if (active && payload && payload.length) {
      return (
        <div className="custom-tooltip">
          <p className="label">{`Education Level: ${label}`}</p>
          <p className="intro">{`Number of People: ${payload[0].value}`}</p>
        </div>
      );
    }
    return null;
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
      {loading && <div>Loading...</div>}
      {!loading && !data && <div>No data available</div>}
      {!loading && data && (
        <BarChart
          width={CHART_WIDTH}
          height={CHART_HEIGHT}
          data={data.data}
          margin={{
            top: 5,
            right: 30,
            left: 20,
            bottom: 5,
          }}
        >
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="EducationLevel" tick={false} />
          <YAxis
            label={{
              value: "Number of People",
              angle: -90,
              position: "insideLeft",
            }}
          />
          <Tooltip content={customTooltip} />
          <Bar dataKey="counts" fill="#8884d8" />
        </BarChart>
      )}
    </Box>
  );
};

export default EducationLevel;
