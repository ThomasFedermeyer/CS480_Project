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
import {
  AgeGenderByLevelAPIResponse,
  CodingLevelType,
  DemographicsType,
} from "../../api/interfaces";
import { getAgeAndGenderByLevel } from "../../api";
import {
  Box,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Button,
} from "@mui/material";
import { useNavigate } from "react-router-dom";

const GenderAgeLevel: React.FC = () => {
  const [data, setData] = useState<AgeGenderByLevelAPIResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [demographic, setDemographic] = useState<DemographicsType>(null);
  const [codingLevel, setCodingLevel] = useState<CodingLevelType>(null);
  const navigate = useNavigate();

  const fetchData = async (
    demographic: DemographicsType,
    codingLevel: CodingLevelType
  ) => {
    setLoading(true);
    try {
      const response = await getAgeAndGenderByLevel(demographic, codingLevel);
      setData(response);
    } catch (error) {
      console.error("Error fetching data:", error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData(demographic, codingLevel);
  }, [demographic, codingLevel]);

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
        <InputLabel id="demographic-label">Demographic</InputLabel>
        <Select
          labelId="demographic-label"
          id="demographic"
          value={demographic == null ? "" : demographic}
          label="Demographic"
          onChange={(e) => setDemographic(e.target.value as DemographicsType)}
        >
          <MenuItem value="">No Selection</MenuItem>
          <MenuItem value="Age">Age</MenuItem>
          <MenuItem value="Gender">Gender</MenuItem>
        </Select>
      </FormControl>
      <FormControl fullWidth sx={{ mb: 2 }}>
        <InputLabel id="codingLevel-label">Coding Level</InputLabel>
        <Select
          labelId="codingLevel-label"
          id="codingLevel"
          value={codingLevel === null ? "" : codingLevel}
          label="Coding Level"
          onChange={(e) => setCodingLevel(e.target.value as CodingLevelType)}
        >
          <MenuItem value="">No Selection</MenuItem>
          <MenuItem value="Learning">Learning</MenuItem>
          <MenuItem value="Professional">Professional</MenuItem>
        </Select>
      </FormControl>

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
          <XAxis dataKey={demographic === "Age" ? "AgeGroup" : "Gender"} />
          <YAxis />
          <Tooltip />
          <Legend />
          <Bar dataKey="counts" fill="#8884d8" />
        </BarChart>
      )}
    </Box>
  );
};

export default GenderAgeLevel;
