import React, { useEffect, useState } from "react";
import {
  Box,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Button,
  Typography,
} from "@mui/material";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
} from "recharts";
import { getAverageSalary } from "../../api";
import { APITechSalaryResponse } from "../../api/interfaces";
import { useNavigate } from "react-router-dom";
import { CHART_HEIGHT, CHART_WIDTH } from "../../utils/globals";

const AverageSalary: React.FC = () => {
  const [data, setData] = useState<APITechSalaryResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [groupBy, setGroupBy] = useState<
    "DeveloperTypeName" | "TechName" | null
  >(null);
  const navigate = useNavigate();

  const fetchData = async (
    groupBy: "DeveloperTypeName" | "TechName" | null
  ) => {
    setLoading(true);
    try {
      const response = await getAverageSalary(groupBy);
      setData(response);
    } catch (error) {
      console.error("Error fetching data:", error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData(groupBy);
  }, [groupBy]);

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
              {`${entry.name} : ${entry.value}`}
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
        onClick={() => navigate("/employment")}
        sx={{ mb: 4 }}
      >
        Back to Employment
      </Button>
      <FormControl fullWidth sx={{ mb: 2 }}>
        <InputLabel id="groupBy-label">Group By</InputLabel>
        <Select
          labelId="groupBy-label"
          id="groupBy"
          value={groupBy === null ? "" : groupBy}
          label="Group By"
          onChange={(e) =>
            setGroupBy(e.target.value as "DeveloperTypeName" | "TechName")
          }
        >
          <MenuItem value="">No Selection</MenuItem>
          <MenuItem value="DeveloperTypeName">Developer Type Name</MenuItem>
          <MenuItem value="TechName">Tech Name</MenuItem>
        </Select>
      </FormControl>

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
          <XAxis
            dataKey={groupBy === "TechName" ? "TechName" : "DeveloperTypeName"}
            tick={false}
          />
          <YAxis
            label={{
              value: "Average Salary",
              angle: -90,
              position: "insideLeft",
              dx: -20, // Adjust horizontal padding
              dy: 10, // Adjust vertical padding
            }}
          />
          <Tooltip content={customTooltip} />
          <Bar dataKey="AvgSalary" fill="#8884d8" />
        </BarChart>
      )}
    </Box>
  );
};

export default AverageSalary;
