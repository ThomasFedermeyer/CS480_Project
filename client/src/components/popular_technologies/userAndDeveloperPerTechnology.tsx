import React, { useEffect, useState } from "react";
import { Box, Typography, Button, TextField } from "@mui/material";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
} from "recharts";
import { getUsersAndDeveloperTypesPerTechnology } from "../../api";
import { APITechCountResponse } from "../../api/interfaces";
import { useNavigate } from "react-router-dom";
import { CHART_HEIGHT, CHART_WIDTH } from "../../utils/globals";

const UserAndDeveloperPerTechnology: React.FC = () => {
  const [data, setData] = useState<APITechCountResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [developerTypeName, setDeveloperTypeName] = useState<string | null>(
    null
  );
  const navigate = useNavigate();

  const fetchData = async (developerTypeName: string | null) => {
    setLoading(true);
    try {
      const response = await getUsersAndDeveloperTypesPerTechnology(
        developerTypeName
      );
      setData(response);
    } catch (error) {
      console.error("Error fetching data:", error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    const delayDebounceFn = setTimeout(() => {
      fetchData(developerTypeName);
    }, 1000);

    return () => clearTimeout(delayDebounceFn);
  }, [developerTypeName]);

  const customTooltip = ({ active, payload, label }: any) => {
    if (active && payload && payload.length) {
      return (
        <div
          className="custom-tooltip"
          style={{
            backgroundColor: "#f5f5f5",
            padding: "10px",
            border: "1px solid #ccc",
            fontSize: "12px",
          }}
        >
          <p className="label">{`${label}`}</p>
          {payload.map((entry: any, index: number) => (
            <p key={`item-${index}`} className="intro">
              {`${entry.name === "counts" ? "Users:" : entry.name} : ${
                entry.value
              }`}
            </p>
          ))}
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
        onClick={() => navigate("/popular_technologies")}
        sx={{ mb: 4 }}
      >
        Back to Popular Technologies
      </Button>
      <Typography variant="h4" gutterBottom>
        Users and Developer Types Per Technology
      </Typography>
      <TextField
        fullWidth
        label="Developer Type Name"
        value={developerTypeName === null ? "" : developerTypeName}
        onChange={(e) => setDeveloperTypeName(e.target.value)}
        sx={{ mb: 2 }}
      />
      {loading && <Typography>Loading...</Typography>}
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
          <XAxis dataKey="TechName" tick={false} />
          <YAxis
            label={{
              value: "Users",
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

export default UserAndDeveloperPerTechnology;
