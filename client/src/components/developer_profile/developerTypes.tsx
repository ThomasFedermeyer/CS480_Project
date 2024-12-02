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
import { APIAvgYearsCodingByDeveloperTypeResponse } from "../../api/interfaces";
import { getDeveloperTypesAndYearsCoding } from "../../api";
import { CHART_HEIGHT, CHART_WIDTH } from "../../utils/globals";

const DeveloperTypes: React.FC = () => {
  const [data, setData] =
    useState<APIAvgYearsCodingByDeveloperTypeResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const fetchData = async () => {
    setLoading(true);
    try {
      const response = await getDeveloperTypesAndYearsCoding();
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
        <div
          className="custom-tooltip"
          style={{
            backgroundColor: "#f5f5f5",
            padding: "10px",
            border: "1px solid #ccc",
          }}
        >
          <p className="label">{`Developer Type: ${label}`}</p>
          <p className="intro">{`Average Years Coding: ${payload[0].value}`}</p>
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
      <Typography variant="h4" gutterBottom>
        Developer Types and Years Coding
      </Typography>
      {loading && <Typography>Loading...</Typography>}
      {!loading && !data && <Typography>No data available</Typography>}
      {!loading && data && (
        <BarChart
          width={CHART_WIDTH}
          height={CHART_HEIGHT}
          data={data.data}
          margin={{
            top: 20,
            right: 30,
            left: 20,
            bottom: 5,
          }}
        >
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="DeveloperTypeName" tick={false} />
          <YAxis
            label={{
              value: "Average Age of Coding",
              angle: -90,
              position: "insideLeft",
            }}
          />
          <Tooltip content={customTooltip} />
          <Bar dataKey="AvgYearsCoding" fill="#8884d8"></Bar>
        </BarChart>
      )}
    </Box>
  );
};

export default DeveloperTypes;
