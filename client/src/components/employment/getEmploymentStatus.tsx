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
import { getRemotePolicyByLocation } from "../../api";
import { APIRemotePolicyResponse } from "../../api/interfaces";
import { useNavigate } from "react-router-dom";
import { CHART_HEIGHT, CHART_WIDTH } from "../../utils/globals";

const GetEmploymentStatus: React.FC = () => {
  const [data, setData] = useState<APIRemotePolicyResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [distributionOf, setDistributionOf] = useState<string | null>(null);
  const [byLocation, setByLocation] = useState<boolean | null>(null);
  const navigate = useNavigate();

  const fetchData = async (
    distributionOf: string | null,
    byLocation: boolean | null
  ) => {
    setLoading(true);
    try {
      const response = await getRemotePolicyByLocation(
        distributionOf,
        byLocation
      );
      setData(response);
    } catch (error) {
      console.error("Error fetching data:", error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData(distributionOf, byLocation);
  }, [distributionOf, byLocation]);

  const determineXAxisKey = (data: APIRemotePolicyResponse["data"]) => {
    if (data.length === 0) return "Unknown";
    const keys = Object.keys(data[0]);
    const xAxisKey = keys.find(
      (key) => key !== "counts" && key !== "error" && key !== "message"
    );
    return xAxisKey || "Unknown";
  };

  const xAxisKey = data ? determineXAxisKey(data.data) : "Unknown";

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
              {`${entry.name === "counts" ? "People Working" : entry.name} : ${
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
        onClick={() => navigate("/employment")}
        sx={{ mb: 4 }}
      >
        Back to Employment
      </Button>
      <FormControl fullWidth sx={{ mb: 2 }}>
        <InputLabel id="distributionOf-label">Distribution Of</InputLabel>
        <Select
          labelId="distributionOf-label"
          id="distributionOf"
          value={distributionOf === null ? "" : distributionOf}
          label="Distribution Of"
          onChange={(e) => setDistributionOf(e.target.value as string)}
        >
          <MenuItem value="">No Selection</MenuItem>
          <MenuItem value="RemotePolicy">Remote Policy</MenuItem>
          <MenuItem value="CompanyName">Company Name</MenuItem>
          <MenuItem value="WorkingTime">WorkingTime</MenuItem>
          <MenuItem value="DeveloperTypeName">Developer TypeName</MenuItem>
        </Select>
      </FormControl>
      <FormControl fullWidth sx={{ mb: 2 }}>
        <InputLabel id="byLocation-label">By Location</InputLabel>
        <Select
          labelId="byLocation-label"
          id="byLocation"
          value={byLocation === null ? "" : byLocation.toString()}
          label="By Location"
          onChange={(e) =>
            setByLocation(
              e.target.value === "" ? null : e.target.value === "true"
            )
          }
        >
          <MenuItem value="">No Selection</MenuItem>
          <MenuItem value="true">True</MenuItem>
          <MenuItem value="false">False</MenuItem>
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
          <XAxis dataKey={xAxisKey} tick={false} />
          <YAxis
            label={{
              value: "Peoople Working",
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

export default GetEmploymentStatus;
