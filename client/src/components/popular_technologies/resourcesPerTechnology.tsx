import React, { useEffect, useState } from "react";
import {
  Box,
  Typography,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  Button,
} from "@mui/material";
import { getResourcesPerTechnology } from "../../api";
import { APITechResourcesResponse } from "../../api/interfaces";
import { useNavigate } from "react-router-dom";

const ResourcesPerTechnology: React.FC = () => {
  const [data, setData] = useState<APITechResourcesResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const fetchData = async () => {
    setLoading(true);
    try {
      const response = await getResourcesPerTechnology();
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
        onClick={() => navigate("/popular_technologies")}
        sx={{ mb: 4 }}
      >
        Back to Popular Technologies
      </Button>
      <Typography variant="h4" gutterBottom>
        Resources Per Technology
      </Typography>
      {loading && <Typography>Loading...</Typography>}
      {!loading && data && (
        <TableContainer component={Paper}>
          <Table>
            <TableHead>
              <TableRow>
                <TableCell>Tech Name</TableCell>
                <TableCell>Resource Names</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {data.data.map((techResource) => (
                <TableRow key={techResource.TechName}>
                  <TableCell>{techResource.TechName}</TableCell>
                  <TableCell>{techResource.ResourceNames.join(", ")}</TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
      )}
    </Box>
  );
};

export default ResourcesPerTechnology;
