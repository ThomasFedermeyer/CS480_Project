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
import { APILearningResourcesResponse } from "../../api/interfaces";
import { getLearningResources } from "../../api";
import {
  Box,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Button,
} from "@mui/material";
import { useNavigate } from "react-router-dom";

const LearningResources: React.FC = () => {
  const [data, setData] = useState<APILearningResourcesResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [byLearning, setByLearning] = useState<boolean | null>(null);
  const [byAge, setByAge] = useState<boolean | null>(null);
  const navigate = useNavigate();

  const fetchData = async (
    byLearning: boolean | null,
    byAge: boolean | null
  ) => {
    setLoading(true);
    try {
      const response = await getLearningResources(byLearning, byAge);
      setData(response);
    } catch (error) {
      console.error("Error fetching data:", error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData(byLearning, byAge);
  }, [byLearning, byAge]);

  const hasAgeGroup = data?.data.some((item) => item.AgeGroup !== undefined);

  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  const customTooltip = ({ active, payload, label }: any) => {
    if (active && payload && payload.length) {
      return (
        <div className="custom-tooltip">
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

  const groupedData = data?.data.reduce((acc, item) => {
    const existing = acc.find((i) => i.AgeGroup === item.AgeGroup);
    if (existing) {
      existing[`${item.ResourceName} (${item.ResourceType})`] = item.counts;
    } else {
      acc.push({
        AgeGroup: item.AgeGroup,
        [`${item.ResourceName} (${item.ResourceType})`]: item.counts,
      });
    }
    return acc;
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
  }, [] as any[]);

  const resourceNames = Array.from(
    new Set(
      data?.data.map((item) => `${item.ResourceName} (${item.ResourceType})`)
    )
  );

  const colors = [
    "#8884d8",
    "#82ca9d",
    "#ffc658",
    "#ff8042",
    "#8dd1e1",
    "#a4de6c",
    "#d0ed57",
    "#ffc658",
  ];

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
      <FormControl fullWidth sx={{ mb: 2 }}>
        <InputLabel id="byLearning-label">By Learning</InputLabel>
        <Select
          labelId="byLearning-label"
          id="byLearning"
          value={byLearning === null ? "" : byLearning.toString()}
          label="By Learning"
          onChange={(e) =>
            setByLearning(
              e.target.value === "" ? null : e.target.value === "true"
            )
          }
        >
          <MenuItem value="">No Selection</MenuItem>
          <MenuItem value="true">True</MenuItem>
          <MenuItem value="false">False</MenuItem>
        </Select>
      </FormControl>
      <FormControl fullWidth sx={{ mb: 2 }}>
        <InputLabel id="byAge-label">By Age</InputLabel>
        <Select
          labelId="byAge-label"
          id="byAge"
          value={byAge === null ? "" : byAge.toString()}
          label="By Age"
          onChange={(e) =>
            setByAge(e.target.value === "" ? null : e.target.value === "true")
          }
        >
          <MenuItem value="">No Selection</MenuItem>
          <MenuItem value="true">True</MenuItem>
          <MenuItem value="false">False</MenuItem>
        </Select>
      </FormControl>

      {loading && <div>Loading...</div>}
      {!loading && !data && <div>No data available</div>}
      {!loading && data && (
        <BarChart
          width={800}
          height={400}
          data={groupedData}
          margin={{
            top: 20,
            right: 30,
            left: 20,
            bottom: 5,
          }}
        >
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey={hasAgeGroup ? "AgeGroup" : "ResourceName"} />
          <YAxis />
          <Tooltip content={customTooltip} />
          <Legend />
          {resourceNames.map((name, index) => (
            <Bar
              key={name}
              dataKey={name}
              stackId={hasAgeGroup ? "a" : undefined}
              fill={colors[index % colors.length]}
            />
          ))}
        </BarChart>
      )}
    </Box>
  );
};

export default LearningResources;
